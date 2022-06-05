# libraries
# from asyncio.windows_utils import pipe
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import StackingRegressor
# from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import StandardScaler
# from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt 
import pickle

# constants
TARGET_COLUMN = 'Production'
STACKING_MODEL_FILE = './models/stacking_model.sav'
LINEAR_MODEL_FILE = './models/linear_model.sav'
RIDGE_MODEL_FILE = './models/ridge_model.sav'
LASSO_MODEL_FILE = './models/lasso_model.sav'
ENET_MODEL_FILE = './models/enet_model.sav'
POLY_LINEAR_MODEL_FILE = './models/poly_linear_model.sav'
POLY_RIDGE_MODEL_FILE = './models/poly_ridge_model.sav'
POLY_LASSO_MODEL_FILE = './models/poly_lasso_model.sav'
POLY_ENET_MODEL_FILE = './models/poly_enet_model.sav'
POLY_STACKING_MODEL_FILE = './models/poly_stacking_model.sav'
POLY_LINEAR_STACKING_MODEL_FILE = './models/poly_linear_stacking_model.sav'

predScores = {}
predR2Scores = {}
predMSE = {}

print('Crop Yield Prediction Model Training')
print('\n\n')

print('Importing Crop Yield dataset')
# dataset with label preprocessing
data = pd.read_csv('./data/dataset.csv')
print('The shape of the dataset is: ', data.shape)

print('\n\n')
print(data.head())

print('\n\n')
print('Dataset Datatypes')
print(data.info())

print('\n\n')
print('Removing Null Values(if any)')
data = data.dropna()
print('Dataset shape after removing null values ', data.shape)

print('\n\n')
print('Performing Label Preprocessing')
labelEncoder = LabelEncoder()
cols = ['State_Name', 'District_Name', 'Season', 'Crop']
for col in cols:
    print(col)
    labelEncoder.fit(data[col])
    data[col] = labelEncoder.transform(data[col])

print('\n')
print('Data after label preprocessing')
print(data.head())


print('\n\n')
print('Filtering data with Interquantile filter (using column "Production" to filter)')

# remove outliers
def subset_by_iqr(df, column, whisker_width=1.5):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    # Apply filter with respect to IQR, including optional whiskers
    filter = (df[column] >= q1 - whisker_width *
              iqr) & (df[column] <= q3 + whisker_width*iqr)
    return df.loc[filter]

data = subset_by_iqr(data, TARGET_COLUMN)  # Filtering with Production column
print('Dataset shape after IQR filter ', data.shape)
print(data.head())

array = data.columns
predictors = array[0:6]
# print(predictors)

# print('Normalizing Data')
# data[predictors] = data[predictors] / \
#     data[predictors].max()  # Normalizing the data


print('\n\n')
print('Splitting dataset into training and testing data')
# training and testing dataset
X = data[predictors].values
y = data[TARGET_COLUMN].values

# poly = PolynomialFeatures(degree=3)
# poly_variables = poly.fit_transform(X)

# print(y)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=40)

# poly_var_train, poly_var_test, res_train, res_test = train_test_split(poly_variables, y, test_size=0.2, random_state=40)

print('Training datapoints for linear regression algorithms ', len(X_train))
print('Testing datapoints for linear regression algorithms ', len(X_test))

# print('\n')

# print('Training datapoints for ploynomial regression algorithms ', len(poly_var_train))
# print('Testing datapoints for polynomial regression algorithms ', len(poly_var_test))

# print('\n\n')

# linear regression
print('\n\n')
print('Linear Regression')
model_linear = LinearRegression()
model_linear.fit(X_train, y_train)

scoreLinear = model_linear.score(X_test, y_test)
print(' - score : ', scoreLinear)
predScores['linear'] = scoreLinear

predTestLinear = model_linear.predict(X_test)
r2Linear = r2_score(y_test, predTestLinear)
print(' - r2 score (on testing data) : ', r2Linear)
predR2Scores['liner'] = r2Linear

mseLinear = np.sqrt(mean_squared_error(y_test, predTestLinear))
print(' - Mean Squared Error (on testing data) : ', mseLinear)
predMSE['linear'] = mseLinear

print('Saving the model')
pickle.dump(model_linear, open(LINEAR_MODEL_FILE, 'wb'))

# polynomial regression
# print('\n\n')
# print('Training Linear Regression Model on polynomial data')
# poly_regression = LinearRegression()
# poly_regression.fit(poly_var_train, res_train)
# socrePolyLinear = poly_regression.score(poly_var_test, res_test)
# print('Polynomial Linear Regression score : ', socrePolyLinear)
# predScores['poly_linear'] = socrePolyLinear
# print('Saving the model')
# pickle.dump(model_linear, open(POLY_LINEAR_MODEL_FILE, 'wb'))


