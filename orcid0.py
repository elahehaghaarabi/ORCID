import pandas as pd
import numpy as np
from xml.etree import ElementTree as ET
from lxml import etree
import re
import datetime
from datetime import *
from dateutil import parser
import pytz
import iso8601
from time import strftime
from dateutil.parser import parse
from pathlib import Path
import os.path



#count unique dates
def unique(list):
    unique_list = []
    for x in list:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def rootInfo(root, root_number):
    dict={}
    k=0
    l=0
    first_created_date = date.today().isoformat()
    last_modified_date =datetime(1000, 1, 1).isoformat()
    modification_count = 0
    # number of unique date modifications for People
    dates=[]
    dates = root[root_number].findall('.//{http://www.orcid.org/ns/common}last-modified-date')
    dates = list(g.text for g in dates)
    dates = list(parse(d).date() for d in dates)
    total_modification_count = len(unique(dates))
        
    for x in root[root_number]:
        root_name = re.sub(r"\s*{.*}\s*", " ", root[root_number].tag)
        dict[root_name +'_lmd'] = "N/A"
        dict[root_name +'_cd'] = "N/A"

        if ((x.tag == "{http://www.orcid.org/ns/common}created-date")  & (x.text!=None)):
           if (x.text < first_created_date):
               first_created_date = x.text
               dict[root_name +'_cd'] = first_created_date
           else:
               first_created_date = date.today().isoformat()

        if (x.tag == "{http://www.orcid.org/ns/common}last-modified-date"):
            if (x.text > last_modified_date):
                last_modified_date = x.text
                dict[root_name +'_lmd'] = last_modified_date
        dict[root_name+' total_mod_count'] = total_modification_count
        #if ((x.tag == "{http://www.orcid.org/ns/common}created-date") & (x.text!=None)):
        #    if (x.text < first_created_date):
        #        first_created_date = x.text
        #        dict[root_name+'_cd'] = first_created_date
        #if (x.tag == "{http://www.orcid.org/ns/common}last-modified-date"):
        #    if ((iso8601.parse_date(x.text).day) != (iso8601.parse_date(last_modified_date).day)):
        #         modification_count +=1
        #    if (((iso8601.parse_date(x.text).day) == (iso8601.parse_date(last_modified_date).day)) & ((iso8601.parse_date(x.text).month) != (iso8601.parse_date(last_modified_date).month))):
        #        modification_count +=1
        #    if (((iso8601.parse_date(x.text).day) == (iso8601.parse_date(last_modified_date).day)) & ((iso8601.parse_date(x.text).month) == (iso8601.parse_date(last_modified_date).month)) & ((iso8601.parse_date(x.text).year) != (iso8601.parse_date(last_modified_date).year))):
        #        modification_count +=1
        #    if (x.text > last_modified_date):
        #        last_modified_date = x.text
        #        dict[root_name+'_lmd'] = last_modified_date
        #dates=[]
        #dates = root[root_number][0].findall('.//{http://www.orcid.org/ns/common}last-modified-date')
        #dates = list(g.text for g in dates)
        #dict[root_name+'_lmd'] = max(dates, default=0)
        #dates = list(parse(d).date() for d in dates)
        #modification_count = len(unique(dates))
        #dict[root_name+'_lmd_count'] = modification_count

        first_created_date = date.today().isoformat()
        last_modified_date =datetime(1000, 1, 1).isoformat()
        for j in range(1, len(root[root_number]), 1):
            child_name = re.sub(r"\s*{.*}\s*", " ", root[root_number][j].tag)
            #dict[root_name + child_name +'_lmd_count'] = modification_count
            dict[root_name +child_name + '_lmd'] = "N/A"
            dict[root_name + child_name + '_cd'] = "N/A"
            dict[root_name + child_name +'_lmd_count'] = "N/A"
            modification_count = 0
            last_modified_date =datetime(1000, 1, 1).isoformat()
            dates=[]
            dates = root[root_number][j].findall('.//{http://www.orcid.org/ns/common}last-modified-date')
            dates = list(g.text for g in dates)
            dates = list(parse(d).date() for d in dates)
            modification_count = len(unique(dates))
            dict[root_name + child_name +'_lmd_count'] = modification_count
            for x in root[root_number][j]:
                if ((x.tag == "{http://www.orcid.org/ns/common}created-date") & (x.text < first_created_date)):
                    first_created_date = x.text
                    dict[root_name + child_name  +'_cd'] = first_created_date
                else:
                    first_created_date = date.today().isoformat()

                if (x.tag == "{http://www.orcid.org/ns/common}last-modified-date"):
                    if (x.text > last_modified_date):
                        last_modified_date = x.text
                        dict[root_name + child_name  +'_lmd'] = last_modified_date

            for k in range(len(root[root_number][j])):
                for x in root[root_number][j][k]:
                    if  (x.tag == "{http://www.orcid.org/ns/common}created-date"):
                        if((x.text != None) & (x.text < first_created_date)):
                            first_created_date = x.text
                            dict[root_name + child_name +'_cd'] = first_created_date
                    if (x.tag == "{http://www.orcid.org/ns/common}last-modified-date"):
                        
                        if (x.text > last_modified_date):
                            last_modified_date = x.text
                            dict[root_name + child_name +'_lmd'] =last_modified_date
                for l in range(len(root[root_number][j][k])):
                    for x in root[root_number][j][k][l]:
                        if  (x.tag == "{http://www.orcid.org/ns/common}created-date"):
                            if (x.text < first_created_date):
                                first_created_date = x.text
                                dict[root_name + child_name +'_cd'] = first_created_date
                        if (x.tag == "{http://www.orcid.org/ns/common}last-modified-date"):
                            if (x.text > last_modified_date):
                                last_modified_date = x.text
                                dict[root_name + child_name +'_lmd'] = last_modified_date
        return dict
