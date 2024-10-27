# user_list_page.py
import pickle
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_log_error
import joblib

# Define rmsle function
def rmsle(y_true, y_pred):
    return np.sqrt(mean_squared_log_error(y_true, y_pred))

# Custom unpickler to include rmsle function
class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'rmsle':
            return rmsle
        return super().find_class(module, name)

def user_list_page(navigate_to):
    st.title("User List 👥")

    # Placeholder list of users (replace with your actual user data)
    users = ['1743', '1976', '473', '859']
    df = pd.read_csv("../data/users_processing_vModel.csv")

    st.write("Select a user to view details:")
    selected_user = st.selectbox("Users", users)

    def set_user_and_navigate():
        st.session_state.selected_user = selected_user
        user = df[df['userid'] == int(selected_user)].drop(['F_Grade'], axis=1)
        
        # Load models using Custom Unpickler
        with open('../models/meta_model.pkl', 'rb') as file:
            meta_model = CustomUnpickler(file).load()
        with open('../models/gtb_model.pkl', 'rb') as file:
            gtb_model = CustomUnpickler(file).load()
        with open('../models/rbf_svr_model.pkl', 'rb') as file:
            rbf_svr_model = CustomUnpickler(file).load()
        with open('../models/rf_model.pkl', 'rb') as file:
            rf_model = CustomUnpickler(file).load()
        with open('../models/xgb_model.pkl', 'rb') as file:
            xgb_model = CustomUnpickler(file).load()
        
        # Predict with loaded models
        stacking_output = np.column_stack((xgb_model.predict(user), gtb_model.predict(user), 
                                           rbf_svr_model.predict(user), rf_model.predict(user)))
        y_pred = meta_model.predict(stacking_output)
        std_dev, mean = 2.750259736738074, 5.126167664670659
        predictions = (y_pred * std_dev) + mean

        # Determine pass or fail
        st.session_state.pass_mark = predictions[0] >= 5
        navigate_to('user_details')

    st.button("Go to User Details", on_click=set_user_and_navigate)