# Ridge regression
print('\n\n')
print('Ridge Regression')
model_ridge = Ridge(alpha=0.01)
model_ridge.fit(X_train, y_train)

scoreRidge = model_ridge.score(X_test, y_test)
print(' - score : ', scoreRidge)
predScores['ridge'] = scoreRidge

predTestRidge = model_ridge.predict(X_test)
r2Ridge = r2_score(y_test, predTestRidge)
print(' - r2 score (on testing data) : ', r2Ridge)
predR2Scores['ridge'] = r2Ridge

mseRidge = np.sqrt(mean_squared_error(y_test, predTestRidge))
print(' - MEan Squared Error (on testing data) : ', mseRidge)
predMSE['ridge'] = mseRidge

print('Saving the model')
pickle.dump(model_ridge, open(RIDGE_MODEL_FILE, 'wb'))

# Polynomial Ridge regression
# print('\n\n')
# print('Training Ridge Regression Model on polynomial data')
# poly_ridge = Ridge(alpha=0.01, fit_intercept=True)
# # poly_ridge.fit(poly_var_train, res_train)
# pipeRidge = make_pipeline(StandardScaler(), poly_ridge)
# pipeRidge.fit(poly_var_train, res_train)
# scorePolyRidge = pipeRidge.score(poly_var_test, res_test)
# print('Polynomial Ridge Regression Socre : ',scorePolyRidge)
# predScores['poly_ridge'] = scorePolyRidge
# print('Saving the model')
# pickle.dump(poly_ridge, open(POLY_RIDGE_MODEL_FILE, 'wb'))

# Lasso regression
print('\n\n')
print('Lasso Regression')
model_lasso = Lasso(alpha=0.01)
model_lasso.fit(X_train, y_train)
scoreLasso = model_lasso.score(X_test, y_test)
print(' - score : ', scoreLasso)
predScores['lasso'] = scoreLasso

predTestLasso = model_lasso.predict(X_test)
r2Lasso = r2_score(y_test, predTestLasso)
print(' - r2 score (on testing data) : ', r2Lasso)
predR2Scores['lasso'] = r2Lasso

mseLasso = np.sqrt(mean_squared_error(y_test, predTestLasso))
print(' - Mean Squared Error (on testing data) : ',mseLasso)
predMSE['lasso'] = mseLasso

print('Saving the model')
pickle.dump(model_lasso, open(LASSO_MODEL_FILE, 'wb'))

# Polynomial Lasso Regression
# print('\n\n')
# print('Training Lasso Regression Model on polynomial data')
# poly_lasso = Lasso(alpha=0.01, fit_intercept=True, max_iter=50000)
# # poly_lasso.fit(poly_var_train, res_train)
# pipeLasso = make_pipeline(StandardScaler(), poly_lasso)
# pipeLasso.fit(poly_var_train, res_train)
# scorePolyLasso = pipeLasso.score(poly_var_test, res_test)
# print('Polynomial Lasso Regression score : ', scorePolyLasso)
# predScores['poly_lasso'] = scorePolyLasso
# print('Saving the model')
# pickle.dump(poly_lasso, open(POLY_LASSO_MODEL_FILE, 'wb'))


# eNet regression
print('\n\n')
print('Elastic Net Regression')
model_enet = ElasticNet(alpha=0.01)
model_enet.fit(X_train, y_train)

scoreENet = model_enet.score(X_test, y_test)
print(' - score: ', scoreENet)
predScores['enet'] = scoreENet

predTestEnet = model_enet.predict(X_test)
r2Enet = r2_score(y_test, predTestEnet)
print(' - r2 socre (on testing data) : ', r2Enet)
predR2Scores['enet'] = r2Enet

mseEnet = np.sqrt(mean_squared_error(y_test, predTestEnet))
print(' - Mean Squared Error (on testing data) : ', mseEnet)
predMSE['enet'] = mseEnet

print('Saving the model')
pickle.dump(model_enet, open(ENET_MODEL_FILE, 'wb'))

# polynomial eNet regression
# print('\n\n')
# print('Training eNet Regression Model with polynomial data')
# poly_enet = ElasticNet(alpha=0.01, fit_intercept=True, max_iter=50000)
# pipeEnet = make_pipeline(StandardScaler(), poly_enet)
# pipeEnet.fit(poly_var_train, res_train)
# # poly_enet.fit(poly_var_train, res_train)
# scorePolyEnet = pipeEnet.score(poly_var_test, res_test)
# print('Polynomial eNet Regression score : ', scorePolyEnet)
# predScores['poly_enet'] = scorePolyEnet
# print('Saving the model')
# pickle.dump(poly_enet, open(POLY_ENET_MODEL_FILE, 'wb'))

