# -*- coding: utf-8 -*-
# @function:
# @Time    : 2020/4/16 21:22
# @Author  : ofen
# @Email   : 52083628@qq.com
# @File    : zet_1.py
# @Software: PyCharm

import time
import csv
from itertools import combinations

# end_k = 14/2 + 1 = 8
def dfs_find(dics:dict, start:int ,end_k:int ,name:list ,all_name:dict):  # 初始化传入参数 name = [start]，
    # all_name_ = {1:{start_people},2:{},3:{},4:{},5:{},6:{},7:{},8:{}}
    if len(name) >= end_k:
        name.pop()
        return name, all_name
    for i in dics[start]:
        if i in name:  # 传到重复的人名直接over
            continue
        else:
            name.append(i)
            if i in all_name[len(name)]:
                all_name[len(name)][i].add(frozenset(name))
            else:
                all_name[len(name)][i] = {frozenset(name)}
            name, all_name = dfs_find(dics, i, end_k, name, all_name)

    if name != []:
        name.pop()  # 某个映射全走完了任然没有匹配，则清空本祭品盘
    return name, all_name

def count_ans(people_dict:dict, start_people:int):  # 分别统计主函数
    # print(start_people, 'start')
    all_name_ = {1:{start_people},2:{},3:{},4:{},5:{},6:{},7:{},8:{}}  # 树结构初始化
    name_ = [start_people]
    _, b = dfs_find(people_dict, start_people, 8, name_, all_name_)  # b储存了前8层中的每一个节点号码

    temp_ans = {4: 0, 6: 0, 8: 0, 10: 0, 12: 0, 14: 0}
    temp_set = set()
    for lobar_nam in range(3, 9):
        # print(lobar_nam)
        temp_set = set()
        for lian in b[lobar_nam].values():
            if len(lian) > 1:
                for i,j in combinations(lian, 2):
                    con_set = i | j
                    if len(con_set) == (lobar_nam - 1) * 2:
                        temp_set.add(con_set)

        temp_ans[(lobar_nam - 1) * 2] = len(temp_set)
    # print(temp_ans, start_people)
    return temp_ans


if __name__ == '__main__':
    time_start = time.clock()
    # 假设2个村子分别是A村和B村，A村有x人，那么用字典people储存所有人的朋友关系，其中前x项是A村人，后面的是B村人
    people = {}

    # 获取映射关系（朋友关系）
    with open('Example.csv', 'r') as f:
        reader = csv.reader(f)
        result = list(reader)
        num_A = len(result)  # 256 A村人数
        num_B = len(result[0])  # 640 B村人数
        # print(result[1])
        for i in range(num_A):
            temp = []
            for j in range(num_B):
                if result[i][j] == '1':
                    temp.append(j + num_A + 1)
            people[i+1] = temp

        for i in range(num_B):
            temp = []
            for j in range(num_A):
                if result[j][i] == '1':
                    temp.append(j+1)
            people[i+1 + num_A] = temp

    # print("Time used:", (time.clock() - time_start))

    # manager = multiprocessing.Manager()
    # ans_list = manager.list()
    ans_list = []
    with open('result.txt', 'w') as f:
        if num_A == 1344:
            for first in range(1, num_A + 1, 192):
                ans_list.append(count_ans(people, first))

            ans2 = {4: 0, 6: 0, 8: 0, 10: 0, 12: 0, 14: 0}
            for ans in ans_list:
                for key in ans.keys():
                    ans2[key] += ans[key]
            for key, items in zip(ans2.keys(), ans2.values()):
                items = items * 2 * 192 // key
                print(key, ':', items)
                f.write(str(key) + ':' + str(items) + '\n')

        elif num_A == 256:
            for first in range(1, num_A + 1, 64):
                ans_list.append(count_ans(people, first))

            ans2 = {4: 0, 6: 0, 8: 0, 10: 0, 12: 0, 14: 0}
            for ans in ans_list:
                for key in ans.keys():
                    ans2[key] += ans[key]
            for key, items in zip(ans2.keys(), ans2.values()):
                items = items * 2 * 64 // key
                print(key, ':', items)
                f.write(str(key) + ':' + str(items) + '\n')
    print("Time used:", (time.clock() - time_start))

