# modelling-personality-from-twts
A study by nerds.
Okay, seriously. Scripts for personality trait recognition based on structural metrics of tweets.

Full paper: ["Analyzing Structural Metrics to Predict Twitter User Personality Traits"](https://www.academia.edu/43608598/Analyzing_Structural_Metrics_to_Predict_Twitter_User_Personality_Traits).  
Made with @zivhd & @kildor22. Part of Project Personality by @EdTheAlchemist. 

### Structural Metrics:
- Words per Tweet
- Characters per word
- Uppercase letters per Tweet
- Punctuation marks per Tweet
- Hashtags per Tweet
- Mentions per Tweet
- Links per Tweet
- Emojis per Tweet
- Emoticons per Tweet
- Consecutive repeated characters per word (ex. "hmmm")
- Consecutive repeated words per Tweet (ex. "pls pls pls")

### Regression Models:
- Mean regression (baseline)
- Linear regression
- Support vector regression

### Notes: 
- Personality traits based on Five Factor Model
- Overwrite core.py from "emoji" library with the one in this repo
- Raw data available only to authors

### Directory tree/file descriptions:
```
root  
├── figures  
│   └── ...all plots per trait-metric pair output by regression.py  
├── practice-data  
│   └── ...practice data files  
├── preprocessed-data  
│   ├── tweet_tweet_pp.csv  (not in repo due to file size)  
|   |   - all preprocessed tweets  
|   |   - output of preprocessing.py on project-data/twitter_tweet.csv  
│   ├── tweet_tweet_pp_practice.csv  
|   |   - output of preprocessing.py on practice-data/tweet_tweet.csv  
│   ├── twt_user_masterlist.csv  
|   |   - info of all twt users  
│   ├── twt_valid_user_masterlist.csv  
|   |   - info of all valid twt users  
│   └── user_metrics.csv  
|       - user metrics for all *valid* twt users  
├── project-data (not in repo due to file size)  
│   ├── user.csv  
│   ├── twitter_tweet.csv  
│   ├── twitter_data.csv  
│   └── personality_test.csv  
├── .gitignore  
├── changelog.txt  
├── core.py  
|   - used instead of core.py in python emoji library  
|   - tokenizes emojis  
├── count.py  
|   - py3, counts metrics for each user  
|   - input:  
|     - preprocessed-data/tweet_tweet_pp.csv  
|     - preprocessed-data/twt_user_masterlist.csv  
|     - preprocessed-data/twt_valid_user_masterlist.csv  
|   - output:  
|     - preprocessed-data/user_metrics.csv  
├── emoticons.txt  
|   - additional emoticons recognized in twts  
├── filter_users.py   
|   - py3, writes masterlist and filters invalid users  
|   - input:  
|     - project-data/twitter_data.csv  
|     - project-data/user.csv  
|     - project-data/personality_test.csv  
|   - output:  
|     - preprocessed-data/twt_user_masterlist.csv  
|     - preprocessed-data/twt_valid_user_masterlist.csv  
├── preprocessing.py  
|   - py2, performs tokenization  
|   - input:  project-data/twitter_tweet.csv  
|   - output: preprocessed-data/tweet_tweet_pp.csv  
├── project-data.zip  
├── README.md  
├── regression.py  
|   - py3, performs regression and outputs plots  
|   - input:  
|     - preprocessed-data/user_metrics.csv  
|     - preprocessed-data/twt_valid_user_masterlist.csv  
|   - output:  
|     - results.txt  
|     - plots in figures/  
└── results.txt  
    - RMSE & R^2 scores for regression on all trait-metric pairs  
```