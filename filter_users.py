#PY3 SCRIPT FOR FILTERING OUT INVALID USERS
import pandas as pd

'''
Criteria for valid Twitter user:
- Tweet count at least 100
- Filipino nationality or dual nationality includes Filipino

Dataframes:
twt_data - UserID, twt user data
user_data - UserID, user data, personality test results
twt_masterlist - UserID, twt data, user data, personality test results of valid twt users
'''

#initialize variables
twt_data_filepath = "project-data/twitter_data.csv"
user_data_filepath = "project-data/user.csv"
per_test_filepath = "project-data/personality_test.csv"

twt_data = pd.read_csv(twt_data_filepath,
                      sep=',', 
                      quotechar='"',
                      index_col = "UserID")

#read from user.csv and personality test results
user_data = pd.concat(map(pd.read_csv, [user_data_filepath, per_test_filepath]), sort=False, axis=1)

#remove duplicate columns
user_data = user_data.loc[:, ~user_data.columns.duplicated()]
user_data = user_data.set_index("UserID")

#remove non-twitter users in user_data
user_data = user_data.reindex(index=twt_data.index)

#output masterlist including invalid twt users
twt_masterlist = pd.concat([twt_data, user_data], sort=False, axis=1)
twt_masterlist.to_csv('preprocessed-data\\twt_user_masterlist.csv')

#remove invalid users
twt_masterlist = twt_masterlist.drop(twt_masterlist[(twt_masterlist.TweetCount < 100)].index)
twt_masterlist = twt_masterlist.drop(twt_masterlist[(twt_masterlist["Nationality"].str.contains("Filipino") == False)].index)
twt_masterlist.to_csv('preprocessed-data\\twt_valid_user_masterlist.csv')