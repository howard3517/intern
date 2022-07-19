
from code import interact
from turtle import color
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

from sklearn.manifold import TSNE




df = pd.read_csv('data.csv',encoding='cp950')

X = df.drop(labels=['part','partnum'],axis=1).values 
y = df['partnum']

tsneModel = TSNE(n_components=2, random_state=42,n_iter=1000)
train_reduced = tsneModel.fit_transform(X)

df1 = pd.DataFrame()
df1['f1'] = train_reduced.T[0]
df1['f2'] = train_reduced.T[1]
df1['partnum'] = y

"""
kmeansModel = KMeans(n_clusters=5, random_state=46)
clusters_pred = kmeansModel.fit_predict(X)

print(kmeansModel.inertia_)
print(kmeansModel.cluster_centers_)
plt.scatter(X.T[1], X.T[2], c=y, cmap=plt.cm.Set1)


kmeans_list = [KMeans(n_clusters=k, random_state=46).fit(X) for k in range(1, 20)]
inertias = [model.inertia_ for model in kmeans_list]
print(inertias)
"""

"""sns.lmplot("income","population", hue='bank', data=df, fit_reg=False, legend=False)
#plt.legend(title='target', loc='upper left', labels=['Iris-Setosa', 'Iris-Versicolour', 'Iris-Virginica'])
plt.show()"""


def tsne():
    from sklearn.manifold import TSNE

    tsneModel = TSNE(n_components=2, random_state=42,n_iter=1000)
    train_reduced = tsneModel.fit_transform(X)

    plt.figure(figsize=(8,6))
    plt.scatter(train_reduced[:, 0], train_reduced[:, 1], c=y, alpha=0.5,
                cmap=plt.cm.get_cmap('nipy_spectral', 12))

    plt.colorbar()
    plt.show()

def pca():
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2, iterated_power=1)
    train_reduced = pca.fit_transform(X)

    plt.figure(figsize=(8,6))
    plt.scatter(train_reduced[:, 0], train_reduced[:, 1], c=y, alpha=0.5,
                cmap=plt.cm.get_cmap('nipy_spectral', 10))

    plt.colorbar()
    plt.show()



def kmeans():
    from sklearn.cluster import KMeans

    kmeansModel = KMeans(n_clusters=12, random_state=46)
    clusters_pred = kmeansModel.fit(X)
    kmeansModel.labels_
    print('-'*60)
    df1['Predict']=clusters_pred
    sns.lmplot('f1', 'f2', hue='partnum', data=df1, fit_reg=False, legend=True)
    #plt.legend(title='target', labels=['文山區', '大安區', '信義區', '松山區', '內湖區', '中正區', '士林區', '中山區', '萬華區', '大同區', '南港區', '北投區'])
    plt.show()

    #sns.lmplot('f1','f2', hue='Predict', data=df1, fit_reg=False, legend=False)
    #plt.scatter(kmeansModel.cluster_centers_[:, 4], kmeansModel.cluster_centers_[:, 5], s=200,c="r",marker='*')
    #plt.legend(title='target', labels=[1,2,3,4,5])
    #plt.show()
    



#tsne()
#pca()
#kmeans()


from sklearn.cluster import KMeans

kmeans_list = [KMeans(n_clusters=k, random_state=46).fit(X)
                for k in range(1, 10)]
inertias = [model.inertia_ for model in kmeans_list]
x = [1,2,3,4,5,6,7,8,9]

kmeansModel = KMeans(n_clusters=5, random_state=46)
clusters_pred = kmeansModel.fit(X)
plt.scatter(train_reduced[:, 0], train_reduced[:, 1], c = kmeansModel.labels_)
plt.show()


plt.plot(x,inertias,color = 'blue')
plt.show()


#使用 inertia 做模型評估 (K value)
from sklearn.decomposition import PCA
pca = PCA(n_components=2, iterated_power=1)
train_reduced = pca.fit_transform(X)
pca.explained_variance_ratio_

#確認降維後能否推論
sns.set()
pca = PCA().fit(X)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance')

#top 10% bank group
bank = df.sort_values('bank',ascending=False).head(120)
id =  bank['grid_id'].values.tolist()

top = []
for i in range(df1.shape[0]):
    top.append(0)

for i in range(len(id)):
    top[id[i]] = 1

df1['bank'] = top

sns.lmplot('f1','f2',data=df1,hue='bank', fit_reg=False, legend=True)
plt.show()