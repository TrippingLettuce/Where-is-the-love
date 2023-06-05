import pandas as pd
import numpy as np


rap_df = pd.read_csv('/home/lettuce/MyCode/pandasproject/Rap-vs-Country-StatisticalStudy/raper_name copy.csv')

input_string = rap_df["Lyrics"][2]

print(input_string)

import re #push the test

def process_string(input_string):
    # Remove all occurrences of a standalone backslash
    input_string = re.sub(r'\\(?![n])', '', input_string)
    
    # Replace all occurrences of \n with a single space
    input_string = re.sub(r'\\n', ' ', input_string)
    
    # Remove specified characters: ',', ''', '(', ')', '?', '"', ':', '-', '!'
    input_string = re.sub(r"[,'\(\)\?\":\-!]", '', input_string)

    return input_string



output_string = process_string(input_string)
print(output_string)


rap_df["Lyrics"][0] = output_string

rap_df.to_csv('/home/lettuce/MyCode/pandasproject/Rap-vs-Country-StatisticalStudy/raper_name copy.csv',index=False)