def hisrootInfo(root):
    dates=[]
    dates = root[2].findall('.//{http://www.orcid.org/ns/common}last-modified-date')
    dates = list(g.text for g in dates)
    dates = list(parse(d).date() for d in dates)
    total_modification_count = len(unique(dates))
    his_dict={}
    last_modified_date =datetime(1000, 1, 1).isoformat()
    first_created_date = date.today().isoformat()
    root_name = re.sub(r"\s*{.*}\s*", " ", root[2].tag)
    his_dict[root_name +'_cd'] = "N/A"
    his_dict[root_name +'_lmd'] = "N/A"
    his_dict[root_name +' total_mod_count'] = total_modification_count
    for x in root[2]:
        if ((x.tag == "{http://www.orcid.org/ns/common}created-date") & (x.text < first_created_date)):
            first_created_date = x.text
            his_dict[root_name +'_cd'] = first_created_date
        else:
            first_created_date = date.today().isoformat()

        if (x.tag == "{http://www.orcid.org/ns/common}last-modified-date"):
            if (x.text > last_modified_date):
                last_modified_date = x.text
                his_dict[root_name +'_lmd'] = last_modified_date
    return his_dict

def latest_affiliation(root):
    #aff_dict = {}
    latest_affiliation = "N/A"
    lmd = datetime(1000, 1, 1).isoformat()
    last_modified_date =[]
    for emp in root[4].findall('.//{http://www.orcid.org/ns/activities}employments'):
        for aff in emp.findall('.//{http://www.orcid.org/ns/activities}affiliation-group'):
            for empsum in aff.findall('.//{http://www.orcid.org/ns/employment}employment-summary'):
                for x in empsum.findall("{http://www.orcid.org/ns/common}last-modified-date"):
                    if (x.text > lmd):
                        lmd = x.text
                        affiliation = empsum.findall('.//{http://www.orcid.org/ns/common}name')
                        affiliation = list(g.text for g in affiliation)
                        latest_affiliation = affiliation[0]
    return latest_affiliation



def main(file_path):
    df = pd.read_csv(file_path, header=0, names=['raw_orcid', 'normalized_orcid', 'orcid_file', 'valid_code'])
    df = df[0:40000]
    aff_dict = {}
    history_dict = {}
    person_dict = {}
    act_dict = {}
    res = pd.DataFrame()
    for _, row in df.iterrows():
        if row.valid_code == 1:
            file_path = row.orcid_file
            normalized_orcid = row.normalized_orcid
        else:
            print('valid code error')      

        print(normalized_orcid)
        
        try:
            tree = ET.parse(file_path.replace('\\', '/'))
            root = tree.getroot()
        except:
            valid = 0
            aff_dict [normalized_orcid] = "N/A"
            history_dict = "N/A"
            person_dict = "N/A"
            act_dict = "N/A"
        valid = 1
        aff_dict [normalized_orcid] = "N/A"
        aff_dict[normalized_orcid] = latest_affiliation(root)
        history_dict = hisrootInfo(root)
        person_dict = rootInfo(root, 3)
        act_dict = rootInfo(root, 4)
        data = {}
        for d in (history_dict, person_dict, act_dict): 
            data.update(d)
        df = pd.Series(data).to_frame()
        df = df.T
        df ['orcid_id'] = normalized_orcid
        df ['valid'] = valid
        df.set_index('orcid_id', inplace = True)
        res = pd.concat([df, res])
        res.to_csv("dates_0_40.csv")
        #print(res)
        df_affiliation = pd.Series(aff_dict).to_frame()
        df_affiliation.index.name = "orcid_id"
        df_affiliation.columns = ["latest_affiliation"]
        df_affiliation ['valid'] = valid
        df_affiliation.to_csv("affiliation_0_40.csv")
        #df = df.transpose
        #df['orcid_id'] = normalized_orcid        
        #frames = [df, df_dates]
        #df_dates = pd.concat(frames)
    #res.to_csv("dates.csv")
        #dir = '//panfs/pan1/bionlp/lulab/qingyu/elaheh/orcid/orcid_analysis'
        #name = normalized_orcid+'.csv'
        #df_dates.to_csv(dir + '/' + name)
        
  

