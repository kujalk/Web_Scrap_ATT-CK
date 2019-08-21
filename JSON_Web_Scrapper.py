#Developer - K.Janarthanan
#Date - 20-8-2019
#Purpose - To retrieve attack techniques used in the attack mentioned in MITRE ATT&CK


'''
This is how JSON data look like
{
'Attack':''
'Information':''
'Techniques_Used':['','','']
}
'''

import requests
from bs4 import BeautifulSoup
import json

software_url ="https://attack.mitre.org/software/"
page= requests.get(software_url)
soup= BeautifulSoup(page.content, 'html.parser')



attack = soup.find('tbody', class_='bg-white')

count=0

for rows in attack.find_all('tr'):
    for columns in rows.find_all('td'):
        
        count+=1
        answer={}
        
        #Info on column 1
        if (count==1):
            attack_name=columns.get_text().strip()
            link_url=columns.find('a')
            answer["URL"]="https://attack.mitre.org"+link_url['href']
            
        #Info on column 3
        if (count==3):
            attack_info=columns.get_text().strip()
            answer["Attack"]=attack_name
            answer["Information"]=attack_info
            
            #Moving to next page and getting the techniques used by attack
            technique_url="https://attack.mitre.org"+link_url['href']
            technique_page=requests.get(technique_url)
            bsoup=BeautifulSoup(technique_page.content, 'html.parser')
            
            techniques=bsoup.find('table', class_='table table-bordered table-light mt-2')
            
            n_count=0
            my_list=[]
            #print("Techniques Used : ")
            for tec in techniques.find_all('td'):
                
                n_count+=1
                
                if(n_count==3):
                    my_list.append(tec.get_text().strip())
                    
                    
                if(n_count==4):
                    n_count=0
                    
            answer["Techniques_Used"]=my_list
            
        if (count==3):
            count=0
            
    
    json_data=json.dumps(answer)
    print ("\n"+json_data)
    
    #Sending data to URL
    
    api_url="http://193.168.3.194:4300/data"
    headers={'Content-type': 'application/json','Accept': 'text/plain'}
    r=requests.post(api_url,data=json_data,headers=headers)
    print("\nData send")
    
print ("Everything finished!!!")