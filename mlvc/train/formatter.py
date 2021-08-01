import numpy as np
import pandas as pd
import ast
import math
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
from .kmeans import *


def unlist_cat_cols_kmeans(df, listed_cat_cols_kmeans):
    for i in listed_cat_cols_kmeans:
        df[i] = df[i].apply(lambda x: " ".join(ast.literal_eval(x)) if isinstance(x, str) else np.nan)


def unlist_last_funding_type(df):
    for i in range(len(df)):
        try:
            df['last_funding_type'][i] = "".join(ast.literal_eval(df['last_funding_type'][i]))
        except:
            continue


def unlist_op_stat(op_stat):
    tags = {'Active': ["['Active']", "'Active']", "['Acive'"],
            'Closed': ["['Closed']", "'Closed']", "['Closed'"]}
    if op_stat is not np.nan:
        for k, v in tags.items():
            if op_stat in v:
                return k
        return k
    else:
        return np.nan


def unlist_company_type(df, company_type):
    for j in range(len(df)):
        if df[company_type][j] is not np.nan:
            if df[company_type][j] == "['For Profit']":
                df[company_type][j] = 'For Profit'
            elif df[company_type][j] == "['Non-profit']":
                df[company_type][j] = 'Non Profit'
            elif df[company_type][j] == "'For Profit']":
                df[company_type][j] = 'For Profit'


def currency_to_usd(df, list_of_other_currency_cols):
    currencies = {'£': 1.42, '€': 1.22, '₹': 0.014, 'CN¥': 0.16, 'ZAR': 0.071, 'CA$': 0.83, 'BDT': 0.012,
                  'SEK': 0.12, 'CHF': 1.11, 'A$': 0.77, '¥': 0.0091, 'DKK': 0.16, '₩': 0.00090, 'R$': 0.20,
                  'AED': 0.27, 'HK$': 0.13, '₪': 0.31, 'SGD': 0.75, 'PLN': 0.27, 'RUB': 0.014, 'NGN': 0.0024,
                  'THB': 0.032, 'NOK': 0.12, 'NT$': 0.03616,
                  'QAR': 0.27, 'MX$': 0.050, 'NZ$': 0.71, 'IDR': 0.000070, 'KES': 0.0093, 'MYR': 0.24,
                  'PHP': 0.021, '₫': 0.00004, 'ISK': 0.0082, 'KWD': 3.33,
                  'TRY': 0.12, 'SAR': 0.27, 'HRK': 0.16, 'SDG': 0.0022, 'MAD': 0.11, 'COP': 0.00027, 'CLP': 0.0014,
                  'EGP': 0.064, 'CZK': 0.046, 'HUF': 0.0034, 'DZD': 0.0074,
                  'SKK': 0.0393914, 'MMK': 0.00061, 'IRR': 0.000024, 'PKR': 0.0064,
                  'TND': 0.36, 'UGX': 0.00028}
    for i in list_of_other_currency_cols:
        for j in range(len(df)):
            if df[i][j] is not np.nan:
                if isinstance(df[i][j], str):
                    if ',' in df[i][j]:
                        df[i][j] = df[i][j].replace(',', '')

                    if "[" in df[i][j]:
                        df[i][j] = "".join(ast.literal_eval(df[i][j]))

                    if df[i][j][0] == '$':
                        df[i][j] = df[i][j][1:]

                    elif df[i][j][1].isdigit():
                        value = str(float(df[i][j][1:-1]) * currencies.get(df[i][j][0]))
                        df[i][j] = value + df[i][j][-1]

                    elif df[i][j][2].isdigit():
                        value = str(float(df[i][j][2:-1]) * currencies.get(df[i][j][0:2]))
                        df[i][j] = value + df[i][j][-1]

                    elif df[i][j][3].isdigit():
                        value = str(float(df[i][j][3:-1]) * currencies.get(df[i][j][0:3]))
                        df[i][j] = value + df[i][j][-1]

                    elif df[i][j][0:3] == "['$":
                        df[i][j] = df[i][j][3:]
                    elif df[i][j][0:3] == "['£":
                        df[i][j] = float(df[i][j][3:]) * 1.42
                    elif df[i][j][0:3] == "['€":
                        df[i][j] = float(df[i][j][3:]) * 1.22
                    elif df[i][j][0:3] == "['₹":
                        df[i][j] = float(df[i][j][3:]) * 0.014
                    elif df[i][j][0:3] == "['¥":
                        df[i][j] = float(df[i][j][3:]) * 0.0091
                    elif df[i][j][0:3] == "['₫":
                        df[i][j] = float(df[i][j][3:]) * 0.00004
                else:
                    df[i][j] = float(df[i][j])


