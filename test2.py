import os
import pandas as pd 
import numpy as np 
from lyricsgenius import Genius
from dotenv import load_dotenv


import pandas as pd

rap_df = pd.read_csv('/home/lettuce/MyCode/pandasproject/Rap-vs-Country-StatisticalStudy/final_rap.csv')

index_list = rap_df.columns.tolist()

my_dict = {key: 0 for key in index_list}

print(my_dict)



