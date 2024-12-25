import os

fp = open('requirements.txt', 'r', encoding='utf-8')

l = fp.read().split('\n')


def do_install(module):
    try:
        print('installing >',module)
        os.system('pip install {}'.format(module))
        return [1, 'pass']
    except Exception as e:
        return [0, e]


#refine values
for module in l:
    if module:
        val = module.rstrip()
        val = val.lstrip()
        val = val.replace(',', '')
        val = val.replace('\t', '')
        if val:
            result, response = do_install(val)
        else:
            print('missing value ')

        if result == 0:
            print('skipping module {}'.format(val))
            print('Err :', respose)

        os.system('cls')

try:        
    fp.close()
except Exception as e:
    print('terminating !!!')