# Weak lerners list
level0 = [
    ('ridge', Ridge(alpha=0.01, fit_intercept=True)),
    ('lasso', Lasso(alpha=0.01, fit_intercept=True, max_iter=50000)),
    ('elasticNet', ElasticNet(alpha=0.01, fit_intercept=True, max_iter=50000))
]

# Meta learner
level1 = LinearRegression()
# level1 = ElasticNet(alpha=0.01)

# stacking regression
print('\n\n')
print('Stacking Regression')
stacking = StackingRegressor(estimators=level0, final_estimator=level1, cv=5)
stacking.fit(X_train, y_train)

scoreStacking = stacking.score(X_test, y_test)
print(' - score : ', scoreStacking)
predScores['stacking'] = scoreStacking

predTestStacking = stacking.predict(X_test)
r2Stacking = r2_score(y_test, predTestStacking)
print(' - r2 score (on testing data) : ', r2Stacking)
predR2Scores['stacking'] = r2Stacking

mseStacking = np.sqrt(mean_squared_error(y_test, predTestStacking))
print(' - Mean Squared Error (on testing data) : ', mseStacking)
predMSE['stacking'] = mseStacking

print('Saving the model')
pickle.dump(stacking, open(STACKING_MODEL_FILE, 'wb'))

# polynomial stacking regression
# print('\n\n')
# print('Training Stacking regression model on polynomial data')
# poly_stacking = StackingRegressor(estimators=level0, final_estimator=level1, cv=5)
# # poly_stacking.fit(poly_var_train, res_train)
# pipeStacking = make_pipeline(StandardScaler(), poly_stacking)
# pipeStacking.fit(poly_var_train, res_train)
# scorePolyStacking = pipeStacking.score(poly_var_test, res_test)
# print('Polynomial Stacking Regression Score : ', scorePolyStacking)
# predScores['poly_stacking'] = scorePolyStacking
# print('Saving the model')
# pickle.dump(poly_stacking, open(POLY_STACKING_MODEL_FILE, 'wb'))


# level01 = [
#     ('ridge', Ridge(alpha=0.01, fit_intercept=True)),
#     ('poly_ridge', make_pipeline(PolynomialFeatures(degree=3), StandardScaler(), Ridge(alpha=0.01, fit_intercept=True))),
#     ('lasso', Lasso(alpha=0.01, fit_intercept=True)),
#     ('poly_lasso', make_pipeline(PolynomialFeatures(degree=3), StandardScaler(), Lasso(alpha=0.01, fit_intercept=True))),
#     ('enet', ElasticNet(alpha=0.01, fit_intercept=True)),
#     ('poly_enet', make_pipeline(PolynomialFeatures(degree=3), StandardScaler(), ElasticNet(alpha=0.01, fit_intercept=True))),
# ]

# level11 = make_pipeline(PolynomialFeatures(degree=3), LinearRegression())


# print('\n\n')
# print('Training stacking with linear and polynomial ridge, lasso, enet as weak learners & polynomial regression as final estimator')
# poly_liear_stacking = StackingRegressor(estimators=level01, final_estimator=level11, cv=5)
# poly_liear_stacking.fit(X_train, y_train)
# scorePolyLinearStacking = poly_liear_stacking.score(X_test, y_test)
# print('Stacking Score : ', scorePolyLinearStacking)
# predScores['poly_linear_stacking'] = scorePolyLinearStacking
# print('Saving the model')
# pickle.dump(poly_liear_stacking, open(POLY_LINEAR_STACKING_MODEL_FILE, 'wb'))


# socre graph 
fig = plt.figure(figsize = (10,5))

plt.bar(list(predScores.keys()), list(predScores.values()), color = 'blue', width = 0.4)

plt.xlabel('Regression Model')
plt.ylabel('Model scores')
plt.title('Regression model score comparision')

plt.show()

# r2 socre graph 
fig = plt.figure(figsize = (10,5))

plt.bar(list(predR2Scores.keys()), list(predR2Scores.values()), color = 'green', width = 0.4)

plt.xlabel('Regression Model')
plt.ylabel('Model r2 scores')
plt.title('Regression model r2 score comparision')

plt.show()

# mse graph 
fig = plt.figure(figsize = (10,5))

plt.bar(list(predMSE.keys()), list(predMSE.values()), color = 'yellow', width = 0.4)

plt.xlabel('Regression Model')
plt.ylabel('Model MSE')
plt.title('Regression model MSE comparision')

plt.show()