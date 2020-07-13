import pandas as pd
from scipy import stats

features_filepath = "preprocessed-data/user_metrics.csv"
users_filepath = "preprocessed-data/twt_valid_user_masterlist.csv"

df_features = pd.read_csv(features_filepath,
                      sep=',', 
                      quotechar='"',
                      index_col = "UserID")



df_users = pd.read_csv(users_filepath,
                      sep=',', 
                      quotechar='"',
                      index_col = "UserID",
                      usecols = ['UserID', 'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism'])

df_corr = pd.DataFrame() # Correlation matrix
df_p = pd.DataFrame()  # Matrix of p-values
for x in df_features.columns:
    for y in df_users.columns:
        corr = stats.pearsonr(df_features[x], df_users[y])
        df_corr.loc[x,y] = corr[0]
        df_p.loc[x,y] = corr[1]

df_corr.to_csv("Extracted_Corr.csv")
df_p.to_csv("Extracted_Pvalue.csv")