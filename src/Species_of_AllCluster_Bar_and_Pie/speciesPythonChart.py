#coding=utf-8

'''
    1.统计所有物种数目大于2的cluster,用柱形图展示
    2.species_size/cluster_size 的饼图
    3.n_species_size / species_num 的饼图
    input file: test_02(all clusters have been sorted by cluster_size)
    output file: species_No_02(all species_tax_ids)
    main(start,end)

'''
import csv
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt

data_file = "./Data/test_02"

#define a function to open .csv file
def dataset(path):
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row

def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
        rect.set_edgecolor('white')

def main(path, start, end):

    cluster_id = []
    cluster_size = []
    cluster_ratio = []
    species_num = []
    species_no = []

    #with open(path, 'r') as file_to_read:
    with open(data_file) as file_to_read:
        while True:
            lines = file_to_read.readline()  #整行读取数据
            if not lines:
                break
            #将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            [id, size, ratio, num,no] = [(row) for row in lines.strip("\n").split(';')]
            cluster_id.append(id) #添加新读取的数据
            cluster_size.append(size)
            cluster_ratio.append(ratio)
            species_num.append(num)
            species_no.append(no)

    new_cluster_size = [int(i)for i in cluster_size]
    new_species_num = [int(i)for i in species_num]

    species = []
    species_dict = {}
    for i in range(len(species_no)):
        dict = {}
        everySpec = species_no[i].split('|')
        for j in range(len(everySpec)):
            Spec = everySpec[j].split('=')
            dict.setdefault(Spec[0], Spec[1])
            if not Spec[0] in species_dict:
                species_dict[Spec[0]] = 1
            else:
                species_dict[Spec[0]] = species_dict[Spec[0]] + 1
        species.append(dict)

    file = open("./Data/species_No_02", "a+", encoding='utf-8')
    keyList = species_dict.keys()
    for key in keyList:
        file.write(key + '\n')
    file.close()

    subCluster_id = []
    subCluster_size = []
    speciesNuminCluster = []
    speciesRatio = []
    for i in range(start-1, end):
        subCluster_id.append(cluster_id[i])
        subCluster_size.append(new_cluster_size[i])
        speciesNuminCluster.append(new_species_num[i])
        subSpeciesRatio = round(new_species_num[i]/new_cluster_size[i],5)
        speciesRatio.append(subSpeciesRatio)

    #画柱形图
    width = 0.3
    # 设置x轴柱子的个数
    ind = np.arange(len(subCluster_id))
    fig = plt.figure(1, figsize=(16, 10), dpi=80)
    ax1 = fig.add_subplot(121)
    bar_cluster_size = ax1.bar(ind, subCluster_size, width, color='forestgreen')
    bar_species_no = ax1.bar(ind + width, speciesNuminCluster, width, color='gold')
    ax1.set_xticks(ind + width/2)
    ax1.set_xticklabels(subCluster_id, rotation=90)
    ax1.set_xlabel('cluster_id')
    ax1.set_ylabel('cluster_size/species_num')
    ax1.set_title("Species Information in Clustering File")
    add_labels(bar_cluster_size)
    add_labels(bar_species_no)
    plt.grid(True)

    #画All Species Ratio of Cluster 饼图
    ax2 = fig.add_subplot(222)
    labels = 'species_ratio:'+'%s' % speciesRatio[0], 'other'
    sizes = speciesRatio[0], (1-speciesRatio[0])
    colors = 'lightgreen', 'gold'
    explode = 0, 0
    ax2.pie(sizes, explode=explode, labels=labels,colors=colors, autopct='%1.1f%%', shadow=True, startangle=50)
    ax2.axis('equal')
    ax2.set_title("All Species Ratio of "+ subCluster_id[0])

    #画Each Species Ratio of Cluster
    labels2 = []
    size2 = []
    expl2 = []
    ax3 = fig.add_subplot(224)
    for key, value in species[start-1].items():
        labels2.append(key)
        size2.append(int(value))
        expl2.append(int(0))
    ax3.pie(size2, explode = expl2,labels = labels2, autopct = '%1.1f%%',startangle=50)
    ax3.axis('equal')
    ax3.set_title("Each Species Ratio of " + subCluster_id[0])

    plt.show()
    plt.close()

main(data_file,199999,200009)
