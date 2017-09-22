# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/19 上午9:29
# @Author  : huaixian
# @File    : Fluent_guben.py
# @Software: pycharm

import pandas as pd
import numpy as np

def preprocess(data_cat_df,data_num_df,y_data):  #data is DataFrame


    #one-hot
    data_cat_dummy=pd.get_dummies(data_cat_df)

    #deal missing value
    mean_cols = data_num_df.mean()
    data_num_df = data_num_df.fillna(mean_cols)
    print data_num_df.isnull().sum().sum()

    #deal normalize  (X-X')/s
    std_cols = data_num_df.std()
    data_num_df = (data_num_df - mean_cols)/std_cols

    #concat
    all_df = pd.concat([data_num_df,data_cat_dummy],axis =1)
    # print y_data

    return all_df.values ,y_data.values #numpy array











