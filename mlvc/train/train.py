from .crunchbase import *

import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.metrics import f1_score
from xgboost import XGBClassifier
from datetime import datetime


class Train():
    def __init__(self, name):
        self.name = name

    def read_data(self):
        df = pd.read_csv('./Data/full_information_0_60k.csv')
        return df

    def train_model(self):
        df = Crunchbase().format_crunchbase()
        subset = df[['type_Group B', 'money_raised_at_ipo', 'number_of_acquisitions', 'type_Unicorn',
                     'employee_cat', 'valuation_at_ipo', 'number_of_investments', 'type_Group A',
                     'type_Emerging Unicorn', 'number_of_lead_investments', 'number_of_lead_investors',
                     'number_of_employee_profiles',
                     'industries_type_2', 'type_For Profit', 'total_products_active', 'ipo_status']]
        x = subset[subset.columns.drop('ipo_status')]
        y = subset[['ipo_status']]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)

        # scale data
        scaler = StandardScaler()
        # save the scaler
        today = datetime.today().strftime('%Y-%m-%d')
        x_train_scaled = scaler.fit_transform(x_train)
        pickle.dump(scaler, open(f"./Model/scaler_{today}.pkl", 'wb'))
        x_test_scaled = scaler.transform(x_test)

        # transform data to balance it
        smote = SMOTE(random_state=42, sampling_strategy=0.5)
        x_train_scaled_smote, y_train_smote = smote.fit_resample(x_train_scaled, y_train)

        xgb = XGBClassifier()
        xgb.fit(x_train_scaled_smote, y_train_smote)
        # save the trained model
        pickle.dump(xgb, open(f"./Model/final_model_{today}.sav", 'wb'))

        y_train_pred_xgb = xgb.predict(x_train_scaled_smote)
        y_test_pred_xgb = xgb.predict(x_test_scaled)
        training_f1_score = f1_score(y_train_smote, y_train_pred_xgb)
        testing_f1_score = f1_score(y_test, y_test_pred_xgb)

        return training_f1_score, testing_f1_score
