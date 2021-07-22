from .Crunchbase import *
import pickle
import ast

class Predict():
    def __init__(self, name):
        self.name = name

    def make_prediction(self):
        input_values = {'last_funding_type': 'Series A', 'hub_tags': 'Unicorn', 'employee': '1001-5000',
                        'industries': "['Banking', 'Internet', 'Mobile', 'Telecommunications']",
                        'total_products_active': 7, 'valuation_at_ipo': 600000,
                        'money_raised_at_ipo': 500000, 'number_of_acquisitions': 14, 'number_of_investments': 44,
                        'number_of_lead_investments': 30, 'number_of_lead_investors': 2,
                        'number_of_employee_profiles': 91, 'company_type': 'For Profit'}

        # code to format input values
        emp = employees_to_le_single(input_values.get('employee'))
        fund_type_A, fund_type_B = grp_last_funding_type_single(input_values.get('last_funding_type'))
        hub_unicorn, hub_emerging_unicorn = hub_tag_cat_single(input_values.get('hub_tags'))
        comp_type = company_type_to_ohe_single(input_values.get('company_type'))
        kmeans_ind = pickle.load(open('./Model/kmeans_industries_2021-07-18.sav', 'rb'))
        tfidf_ind = pickle.load(open('./Model/tfidf_industries_2021-07-18.pkl', 'rb'))
        ind = " ".join(ast.literal_eval(input_values.get('industries')))[0]
        ind_pred = kmeans_ind.predict(tfidf_ind.transform([ind]))[0]

        final_input_values = []
        final_input_values.append(emp)
        final_input_values.append(fund_type_A)
        final_input_values.append(fund_type_B)
        final_input_values.append(input_values.get('money_raised_ipo'))
        final_input_values.append(input_values.get('valuation_ipo'))
        final_input_values.append(hub_unicorn)
        final_input_values.append(comp_type)
        final_input_values.append(hub_emerging_unicorn)
        final_input_values.append(ind_pred)
        final_input_values.append(input_values.get('total_products_active'))
        final_input_values.append(input_values.get('number_of_acquisitions'))
        final_input_values.append(input_values.get('number_of_investments'))
        final_input_values.append(input_values.get('number_of_lead_investments'))
        final_input_values.append(input_values.get('number_of_lead_investors'))
        final_input_values.append(input_values.get('number_of_employee_profiles'))

        model = pickle.load(open('./Model/final_model_2021-07-18.sav', 'rb'))
        scaler = pickle.load(open('./Model/scaler_2021-07-18.pkl', 'rb'))
        scaled_input = scaler.transform(np.asarray(final_input_values).reshape(-1, 15))
        pred = model.predict(scaled_input)
        final_pred = ''
        if pred[0] == 0:
            final_pred = final_pred + 'Private or Delisted'
        else:
            final_pred = final_pred + 'Public'

        return final_pred
