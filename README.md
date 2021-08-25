# ORCID
ElementTree library is used to parse the .xml ORCID profiles .

The unique Function returns unique values (dates) in a list.

The rootInfo Function receives the root extracted by the ElemenTree library and the desired root number. The function returns a dictionary containing first created date, last modified date and number of date modifications for each subcategory of the ORCID profile roots (People and Activity). 

hisrootInfo is also used to extract first created date, last modified date and number of date modifications for the History section of the ORCID profile.

The latest_affiliation Function receives the root of the .xml file and returns the most recent affiliation of the author. 

The main Function receives the .xml file path and returns a dataframe with the ORCID ID number of the author (profile), first created date, last modified date and the frequncy of date modifications for each subcategory of main categories (History, People and Activity) in a date.csv file. 
Also, latest affiliation of authors are saved in another file (affiliation.csv) with their ORCID ID. 
