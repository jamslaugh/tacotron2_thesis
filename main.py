from research_preprocessing.conciliator import *
from research_preprocessing.data_ingestion import inserted_df
from research_preprocessing.data_loader import EafReader

import pandas as pd
import numpy as np
import os

#TODO: 1) estabilish the logic behind the data loading;
#      2) estabilish the logic behind the conciliation;
#      3) create the time_conciliation table
#      4) clean the mess. Fill NA both with PRL token or specific prolongation.