def remove_tmbk(df, list_of_tmbk_cols):
    for i in list_of_tmbk_cols:
        for j in range(len(df)):
            if df[i][j] is not np.nan:
                if isinstance(df[i][j], str):
                    if df[i][j][-1] == 'B':
                        df[i][j] = float(df[i][j][:-1]) * 1000000000
                    elif df[i][j][-1] == 'M':
                        df[i][j] = float(df[i][j][:-1]) * 1000000
                    elif df[i][j][-1] == 'K':
                        df[i][j] = float(df[i][j][:-1]) * 100000
                    elif df[i][j][-1] == 'T':
                        df[i][j] = float(df[i][j][:-1]) * 1000000000000
                else:
                    df[i][j] = float(df[i][j])


def remove_commas_numeric(df, list_of_numeric_cols_w_comma):
    for i in list_of_numeric_cols_w_comma:
        df[i] = df[i].apply(lambda x: float(x.replace(',', '')) if x is not np.nan else np.nan)


def unstring_numeric(df, list_of_string_numeric_cols):
    for i in list_of_string_numeric_cols:
        df[i] = df[i].apply(lambda x: float(str(x).replace(',', '')) if x is not np.nan else np.nan)


def hub_tag_cat(hub_tag):
    tags = {'Unicorn': ['Unicorn', 'Pledge 1%, Unicorn'],
            'Exited Unicorn': ['Exited Unicorn', 'Exited Unicorn, Pledge 1%',
                               'Crunchbase Venture Program, Exited Unicorn'],
            'Emerging Unicorn': ['Emerging Unicorn', 'Emerging Unicorn, Pledge 1%'],
            'Others': ['Crunchbase Venture Program', 'Crunchbase Venture Program, Pledge 1%', 'Pledge 1%']}

    if hub_tag is not np.nan:
        for k, v in tags.items():
            if hub_tag in v:
                return k
        return k
    else:
        return np.nan


def location_city_in_startup_cluster(df):
    # top 20 most prominent startup locations
    top_20_startup_locations = ['Silicon Valley', 'New York', 'London', 'Beijing', 'Boston',
                                'Tel Aviv', 'Los Angeles', 'Shanghai', 'Seattle', 'Stockholm',
                                'Washington DC', 'Amsterdam', 'Paris', 'Chicago', 'Tokyo',
                                'Berlin', 'Singapore', 'Toronto-Waterloo', 'Austin', 'Seoul']

    df['in_startup_cluster'] = df['location_city'].apply(lambda x: 1 if x in top_20_startup_locations else 0)


def create_tfidf_array(data):
    tf_idf_vectorizor = TfidfVectorizer(stop_words='english', max_features=20000)
    tf_idf = tf_idf_vectorizor.fit_transform(data)
    tf_idf_norm = normalize(tf_idf)
    tf_idf_array = tf_idf_norm.toarray()
    return tf_idf_array


def dim_reduction(data):
    tf_idf_array = create_tfidf_array(data)
    sklearn_pca = PCA(n_components=2)
    reduced_dim = sklearn_pca.fit_transform(tf_idf_array)
    return reduced_dim


def elbow_plot(data, start, end):
    # tf_idf_array = create_tfidf_array(data)
    reduced_dim = dim_reduction(data)

    number_clusters = range(start, end)
    kmeans = [KMeans(n_clusters=i, max_iter=600) for i in number_clusters]

    score = [kmeans[i].fit(reduced_dim).score(reduced_dim) for i in range(len(kmeans))]

    plt.plot(number_clusters, score)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Score')
    plt.title('Elbow Method')
    plt.show()


def hub_tags_to_ohe(df):
    ohe_types = pd.get_dummies(df['hub_tags_cat'], prefix='type')
    new_df = pd.concat([df.drop('hub_tags_cat', axis=1), ohe_types], axis=1)
    return new_df


def company_type_to_ohe(df):
    ohe_types = pd.get_dummies(df['company_type'], prefix='type')
    new_df = pd.concat([df.drop('company_type', axis=1), ohe_types], axis=1)
    return new_df


