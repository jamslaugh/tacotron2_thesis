from data_processing.data_wrangler import *
import os
import argparse
import re

#TODO: add text file with named files to convert them. Next, make the dataframe compatible to Tacotron 2.

args = argparse.ArgumentParser(description='Process Data')
# args.add_argument('file')
args.add_argument('file_path')
args.add_argument('--text_file',dest='text_file',type=bool,
                  help='Tells wether text_file has to be considered or not')
args.add_argument('--token',dest='token',type=bool,
                  help='Tells wether token substitution has to be considered or not')
args.add_argument('--research_keys',dest='research_keys',nargs='+',default=['dstr','ORT'],
                  help='The list of keys to be searched')
args.add_argument('--cfg_path',dest='cfg_file_path',default='config_file.txt',
                  help='The cfg file contains the filenames to be processed')
args.add_argument('--debug',dest='debug',default=False,type=bool,
                  help='Debug mode')
def folder_reader(file_path,config_file_path='config_file.txt',text_file=True,token=True,research_keys=['dstr', 'ORT'],debug=False):

    with open(config_file_path,'r+') as file:
        files_list = file.read().split('\n')

    wav_reference = [re.sub(r'_.*',"",el) for el in files_list]

    for _ in range(len(files_list)):

        out_filename = files_list[_]

        if debug:

            print("Debugging, the filename is: ",out_filename)

        if text_file:

            out_dict = DataLoad(out_filename, file_path, keys_to_search=research_keys, text_file = True)

        else:

            out_filename = out_filename + ".eaf"
            out_dict = DataLoad(out_filename, file_path, keys_to_search=research_keys, text_file=False)

        if token:

            ort_data_new = data_wrangle(out_dict, token=True)

        else:

            ort_data_new = data_wrangle(out_dict, token=False)

        ort_data_new['wav_reference'] = wav_reference[_] + '.wav'
        ort_data_new=ort_data_new.drop(0,axis=1)

    return ort_data_new


if __name__ == '__main__':

    arguments = args.parse_args()
    out_path =  arguments.file_path
    text_file = arguments.text_file
    token = arguments.token
    research_keys = arguments.research_keys
    cfg_path = arguments.cfg_file_path
    debug = arguments.debug
    ort_data_new=folder_reader(out_path,cfg_path,text_file,token,research_keys,debug)
    ort_data_new.to_csv(os.path.join('', 'preprocessing_results/trial.csv'),index=False)

# if __name__ == '__main__':
#
#     arguments = args.parse_args()
#     out_filename, out_path = arguments.file, arguments.file_path
#     text_file = arguments.text_file
#     token = arguments.token
#     print(os.getcwd())
#     if text_file:
#         out_dict = output_dict = DataLoad(out_filename, out_path, keys_to_search=['dstr', 'ORT'], text_file = True)
#     else:
#         out_filename = out_filename + ".eaf"
#         out_dict = output_dict = DataLoad(out_filename, out_path, keys_to_search=['dstr', 'ORT'], text_file=False)
#     if token:
#         ort_data_new = data_wrangle(out_dict, token=True)
#     else:
#         ort_data_new = data_wrangle(out_dict, token=False)
#     ort_data_new['file'] = out_filename
#     ort_data_new=ort_data_new.drop(0,axis=1)
#     ort_data_new.to_csv(os.path.join('', 'preprocessing_results/trial.csv'),index=False)

#TODO: understand why _L files are not red correctly.