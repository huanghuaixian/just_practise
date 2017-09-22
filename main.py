# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/18 下午2:02
# @Author  : huaixian
# @File    : stock.py
# @Software: pycharm

from sklearn.linear_model import Ridge
from sklearn.ensemble import BaggingRegressor
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import AdaBoostClassifier
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
from preprocess import *
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split,StratifiedShuffleSplit,StratifiedKFold
from sklearn.metrics import classification_report
from sklearn import preprocessing

#测试岭回归的最佳参数
def test_ridge(trainX,trainY):
    ridge = Ridge(15)
    params = [1, 10, 15, 20, 25, 30, 40]
    test_scores = []
    for param in params:
        clf = BaggingRegressor(n_estimators=param)
        test_score = np.sqrt(-cross_val_score(clf,trainX,trainY,cv=10,scoring ='neg_mean_squared_error'))
        test_scores.append(np.mean(test_score))
    plt.plot(params,test_scores)
    plt.title("tree_n_estimator vs CV error")
    plt.show()

#测试AdaBoostRegressor的最佳参数
def test_AdaBoost(trainX,trainY):
    params = [10,15,20,25,30,35,40,45,50]
    ridge = Ridge(15)
    test_scores=[]
    for param in params:
        clf = AdaBoostClassifier(n_estimators=param)
        test_score=np.sqrt(-cross_val_score(clf,trainX,trainY,cv=10,scoring="neg_mean_squared_error"))
        test_scores.append(np.mean(test_score))
    plt.plot(params,test_scores)
    plt.title('AdaBoost_ridge_n_estimator vs CV error')
    plt.show()


#测试xgb的最佳参数
def test_xgb(trainX,trainY):
    params = [1,2,3,4,5,6]
    test_scores =[]
    for param in params:
        clf = XGBRegressor(max_depth=param)
        test_score=np.sqrt(-cross_val_score(clf,trainX,trainY,cv=10,scoring="neg_mean_squared_error"))
        test_scores.append(np.mean(test_score))
    plt.plot(params,test_scores)
    plt.title('xgb_n_estimators vs CV error')
    plt.show()

#(x - x')/s  转为正太分布
def scaling(data):
    data_array = np.array(data)
    data_max = np.max(data_array)
    data_min = np.min(data_array)
    data_scaling = (data_array - data_min)/(data_max-data_min)
    data_scaling_mean =np.mean(data_scaling)
    return data_scaling_mean

def concat_zhaopin(data_X1,data_X2,data_x3,data_x4,data_x5):
    all_df = pd.concat([data_X1,data_X2,data_x3,data_x4,data_x5],axis=0)
    all_cat = all_df[['workLocation','workExperience','industry','postCategory','job','education','company']]
    all_num = all_df[['recruitmentNumber','bottomSalary','avgSalary']]
    all_y = all_df['avgSalary']
    return all_df,all_cat,all_num,all_y

def zhao_people(all_df):
    all_cat_peo = all_df[['workLocation', 'workExperience', 'industry', 'postCategory', 'job', 'education', 'company']]
    all_num_peo = all_df[['topSalary', 'bottomSalary', 'avgSalary']]
    all_y_peo = all_df['recruitmentNumber']
    print all_df.shape,all_cat_peo.shape,all_y_peo.shape
    return all_cat_peo,all_num_peo,all_y_peo


#预测数据融合
def merge(y_Salary,y_FCA):

    y_total = 0.5*y_Salary + 0.5*y_FCA
    return y_total


if __name__== "__main__":
    # 预测工资数据
    # dataXS =pd.read_csv()
    fuwu = pd.read_csv('/Users/huanghuaixian/bigdata/real_practise/zhaopin/fuwu.csv', index_col=0)
    it = pd.read_csv('/Users/huanghuaixian/bigdata/real_practise/zhaopin/it.csv', index_col=0)
    jinrong = pd.read_csv('/Users/huanghuaixian/bigdata/real_practise/zhaopin/jinrong.csv', index_col=0)
    SCZZ = pd.read_csv('/Users/huanghuaixian/bigdata/real_practise/zhaopin/SCZZ.csv', index_col=0)
    jiaoyu = pd.read_csv('/Users/huanghuaixian/bigdata/real_practise/zhaopin/jiaoyu.csv', index_col=0)
    all_df, all_cat, all_num, all_y =concat_zhaopin(fuwu,it,jinrong,SCZZ,jiaoyu)
    train_Salary,train_Salary_y = preprocess(all_cat,all_num,all_y)

    # AdaBoostRegressor
    ridge = Ridge(15)
    trainX_Sal,testX_Sal,trainy_Sal,testy_Sal = train_test_split(train_Salary,train_Salary_y,test_size=0.1,random_state=1)
    clf_Ada = AdaBoostRegressor(n_estimators=10,base_estimator=ridge)
    clf_Ada.fit(trainX_Sal,trainy_Sal)
    # scores = clf_Ada.score(testXF,testyF)
    y_Sal =clf_Ada.predict(testX_Sal)
    # print y_Sal
    sal_pred =scaling(y_Sal)
    print sal_pred
    scores_Sal_C = cross_val_score(clf_Ada,train_Salary,train_Salary_y)
    scores_Sal_CV = np.mean(scores_Sal_C)
    scores_Sal =clf_Ada.score(testX_Sal,testy_Sal)
    print 'AdaBoostRegression:',scores_Sal
    print 'AdaBoostRegression_cv:', scores_Sal_CV
    print 'finished with the mean-Salary(平均工资预测ok)'

    #预测股票数据流通股本
    dataXFCA = pd.read_csv('/Users/huanghuaixian/desktop/final.csv',encoding ="GBK")
    data_cat_df = dataXFCA[['area','province','city','year','month','day','industry']].astype(str)
    y_data = dataXFCA['fcA']
    data_num_df = dataXFCA[['gcA']]
    train ,y_data= preprocess(data_cat_df,data_num_df,y_data)
    trainXF,testXF,trainyF,testyF = train_test_split(train,y_data,test_size=0.1,random_state=1)

    #BaggingRegression
    ridge = Ridge(15)
    clf = BaggingRegressor(n_estimators=15,base_estimator=ridge)
    clf.fit(trainXF,trainyF)
    y_FCA = clf.predict(testXF)
    # print y_FCA
    #deal with scaling
    FCA_pred =scaling(y_FCA)
    print FCA_pred
    scores = clf.score(testXF,testyF)
    scores_c = cross_val_score(clf_Ada, train_Salary, train_Salary_y)
    scores_cv = np.mean(scores_c)
    print 'Baggingregression:', scores
    print 'BaggingRegression_CV',scores_cv
    print 'finished with the FCA(完成流通股本预测)'

    y =merge(sal_pred,FCA_pred)
    print '行业衡量标准：',y
    print 'ok'