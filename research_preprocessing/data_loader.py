import xml.etree.ElementTree as et
import os
import pandas as pd
import sys

class EafReader():

    def __init__(self,filename,path,text_file=False):
        """
        Class to reat EAF files into python pandas. It can also be subqueried.
        :param filename: a string, the filename which we are pointing towards
        :param path: a string, the path to the file.
        """
        self.filename = filename
        self.filepath = os.path.join(*path.split(os.path.sep), self.filename)

        if not text_file:
            try:
                self.xtree = et.parse(self.filepath)
                self.xroot = self.xtree.getroot()
            except:
                raise Exception(f'Please specify a valid filename and/or path.\n File: {self.filename} \n ' +
                                f'@ path: {self.filepath} is invalid.\n\n' +
                                f' This is the error:\n {sys.exc_info()[1]}\n{sys.exc_info()[2]}\n\n' +
                                f'The DIRECTORIES queried are\n {os.listdir()},\n\n while the WORKING DIR is {os.getcwd()}')

    def data_time(self):

        ts = []
        for node in self.xroot:
            for child in node.getchildren(): #TODO fix here!
                ts.append(child.attrib)
        data_time = pd.DataFrame([el for el in ts if len(el.keys()) > 0 if list(el.keys())[0].startswith('TIME')])
        return data_time

    def parser(self,attribute):
        """
        the parser method is used to parse the data from the EAF file
        :param attribute: the attribute we are looking for. At the moment, only 'ORT' or 'dstr'.
        :return: annot, annot_df two lists, one containing the annotations and the other containing all other info.
        """
        annot = []
        annot_df = []
        for el in self.xroot.findall('./TIER'):
            if el.attrib['TIER_ID'] == attribute:
                for k in el.findall('./ANNOTATION/ALIGNABLE_ANNOTATION'):
                    annot_df.append(k.attrib)
                    annot.append(k.find('ANNOTATION_VALUE').text)
        return annot, annot_df

    def dataframe_creator(self,annot,AnnotDf,annot_type='dstr'):

        """
        This method creates a pandas Data Frame with all the necessary data.
        :param annot: the annotation list
        :param AnnotDf: the data list.
        :return: annot_df, the dataframe with all relevant data.
        """

        annot_df = pd.DataFrame(AnnotDf)
        annot_df[annot_type] = annot
        data_time = self.data_time()
        annot_df = pd.merge(annot_df,data_time,
                            left_on='TIME_SLOT_REF1',
                            right_on='TIME_SLOT_ID',
                            how='left')
        annot_df = annot_df.rename(columns={'TIME_VALUE':'Begin Time',
                                            'annotation':annot_type}).drop('TIME_SLOT_ID',axis=1)
        annot_df = pd.merge(annot_df,
                            data_time,
                            left_on='TIME_SLOT_REF2',
                            right_on='TIME_SLOT_ID',
                            how='left').rename(columns={'TIME_VALUE':'End Time'})
        annot_df.drop(['TIME_SLOT_REF1','TIME_SLOT_REF2','TIME_SLOT_ID'],
                      axis=1,
                      inplace=True)
        annot_df[['Begin Time', 'End Time']] = annot_df[['Begin Time', 'End Time']].apply(lambda x: x.astype('int64'))
        annot_df['Nr'] = annot_df.index + 1

        return annot_df

    def csv_reader(self):
        try:
            df = pd.read_csv(self.filepath,sep='\t')
        except:
            raise Exception(f'Please specify a valid filename and/or path.\n File: {self.filename} \n ' +
                            f'@ path: {self.filepath} is invalid.\n\n' +
                            f' This is the error:\n {sys.exc_info()[1]}\n{sys.exc_info()[2]}\n\n'+
                            f'The DIRECTORIES queried are\n {os.listdir()},\n\n while the WORKING DIR is {os.getcwd()}')

        df = df.dropna(how='all', axis=1)

        return df