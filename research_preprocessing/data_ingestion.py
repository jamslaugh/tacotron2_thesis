import pandas as pd
import numpy as np

def insert_indf(df,match_rule,df_to_insert_pre,df_to_insert_post,subst = False):
    """
    Function to insert specific rows in Data Frame to obtain new time values within
    :param df: The dataframe we start with
    :param match_rule: the matching rule we want to cut by
    :param df_to_insert_pre: the values to be inserted pre
    :param df_to_insert_post: the values to be inserted post
    :param subst: the eventual presence of a substring
    :return: df, a modified and expanded Data Frame
    """
    index = df.loc[match_rule,:].index
    for el in index:

        if not subst:
            upp_df = df.loc[:el,:]
            low_df = df.loc[el+1:,:]
        else:
            upp_df = df.loc[:el-1,:]
            low_df = df.loc[el+1:,:]
        df = pd.concat([upp_df,df_to_insert_pre.loc[el],df_to_insert_post.loc[el],low_df])
        df = df.reset_index(drop=True)
    return df

def inserted_df(df,match_rule='\w+\s*\<.*\>',subst = False):

    """
    Automates the Data Insertion
    :param df: The original Data Frame
    :param match_rule: regex rule
    :param subst: eventual substring presence
    :return: ort_data_new - the dataframe generated
    """

    values = df.loc[df.ORT.str.match(match_rule), :].ORT.str.split('\s*\<|\>', expand=True).iloc[:, 1:]
    disfl = '<' + values.iloc[:, 0].astype('str') + '>'
    post = values.iloc[:, 1]
    disfl = disfl.to_frame(name='ORT')
    post = post.replace({'': np.nan, ' ': np.nan})
    post = post.to_frame(name='ORTP')
    ort_data_new = insert_indf(df, df.ORT.str.match(match_rule), disfl, post,subst=subst)
    #na removal
    ort_data_new = ort_data_new.dropna(how='all')
    ort_data_new['Nr'] = ort_data_new.Nr.fillna(method='ffill')
    ort_data_new['Nr'] = ort_data_new.Nr.astype('int')
    ort_data_new = ort_data_new.reset_index(drop=True)

    return ort_data_new
