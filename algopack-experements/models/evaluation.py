# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 11:09:50 2023

@author: timka
"""

from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import NeighborhoodComponentsAnalysis
from sklearn.decomposition import FastICA
import umap
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score , precision_score, recall_score , f1_score , roc_curve, roc_auc_score

def evaluation(y_true,y_pred,name):
    _pres , _rec , _f , _all = precision_recall_fscore_support(y_true, y_pred)
    print(name)
    print(f"Количество предсказанных нулей {len([x for x in y_pred if x == 0])}/{len([x for x in y_true if x == 0])}")
    print(f"Количество предсказанных единиц {len([x for x in y_pred if x == 1])}/{len([x for x in y_true if x == 1])}")
    for i in range(len(_pres)):
        print(f"LABEL : {i}")
        print(f"Presision для {i} = {_pres[i]}")
        print(f"Recall для {i} = {_rec[i]}")
        print(f"F-Score для {i} = {_f[i]}")
        print(f"Примеров для {i} = {_all[i]}")
        print("------------------------------")
    
    print(f"Accuracy: {accuracy_score(y_true, y_pred)}")
    print(f"Presision: {precision_score(y_true, y_pred)} доля действительно True из всех True")
    print(f"Recall: {recall_score(y_true, y_pred)} надейно всех положительных классов")
    print(f"F1 score: {f1_score(y_true, y_pred)}")
    fpr, tpr, _ = roc_curve(y_true,y_pred)
    auc = roc_auc_score(y_true, y_pred)
    plt.plot (fpr,tpr)
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    #create ROC curve
    plt.plot (fpr,tpr,label=" AUC= "+str(auc))
    plt.show()
    plt.show()
    

def plotTransformData(model,X,Y_true,xlabel=0,ylabel=1):
    X_embedded = model.transform(X)
    if type(model)!=LinearDiscriminantAnalysis:
        plt.scatter(X_embedded[:, xlabel], X_embedded[:, ylabel], c=Y_true, s=5, cmap="Set1")
        plt.scatter([X_embedded[:, xlabel][0]],[X_embedded[:, ylabel][0]],c='b')
    else:
        plt.scatter(X_embedded[:, 0], [x for x in range(len(X_embedded[:, 0]))], c=Y_true, s=5, cmap="Set1")
        plt.scatter([X_embedded[:, 0][0]],[0],c='b')
    return X_embedded


def plotTSNE(X,Y_true,n_components,xlabel=0,ylabel=1):
    tsne = TSNE(n_components=n_components, learning_rate='auto',init='random', perplexity=3)
    X_embedded = tsne.fit_transform(X)
    plt.scatter(X_embedded[:, xlabel], X_embedded[:, ylabel], c=Y_true, s=5, cmap="Set1")
    plt.scatter([X_embedded[:, xlabel][0]],[X_embedded[:, ylabel][0]],c='b')
    return tsne


def plotUMAP(X,Y_true,n_components,xlabel=0,ylabel=1):
    manifold = umap.UMAP(n_components=n_components).fit(X,Y_true)
    plotTransformData(manifold,X,Y_true,xlabel=xlabel,ylabel=ylabel)
    return manifold


def plotPCA(X,Y_true,n_components,xlabel=0,ylabel=1):
    pca = PCA(n_components=n_components, random_state=42)
    pca.fit(X,Y_true)
    plotTransformData(pca,X,Y_true,xlabel=xlabel,ylabel=ylabel)
    return pca


def plotLDA(X,Y_true,n_components,xlabel=0,ylabel=1):
    lda = LinearDiscriminantAnalysis(n_components=1)
    lda.fit(X,Y_true)
    plotTransformData(lda,X,Y_true,xlabel=xlabel,ylabel=ylabel)
    return lda


def plotNCA(X,Y_true,n_components,xlabel=0,ylabel=1):
    nca = NeighborhoodComponentsAnalysis(n_components=n_components)
    nca.fit(X,Y_true)
    plotTransformData(nca,X,Y_true,xlabel=xlabel,ylabel=ylabel)
    return nca


def plotICA(X,Y_true,n_components,xlabel=0,ylabel=1):
    transformer = FastICA(n_components=n_components,random_state=0,whiten='unit-variance')
    transformer.fit(X)
    plotTransformData(transformer,X,Y_true,xlabel=xlabel,ylabel=ylabel)
    return transformer