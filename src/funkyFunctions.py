import os
import pandas as pd 
import numpy as np 
from lyricsgenius import Genius
from dotenv import load_dotenv
import re
import requests


load_dotenv()  # Load environment variables from the .env file

genius_key = os.getenv('GENUIS_KEY')
genius = Genius(genius_key,timeout=30)
genius.verbose = False
genius.remove_section_headers = True
genius.excluded_terms = ["(Remix)", "(Live)"]

def getData(rap_df):

    song_number = 2
    #Fill Songs and Lyrics Column with Nan
    rap_df['Songs'] = np.nan
    rap_df['Lyrics'] = np.nan
    #Show head
    print(rap_df.head())

    #Loop through rows
    #for x in range(loc(rap_df)):
    for x in range(3):
        #Get artist name
        artist_name = rap_df.loc[x][0]
        print(f"Getting Data for {artist_name}")
        #Pull song data from genuis
        # Retry mechanism
        retries = 3
        while retries > 0:
            try:
                # Pull song data from genius
                artist = genius.search_artist(artist_name, max_songs=song_number, sort="popularity")
                break
            except requests.exceptions.Timeout:
                retries -= 1
                print(f"Request timed out. Retrying... {retries} attempts remaining.")
                if retries == 0:
                    print(f"Failed to get data for {artist_name}. Skipping...")
                    continue
        #Temp song and lyric list
        song_list = []
        song_lyrics_list = []

        #iiterate through songs and year 
        for song in artist.songs:
            print(song.title)
            song_list.append(song.title)


        # Add to row
        rap_df['Songs'][x] = song_list

        # Iterate over the lyrics and add them to the list
        for song in song_list:
            lyrics = genius.search_song(artist_name,song)
            song_lyrics_list.append(lyrics.lyrics)
        #Add to row
        rap_df['Lyrics'][x] = song_lyrics_list

    print("Data Has Been Recived")
    #Show head
    print(rap_df.head())
    


def cleanData(rap_df):
    print("Cleaning Data...")

    for x in range(2):
        name = rap_df["Rap Name"][x]
        print(f"Cleaning data for {name}")

        lyrics_list = rap_df["Lyrics"][x]
        cleaned_lyrics_list = []

        #Maybe not go trhough loop

        cleaned_lyric = process_string(lyrics_list)
        cleaned_lyrics_list.append(cleaned_lyric)

        rap_df["Lyrics"][x] = cleaned_lyrics_list

    print("Cleaned Data")
    rap_df.to_csv("/home/lettuce/MyCode/Statistical-Analysis-of-Music-Genres/src/rap_mid2.csv",index=False)
    print(rap_df.head())


def process_string(input_string):
    # Remove all occurrences of a standalone backslash
    input_string = re.sub(r'\\(?![n])', '', input_string)
    
    # Replace all occurrences of \n with a single space
    input_string = re.sub(r'\\n', ' ', input_string)
    
    # Remove specified characters: ',', ''', '(', ')', '?', '"', ':', '-', '!'
    input_string = re.sub(r"[,'\(\)\?\":\-!]", '', input_string)

    return input_string


#Create a dictornary Key is word Value is count 
# IF there is a new word apphend the dictonary
# IF word exist then add 1 to value 
def organizeDataTotal(rap_df):
    #Overall for all rappers
    lyric_dict_all_rap = {}

    print("")
    print("Organizing TotalData...")
    print("")

    #Itterate through each row 
    for x in range(4):
    #Take lyric column
        lyrics = rap_df['Lyrics'][x]
        words = lyrics.lower().split()
        for word in words: 
            if word in lyric_dict_all_rap:
                lyric_dict_all_rap[word] += 1
            else:
                lyric_dict_all_rap[word] = 1


    # Append the key-value pair to the dictionary
    #my_dict[key] = value
    #Sorting the dictonary 
    sorted_word_count = sorted(lyric_dict_all_rap.items(), key=lambda item: item[1], reverse=True)
    #Put in new data frame 
    #Rows 
    my_index = ['Total']
    for x in range(len(rap_df)):
        my_index.append(rap_df['Rap Name'][x])
    #Put in new data frame
    #Columns
    my_columns = []             #Go to top 500 words when we have more data
    for key, value in sorted_word_count[:500]:
        my_columns.append(key)

    #Fill in data with Nan
    nan_array = np.empty((len(my_index), len(my_columns)))
    nan_array[:] = np.NaN
    #Filling in Total Row
    total_list = []
    for key, value in sorted_word_count[:500]:
        total_list.append(value)

    #Create DF
    rap_final = pd.DataFrame(nan_array,index=my_index,columns=my_columns) 
    #Add total values
    rap_final.loc["Total"] = total_list
    
    # Create a new DataFrame with "Artist Name" as the first column
    artist_name_df = pd.DataFrame(['Total'] + rap_df['Rap Name'].tolist(), columns=["Artist Name"])
    
    # Reset the index of rap_final DataFrame to be numeric
    rap_final.reset_index(drop=True, inplace=True)

    # Concatenate the artist_name_df DataFrame with rap_final DataFrame
    rap_final = pd.concat([artist_name_df, rap_final], axis=1)

    #Index needs to be True
    #rap_final.to_csv("/home/lettuce/MyCode/pandasproject/rap_end.csv",index=False)


#Had to use ChatGpt for some of this as Idk 
def organizeDataArtist(rap_df, rap_final):
    print("Organizing Data...")

    #Grab Total Row
    total = rap_final.iloc[0].to_dict()

    #Get index list
    index_list = rap_final.columns.tolist()

    for x in range(4):
        artist_name = rap_df["Rap Name"][x]  # Update the index to start from 0
        print(f"Organizing Lyrics for {artist_name}")

        # Temp dictionary reset (Uses most common [] words)
        dick = {key: 0 for key in index_list}

        # Add artist column
        dick["Artist Name"] = artist_name

        # Take lyric column
        lyrics = rap_df['Lyrics'][x]  # Update the index to start from 0
        words = lyrics.lower().split()
        for word in words:
            if word in index_list:
                # Add one to dick
                dick[word] += 1

        # Update the row in rap_final DataFrame
        rap_final.loc[x] = dick

    #So bassically I have to create a new empty row and save the total to top cuz I am a dumb ass somehow
    nan_row = pd.DataFrame(columns=rap_final.columns, index=[0])
    nan_row.loc[0] = np.nan
    rap_final = pd.concat([nan_row, rap_final], ignore_index=True)
    
    rap_final.loc[0] = total

    #Gonna also change nword to nword  ok
    #Want to talk or not to talk about the use of the nword in rap 
    #N-word N-words HardR
    
    #Add like column to front
    

    #rap_final.to_csv("/home/lettuce/MyCode/pandasproject/rap_end.csv",index=False)
    print("Organized Data")





