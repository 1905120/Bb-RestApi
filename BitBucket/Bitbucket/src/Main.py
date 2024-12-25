import __Bitbucket__
from datetime import datetime
import calendar
import colorful
import output_csv
import time
import I_O
import os
import __CONFIG__
import common_var
import traceback
import socket

def build_file_name(project, since_tag, until_tag, is_range):
    tag = 'T24.DEV.{}.PRI'
    if until_tag == bb.dev_branch:
        tag = tag.format('CURRENT')
    else:
        tag = tag.format(until_tag.split('.')[2])
    tmp = str(datetime.today().strftime('%Y-%m-%d')).split('-')
    year = tmp[0]
    month = int(tmp[1])
    date = tmp[2]
    formated_date = '{}-{}-{}'.format(date, calendar.month_name[month][0 : 3], year)
    common_var.commits_file = common_var.commits_file.format(project, formated_date, tag)
    common_var.commits_file = '{}\\{}'.format(bb.run_output_dir(), common_var.commits_file)
    common_var.commits_file = bb.add_file_sequence(common_var.commits_file)
    return

def process_commit_details(bb):

    total_repo_to_check                  = []
    total_proj_to_check                  = []
    processed_repo                       = []
    total_repositories_in_all_proj       = []
    
    input_proj ,input_repos = I_O.get_projects_and_repo_from_input()

    if not(input_repos) and not(input_proj):
        if bb.read_repositories_from_file():
            total_repo_to_check.extend(bb.retail_modules)
        if bb.read_projects_from_file():
            total_proj_to_check.extend(bb.projects)
    elif input_repos and not(input_proj):
        if bb.read_projects_from_file():
            total_proj_to_check.extend(bb.projects)
        total_repo_to_check.extend(input_repos)
    elif not(input_repos) and input_proj:
        if bb.read_repositories_from_file():
            total_repo_to_check.extend(bb.retail_modules)
        total_proj_to_check.extend(input_proj)
    else:
        total_repo_to_check.extend(input_repos)
        total_proj_to_check.extend(input_proj)

    #print(total_proj_to_check, '\n', total_repo_to_check)

    #get all projects from BB
    project_list = bb.get_project()
    
    c = 0

    #loop through the projects
    for project in project_list:
        #print(project)
        if total_proj_to_check:
            if project['key'] not in total_proj_to_check:
                continue
        #print(project['key'])
        repo_list = bb.get_repositories(project['key'])
        #print(len(repo_list))
        #print('---------------------Searching in : {}---------------------'.format(project['key']))
        bb.dev_tag          = ''
        bb.get_data_since   = '' 
        bb.get_data_until   = ''

        bb.list_of_tags = []
        #loop through the repositories
        for repo in repo_list:

            name = repo['name']
            
            total_repositories_in_all_proj.append(name)
            
            if total_repo_to_check:
                if name not in total_repo_to_check:
                    continue
            
            list_of_tags = bb.get_tag(project['key'], name)
                
            print_repo = True

            if c == 0:
                
                build_file_name(project['key'], list_of_tags[0][0], list_of_tags[0][1], 0)
                os.system('cls')
                if not(bb.open_output_file()):
                    return
                    
                output_csv.update_headers(bb.file_ptr, bb.add_repo, bb.update_pr_details, bb.add_code_changes, bb.add_parent_details, bb.mutiple_tag_process, bb.update_tag_details )

            print('>',name)
            
            for tag_pair in list_of_tags:

                if len(tag_pair) != 2:
                    print(colorful.red('Missing TAG !!!'))
                    exit()

                since = tag_pair[0]
                until = tag_pair[1]
                          
                if not(since) or not(until):
                    print('Skiping Project : ', project['key'])
                    break
                
                #print(since, '-', until)
                
                if since and until:
                    bb.process_commit_pr_details(project['key'], name, since, until)
                    processed_repo.append(name)
                    
            c += 1
                    
                    
    bb.close_output_file()
    if total_repo_to_check:
        return [total_repo_to_check, processed_repo]
    else:
        return [total_repositories_in_all_proj, processed_repo]


def get_missed_repo(total_repo, processed_repo):
    print_one_time = True
    c = 0
    for repo in total_repo:
        if repo not in processed_repo:
            c += 1
            if print_one_time:
                print('\nNot Yet processed >')
            print('{}. {}'.format(c, colorful.red(repo)))
            print_one_time = False
    return


def init_process(bb):
    bb.username, bb.password, bb.update_pr_details, bb.add_code_changes, bb.add_parent_details, bb.add_repo = __CONFIG__.read_credentials_file()
    bb.define_api_conn()
    return
############################################## process start ########################################################
start_time  = time.time()

if __name__ == "__main__":
    try:
        bb = __Bitbucket__.bitbucket()
        init_process(bb)
        total_repo, processed_repo = process_commit_details(bb)
        get_missed_repo(total_repo, processed_repo)
    except socket.error as err:
        try:
            erro_Det = err.response.json()
        except:
            erro_Det = {}
        if 'errors' in erro_Det:
            for idx, ele in enumerate(erro_Det):
                print(colorful.red('Err @Main :'),erro_Det[ele][idx]['message'], '\n')
        else:
            print(colorful.red('Err @Main :'),'Please Check you NETWORK/VPN connection and try again !!!\n')
        exit()
        
    except Exception as err:
        print(colorful.red('Err @Main :'),err, '\n')
        exit()

end_time = time.time()
############################################# process end ##########################################################

print("\n\n--- Your Request processed in {} mins ---\n".format( colorful.green(str(round((end_time - start_time) / 60 , 2)))))
