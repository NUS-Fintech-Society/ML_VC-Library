import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; 
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from unsupervised_models import HierarchicalClustering, KMeansClustering, KPrototypeClustering


if __name__ == "__main__":
    print("Running as script")
    companies = pd.read_csv("/Users/Daniel/Documents/University Summer/FinTech VC/Dataset/v2/1-50.csv",index_col = 0)
    
    def null_value(df):
        num_null = df.isna().sum().sort_values(ascending = False)
        percent_null = (df.isna().sum() / df.isna().count()) * 100
        result = pd.concat([num_null, percent_null], axis = 1, keys = ["Number of NA", "%"])
        return result

    non_null_col = null_value(companies)
    non_null_columns = non_null_col[non_null_col["%"]<= 14].index.tolist()
    df_numerical = companies.select_dtypes(include = np.number)
    features = df_numerical[df_numerical.columns.intersection(non_null_columns).tolist()]

    # # Hierarchical Clustering
    # hiera_data = features.dropna()

    # hc = HierarchicalClustering()
    # hc.load_data(normalize(hiera_data))
    # hc.dendrogram_visual()
    # hc.set_params(4)
    # hc.fit_predict()
    # hc.hierarchical_visual(1, 2)
    # hc.hierarchical_visual(2, 3)
    # hc.hierarchical_visual(3, 4)
    # hc.hierarchical_visual(5, 6)


    # KMeans Clustering
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features.dropna())
    
    # With unscaled features
    kmeans = KMeansClustering()
    kmeans.load_data(features.dropna())
    # kmeans.elbow_method()
    # kmeans.elbow_method(20)
    # kmeans.silhouette_method()
    kmeans.set_params(4)
    kmeans.fit_predict()
    # kmeans.kmeans_visual(1, 2)
    # kmeans.kmeans_visual(2, 3)
    # kmeans.kmeans_visual(3, 4)
    # kmeans.kmeans_visual(2, 4)
    kmeans.centroid_position()

    # # With scaled features
    # kmeans = KMeansClustering()
    # kmeans.load_data(scaled_features, features.dropna().columns.values)
    # #kmeans.add_scaler
    # # kmeans.elbow_method()
    # # kmeans.elbow_method(20)
    # # kmeans.silhouette_method()
    # kmeans.set_params(4)
    # kmeans.fit_predict()
    # #kmeans.kmeans_visual(1, 2)
    # kmeans.kmeans_visual(1, 2, scaler)
    # kmeans.kmeans_visual(2, 3, scaler)
    # kmeans.kmeans_visual(3, 4, scaler)
    # kmeans.kmeans_visual(2, 4, scaler)

    # K-Prototype Clustering
    features = companies[companies.columns.intersection(non_null_columns).tolist()]
    cat_columns_selected = ["Profile Type", "Number of Employees", "IPO Status"]
    numerical_col_selected = list(features.select_dtypes([np.number]).columns)
    features_selected = numerical_col_selected + cat_columns_selected

    df_kprototype = features[features_selected].dropna().reset_index(drop=True)

    kprototype = KPrototypeClustering()
    kprototype.load_data(df_kprototype)
    kprototype.kprototype_elbow_method(10)
    kprototype.set_params(3)
    kprototype.fit_predict()
    kprototype.kprototype_visual(1, 2)
    kprototype.kprototype_visual(2, 3)
    kprototype.kprototype_visual(3, 4)
    kprototype.kprototype_visual(2, 4)
    kprototype.centroid_position()



