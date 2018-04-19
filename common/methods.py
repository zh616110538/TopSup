# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/9 10:39
# @desc    :

import requests
import webbrowser
import urllib.parse

# # 颜色兼容Win 10
from colorama import init,Fore
init()

def open_webbrowser(question):
    webbrowser.open('https://baidu.com/s?wd=' + urllib.parse.quote(question))

def open_webbrowser_count(question,choices):
    l = ['\n-- 方法2： 题目+选项搜索结果计数法 --\n']
    #print('\n-- 方法2： 题目+选项搜索结果计数法 --\n')
    l.append('Question: ' + question)
    #print('Question: ' + question)
    if '不是' in question:
        #print('**请注意此题为否定题,选计数最少的**')
        l.append('**请注意此题为否定题,选计数最少的**')

    counts = []
    for i in range(len(choices)):
        # 请求
        req = requests.get(url='http://www.baidu.com/s', params={'wd': question + choices[i]})
        content = req.text
        index = content.find('百度为您找到相关结果约') + 11
        content = content[index:]
        index = content.find('个')
        count = content[:index].replace(',', '')
        counts.append(count)
        #print(choices[i] + " : " + count)
    return output(choices, counts,l)

def count_base(question,choices):
    l = ['\n-- 方法3： 题目搜索结果包含选项词频计数法 --\n']
    #print('\n-- 方法3： 题目搜索结果包含选项词频计数法 --\n')
    # 请求
    req = requests.get(url='http://www.baidu.com/s', params={'wd':question})
    content = req.text
    #print(content)
    counts = []
    #print('Question: '+question)
    l.append('Question: ' + question)
    if '不是' in question:
        #print('**请注意此题为否定题,选计数最少的**')
        l.append('**请注意此题为否定题,选计数最少的**')
    for i in range(len(choices)):
        counts.append(content.count(choices[i]))
        #print(choices[i] + " : " + str(counts[i]))
    return output(choices, counts,l)

def output(choices, counts,l):
    counts = list(map(int, counts))
    #print(choices, counts)

    # 计数最高
    index_max = counts.index(max(counts))

    # 计数最少
    index_min = counts.index(min(counts))

    if index_max == index_min:
        #print(Fore.RED + "高低计数相等此方法失效！" + Fore.RESET)
        l.append(Fore.RED + "高低计数相等此方法失效！" + Fore.RESET)
        return l

    for i in range(len(choices)):
        #print()
        if i == index_max:
            # 绿色为计数最高的答案
            #print(Fore.GREEN + "{0} : {1} ".format(choices[i], counts[i]) + Fore.RESET)
            l.append(Fore.GREEN + "{0} : {1} ".format(choices[i], counts[i]) + Fore.RESET)
        elif i == index_min:
            # 红色为计数最低的答案
            #print(Fore.MAGENTA + "{0} : {1}".format(choices[i], counts[i]) + Fore.RESET)
            l.append(Fore.MAGENTA + "{0} : {1}".format(choices[i], counts[i]) + Fore.RESET)
        else:
            #print("{0} : {1}".format(choices[i], counts[i]))
            l.append("{0} : {1}".format(choices[i], counts[i]))
    return l


def run_algorithm(al_num, question, choices):
    res = None
    if al_num == 0:
        open_webbrowser(question)
    elif al_num == 1:
        res = open_webbrowser_count(question, choices)
    elif al_num == 2:
        res = count_base(question, choices)
    if res:
        for i in res:
            print(i+'\n')

if __name__ == '__main__':
    question = '新装修的房子通常哪种化学物质含量会比较高?'
    choices = ['甲醛', '苯', '甲醇']
    run_algorithm(1, question, choices)


