## Imports
from research_preprocessing.conciliator import *
from research_preprocessing.data_ingestion import inserted_df
from research_preprocessing.data_loader import EafReader

import pandas as pd
import numpy as np
import os

## Data Load

def DataLoad(filename,path,keys_to_search=['dstr','ORT'],text_file = False):
    """
    This function loads the data to make it usable from the Tacotron2 algo. If text_file = True, please be sure to name
    all the desired data in a form like G01V01P01_[ dstr, ort] for both the dstr level and ort level, respectively, where
    G01V01P01 has to be inserted as the filename.

    :param filename: The filename to be loaded
    :param path: The path to be used
    :param keys_to_search: iterable, indicates the keys to be used in the extraction.
    :param text_file: Bool, default False, indicates wether we are loading an EAF (false) or a txt (True). If true only
    the prefix filename has to be given.
    :return: OUTPUT_DICT a dictionary of Data Frames to be used.
    """

    OUTPUT_DICT = {}

    if not text_file:

        rdr = EafReader(filename, path, text_file=False)

        for key in keys_to_search:

            annot, annot_df = rdr.parser(key)
            DF = rdr.dataframe_creator(annot, annot_df, annot_type=key.lower())

            OUTPUT_DICT[key.lower()] = DF
    else:



        for key in keys_to_search:

            rdr = EafReader(filename+'_'+key.lower()+'.txt', path, text_file=True)
            DF = rdr.csv_reader()

            OUTPUT_DICT[key.lower()] = DF

    return OUTPUT_DICT

if __name__ == '__main__':
    output_dir = DataLoad('G01V01P01','.\Data EAF\Training Data - EAF',keys_to_search=['dstr','ORT'],text_file = True)
    conc_data = conciliator(output_dir['dstr'],output_dir['ort'])
    ort_data_new = inserted_df(output_dir['ort'])
    ort_data_new = time_conciliation(ort_data_new,conc_data)
    ort_data_new.to_csv(os.path.join('preprocessing_results','trial.csv'))
#TODO: Implement ort_data_new post processing cleaning. To be decided whether prl token or not.