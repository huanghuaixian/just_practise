# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/18 下午4:53
# @Author  : huaixian
# @File    : salary_preprocessing.py
# @Software: pycharm


import pandas as pd
import numpy as np
import json

class SalaryQinXi():
    def __init__(self):
        #原始数据，需要清洗的数据,修改相应的文件路径
        self.data_yuanshi = "/Users/huanghuaixian/bigdata/real_practise/QXdata/SCZZ_china.csv"
        self.ReadMe = '/Users/huanghuaixian/bigdata/real_practise/QXdata/SCZZ-ReadMe.json'
        self.data_QX = '/Users/huanghuaixian/bigdata/real_practise/QXdata/SCZZ.csv'
        #################################################
        self.df = pd.read_csv(self.data_yuanshi ,encoding="utf-8")
        self.D = {}
        self.m = 0
        self.data_yuanshi = "/Users/huanghuaixian/bigdata/real_practise/QXdata/it_china.csv"
        with open(self.ReadMe, 'w') as f:
            f.write('****************数字化记录\n')

    #删除含‘面议’的数据
    def DataDelete(self):
        self.df.monthlySalary = self.df.monthlySalary.fillna(u'面议')
        for index, row in self.df.iterrows():
            if u'面议' in row['monthlySalary']:
                self.df.drop(index, axis=0, inplace=True)

        self.df.drop('province', axis=1, inplace=True)
        self.df.drop('ReleaseDate', axis=1, inplace=True)
        # self.df.drop('monthlySalary', axis=1, inplace=True)

    def cut_wordl(self,word):
        position = word.find('-')
        if position != -1:
            bottomSalary = word[:position]
        else:
            bottomSalary = word[:word.find(u'元')]
        return bottomSalary

    def cut_wordh(self,word):
        position = word.find('-')
        if position != -1:
            topSalary = word[position:-3]
            topSalary = topSalary[1:]
        else:
            topSalary = word[:word.find(u'元')]
        return topSalary
    #人数去除人
    def cut_wordn(self,word):
        position = word.find(u'人')
        print word
        if position != -1:
            popNumber = word[:position]
        else:
            popNumber = -1
        return popNumber
    #数字化
    def get_number(self,word):
        i = 1
        for k, v in self.D.items():
            if word is k:
                i = 0
        if i == 1:
            self.m = self.m + i
            self.D[word] = self.m
        for k, v in self.D.items():
            if word is k:
                word = v
        # print D
        # print '+1'
        # with open('../data/ReadMe.json','w') as f:
        #     json_item = json.dumps(self.D, ensure_ascii=False)
        #     str = json_item.encode('utf-8')
        #     f.write(str)
        return word
    #日期规范
    # def get_time(self,word):
    #     for k, v in self.D.items():
    #         if word is k:
    #             i = 0
    #     if i == 1:
    #         self.D[word] = word
    #     for k, v in self.D.items():
    #         if u'小时' in k:
    #             v = '2017-09-18'

    def write(self):
        with open(self.ReadMe,'a') as f:
            json_item = json.dumps(self.D, ensure_ascii=False)
            str = json_item.encode('utf-8')
            f.write(str+'\n\n')

    def run(self):
        self.DataDelete()
        #月薪的下限
        self.df['bottomSalary'] = self.df.monthlySalary.apply(self.cut_wordl)
        # 月薪的上限
        self.df['topSalary'] = self.df.monthlySalary.apply(self.cut_wordh)
        ##########
        self.df.bottomSalary = self.df.monthlySalary.apply(self.cut_wordl)
        self.df.topSalary = self.df.monthlySalary.apply(self.cut_wordh)
        # 数据类型转为int类型
        self.df.topSalary = self.df.bottomSalary.astype('int')
        self.df['bottomSalary'] = self.df['bottomSalary'].astype('int')
        self.df.topSalary = self.df.topSalary.astype('int')
        self.df['topSalary'] = self.df['topSalary'].astype('int')
        self.df['avgSalary'] = (self.df.topSalary + self.df.bottomSalary) / 2

        #修改人数
        rementNumber = self.df.recruitmentNumber.apply(self.cut_wordn)
        self.df.recruitmentNumber = rementNumber
        self.df.recruitmentNumber.astype('int')
        # print rementNumber
        #city 数字化
        self.D = {}
        self.m = 0
        city = self.df.workLocation.apply(self.get_number)
        self.df.workLocation = city
        self.df.workLocation.astype('int')
        self.write()
        #workExperience 数字化
        self.D = {}
        self.m = 0
        workExperience = self.df.workExperience.apply(self.get_number)
        self.df.workExperience = workExperience
        self.df.workExperience.astype('int')
        self.write()
        #education 数字化
        self.D = {}
        self.m = 0
        education = self.df.education.apply(self.get_number)
        self.df.education = education
        self.df.education.astype('int')
        self.write()
        #industry 数字化
        self.D = {}
        self.m = 0
        industry = self.df.industry.apply(self.get_number)
        self.df.industry = industry
        self.df.industry.astype('int')
        self.write()
        # postCategory 数字化
        self.D = {}
        self.m = 0
        postCategory = self.df.postCategory.apply(self.get_number)
        self.df.postCategory = postCategory
        self.df.postCategory.astype('int')
        self.write()
        # company 数字化
        self.D = {}
        self.m = 0
        company = self.df.company.apply(self.get_number)
        self.df.company = company
        self.df.company.astype('int')
        self.write()
        # job 数字化
        self.D = {}
        self.m = 0
        job = self.df.job.apply(self.get_number)
        self.df.job = job
        self.df.job.astype('int')
        self.write()


        ##################
        self.df.drop('monthlySalary', axis=1, inplace=True)
        #清洗完成的数据，生成的csv名字和路径
        self.df.to_csv(self.data_QX,encoding='utf-8')
        print '清洗完成'

if __name__ == '__main__':
    SQX = SalaryQinXi()
    SQX.run()