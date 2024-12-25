



def update_headers(file_ptr, add_repo, update_pr_details, add_code_changes, add_parent_details, mutiple_tag_process, update_tag_details):

    column_idx = ''

    if update_tag_details:

        column_idx += 'Run Tag,'

    if add_repo:

        column_idx += 'Repo,'

    column_idx += 'Commit Reference,'

    column_idx += 'Task Refrence,'

    if add_parent_details:
        
        column_idx += 'Parent Reference,'
        
        column_idx += 'Parent Type,'

    column_idx += 'Description,'

    if add_code_changes:
    
        column_idx += 'Component,'

        column_idx += 'Artifacts,'

    column_idx += 'Owner,'

    if update_pr_details:

        column_idx += 'Reviewers,'

        column_idx += 'Merge time,'
    
    file_ptr.write('{}\n'.format(column_idx))
    
    return


def write_output_file(file_ptr, update_tag_details, add_repo, add_parent_details, update_pr_details, mutiple_tag_process, add_code_changes, change_set_count, code_change, commit_id, task_id, parent_task_ref, parent_task_type, commit_msg, author, reviewers, pr_merge_dt, run_idx, repo):

    write_str1 = ''

    write_str2 = ''

    if update_tag_details:
        
        write_str1 += '{},'.format(run_idx)

    if add_repo:

        write_str1 += '{},'.format(repo)

    write_str1 += '{},'.format(commit_id)

    write_str1 += '{},'.format(task_id)

    if add_parent_details:
        
        write_str1 += '{},'.format(parent_task_ref)

        write_str1 += '{},'.format(parent_task_type)

    write_str1 += '{},'.format(commit_msg)

    write_str2 += '{},'.format(author)

    if update_pr_details:

        write_str2 += '{},'.format(reviewers)

        write_str2 += '{},'.format(pr_merge_dt)
    
    if add_code_changes:
                
        while change_set_count:
                    
            component = 'unable to fetch component'
            if len(code_change[change_set_count - 1]) > 1:
                component = code_change[change_set_count - 1][0]
            path = ''
                    
            if len(code_change[change_set_count - 1]) > 2:
                for ele in code_change[change_set_count - 1][1 : len(code_change[change_set_count - 1]) - 1]:
                    path += ele
                    path += '/'
                path = path.rstrip('/')

            if not(path):
                path = 'path missing'
                
            file = code_change[change_set_count - 1][-1].replace(',', ';')

            write_str = '{} {}, {}, {}\n'.format(write_str1, component, file, write_str2)
                
            file_ptr.write(write_str)
        
            change_set_count -= 1
    else:
        
        write_str = '{} {}\n'.format(write_str1, write_str2)

        file_ptr.write(write_str)
        
    return
