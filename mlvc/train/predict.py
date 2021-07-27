from .crunchbase import *
import pickle
import ast


class Predict():
    def __init__(self, name):
        self.name = name

    def make_prediction(self):
        """Makes prediction
        Returns
        -------
        target value
            Returns Public or, Private or Delisted as target values
        """

        input_values = {'last_funding_type': 'Series A', 'employee': '1001-5000', 'number_of_events': 33,
                        'industries': "['Banking', 'Internet', 'Mobile', 'Telecommunications']",
                        'total_products_active': 7, 'valuation_at_ipo': 600000,
                        'money_raised_at_ipo': 500000, 'number_of_acquisitions': 14, 'number_of_investments': 44,
                        'number_of_lead_investments': 30, 'number_of_lead_investors': 2, 'number_of_investors': 30,
                        'number_of_employee_profiles': 91, 'company_type': 'For Profit'}

        # code to format input values
        emp = employees_to_le_single(input_values.get('employee'))
        fund_type_A, fund_type_B = grp_last_funding_type_single(input_values.get('last_funding_type'))
        comp_type = company_type_to_ohe_single(input_values.get('company_type'))
        kmeans_ind = pickle.load(open('./Model/kmeans_industries_2021-07-25.sav', 'rb'))
        tfidf_ind = pickle.load(open('./Model/tfidf_industries_2021-07-25.pkl', 'rb'))
        ind = " ".join(ast.literal_eval(input_values.get('industries')))[0]
        ind_pred = kmeans_ind.predict(tfidf_ind.transform([ind]))[0]
        if ind_pred == 0:
            ind_type_0 = 1
        else:
            ind_type_0 = 0

        final_input_values = [emp, fund_type_A, fund_type_B, input_values.get('money_raised_ipo'),
                              input_values.get('valuation_ipo'), comp_type, ind_type_0,
                              input_values.get('total_products_active'), input_values.get('number_of_acquisitions'),
                              input_values.get('number_of_investments'), input_values.get('number_of_lead_investments'),
                              input_values.get('number_of_lead_investors'), input_values.get('number_of_investors'),
                              input_values.get('number_of_employee_profiles'), input_values.get('number_of_events')]

        model = pickle.load(open('./Model/final_model_2021-07-25.sav', 'rb'))
        scaler = pickle.load(open('./Model/scaler_2021-07-25.pkl', 'rb'))
        scaled_input = scaler.transform(np.asarray(final_input_values).reshape(-1, 15))
        pred = model.predict(scaled_input)
        final_pred = ''
        if pred[0] == 0:
            final_pred = final_pred + 'Private or Delisted'
        else:
            final_pred = final_pred + 'Public'

        return final_pred
