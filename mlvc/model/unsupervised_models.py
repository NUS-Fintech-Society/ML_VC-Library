import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; 
sns.set_style("darkgrid")

from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.datasets import make_blobs, make_classification
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering

from kmodes.kprototypes import KPrototypes

def null_value(df):
    num_null = df.isna().sum().sort_values(ascending = False)
    percent_null = (df.isna().sum() / df.isna().count()) * 100
    result = pd.concat([num_null, percent_null], axis = 1, keys = ["Number of NA", "%"])
    return result

class HierarchicalClustering:
    def __init__(self):
        self.data = None
        self.matrix = None
        self.model = None
        self.pred = None

        # Model params
        self.n_clusters = None
        self.affinity = None
        self.linkage = None

        # Visualisation
        self.feature_names = np.array([])
    
    def load_data(self, matrix):
        if (type(matrix) == pd.DataFrame):
            self.data = matrix
            self.matrix = matrix.to_numpy()
            self.feature_names = matrix.columns.values
        elif (type(matrix) == np.ndarray):
            self.data = pd.DataFrame(matrix)
            self.matrix = matrix

        else:
            print("Invalid data loaded")
    
    def set_params(self, n_clusters, affinity = "euclidean", linkage = "ward"):
        self.n_clusters = n_clusters
        self.affinity = affinity
        self.linkage = linkage

        # Creating the model
        self.model = AgglomerativeClustering(n_clusters, affinity, linkage)
    
    def fit_predict(self):
        if (self.matrix.any() and self.model):
            self.pred = self.model.fit_predict(self.matrix)
        elif (not self.matrix.any()):
            print("No data loaded")
        else:
            print("No model params set")
            

        

    # Creating a Dendrogram 
    def dendrogram_visual(self):
        # Checking to see if data has been loaded
        if (self.matrix is None):
            return None
        
        data_scaled = normalize(self.matrix)
        
        # Creating the linkage matrix
        linked = linkage(data_scaled, method = "ward", metric = "euclidean")
        print("Created linkage matrix")
        
        # Plotting the dendrogram
        plt.figure(figsize = (12, 6))
        plt.title("Dendrogram")
        plt.ylabel("Distance")
        labelList = range(1, len(self.matrix) + 1)
        dend = dendrogram(linked, orientation= 'top', labels= labelList, 
                    distance_sort = "descending", show_leaf_counts = True)
        plt.show()

        return None

    
    # Visualising the clusters    
    def hierarchical_visual(self, x1, x2, scaled = True, scaler = None):
        
        limit = self.matrix.shape[1]

        X = self.matrix
        label = self.model.labels_

        if (x1 > limit or x2 > limit):
            print("Invalid feature selected")
            return None
        
        # Changing the selected feature to column index
        x1 = x1 - 1
        x2 = x2 - 1
        
        # Whether to plot to actual scale
        if (scaled and scaler):
            X = scaler.inverse_transform(X)
            
        plt.figure(figsize = (12, 6))
        
        sns.scatterplot(x = X[:, x1].reshape(-1),y = X[:, x2].reshape(-1), hue = label,
                        alpha = 0.7,
                    palette = sns.color_palette("Set2", n_colors=len(np.unique(label))))

        #sns.scatterplot(centers[:, x1].reshape(-1), centers[:, x2].reshape(-1),
                    #color = 'black', s = 200, alpha = 0.5)
        
        if (self.feature_names.any()):
            plt.xlabel(self.feature_names[x1])
            plt.ylabel(self.feature_names[x2])
            
        plt.show()
    
