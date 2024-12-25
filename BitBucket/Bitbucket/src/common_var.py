import re

username                        = ''
password                        = ''
#---------------------------------------------------------------------------------------------------------------
option_tag_count                = 15 # No of tags to be shown
#---------------------------------------------------------------------------------------------------------------
file_extention                  = '.csv'
headers                         = {"Accept": "application/json"}
reviewers_sep                   = ' \\ '
pr_method                       = "GET"
commits_file                    = '{}_commits details_{}_{}'
dev_tag_pattern                 = r'[A-Z]*[0-9]*DEV.[0123456789]+.PRI'
dev_tag_re                      = re.compile(dev_tag_pattern)
multi_range_input_re            = r' *[0-9] *~~ *[0-9] *'
input_pattern_multi             = re.compile(multi_range_input_re)
single_range_input_re           = r' *[0-9]* *~{1} *[0-9]* *'
input_pattern_single            = re.compile(single_range_input_re)
single_range_input_right_re     = r' *[0-9]* *~{1} *[0-9]+ *'
input_pattern_single_right      = re.compile(single_range_input_right_re)
single_range_input_left_re      = r' *[0-9]+ *~{1} *[0-9]* *'
input_pattern_single_left       = re.compile(single_range_input_left_re)
unique_val_re                   = r'\s*[0-9]+\s*'
null_pattern                    = re.compile(r'\s+')
valid_characters                = re.compile(r'[0-9]*[A-Z]+[0-9]*')
unique_input_pattern            = re.compile(unique_val_re)
spl_char_multi                  = re.compile(r'~')
spl_char_single                 = re.compile(r'~~')
