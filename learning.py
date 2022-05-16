# libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import StackingRegressor
import pickle

# constants
TARGET_COLUMN = 'Production'
STACKING_MODEL_FILE = './models/stacking_model.sav'
LINEAR_MODEL_FILE = './models/linear_model.sav'
RIDGE_MODEL_FILE = './models/ridge_model.sav'
LASSO_MODEL_FILE = './models/lasso_model.sav'
ENET_MODEL_FILE = './models/enet_model.sav'

# dataset with label preprocessing
data = pd.read_csv('./data/pre-dataset.csv')
print('The shape of the dataframe is: ', data.shape)


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


array = data.columns
predictors = array[0:6]
# print(predictors)
# data[predictors] = data[predictors] / \
#     data[predictors].max()  # Normalizing the data


# training and testing dataset
X = data[predictors].values
y = data[TARGET_COLUMN].values
# print(y)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=40)


# Weak lerners list
level0 = [
    ('ridge', Ridge(alpha=0.01)),
    ('lasso', Lasso(alpha=0.01)),
    ('elasticNet', ElasticNet(alpha=0.01))
]

# Meta learner
level1 = LinearRegression()
# level1 = ElasticNet(alpha=0.01)

# linear regression
model_linear = LinearRegression()
model_linear.fit(X_train, y_train)
scoreLinear = model_linear.score(X_test, y_test)
print('Linear regression score : ', scoreLinear)
pickle.dump(model_linear, open(LINEAR_MODEL_FILE, 'wb'))

# Ridge regression
model_ridge = Ridge(alpha=0.01)
model_ridge.fit(X_train, y_train)
scoreRidge = model_ridge.score(X_test, y_test)
print('Ridge Regression score : ', scoreRidge)
pickle.dump(model_ridge, open(RIDGE_MODEL_FILE, 'wb'))

# Lasso regression
model_lasso = Lasso(alpha=0.01)
model_lasso.fit(X_train, y_train)
scoreLasso = model_lasso.score(X_test, y_test)
print('Lasso regression score : ', scoreLasso)
pickle.dump(model_lasso, open(LASSO_MODEL_FILE, 'wb'))

# eNet regression
model_enet = ElasticNet(alpha=0.01)
model_enet.fit(X_train, y_train)
scoreENet = model_enet.score(X_test, y_test)
print('Elastic Net Regression score: ', scoreENet)
pickle.dump(model_enet, open(ENET_MODEL_FILE, 'wb'))


# Trining stacking regression
stacking = StackingRegressor(estimators=level0, final_estimator=level1, cv=5)
stacking.fit(X_train, y_train)
scoreStacking = stacking.score(X_test, y_test)
print('Stacking regression score : ', scoreStacking)
pickle.dump(stacking, open(STACKING_MODEL_FILE, 'wb'))
