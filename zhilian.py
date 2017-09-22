# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/14 下午4:31
# @Author  : huaixian
# @File    : zhilian.py
# @Software: pycharm


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @time  : 2017/7/21 8:53
# @Author : yang chuanwei
# @File   : ZLZP.py
# @Softwore : PyCharm

import time
import requests
import json
from scrapy import Selector

class ZhilianZP():
    def __init__(self):
        self.fp = open('./ZLZPTail.json','w')
        self.url = 'http://sou.zhaopin.com'
        self.tag = 0
        self.headers = {
            'Connection':'keep-alive'
            ,'Host':'sou.zhaopin.com'
            ,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
            ,'Cookie':'JSSearchModel=0; LastCity%5Fid=545; LastCity=%e6%b2%b3%e5%8d%97; BLACKSTRIP=yes; dywez=95841923.1505350973.2.2.dywecsr=baidu|dyweccn=(organic)|dywecmd=organic; LastJobTag=%e4%ba%94%e9%99%a9%e4%b8%80%e9%87%91%7c%e7%bb%a9%e6%95%88%e5%a5%96%e9%87%91%7c%e5%85%a8%e5%8b%a4%e5%a5%96%7c%e5%b8%a6%e8%96%aa%e5%b9%b4%e5%81%87%7c%e5%b9%b4%e5%ba%95%e5%8f%8c%e8%96%aa%7c%e5%8c%85%e4%bd%8f%7c%e5%8a%a0%e7%8f%ad%e8%a1%a5%e5%8a%a9%7c%e8%8a%82%e6%97%a5%e7%a6%8f%e5%88%a9%7c%e5%8c%85%e5%90%83%7c%e5%91%98%e5%b7%a5%e6%97%85%e6%b8%b8%7c%e5%bc%b9%e6%80%a7%e5%b7%a5%e4%bd%9c%7c%e9%a4%90%e8%a1%a5%7c%e5%b9%b4%e7%bb%88%e5%88%86%e7%ba%a2%7c%e4%ba%a4%e9%80%9a%e8%a1%a5%e5%8a%a9%7c%e5%85%8d%e8%b4%b9%e7%8f%ad%e8%bd%a6%7c%e9%80%9a%e8%ae%af%e8%a1%a5%e8%b4%b4%7c%e8%a1%a5%e5%85%85%e5%8c%bb%e7%96%97%e4%bf%9d%e9%99%a9%7c%e5%ae%9a%e6%9c%9f%e4%bd%93%e6%a3%80%7c%e9%ab%98%e6%b8%a9%e8%a1%a5%e8%b4%b4%7c%e6%88%bf%e8%a1%a5%7c%e8%82%a1%e7%a5%a8%e6%9c%9f%e6%9d%83%7c%e9%87%87%e6%9a%96%e8%a1%a5%e8%b4%b4%7c%e4%b8%8d%e5%8a%a0%e7%8f%ad%7c%e5%88%9b%e4%b8%9a%e5%85%ac%e5%8f%b8%7c%e6%af%8f%e5%b9%b4%e5%a4%9a%e6%ac%a1%e8%b0%83%e8%96%aa%7c%e4%bd%8f%e6%88%bf%e8%a1%a5%e8%b4%b4%7c%e5%81%a5%e8%ba%ab%e4%bf%b1%e4%b9%90%e9%83%a8%7c%e6%97%a0%e8%af%95%e7%94%a8%e6%9c%9f%7c14%e8%96%aa; LastSearchHistory=%7b%22Id%22%3a%2289e4f3e6-bff6-45c4-b9fe-6f0d92c8ddcf%22%2c%22Name%22%3a%22it+%2b+%e6%b2%b3%e5%8d%97%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3f%26jl%3d%25e6%25b2%25b3%25e5%258d%2597%26kw%3dit%26p%3d1%26isadv%3d0%22%2c%22SaveTime%22%3a%22%5c%2fDate(1505354658502%2b0800)%5c%2f%22%7d; urlfrom=121126445; urlfrom2=121126445; adfcid=none; adfcid2=none; adfbid=0; adfbid2=0; dywea=95841923.3655429353057721300.1505302951.1505350973.1505352627.3; dywec=95841923; dyweb=95841923.5.9.1505354676902'
            ,'Upgrade-Insecure-Requests':'1'

        }
        self.count=0

    def get_list(self,url):


        try:
            r = requests.get(url, headers=self.headers)
        except Exception, e:
            print u'1.当前列表页错误，url: ' + url + u', 错误信息：' + str(e)
            return
        # print u'当前地址' ,url
        body = Selector(text=r.text)
        divs = body.xpath('//*[@id="newlist_list_content_table"]/table')[1:]
        # print 'divs:', len(divs)
        # with open('./check3_html.html', 'w') as fp:
        #     fp.write(r.content)
        # str = body.xpath('//*[@id="newlist_list_content_table"]/table[2]/tr[1]/td[1]/div[1]/a[1]/@href').extract()
        # if str:
        #     str=str[0].strip()
        # print 'str',str
        # 详情页

        # div_None = body.xpath('//*[@class="show_recommend_tips"]')
        # print 'divs:',divs,int(divs)
        # if div_None :
        #     print u'没有职位了'
        #     return 1
        # else:
        #     tables = divs.xpath('table')[1:]
        #     print 'tables:' ,len(tables)

        for table in divs:
            # if not div_None :
            #     print u'后面都没有了（都不是的）'
            #     return 2
            # else:
            # print 'table:' ,table
            detail_url = table.xpath('tr[1]/td[1]/div[1]/a[1]/@href').extract()
            # print '详情地址22', detail_url
            if detail_url:
                detail_url = detail_url[0].strip()
                self.get_detail(detail_url)


        # 分页
        # count=0
        next=None
        try:
            next = body.xpath('//*[@class="pagesDown-pos"]/a/@href').extract()
        except Exception ,e2:
            print 'error',e2
        if next:
            next_url= next[0].strip()
            print u'***************************页数：',next_url[-2:]
            if self.tag==0:
                self.get_list(next_url)



    def get_detail(self,detail_url):
        time.sleep(1)

        headers = {
            'Connection': 'keep-alive'
            , 'Host': 'jobs.zhaopin.com'
            ,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
            ,
            'Cookie': 'JSSearchModel=0; dywez=95841923.1505350973.2.2.dywecsr=baidu|dyweccn=(organic)|dywecmd=organic; stayTimeCookie=1505356729088; referrerUrl=http%3A//jobs.zhaopin.com/457962538250591.htm%3Fssidkey%3Dy%26ss%3D201%26ff%3D03%26sg%3D4f0a05783791409a84f9e81f7537d0cf%26so%3D2; LastCity%5Fid=548; LastCity=%e5%b9%bf%e4%b8%9c; LastSearchHistory=%7b%22Id%22%3a%22db8a0523-ece3-4437-97d0-d3ce8297a88b%22%2c%22Name%22%3a%22it+%2b+%e5%b9%bf%e4%b8%9c%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fjl%3d%25e5%25b9%25bf%25e4%25b8%259c%26kw%3dit%22%2c%22SaveTime%22%3a%22%5c%2fDate(1505356915541%2b0800)%5c%2f%22%7d; urlfrom=121126445; urlfrom2=121126445; adfcid=none; adfcid2=none; adfbid=0; adfbid2=0; dywea=95841923.3655429353057721300.1505302951.1505350973.1505352627.3; dywec=95841923; dyweb=95841923.8.9.1505354676902'
            , 'Upgrade-Insecure-Requests': '1'

        }
        try:
            r= requests.get(detail_url,headers = headers,timeout=30)
        except Exception,e:
            print "flase"
            return
        if r.status_code != 200:
            print '请求错误', r.status_code
            return
        # print u'详细地址11',detail_url, '\n网页代码' , r.status_code
        body = Selector(text=r.text)
        with open('./check5xq_html.html', 'w') as fp:
            fp.write(r.content)
        item = self.get_item()

        item[u'行业']=self.job
        item[u'省份']=self.addSF

        str = body.xpath('//*[@class="top-fixed-box"]/div[1]/div[1]/h1/text()').extract()
        if str:
            item[u'职位名'] = str[0].strip()
            print 'zwm', str[0].strip

        str = body.xpath('string(//*[@class="company-name-t"]/a/text())').extract()
        if str:
            item[u'公司名'] = str[0].strip()

        # str = body.xpath('string(//body/div[5]/div/div/div)').extract()
        # if str:
        #     item[u'福利标签'] = str[0].strip()
        #     print 'flbq',str[0].strip

        str = body.xpath('//*[@class="terminalpage-left"]/ul/li[1]/strong[1]/text()').extract()
        if str:
            self.count +=1
            print self.count
            item[u'月薪'] = str[0].strip()

        str = body.xpath('//*[@class="terminalpage-left"]/ul/li[2]/strong/a/text()').extract()
        if str:
            item[u'工作地点'] = str[0].strip()

        str = body.xpath('//*[@class="terminalpage-left"]/ul/li[3]/strong/span/text()').extract()
        if str :
            item[u'发布日期'] = str[0].strip()

        # str = body.xpath('//*[@class="terminalpage-left"]/ul/li[4]/strong/text()').extract()
        # if str:
        #     item[u'工作性质'] = str[0].strip()
        #     print 'gzxz', str[0].strip

        str = body.xpath('//*[@class="terminalpage-left"]/ul/li[5]/strong/text()').extract()
        if str:
            item[u'工作经验'] = str[0].strip()

        str = body.xpath('//*[@class="terminalpage-left"]/ul/li[6]/strong/text()').extract()
        if str:
            item[u'学历'] = str[0].strip()
        # str = body.xpath('//*[@id="nav1"]/section[1]/div[1]/span[1]/text()').extract()
        # if str:
        #     item[u'岗位名字'] = str[0].strip()

        str = body.xpath('//*[@class="terminalpage-left"]/ul/li[7]/strong/text()').extract()
        if str:
            item[u'招聘人数'] = str[0].strip()

        str = body.xpath('//*[@class="terminalpage-left"]/ul/li[8]/strong/a/text()').extract()
        if str:
            item[u'职位类别'] = str[0].strip()

        # str = body.xpath('string(//*[@class="terminalpage-main clearfix"]/div/div[1])').extract()
        # if str:
        #     item[u'职位描述'] = str[0].strip()
        # str = body.xpath('//*[@class="terminalpage-main clearfix"]/div/div/h2/text()').extract()
        # if str:
        #     item[u'工作地址'] = str[0].strip()
        # str = body.xpath('string(//*[@class="terminalpage-main clearfix"]/div/div[2])').extract()
        # if str:
        #     item[u'公司介绍'] = str[0].strip()
        # str = body.xpath('//*[@class="terminal-ul clearfix terminal-company mt20"]/li[1]/strong/text()').extract()
        # if str:
        #     item[u'公司规模'] = str[0].strip()
        # str = body.xpath('//*[@class="terminal-ul clearfix terminal-company mt20"]/li[2]/strong/text()').extract()
        # if str:
        #     item[u'公司性质'] = str[0].strip()
        #
        # str = body.xpath('//*[@class="terminal-ul clearfix terminal-company mt20"]/li[3]/strong/text()').extract()
        # if str:
        #     item[u'公司行业'] = str[0].strip()
        # print item

        self.write(item)


    def get_urls(self,url):
        time.sleep(4)

        r = requests.get(url,headers =self.headers)
        if r.status_code != 200:
            print '请求错误', r.status_code
            return
        body = Selector(text=r.text)
        addrs = body.xpath('//*[@class="newlist_sx"]/div[3]/div[1]/div[2]/a')[1:]
        ases = {}
        # # 获取区域地址，接着获取职位类别地址
        # for addr in addrs:
        #     addr_url = addr.xpath('@href').extract()[0]
        #     addr_name = addr.xpath('text()').extract()
        #     if addr_name:
        #         addr_name = addr_name[0].strip()
        #     ar_url = self.url + addr_url
        #     print 'at_url:' ,ar_url
        #     time.sleep(1)
        #     ar = requests.get(ar_url,headers =self.headers)
        #     abody = Selector(text=ar.text)
        #     job_sorts = abody.xpath('//*[@class="newlist_moresearch"]/div/div[2]/ul/li[5]/div/a')[1:]
        #     for sort in job_sorts:
        #         jobso_url = sort.xpath('@href').extract()[0]
        #         jobso_name = sort.xpath('text()').extract()[0]
        #         jobar_url = self.url + jobso_url
        #         name = addr_name + '-' +jobso_name
        #         print name
        #         print 'jobar_url:', jobar_url
        #
        #         ases[name] = jobar_url
        # # self.get_item()['urls'] = ases
        return ases


    def get_item(self):
        item = {
            u'行业':''
            ,u'省份':''
            ,u'职位名': ''
            , u'公司名': ''
            # ,u'福利标签': ''
            ,u'月薪': ''
            ,u'工作地点': ''
            ,u'发布日期': ''
            # ,u'工作性质': ''
            ,u'工作经验': ''
            ,u'学历': ''
            ,u'招聘人数': ''
            ,u'职位类别': ''
            # ,u'职位描述': ''
            # ,u'工作地址': ''
            # ,u'公司介绍': ''
            # ,u'公司规模': ''
            # ,u'公司性质': ''
            # ,u'公司行业':''

        }
        return item
    def write(self,item):
        # 数据写入
        json_item = json.dumps(item, ensure_ascii=False)
        str = json_item.encode('utf-8')
        self.fp.write(str + '\n')
    def run(self):
        jobs = [u'生产制造']
        addSFs=[u'全国']
        for job in jobs:
            for addSF in addSFs:
                url = self.url + '/jobs/searchresult.ashx?jl='+ addSF + '&kw='+job
                print url
                # ases = self.get_urls(url)
                self.job=job
                self.addSF=addSF
                self.get_list(url)
                # self.get_item()
        # print ases
        # for k,v in url.items():
        #     self.get_list(v)
        #     self.get_item()[k] = v
        # url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%88%90%E9%83%BD&kw=java%E5%B7%A5%E7%A8%8B%E5%B8%88&isfilter=1&p=1&re=2117'
        # se
        self.fp.close()

if __name__ == '__main__':
    zp = ZhilianZP()
    zp.run()