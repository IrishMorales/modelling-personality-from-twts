import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import r2_score

metric_filepath = "preprocessed-data/user_metrics.csv"
user_data_filepath = "preprocessed-data/twt_valid_user_masterlist.csv"

metric = pd.read_csv(metric_filepath,
                     index_col = 0)

user_data = pd.read_csv(user_data_filepath, 
                        sep=',', 
                        quotechar='"')

trait_list = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]

#get list of structural metrics
metric_list = list(metric)
del metric_list[0]

#creates and prints scatter plot of regression on test data
def plot(trait_name, metric_name, x, y, mean_reg, linear_reg, svr):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
    plt.scatter(x_test, y_test)
    plt.plot(x_test, mean_reg.predict(x_test), color = "black")
    plt.plot(x_test, linear_reg.predict(x_test), color = "red")
    
    x_test = np.arange(min(x), max(x), 0.1)
    x_test = x_test.reshape((len(x_test), 1))
    plt.plot(x_test, svr.predict(x_test), color = "green")
    
    plot_title = trait_name + " vs " + metric_name
    plt.title(plot_title)
    plt.xlabel(metric_name)
    plt.ylabel(trait_name)
    
    #output plot as .png
    filename = "figures/" + trait_name + " vs " + metric_name + ".png"
    plt.savefig(filename, bbox_inches='tight')
    
    plt.show()

#evaluate based on RMSE and R^2
def evaluate(y_true, y_pred, regressor_type):
    print("Evaluation of", regressor_type,
          file = results)    
    print('RMSE: %.4f' % np.sqrt(metrics.mean_squared_error(y_true, y_pred)),
          file = results)
    print("R^2: " + '%.4f' % (r2_score(y_true, y_pred)*100) + "%",
          file = results)
    
#create baseline (mean) regressor
def get_mean_reg(trait_name, metric_name, x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
    
    # Create baseline regressor (always predicts mean)
    from sklearn.dummy import DummyRegressor
    mean_regressor = DummyRegressor(strategy='mean')
    mean_regressor.fit(x_train, y_train)
    
    evaluate(y_test, mean_regressor.predict(x_test), "Baseline Regressor")
    return mean_regressor

#perform linear regression
def get_linear_reg(trait_name, metric_name, x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
    lin_regressor = LinearRegression()
    lin_regressor.fit(x_train, y_train)
    
    evaluate(y_test, lin_regressor.predict(x_test), "Linear Regression")
    return lin_regressor

''' Commented out because logistic regression is a classification method
#perform logistic regression
def logistic_reg(trait_name, metric_name, x, y):
    from sklearn.linear_model import LogisticRegression
    from sklearn import preprocessing
    from sklearn import utils

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
    log_regressor = LogisticRegression(solver = 'lbfgs', multi_class='auto')
    #transform data from continuous to multiclass for log reg only
    lab_enc = preprocessing.LabelEncoder()
    y_train = lab_enc.fit_transform(y_train)
    log_regressor.fit(x_train, y_train)
    
    y_pred = log_regressor.predict(x_test)
    evaluate(y_test, y_pred)
    
    df = pd.DataFrame({'x': x_test[:,0], 'y': y_test})
    df = df.sort_values(by='x')
    from scipy.special import expit
    
    plt.figure(1)
    sigmoid_function = expit(df['x'] * log_regressor.coef_[0][0] + log_regressor.intercept_[0]).ravel()
    plt.plot(df['x'], sigmoid_function)
    plt.scatter(df['x'], df['y'], c=df['y'], cmap='rainbow', edgecolors='b')
'''

#perform support vector regression
def get_svr(trait_name, metric_name, x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
    
    from sklearn.svm import SVR
    regressor = SVR(kernel='rbf', gamma='scale')
    regressor.fit(x,y)
    y_pred = regressor.predict(x_test)

    evaluate(y_test, y_pred, "Support Vector Regression")
    return regressor

#open results.txt for writing
results = open('results.txt', 'w')

#run all regression
for trait_name in trait_list:
    for metric_name in metric_list:
        print (trait_name, "vs", metric_name, 
               file = results)
        
        mean_reg   = get_mean_reg   (trait_name, metric_name, 
                     metric[metric_name].values.reshape(-1,1), user_data[trait_name])
        linear_reg = get_linear_reg (trait_name, metric_name, 
                     metric[metric_name].values.reshape(-1,1), user_data[trait_name])
        svr        = get_svr        (trait_name, metric_name, 
                     metric[metric_name].values.reshape(-1,1), user_data[trait_name])\
        
        plot(trait_name, metric_name, 
             metric[metric_name].values.reshape(-1,1), user_data[trait_name],
             mean_reg, linear_reg, svr)
        
        print ("-----------------------------------------------------------",
               file = results)
        
results.close()