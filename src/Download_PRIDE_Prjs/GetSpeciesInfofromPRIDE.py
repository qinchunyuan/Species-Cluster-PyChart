#coding=utf-8

import json
import urllib.request
import urllib
import pandas as pd

# 利用urllib获取网络数据
def registerUrl(project_id):
    try:
        url = "https://www.ebi.ac.uk/pride/ws/archive/project/"+ project_id
        data = urllib.request.urlopen(url).read()
        return data
    except Exception as e:
        print(e)

def Url(taxId):
    try:
        url = "https://www.ebi.ac.uk/ena/data/taxonomy/v1/taxon/tax-id/%d" % taxId
        data = urllib.request.urlopen(url).read()
        return data
    except Exception as e:
        print(e)

def Url_name(species_name):
    try:
        url = "https://www.ebi.ac.uk/ena/data/taxonomy/v1/taxon/any-name/"+species_name
        print(url)
        data = urllib.request.urlopen(url).read()
        return data
    except Exception as e:
        print(e)

def s_Info_by_projects_id():
    data = registerUrl()
    file = open("./Data/SP_TEST", "a+", encoding="utf-8")
    file.write(data.decode("utf-8") + "\n")
    file.close()
    print(data.decode("utf-8"))

def s_name_by_species_taxids():
    taxon_ids = []
    with open('./Data/TaxonInfo/species_No_01', 'r') as textfile:
        while True:
            lines = textfile.readline()
            if not lines:
                break
            line = lines.strip("\n")
            taxon_ids.append(line)
    textfile.close()

    Species_No_Info = []
    file = open("./Data/TaxonInfo/01", "a+", encoding='utf-8')
    for id in taxon_ids:
        data = Url(int(id))
        s = data.decode("utf-8").replace("\n", "")
        file.write(s + "\n")
    file.close()
    return


def s_taxids_by_species_name():
    species_name = []
    with open("./Data/TaxonInfo/species_name_cp", 'r') as file:
        while True:
            lines = file.readline()
            if not lines:
                break
            line = lines.strip("\n").replace(" ","%20").strip("'")
            species_name.append(line)
    file.close()

    s_file = open("./Data/TaxonInfo/species_tax_id", "a+", encoding='utf-8')
    for name in species_name:
        print(name)
        data = Url_name(name)
        print(data)
        s = data.decode("utf-8").replace("\n","").replace("\n","").replace("    ","").replace("   ","").replace("  ","").replace(": ",":")
        s_file.write(s + "\n")
    s_file.close()

    return

def analyser():
    list = []
    with open("./Data/TaxonInfo/species_tax_id",'r', encoding='UTF-8') as f:
        dict = {}
        while True:
            lines = f.readline()
            if not lines:
                break
            line = lines.strip()
            dict = json.loads(line)
            list.append(dict)
    f.close()

    species_list = []
    with open("./Data/TaxonInfo/s_name_tax_id", 'r', encoding='UTF-8') as file:
        while True:
            lines = file.readline()
            if not lines:
                break
            line = lines.strip("\n")
            species_list.append(line)
    file.close()

    projectIds_list = []
    taxIds_list = []
    s_name_list = []
    species_name_list = []
    for i in range(len(list)):
        if len(list[i]) == 1:
            dict = list[i][0]
            taxid = dict.get("taxId")
            s_name = dict.get("scientificName")
            taxIds_list.append(taxid)
            s_name_list.append(s_name)
        else:
            t_n = ""
            for k in range(len(list[i])):
                sub_dict = list[i][k]
                taxids = list[i][k].get("taxId")
                if t_n == "":
                    t_n = taxids
                else:
                    t_n = t_n + "," + taxids
                print(t_n)
            taxIds_list.append(t_n)
            s_name_list.append(list[i][0].get("scientificName"))
    print(taxIds_list)


    for name in species_list:
        s_name = name
        species_name_list.append(s_name)

    columns = ["tax_id", "s_name","species_name"]
    dataFrame = pd.DataFrame({'tax_id': taxIds_list, 's_name': s_name_list, 'species_name': species_name_list})
    dataFrame.to_csv("./Data/taxid_name.csv", index=False, sep=',', columns=columns)


if __name__ == "__main__":
    #s_taxids_by_species_name()
    analyser()