file_path = '//panfs/pan1/bionlp/lulab/qingyu/pubmed_orcid/010721/cleaned_pmid_orcid/valid_orcid_unique.csv'
main(file_path)


                                

                    



 #his_dict={}
    #string = root[2].tag
    #string = re.sub(r"\s*{.*}\s*", " ", string)
    #his_dict[string] = []
    #pacific = pytz.timezone("US/Pacific")
    #first_created_date = date.today().isoformat()
    #last_modified_date = date.today().isoformat()
    #modification_count = 0
    #for x in root[2]:
    #    if ((x.tag == "{http://www.orcid.org/ns/common}created-date") & (x.text < first_created_date)):
    #        first_created_date = x.text
    #        his_dict[string].append(first_created_date)
    #    if (x.tag == "{http://www.orcid.org/ns/common}last-modified-date"):
    #        modification_count +=1
    #        if (x.text > last_modified_date):
    #            last_modified_date = x.text
    #            his_dict[string].append(last_modified_date)
    #            his_dict[string].append(modification_count)

    

    #act_dict={}
    #j=0
    #k=0
    #l=0
    #n=0
    #for j in range(len(root[4])):
    #    act_dict[re.sub(r"\s*{.*}\s*", " ", root[4][j].tag)] = []
    #    for x in root[4][j]:
    #        if (x.tag == "{http://www.orcid.org/ns/common}created-date"):
    #            act_dict[re.sub(r"\s*{.*}\s*", " ", root[4][j].tag)].append(x.text)
    #            n=n+1
    #        if (x.tag == "{http://www.orcid.org/ns/common}last-modified-date"):
    #            act_dict[re.sub(r"\s*{.*}\s*", " ", root[4][j].tag)].append(x.text)
    #            #print(re.sub(r"\s*{.*}\s*", " ", root[4][j].tag), 'lmd'+x.text)
    #            n=n+1
    #    for k in range(len(root[4][j])):
    #        for x in root[4][j][k]:
    #            if (x.tag == "{http://www.orcid.org/ns/common}created-date"):
    #                act_dict[re.sub(r"\s*{.*}\s*", " ", root[4][j].tag)].append(x.text)
    #                #print(re.sub(r"\s*{.*}\s*", " ", root[4][j].tag), 'cd'+x.text)
    #                n=n+1
    #            if (x.tag == "{http://www.orcid.org/ns/common}last-modified-date"):
    #                act_dict[re.sub(r"\s*{.*}\s*", " ", root[4][j].tag)].append(parser.parse(x.text))
    #        for l in range(len(root[4][j][k])):
    #            for x in root[4][j][k][l]:
    #                if (x.tag == "{http://www.orcid.org/ns/common}created-date"):
    #                    act_dict[re.sub(r"\s*{.*}\s*", " ", root[4][j].tag)].append(parser.parse(x.text))
    #                    #print(re.sub(r"\s*{.*}\s*", " ", root[4][j].tag), 'cd'+x.text)
    #                    n=n+1
    #                if (x.tag == "{http://www.orcid.org/ns/common}last-modified-date"):
    #                    act_dict[re.sub(r"\s*{.*}\s*", " ", root[4][j].tag)].append(parser.parse(x.text))
    #                    #print(re.sub(r"\s*{.*}\s*", " ", root[4][j].tag), 'lmd'+x.text)
    #                    n=n+1
            
    #data = {}
    #for d in (his_dict, person_dict, act_dict): 
    #    data.update(d)
    #df_dates= pd.DataFrame.from_dict(person_dict, orient="index")
    #df_dates.to_csv(normalized_orcid+'.csv')


