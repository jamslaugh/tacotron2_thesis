## Imports
from research_preprocessing.conciliator import *
from research_preprocessing.data_ingestion import inserted_df
from research_preprocessing.data_loader import EafReader

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
            DF = rdr.dataframe_creator(annot, annot_df, annot_type=key)

            OUTPUT_DICT[key.lower()] = DF
    else:



        for key in keys_to_search:

            rdr = EafReader(filename+'_'+key.lower()+'.txt', path, text_file=True)
            DF = rdr.csv_reader()

            OUTPUT_DICT[key.lower()] = DF

    return OUTPUT_DICT

def data_wrangle(output_dict,token=True,conciliation = False):
    """
    This function is used to wrangle data and prepare the output for the Tacotron 2 algorythm
    :param output_dict: a dictionary containing dstr and ort keys
    :param token: bool type, if the <PRL> token has to be inserted or not. If False inserts the prolongation per se.
    :param conciliation: bool type, to be used only if you want annotation levels ORT and dstr to match. Note that if token = True, then conciliation = True
    :return: ort_data_new a Data Frame with processed data
    """
    if token:
        conciliation = True

    ort_data_new = output_dict['ort']
    if conciliation:
        ort_data_new = inserted_df(ort_data_new)
        conc_data = conciliator(output_dict['dstr'], output_dict['ort'])
        ort_data_new = time_conciliation(ort_data_new,conc_data)
    ort_data_new['Duration'] = ort_data_new['End Time'] - ort_data_new['Begin Time']
    if token:
        ort_data_new.ORT = ort_data_new.ORT.fillna('<PRL>')
    else:
        ort_data_new.ORT = ort_data_new.ORT.fillna(ort_data_new.iloc[:,0].dropna())
    if conciliation:
        ort_data_new.ORT = ort_data_new.ORT.str.replace(r'(\w+)(\s)(\<.*\>)', r'\1')
        ort_data_new.ORT = ort_data_new.ORT.str.replace(r'(\w+)(\<.*\>)', r'\1')
    else:
        ort_data_new.ORT = ort_data_new.ORT.str.replace(r'(\w+)(\s)(\<)(.*)(\>)', r'\1\4').str.replace(r'(\w+)(\<)(.*)(\>)',r'\1\3')
    return ort_data_new
    #ort_data_new.to_csv(os.path.join('../preprocessing_results', 'trial.csv'))
    # filename G01V01P01, ..\..\Data EAF\Training Data EAF