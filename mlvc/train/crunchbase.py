from .formatter import *
import warnings
import pickle
from datetime import datetime
from mlvc.config import config
import os

warnings.filterwarnings("ignore")


class Crunchbase():
    # Global Variables
    def __init__(self):
        self.data_filepath = os.path.join(os.getcwd(), config.DATA_SAVE_DIR, f'{config.DOWNLOAD_FILE_NAME}.csv')
        self.model_directory = config.MODEL_SAVE_DIR

    def read_data(self):
        df = pd.read_csv(self.data_filepath)
        return df

    def format_crunchbase(self):
        """Processes the data
        Returns
        -------
        dataframe
            With the relevant columns required for model
        """

        df = self.read_data()
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df[df['profile_type'] == "ORGANIZATION"]

        df.drop(['name', 'profile_type', 'website', 'about', 'investor', 'funds_raised', 'product_downloads',
                 'founded_date', 'closed_date', 'founders', 'delisted_date', 'last_funding',
                 'stock_symbol', 'headquarters_regions', 'ipo_date', 'sub-organization_of',
                 'acquired_by', 'announced_date', 'number_of_exits', 'ipo_share_price'], axis=1, inplace=True)
        df.dropna(how="all", inplace=True)
        df.reset_index(inplace=True)
        df.drop(['index'], axis=1, inplace=True)
        df = df[df['last_funding_type'].notna()]
        df.reset_index(inplace=True)
        df.drop(['index'], axis=1, inplace=True)

        unlist_cat_cols_kmeans(df, ['industries', 'related_hubs', 'hub_tags', 'diversity_spotlight_(us_only)', 'price',
                                    'investment_stage'])
        unlist_last_funding_type(df)
        df['operating_status'] = df['operating_status'].apply(lambda x: unlist_op_stat(x))
        unlist_company_type(df, 'company_type')
        currency_to_usd(df, ['total_funding_amount', 'total_fund_raised', 'valuation_at_ipo', 'money_raised_at_ipo',
                             'price'])
        remove_tmbk(df, ['total_funding_amount', 'total_fund_raised', 'valuation_at_ipo', 'money_raised_at_ipo',
                         'price'])
        remove_commas_numeric(df, ['monthly_visits', 'number_of_articles', 'downloads_last_30_days'])
        unstring_numeric(df, ['number_of_funding_rounds', 'number_of_lead_investors', 'number_of_investors',
                              'number_of_funds', 'number_of_investments', 'number_of_lead_investments',
                              'number_of_diversity_investments', 'number_of_acquisitions',
                              'number_of_board_member_and_advisor_profiles', 'number_of_employee_profiles',
                              'total_products_active', 'active_tech_count', 'number_of_events'])
        df['monthly_visits_growth'] = df['monthly_visits_growth'].apply(
            lambda x: float(x.replace(',', '').replace('%', '')) * 100 if x is not np.nan else np.nan)
        df['hub_tags_cat'] = df['hub_tags'].apply(lambda x: hub_tag_cat(x))
        df['location_country'] = df['location'].apply(lambda x: str(x).split(",")[-1].lstrip())
        df['location_city'] = df['location'].apply(lambda x: str(x).split(",")[0].lstrip())
        location_city_in_startup_cluster(df)

        # clustering and one hot encoding industries
        ind = df[['industries']]
        ind.dropna(inplace=True)
        tfidf_vectorizer_industries = TfidfVectorizer()
        tfidf_industries = tfidf_vectorizer_industries.fit_transform(ind['industries'])
        today = datetime.today().strftime('%Y-%m-%d')
        pickle.dump(tfidf_vectorizer_industries, open(os.path.join(os.getcwd(), config.MODEL_SAVE_DIR, f'tfidf_industries_{today}.pkl'), 'wb'))
        kmeans_ind = KMeans(n_clusters=3).fit(tfidf_industries)
        pickle.dump(kmeans_ind, open(os.path.join(os.getcwd(), config.MODEL_SAVE_DIR, f'kmeans_industries_{today}.sav'), 'wb'))
        predicted_values_industry = kmeans_ind.predict(tfidf_industries)

        # clustering and one hot encoding related hubs
        hubs = df[['related_hubs']]
        hubs.dropna(inplace=True)
        tfidf_vectorizer_hubs = TfidfVectorizer()
        tfidf_hubs = tfidf_vectorizer_hubs.fit_transform(hubs['related_hubs'])
        pickle.dump(tfidf_vectorizer_hubs, open(os.path.join(os.getcwd(), config.MODEL_SAVE_DIR, f'tfidf_hubs_{today}.pickle'), 'wb'))
        kmeans_hubs = KMeans(n_clusters=3).fit(tfidf_hubs)
        pickle.dump(kmeans_hubs, open(os.path.join(os.getcwd(), config.MODEL_SAVE_DIR, f'kmeans_hubs_{today}.sav'), 'wb'))
        predicted_values_hubs = kmeans_hubs.predict(tfidf_hubs)

        ind_pred = pd.concat([ind['industries'], pd.Series(predicted_values_industry, index=ind.index)], axis=1)
        ind_pred_ohe = pd.get_dummies(ind_pred[0], prefix='type')
        ind_pred_ohe.columns = ['industries_type_0', 'industries_type_1', 'industries_type_2']
        df_merged = df.merge(ind_pred_ohe, how='outer', left_index=True, right_index=True)
        hubs_pred = pd.concat([hubs['related_hubs'], pd.Series(predicted_values_hubs, index=hubs.index)], axis=1)
        hubs_pred_ohe = pd.get_dummies(hubs_pred[0], prefix='type')
        hubs_pred_ohe.columns = ['related_hubs_type_0', 'related_hubs_type_1', 'related_hubs_type_2']
        df_merged2 = df_merged.merge(hubs_pred_ohe, how='outer', left_index=True, right_index=True)

        df_merged2 = hub_tags_to_ohe(df_merged2)
        df_merged2 = company_type_to_ohe(df_merged2)
        employees_to_le(df_merged2)
        df_merged2 = df_merged2[df_merged2['ipo_status'].notna()]
        df_merged2.reset_index(inplace=True)
        df_merged2.drop(['index'], axis=1, inplace=True)
        df_merged2['ipo_status'] = df_merged2['ipo_status'].apply(lambda x: grp_ipostatus(x))
        opstatus_to_le(df_merged2)
        ipostatus_to_le(df_merged2)

        # replace nan in numeric columns with medians of each column
        df_merged2.drop(['location', 'employee', 'industries', 'related_hubs',
                         'hub_tags', 'investment_stage', 'location_country', 'location_city',
                         'diversity_spotlight_(us_only)', 'hiring_status', 'investor_type'], axis=1, inplace=True)
        df_merged2['number_of_funding_rounds'].replace(np.nan, df_merged2['number_of_funding_rounds'].median(),
                                                       inplace=True)
        df_merged2['number_of_lead_investors'].replace(np.nan, df_merged2['number_of_lead_investors'].median(),
                                                       inplace=True)
        df_merged2['number_of_investors'].replace(np.nan, df_merged2['number_of_investors'].median(), inplace=True)
        df_merged2['number_of_funds'].replace(np.nan, df_merged2['number_of_funds'].median(), inplace=True)
        df_merged2['total_funding_amount'].replace(np.nan, df_merged2['total_funding_amount'].median(), inplace=True)
        df_merged2['total_fund_raised'].replace(np.nan, df_merged2['total_fund_raised'].median(), inplace=True)
        df_merged2['number_of_investments'].replace(np.nan, df_merged2['number_of_investments'].median(), inplace=True)
        df_merged2['number_of_lead_investments'].replace(np.nan, df_merged2['number_of_lead_investments'].median(),
                                                         inplace=True)
        df_merged2['number_of_diversity_investments'].replace(np.nan,
                                                              df_merged2['number_of_diversity_investments'].median(),
                                                              inplace=True)
        df_merged2['number_of_acquisitions'].replace(np.nan, df_merged2['number_of_acquisitions'].median(),
                                                     inplace=True)

        df_merged2['number_of_board_member_and_advisor_profiles'].replace(np.nan, df_merged2[
            'number_of_board_member_and_advisor_profiles'].median(), inplace=True)
        df_merged2['number_of_employee_profiles'].replace(np.nan, df_merged2['number_of_employee_profiles'].median(),
                                                          inplace=True)
        df_merged2['total_products_active'].replace(np.nan, df_merged2['total_products_active'].median(), inplace=True)
        df_merged2['monthly_visits'].replace(np.nan, df_merged2['monthly_visits'].median(), inplace=True)
        df_merged2['monthly_visits_growth'].replace(np.nan, df_merged2['monthly_visits_growth'].median(), inplace=True)
        df_merged2['active_tech_count'].replace(np.nan, df_merged2['active_tech_count'].median(), inplace=True)
        df_merged2['number_of_articles'].replace(np.nan, df_merged2['number_of_articles'].median(), inplace=True)
        df_merged2['number_of_events'].replace(np.nan, df_merged2['number_of_events'].median(), inplace=True)
        df_merged2['valuation_at_ipo'].replace(np.nan, df_merged2['valuation_at_ipo'].median(), inplace=True)
        df_merged2['money_raised_at_ipo'].replace(np.nan, df_merged2['money_raised_at_ipo'].median(), inplace=True)
        df_merged2['downloads_last_30_days'].replace(np.nan, df_merged2['downloads_last_30_days'].median(),
                                                     inplace=True)
        df_merged2['price'].replace(np.nan, df_merged2['price'].median(), inplace=True)
        df_merged2['in_startup_cluster'].replace(np.nan, df_merged2['in_startup_cluster'].median(), inplace=True)
        df_merged2['employee_cat'].replace(np.nan, df_merged2['employee_cat'].median(), inplace=True)

        # replace nan values in industries and related hubs with most common ohe category
        replace_nan_industries(df_merged2)
        replace_nan_related_hubs(df_merged2)

        df_merged2['last_funding_type'] = df_merged2['last_funding_type'].apply(lambda x: grp_last_funding_type(x))
        df_merged2 = last_funding_type(df_merged2)

        return df_merged2