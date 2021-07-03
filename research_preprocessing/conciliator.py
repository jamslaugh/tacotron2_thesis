import pandas as pd

def conciliator(dstr_df, ort_df):
    """
    This function creates the conciliation table between dstr and ort Data Frames
    :param dstr_df: The dstr Data Frame
    :param ort_df:  The ort Data Frame
    :return conc_data: The conciliated data
    """
    conciliation = []
    for cold, rowd in dstr_df.iterrows():
        for colo, rowo in ort_df.iterrows():
            if rowd['Begin Time'] > rowo['Begin Time'] and rowd['Begin Time'] < rowo['End Time']:
                conciliation.append({'conc_ort':rowo['Nr'],
                                     'conc_dstr':rowd['Nr'],
                                     'beg_tm_ort':rowo['Begin Time'],
                                     'end_tm_ort':rowo['End Time'],
                                     'beg_tm_dstr':rowd['Begin Time'],
                                     'end_tm_dstr':rowd['End Time'],
                                     'dstr':rowd['dstr'],
                                     'ort':rowo['ORT']})
    conc_data = pd.DataFrame(conciliation)
    return conc_data

def time_conciliation(ort_data_new, conc_data):
    """
        Function to make time conciliation among ort data and dstr data through conciliation table
        :param ort_data_new: Data Frame with inserted rows in disfluence points
        :param conc_data: conciliation Data Frame
        :return ort_data_new: the processed dataframe
        """
    for idx in ort_data_new.index:

        if pd.isnull(ort_data_new.loc[idx, 'Begin Time']):

            if conc_data.loc[(conc_data.conc_ort == ort_data_new.loc[idx, 'Nr']), 'beg_tm_dstr'].values.shape[0] == 1:

                ort_data_new.loc[idx - 1, 'End Time'] = conc_data.loc[
                    (conc_data.conc_ort == ort_data_new.loc[
                        idx,
                        'Nr']),
                    'beg_tm_dstr'].values;

                ort_data_new.loc[idx, 'Begin Time'] = conc_data.loc[
                    (conc_data.conc_ort == ort_data_new.loc[
                        idx,
                        'Nr']),
                    'beg_tm_dstr'].values;

                ort_data_new.loc[idx, 'End Time'] = conc_data.loc[
                    (conc_data.conc_ort == ort_data_new.loc[
                        idx,
                        'Nr']),
                    'end_tm_ort'].values;

            elif conc_data.loc[(conc_data.conc_ort == ort_data_new.loc[idx, 'Nr']), 'beg_tm_dstr'].values.shape[
                0] > 1:
                ort_data_new.loc[idx - 1, 'End Time'] = conc_data.loc[
                    (conc_data.conc_ort == ort_data_new.loc[
                        idx,
                        'Nr']) & (
                            conc_data.dstr == 'PRL'
                    ),
                    'beg_tm_dstr'].values;

                ort_data_new.loc[idx, 'Begin Time'] = conc_data.loc[
                    (conc_data.conc_ort == ort_data_new.loc[
                        idx,
                        'Nr']) & (
                            conc_data.dstr == 'PRL'),
                    'beg_tm_dstr'].values;

                ort_data_new.loc[idx, 'End Time'] = conc_data.loc[
                    (conc_data.conc_ort == ort_data_new.loc[
                        idx,
                        'Nr']) & (
                            conc_data.dstr == 'PRL'),
                    'end_tm_ort'].values;

    return ort_data_new.dropna(subset=['Begin Time', 'End Time'], how='all').reset_index(drop=True)