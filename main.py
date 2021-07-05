from data_processing.data_wrangler import *
import os
import argparse

#TODO: add text file with named files to convert them. Next, make the dataframe compatible to Tacotron 2.

args = argparse.ArgumentParser(description='Process Data')
args.add_argument('file')
args.add_argument('file_path')
args.add_argument('--text_file',dest='text_file',type=bool,help='Tells wether text_file has to be considered or not')
args.add_argument('--token',dest='token',type=bool,help='Tells wether token substitution has to be considered or not')

if __name__ == '__main__':

    arguments = args.parse_args()
    out_filename, out_path = arguments.file, arguments.file_path
    text_file = arguments.text_file
    token = arguments.token
    print(os.getcwd())
    if text_file:
        out_dict = output_dict = DataLoad(out_filename, out_path, keys_to_search=['dstr', 'ORT'], text_file = True)
    else:
        out_dict = output_dict = DataLoad(out_filename, out_path, keys_to_search=['dstr', 'ORT'], text_file=False)
    if token:
        ort_data_new = data_wrangle(out_dict, token=True)
    else:
        ort_data_new = data_wrangle(out_dict, token=False)

    ort_data_new.to_csv(os.path.join('', 'preprocessing_results/trial.csv'))