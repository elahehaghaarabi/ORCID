# ORCID
The XML parsing is done through ElementTree package.

The unique Function returns unique values (dates) in a list.

The rootInfo Function receives the root extracted by the ElemenTree package and desired root number. The function returns a dictionary containing first created date, last modified date and number of date modifications for each subcategory of the ORCID profile. 

hisrootInfo is also used to extract first created date, last modified date and number of date modifications for History section of the ORCID profile.

The latest_affiliation Function receives the root of the xml file and returns the most recent affiliation of the author. 

The main Function receives the data file path and returns a dataframe with the ORCID ID number, first created date, last modified date and frequnce of date modifications in for each subcategory of main categories (History, People and Activity) in a date.csv file. 
Also, latest affiliations of authors are saved in another file (affiliation.csv) with their ORCID ID. 
