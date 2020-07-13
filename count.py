#PY3 SCRIPT FOR COUNTING METRICS
import pandas as pd
import string
from itertools import groupby
from ast import literal_eval

'''
DATAFRAMES:
raw_twt - dataframe of users and tweets
twt_twt - preprocessed dataframe of users and tweets
twt_twt_ns - a copy of twt_twt without special tokens
twt_twt_ns_np - a copy of twt_twt without special tokens and punctuations
user_data - dataframe of tweet count, fave count, etc. per user
user_cnt - dataframe of metric count per user
'''

#function to remove special tokens from tweet
def rm_special(tweet):
    special_tokens = ["USERNAME", "URL", "HASHTAG", "EMOTICON", "EMOJI", "NUMBER"]
    new_tweet = [token for token in tweet if not token in special_tokens]
    return new_tweet

#function to count uppercase letters in tweet
def count_uppercase(tweet):
    count = sum(sum(1 for char in word if char.isupper()) for word in tweet)
    return count

#function to count given metric across twts
def count_metric(metric):
    return twt_twt["Text"].apply(lambda row : row.count(metric))

#function to count punctuation in twts
def count_punctuation(tweet):
    punctuation_count = 0
    for token in tweet:
        for character in token:
            if character in string.punctuation:
                punctuation_count +=1  
    return punctuation_count

    
#function to count consecutive repeated chars
def count_rep_chars(tweet):
    '''
    1. converts word to lowercase using .lower()
    2. group consecutive unique chars in each word using groupby()
    3. iterates over groups
    4. count times each char is repeated in current group
    5. if char repeated in current group > 1 time, add to sum
    Example:
    groups = groupby("Tttteeeeests".lower()) 
    - returns ((t, <itertools._grouper object>), 
               (e, <itertools._grouper object>),
               (s, <itertools._grouper object>),
               (t, <itertools._grouper object>),
               (s, <itertools._grouper object>))
    '''
    charRepSum = 0
    for word in tweet:
        groups = groupby(word.lower())
        for group in groups:
            charRep = (sum(1 for char in group[1]))
            if (charRep > 1):
                charRepSum += charRep          
    return charRepSum


#function to count consecutive repeated words
def count_rep_words(tweet):
    '''
    1. converts tweet to lowercase using .lower()
    2. group consecutive unique words in each tweet using groupby()
       and removes punctuation using if .isalpha()
    3. iterates over groups
    4. count times each word is repeated in current group
    5. if word repeated in current group > 1 time, add to sum
    Example:
    tweet = ["papasa", "papasa", "pApaSa", "pls", "lang", "!"]
    - returns ((papasa, <itertools._grouper object>), 
               (pls, <itertools._grouper object>),
               (lang, <itertools._grouper object>))
    '''
    wordRepSum = 0
    groups = groupby(word.lower() for word in tweet if word[0].isalpha())
    for group in groups:
        wordRep = (sum(1 for word in group[1]))
        if (wordRep > 1):
            wordRepSum += wordRep
    return wordRepSum


#initialize variables
twt_twt_filepath = "preprocessed-data/tweet_tweet_pp.csv"
user_data_filepath = "preprocessed-data/twt_user_masterlist.csv"
valid_user_filepath = "preprocessed-data/twt_valid_user_masterlist.csv"

#read tweet data from csv, import into dataframe
twt_twt = pd.read_csv(twt_twt_filepath, 
                      sep=',', 
                      quotechar='"',
                      index_col="TweetID",
                      usecols = ["TweetID", "UserID", "Text"])

twt_twt = twt_twt.sort_values("UserID")

user_data = pd.read_csv(user_data_filepath,
                      sep=',', 
                      quotechar='"',
                      usecols = ["UserID", "TweetCount"])

valid_user = pd.read_csv(valid_user_filepath,
                      sep=',', 
                      quotechar='"',
                      index_col = "UserID",
                      usecols = ["UserID", "TweetCount"])

user_cnt = pd.DataFrame(columns = ['UserID'])
twt_average = pd.DataFrame()

