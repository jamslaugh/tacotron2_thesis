import xml.etree.ElementTree as et
import os
import pandas as pd
class EafReader():

    def __init__(self,filename,path):
        """
        Class to reat EAF files into python pandas. It can also be subqueried.
        :param filename: a string, the filename which we are pointing towards
        :param path: a string, the path to the file.
        """
        self.filename = filename
        self.xtree = et.parse(os.path.join(*path.split(os.path.sep),self.filename))
        self.xroot = self.xtree.getroot()
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

def insert_indf(df,match_rule,df_to_insert_pre,df_to_insert_post,subst = False):
    index = df.loc[match_rule,:].index
    for el in index:
        if not subst:
            upp_df = df.loc[:el,:]
            low_df = df.loc[el+1:,:]
        else:
            upp_df = df.loc[:el-1,:]
            low_df = df.loc[el+1:,:]
        df = pd.concat([upp_df,df_to_insert_pre.loc[el],df_to_insert_post.loc[el],low_df])
    #df = df.reset_index(drop=True)
    return df
