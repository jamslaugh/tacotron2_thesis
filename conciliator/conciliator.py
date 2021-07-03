import pandas as pd
import numpy as np
def conciliator(annot_df, ort_df):
    import numpy as np
    conciliation = []
    for cold, rowd in annot_df.iterrows():
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