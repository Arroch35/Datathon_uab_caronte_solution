def rmsle(y_true, y_pred):
    return np.sqrt(mean_squared_log_error(y_true, y_pred))

# Import necessary libraries if required
import numpy as np
from sklearn.metrics import mean_squared_log_error
import pandas as pd

# Now load the model
import joblib
with open('../models/meta_model.pkl', 'rb') as file:
    meta_model = joblib.load(file)
with open('../models/gtb_model.pkl', 'rb') as file:
    gtb_model = joblib.load(file)
with open('../models/rbf_svr_model.pkl', 'rb') as file:
    rbf_svr_model = joblib.load(file)
with open('../models/rf_model.pkl', 'rb') as file:
    rf_model = joblib.load(file)
with open('../models/xgb_model.pkl', 'rb') as file:
    xgb_model = joblib.load(file)


df = pd.read_csv("../data/users_processing_vModel.csv")
user = df[df['userid'] == int('1743')]
user = user.drop(['F_Grade'], axis=1)

stacking_output= np.column_stack((xgb_model.predict(user), gtb_model.predict(user), rbf_svr_model.predict(user), rf_model.predict(user)))
y_pred = meta_model.predict(stacking_output)

std_dev, mean = 2.750259736738074, 5.126167664670659
predictions = (y_pred * std_dev) + mean

print(predictions[0])