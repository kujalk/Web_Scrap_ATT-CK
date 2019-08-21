import requests
from bs4 import BeautifulSoup

software_url ="https://attack.mitre.org/software/"
page= requests.get(software_url)
soup= BeautifulSoup(page.content, 'html.parser')



attack = soup.find('tbody', class_='bg-white')

count=0

for rows in attack.find_all('tr'):
    for columns in rows.find_all('td'):
        
        count+=1
        
        #Info on column 1
        if (count==1):
            attack_name=columns.get_text().strip()
            link_url=columns.find('a')
            print("\nURL is : https://attack.mitre.org"+link_url['href'])
            
        #Info on column 3
        if (count==3):
            attack_info=columns.get_text().strip()
            print ("Attack : "+attack_name+"\nInformation : "+attack_info+"\n")
            
            #Moving to next page and getting the techniques used by attack
            technique_url="https://attack.mitre.org"+link_url['href']
            technique_page=requests.get(technique_url)
            bsoup=BeautifulSoup(technique_page.content, 'html.parser')
            
            techniques=bsoup.find('table', class_='table table-bordered table-light mt-2')
            
            n_count=0
            print("Techniques Used : ")
            for tec in techniques.find_all('td'):
                
                n_count+=1
                
                if(n_count==3):
                    print(" - "+tec.get_text().strip())
                    
                if(n_count==4):
                    n_count=0
            
        if (count==3):
            count=0