##coding=utf-8
import json
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
from plotly import tools
from plotly.graph_objs import *
import pandas as pd

'''
    Data: all species in the projects json files download from PRIDE API
    Pie

'''

def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
        #柱形图边缘用白色填充，为了更加清晰可分辨
        rect.set_edgecolor('white')

if __name__ == '__main__':

    Pride_Species_Info = []
    with open('./Data/test_01','r',encoding='UTF-8') as textfile:
        dict = {}
        while True:
            lines = textfile.readline()
            if not lines:
                break
            line = lines.strip()
            dict = json.loads(line)
            Pride_Species_Info.append(dict)
    textfile.close()

    Species_No_Info = []
    with open('./Data/Species_name_02', 'r', encoding='UTF-8') as file:
        spec_no_dict = {}
        while True:
            lines = file.readline()
            if not lines:
                break
            line = lines.strip()
            spec_no_dict = json.loads(line)
            Species_No_Info.append(spec_no_dict)
    file.close()
    print(Species_No_Info)

    species_dict = {}
    for i in range(len(Pride_Species_Info)):
        value = str(Pride_Species_Info[i].get("species")).strip('[').strip(']').split(",")
        for vals in value:
            val = vals.strip(" ")
            if not val in species_dict:
                species_dict[val] = 1
            else:
                species_dict[val] = species_dict[val] + 1

    #print(species_dict)
    #print(species_dict.get("'Homo sapiens (Human)'"))
    #print(len(species_dict))

    keyList = species_dict.keys()
    smallKey = []
    smallValue = []
    keyTarget = []
    valueTarget = []
    sub_dict = {}
    for key in keyList:
        no = species_dict.get(key)
        if no == 1:
            smallKey.append(key)
            smallValue.append(no)
        else:
            keyTarget.append(key)
            valueTarget.append(no)
    for i in range(len(keyTarget)):
        sub_dict[keyTarget[i]] = valueTarget[i]
    '''
    df = pd.DataFrame.from_dict(sub_dict, orient='index')
    print(df.shape)
    data = [Bar(x = df.index, y = df[0])]
    print(data)

    #df.plot.bar()
    #plt.show()
    '''


    '''
    file = open("./Data/", "a+", encoding='utf-8')
    for i in range(len(smallKey)):
        key = smallKey[i]
        value = smallValue[i]
        s = key + ":" + str(value)
        file.write(s + '\n')
    file.close() 
    print(len(keyTarget))
    print(len(valueTarget))
    '''

    # 画柱形图
    #width = 0.2
    # 设置x轴柱子的个数
    #ind = np.arange(len(keyTarget))
    fig = plt.figure(1, figsize=(16, 12), dpi=80)
    #ax1 = fig.add_subplot(121)
    #bar_species_size = ax1.bar(ind, valueTarget, width, color='forestgreen')
    #ax1.set_xticks(ind )
    #ax1.set_xticklabels(keyTarget, rotation=90)
    #ax1.set_xlabel('Species Name')
    #ax1.set_ylabel('Species Count')
    #ax1.set_title("Species Information in PRIDE_Cluster_Project File")
    #add_labels(bar_species_size)
    #plt.grid(True)

    # 画All Species Ratio of Cluster 饼图
    explode = []
    ax2 = fig.add_subplot(111)
    labels = keyTarget
    sizes = valueTarget
    for i in range(len(labels)):
        explode.append(int(0))
    ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=10)
    ax2.axis('equal')
    ax2.set_title("All Species Ratio")

    plt.show()
    plt.close()