#converts each tweet into a list instead of a string
twt_twt['Text'] = twt_twt["Text"].apply(literal_eval)

#removes userIDs in user_data that are not in twt_twt
user_data = user_data.sort_values("UserID")
user_data = user_data.set_index("UserID")
user_data = user_data.reindex(index = twt_twt.UserID.unique())

#initialize twt_twt_ns: a copy of twt_twt without special tokens
twt_twt_ns = twt_twt.copy()
twt_twt_ns['Text'] = twt_twt["Text"].apply(rm_special)

#initialize twt_twt_ns_np: a copy of twt_twt without special tokens and punctuations
twt_twt_ns_np = twt_twt_ns.copy()
twt_twt_ns_np["Text"] = twt_twt_ns['Text'].astype(str).str.replace(r'[^\w\s]+', '')

#count metrics per tweet and store in twt_twt
twt_twt["UsernameCount"] = count_metric("USERNAME")
twt_twt["URLCount"] = count_metric("URL")
twt_twt["HashtagCount"] = count_metric("HASHTAG")
twt_twt["EmojiCount"] = count_metric("EMOJI")
twt_twt["EmoticonCount"] = count_metric("EMOTICON")

#count words, uppercase letters and total characters
twt_twt['WordCount'] = twt_twt_ns_np['Text'].str.split().str.len()
twt_twt['CharacterCount'] = twt_twt_ns['Text'].apply(''.join).str.len()
twt_twt['UppercaseCount'] = twt_twt_ns['Text'].apply(count_uppercase)
twt_twt['PunctuationCount'] = twt_twt_ns['Text'].apply(count_punctuation)

#count consecutive repeating characters
twt_twt['CharRepCount'] = twt_twt_ns["Text"].apply(count_rep_chars)
twt_twt['WordRepCount'] = twt_twt_ns["Text"].apply(count_rep_words)

#count metrics per user and store in user_cnt
for user_id in twt_twt.UserID.unique():
    tmp_user_cnt = twt_twt.loc[twt_twt["UserID"] == user_id].sum(skipna=True, numeric_only=True)
    #overwrite summed UserIDs with current UserID
    tmp_user_cnt[0] = user_id
    user_cnt = user_cnt.append(tmp_user_cnt,
                               ignore_index = True)

user_cnt = user_cnt.set_index(user_cnt["UserID"])
user_cnt['TweetCount'] = user_data['TweetCount'].copy()

#Counts Averages
twt_average['TweetCount'] = user_cnt['TweetCount']
twt_average = twt_average.set_index(user_data.index)
twt_average['URLAverage'] = user_cnt['URLCount'].div(user_cnt['TweetCount'])
twt_average['UsernameAverage'] = user_cnt['UsernameCount'].div(user_cnt['TweetCount'])
twt_average['HashtagAverage'] = user_cnt['HashtagCount'].div(user_cnt['TweetCount'])
twt_average['EmojiAverage'] = user_cnt['EmojiCount'].div(user_cnt['TweetCount'])
twt_average['EmoticonAverage'] = user_cnt['EmoticonCount'].div(user_cnt['TweetCount'])
twt_average['WordAverage'] = user_cnt['WordCount'].div(user_cnt['TweetCount'])
twt_average['CharacterAverage'] = user_cnt['CharacterCount'].div(user_cnt['TweetCount'])
twt_average['UppercaseAverage'] = user_cnt['UppercaseCount'].div(user_cnt['TweetCount'])
twt_average['PunctuationAverage'] = user_cnt['PunctuationCount'].div(user_cnt['TweetCount'])
twt_average['CharrepAverage'] = user_cnt['CharRepCount'].div(user_cnt['TweetCount'])
twt_average['WordrepAverage'] = user_cnt['WordRepCount'].div(user_cnt['TweetCount'])
#remove non-valid users in twt_average

twt_average = twt_average.reindex(index = valid_user.index)

#output data
twt_average.to_csv('preprocessed-data\\user_metrics.csv', index=True)