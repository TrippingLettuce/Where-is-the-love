import os
import pandas as pd 
import numpy as np 
from lyricsgenius import Genius
from dotenv import load_dotenv
import funkyFunctions

load_dotenv()  # Load environment variables from the .env file

genius_key = os.getenv('GENUIS_KEY')
genius = Genius(genius_key,timeout=15)
genius.verbose = False
genius.remove_section_headers = True
genius.excluded_terms = ["(Remix)", "(Live)"]

#Define Dataframes
#csv_start = pd.read_csv('/home/lettuce/MyCode/Statistical-Analysis-of-Music-Genres/src/rap_ERA.csv')



#Get data 
#funkyFunctions.getData(csv_start)
#Clean Data 
csv_mid = pd.read_csv('/home/lettuce/MyCode/pandasproject/rap_mid1.csv')
funkyFunctions.cleanData(csv_mid)
#Organize Data
#csv_mid = pd.read_csv('/home/lettuce/MyCode/pandasproject/rap_mid2.csv')
#funkyFunctions.organizeDataTotal(csv_mid)
#Orgaize Data Artist
#csv_final = pd.read_csv('/home/lettuce/MyCode/pandasproject/rap_end.csv')
#funkyFunctions.organizeDataArtist(csv_mid, csv_final)

#Anaylize Data


#Eras of rap


# Take 50 top hip hop and 50 top rap combo

#TOp 100 country

#raper_df = pd.read_csv('/home/lettuce/MyCode/pandasproject/raper_name.csv')

#print(raper_df.head().to_string())