##coding=utf-8
import json
import pandas as pd

def Get_species():
    Pride_Species_Info = []
    with open('./data/json_02.txt', 'r', encoding='UTF-8') as textfile:
        while True:
            lines = textfile.readline()
            if not lines:
                break
            line = lines.strip()
            dict = json.loads(line)
            Pride_Species_Info.append(dict)
    textfile.close()

    taxids_list = []
    species_name_list =[]
    df = pd.read_csv('./data/taxid_name.csv')
    dataSet = df[["tax_id","s_name","species_name"]]
    tuples = [tuple(x) for x in dataSet.values]
    for i in range(len(tuples)):
        tup = tuples[i]
        taxids = tup[0]
        taxids_list.append(taxids)
        species = tup[-1]
        species_name_list.append(species)

    sub_project_ids = []
    sub_taxids_list = []
    sub_species_name_list = []
    for i in range(len(Pride_Species_Info)):
        project_id = Pride_Species_Info[i].get("accession")

        value = str(Pride_Species_Info[i].get("species")).strip('[').strip(']').split(",")
        if value[0] == "":
            sub_project_ids.append(project_id)
            sub_species_name_list.append("null")
            sub_taxids_list.append("null")

        elif len(value) == 1 and value[0] != "":
            for j in range(len(species_name_list)):
                if value[0] == species_name_list[j]:
                    string = taxids_list[j].strip("\"").split(",")
                    if len(string) > 1:
                        for i in range(len(string)):
                            taxid = string[i]
                            sub_taxids_list.append(taxid)
                            sub_project_ids.append(project_id)
                            sub_species_name_list.append(value[0])
                    else:
                        taxid = taxids_list[j]
                        sub_taxids_list.append(taxid)
                        sub_project_ids.append(project_id)
                        sub_species_name_list.append(value[0])
                    break

        elif len(value) > 1:
            for i in range(len(value)):
                val = value[i].strip(" ")
                sub_project_ids.append(project_id)
                sub_species_name_list.append(val)
                for j in range(len(species_name_list)):
                    if val == species_name_list[j]:
                        string = taxids_list[j].strip("\"").split(",")
                        if len(string) > 1:
                            taxid = string[i]
                            sub_taxids_list.append(taxid)
                        else:
                            taxid = taxids_list[j]
                            sub_taxids_list.append(taxid)
                        break

    col = ["project_id","tax_id","species_name"]
    dataFrame = pd.DataFrame({"project_id":sub_project_ids,"tax_id":sub_taxids_list,"species_name":sub_species_name_list})
    dataFrame.to_csv("./data/prj_taxid_name_04.csv", index=False, sep=',',mode="w", columns=col)

    return
'''
    columns = ["project_id", "species"]
    dataFrame = pd.DataFrame({'project_id': prj_ids, 'species': species})
    # dataFrame.to_csv("./data/test_02.csv", index=False, sep=',',columns=columns)

    file = open("./data/species_name_03", "a+", encoding='utf-8')
    keyList = species_dict.keys()
    for key in keyList:
        # value = species_dict.get(key)
        s = "\"" + key + "\""
        file.write(key + '\n')
    file.close()
'''

if __name__ == '__main__':
    Get_species()