def employees_to_le(df):
    employees = {'1-Oct': 1, '1-10': 1, 'Nov-50': 2, '11-50': 2, '51-100': 3, '101-250': 4, '251-500': 5,
                 '501-1000': 6, '1001-5000': 7, '5001-10000': 8, '10001+': 9}

    df['employee'] = df['employee'].apply(lambda x: x if x in employees.keys() else np.nan)
    df["employee_cat"] = df["employee"]
    df.replace({'employee_cat': employees}, inplace=True)


def grp_ipostatus(ipo):
    tags = {'Success': ['Public'],
            'Failure': ['Delisted', 'Private']}

    if ipo is not np.nan:
        for k, v in tags.items():
            if ipo in v:
                return k
        return k
    else:
        return np.nan


def grp_last_funding_type(last_fund):
    tags = {'Group A': ['Pre-Seed', 'Debt Financing', 'Private Equity', 'Angel', 'Seed', 'Initial Coin Offering',
                        'Venture - Series Unknown', 'Equity Crowdfunding'],
            'Group B': ['Secondary Market', 'Post-IPO Secondary', 'Post-IPO Equity', 'Series G', 'Series H', 'Series I',
                        'Series F', 'Post-IPO Debt'],
            'Group C': ['Product Crowdfunding', 'Corporate Round', 'Convertible Note', 'Undisclosed', 'Series A',
                        'Series B', 'Series C', 'Grant', 'Series D', 'Series E', 'Non-equity Assistance']}

    if last_fund is not np.nan:
        for k, v in tags.items():
            if last_fund in v:
                return k
        return k
    else:
        return np.nan


def last_funding_type(df):
    ohe_types = pd.get_dummies(df['last_funding_type'], prefix='type')
    new_df = pd.concat([df.drop('last_funding_type', axis=1), ohe_types], axis=1)
    return new_df


def opstatus_to_le(df):
    df["operating_status"] = df["operating_status"].astype('category').cat.codes


# target variable, private and delisted is 0, public is 1
def ipostatus_to_le(df):
    df["ipo_status"] = df["ipo_status"].astype('category').cat.codes


def replace_nan_industries(df):
    for i in range(len(df)):
        if math.isnan(df['industries_type_0'][i]):
            df['industries_type_0'][i] = 0
        if math.isnan(df['industries_type_1'][i]):
            df['industries_type_1'][i] = 0
        if math.isnan(df['industries_type_2'][i]):
            df['industries_type_2'][i] = 1


def replace_nan_related_hubs(df):
    for i in range(len(df)):
        if math.isnan(df['related_hubs_type_0'][i]):
            df['related_hubs_type_0'][i] = 1
        if math.isnan(df['related_hubs_type_1'][i]):
            df['related_hubs_type_1'][i] = 0
        if math.isnan(df['related_hubs_type_2'][i]):
            df['related_hubs_type_2'][i] = 0


####### methods for single values #######
def company_type_to_ohe_single(type):
    if type == "For Profit":
        return 1
    else:
        return 0


def unlist_industries_and_hub_tags(ind, ht):
    new_ind = " ".join(ast.literal_eval(ind))
    new_ht = " ".join(ast.literal_eval(ht))
    return new_ind, new_ht


def employees_to_le_single(employ):
    employees = {'1-10': 1, '11-50': 2, '51-100': 3, '101-250': 4, '251-500': 5,
                 '501-1000': 6, '1001-5000': 7, '5001-10000': 8, '10001+': 9}

    if employ in employees.keys():
        employ_new = employees.get(employ)

    return employ_new


def grp_last_funding_type_single(last_fund):
    grp = ''
    tags = {'Group A': ['Pre-Seed', 'Debt Financing', 'Private Equity', 'Angel', 'Seed', 'Initial Coin Offering',
                        'Venture - Series Unknown', 'Equity Crowdfunding'],
            'Group B': ['Secondary Market', 'Post-IPO Secondary', 'Post-IPO Equity', 'Series G', 'Series H', 'Series I',
                        'Series F', 'Post-IPO Debt'],
            'Group C': ['Product Crowdfunding', 'Corporate Round', 'Convertible Note', 'Undisclosed', 'Series A',
                        'Series B', 'Series C', 'Grant', 'Series D', 'Series E', 'Non-equity Assistance']}

    if last_fund is not np.nan:
        for k, v in tags.items():
            if last_fund in v:
                grp = grp + k
    # return type grp A, type grp B
    if grp == 'Group A':
        return 1, 0
    elif grp == 'Group B':
        return 0, 1
    else:
        return 0, 0