##############  KMeans Clustering ######################
class KMeansClustering:
    def __init__(self):
        self.data = None
        self.matrix = None
        self.model = None
        self.pred = None

        # Model params
        self.n_clusters = None
        self.n_init = None
        self.max_iter= None
        self.random_state = None

        # Visualisation
        self.feature_names = np.array([])
    
    def load_data(self, matrix, feature_names=np.array([])):
        if (type(matrix) == pd.DataFrame):
            df_numerical = matrix.select_dtypes(include = np.number)
            self.data = df_numerical
            self.matrix = df_numerical.to_numpy()
            self.feature_names = df_numerical.columns.values
        elif (type(matrix) == np.ndarray):
            self.data = pd.DataFrame(matrix)
            self.matrix = matrix
            self.feature_names = feature_names

        else:
            print("Invalid data loaded")
    
    def set_params(self, n_clusters, n_init = 10, max_iter = 300, random_state = 42):
        self.n_clusters = n_clusters
        self.n_init = n_init
        self.max_iter= max_iter
        self.random_state = random_state

        # Creating the model
        self.model = KMeans(
                        init = "random",
                        n_clusters = n_clusters,
                        n_init = n_init,
                        random_state = random_state)
                
    
    def fit_predict(self):
        if (self.matrix.any() and self.model):
            self.pred = self.model.fit_predict(self.matrix)
        elif (not self.matrix.any()):
            print("No data loaded")
        else:
            print("No model params set")

    # Creating a elbow method plot
    # Pick the cluster with the last significant decrease in WSS score
    # (Reasonable trade-off between error and number of clusters)   
    def elbow_method(self, max_clusters = 10):

        scaled_features = self.matrix
        WSS = []
        
        for cluster in range(1, max_clusters):
            kmeans = KMeans(init = "k-means++", n_clusters = cluster,
                            n_init = 10, random_state = 42)
            kmeans.fit(scaled_features)
            WSS.append(kmeans.inertia_)

        frame = pd.DataFrame(data = {"Clusters": range(1,max_clusters), "WSS": WSS})
        plt.figure(figsize = (12, 6))
        sns.lineplot(frame["Clusters"], frame["WSS"], marker = "o")
        plt.xlabel("Number of Clusters")
        plt.ylabel("WSS")
        plt.xticks(np.arange(1, max_clusters+1, 1))
        plt.show()

    # Creating a silhouette method plot
    # Pick the cluster with the maximum score
    def silhouette_method(self, max_clusters = 10):

        scaled_features = self.matrix
        silhouette_coef = []
        
        # We start at 2 clusters for silhouette coefficient
        for cluster in range(2, max_clusters):
            kmeans = KMeans(init = "k-means++", n_clusters = cluster,
                            n_init = 10, random_state = 42)
            kmeans.fit(scaled_features)
            score = silhouette_score(scaled_features, kmeans.labels_)
            silhouette_coef.append(score)

        frame = pd.DataFrame(data = {"Clusters": range(2,max_clusters), 
                                    "Silhouette Coefficient": silhouette_coef})
        plt.figure(figsize = (12, 6))
        sns.lineplot(frame["Clusters"], 
                    frame["Silhouette Coefficient"], marker = "o")
        plt.xlabel("Number of Clusters")
        plt.ylabel("Silhouette Coefficient")
        plt.xticks(np.arange(2, max_clusters+1, 1))
        plt.show()

    
    # Visualising the clusters    
    def kmeans_visual(self, x1, x2, scaler=None, scaled = True):
        limit = self.matrix.shape[1]
        
        X = self.matrix
        pred = self.pred
        centers = self.model.cluster_centers_
        feature_names = self.feature_names

        print(limit, x1, x2)
        if (x1 > limit or x2 > limit):
            print("Invalid feature selected")
            return None
        
        # Changing the selected feature to column index
        x1 = x1 - 1
        x2 = x2 - 1
        
        # Whether to plot to actual scale
        if (scaled and scaler):
            centers = scaler.inverse_transform(centers)
            X = scaler.inverse_transform(X)
            
        plt.figure(figsize = (12, 6))
        
        sns.scatterplot(x = X[:, x1].reshape(-1),y = X[:, x2].reshape(-1),hue = pred,
                    palette = sns.color_palette("Set2", n_colors=len(centers)))

        sns.scatterplot(centers[:, x1].reshape(-1), centers[:, x2].reshape(-1),
                    color = 'black', s = 200, alpha = 0.5)
        
        if feature_names.any():
            plt.xlabel(feature_names[x1])
            plt.ylabel(feature_names[x2])
            
        plt.show()
        
    # Interpreting the cluster centroids
    def centroid_position(centers, columns):
        pd.set_option('display.float_format', lambda x: '%.3f' % x)
        # pd.reset_option('display.float_format')
        centers = pd.DataFrame(centers, columns= feature_names)
        print(centers)




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
    non_null_col = null_value(companies)
    non_null_columns = non_null_col[non_null_col["%"]<= 14].index.tolist()
    df_numerical = companies.select_dtypes(include = np.number)
    features = df_numerical[df_numerical.columns.intersection(non_null_columns).tolist()]

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features.dropna())
    
    # # With unscaled features
    # kmeans = KMeansClustering()
    # kmeans.load_data(features.dropna())
    # # kmeans.elbow_method()
    # # kmeans.elbow_method(20)
    # # kmeans.silhouette_method()
    # kmeans.set_params(4)
    # kmeans.fit_predict()
    # kmeans.kmeans_visual(1, 2)
    # kmeans.kmeans_visual(2, 3)
    # kmeans.kmeans_visual(3, 4)
    # kmeans.kmeans_visual(2, 4)

    # With scaled features
    kmeans = KMeansClustering()
    kmeans.load_data(scaled_features, features.dropna().columns.values)
    #kmeans.add_scaler
    # kmeans.elbow_method()
    # kmeans.elbow_method(20)
    # kmeans.silhouette_method()
    kmeans.set_params(4)
    kmeans.fit_predict()
    #kmeans.kmeans_visual(1, 2)
    kmeans.kmeans_visual(1, 2, scaler)
    kmeans.kmeans_visual(2, 3, scaler)
    kmeans.kmeans_visual(3, 4, scaler)
    kmeans.kmeans_visual(2, 4, scaler)



