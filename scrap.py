import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import urllib3
import re
import csv
# Login credentials
username = "guadalupe.tunon@gmail.com"
password = "47234228"

# Load the .csv file into a DataFrame
data = pd.read_csv('predata.csv')

# Path to the Chrome extension folder
# Path to the ChromeDriver executable
chromedriver_path = "D:\chromedriver-win64\chromedriver.exe"

# Set up Chrome options to load the extension
options = Options()

# Set up the WebDriver with Chrome options
driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

header = ['Name', 'Age', 'Occupation']
with open('result.csv', mode='w',newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['ID','Dir', 'doc_code','doc_title','doc_date','doc_content','pdf_link','file_name'])

code_pattern = r"<label[^>]*>\s*<i>(.*?)<\/i>\s*<\/label>"           #get code
title_pattern = r"<td class='TdFormClaro'[^>]*>([^<]*)</td>"  # get title
date_pattern_1 = r"<b>Inicial&nbsp;:&nbsp;</b>(\d{1,2}/\d{1,2}/\d{4})"  #get date
date_pattern_2 = r"<b>Inicial&nbsp;:&nbsp;</b>(\d{1,2}/\d{4})"  #get date
date_pattern_3 = r"<b>Inicial&nbsp;:&nbsp;</b>(\d{4})"  #get date
content_pattern = r"<b>3\.1\.1.*?</b>.*?/(\#/.+?)</td>"         # contents 
link_pattern = r"onClick=\"javascript:fjs_Link_download\((.*?)\);\""  
try:
    # Open the login page
    driver.get("https://sian.an.gov.br/sianex/consulta/login-novo-com-cadastro.asp")
    # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # Wait for the login page to load
    time.sleep(2)

    # Find and fill in the username and password fields
    driver.find_element(By.ID, "login").send_keys(username)
    driver.find_element(By.ID, "senha").send_keys(password)
    # Find and click the login button
    login_button = driver.find_element(By.ID, "botao_entrar_estilizado")
    input('Continue: ')
    login_button.click()

    input('Waiting...')
    cnt = 0
    reloading = 0
    for i in range(len(data)):
        cnt = cnt + 1
        next_page = driver.find_element(By.XPATH, "//a[@class='page-link next' and text()='Próximo']")
        if next_page:
            if cnt == 10:
                next_page.click()
                cnt = 0
                reloading = reloading + 1
        else:
            if cnt == 10:
                driver.refresh()
        
        send_cookie=""
        cookies = driver.get_cookies()
        for cookie in cookies:
            if not "_" in cookie["name"]:
                send_cookie+=cookie["name"] +"="+cookie["value"]+";"
            elif cookie["name"]=="TSPD_101_DID":
                send_cookie+=cookie["name"] +"="+cookie["value"]+";"
            else:
                continue
        send_cookie = send_cookie[:-1]
        
        headers = {
            "accept":"*/*",
            "accept-encoding":"gzip, deflate, br, zstd",
            "accept-language":"en-US,en;q=0.9",
            "Cache-Control":"max-age=0",
            "connection":"keep-alive",
            "content-type":"application/x-www-form-urlencoded",
            "cookie":send_cookie,
            "host":"sian.an.gov.br",
            "origin":"https://sian.an.gov.br",
            'sec-ch-ua':'"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile":"?0",
            "sec-ch-ua-platform":"'Windows'",
            "sec-fetch-dest":"empty",
            "sec-fetch-mode":"cors",
            "sec-fetch-site":"same-origin",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
        }

        body = {
            "ID": str(data["ID"][i]),
            "Dir":data["Dir"][i],
            "niv":'4'
        }

        url = "https://sian.an.gov.br/sianex/consulta/Pesquisa_Livre_Controle.asp?Dir="
        response = requests.post(url, data=body, headers=headers, verify=False)
        insert_data =[]

        insert_data.append(data["ID"][i])
        insert_data.append(data["Dir"][i])

        match = re.search(code_pattern, response.text)
        if match:
            precode = match.group(1).strip()
            if "Dossiê" in precode:
                code = precode.replace(" - Dossiê", "")
                insert_data.append(code)
            elif "item" in precode:
                code = precode.replace(" - item", "")
                insert_data.append(code)
            elif "S&eacute;rie" in precode:
                code = precode.replace(" - S&eacute;rie", "")
                insert_data.append(code)
            else:
                insert_data.append(match.group(1).strip())
        else:
            insert_data.append("")

        
        # Perform the search
        match = re.search(title_pattern, response.text)
        if match:
            insert_data.append(match.group(1).strip())  # Strip to remove any leading or trailing whitespace
        else:
            insert_data.append("")

        

        # Perform the search
        match = re.search(date_pattern_1, response.text) or re.search(date_pattern_2, response.text) or re.search(date_pattern_3, response.text)
        if match:
            insert_data.append(match.group(1))
        else:
            insert_data.append("NA")

        
        # Extract the section following <b>3.1.1</b>
        # match = re.search(content_pattern, response.text, re.DOTALL)
        # if match:
        #     insert_data.append(match.group(1).strip())
        # else:
        #     insert_data.append("NA")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the <b> tag with '3.1.1' text
        label = soup.find('b', string="3.1.1 - Especificação do conteúdo")

        # Find the associated table content by navigating from the label
        if label:
            parent_td = label.find_parent('td')
            table = parent_td.find_next('table') if parent_td else None
            content_td = table.find('td', class_='TdFormClaro') if table else None
            content = content_td.get_text(strip=True) if content_td else "Content not found"
            if content:
                insert_data.append(content)
            else:
                insert_data.append("NA")
        else:
            content = "Label '3.1.1' not found"
               #link, file name.
        match = re.findall(link_pattern, response.text)        
        if match:
            rematch =  [part.strip(" '") for part in match[0].split(",")]
            insert_data.append( "http://imagem.sian.an.gov.br/acervo/derivadas/"+rematch[0])
            insert_data.append( rematch[1])
        else:
            insert_data.append("")
        print(insert_data)
        print(reloading)
        with open('result.csv', mode='a',newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(insert_data)
    # Extract and update the cookie
    # if 'Set-Cookie' in response.headers:
    #     # Get new cookie string
    #     new_cookie = response.headers['Set-Cookie']
        
    #     # Extract "TSf172a88f027" from the new cookie
    #     new_ts_value = re.search(r"TSf172a88f027=([^;]+)", new_cookie)
    #     if new_ts_value:
    #         new_ts_value = new_ts_value.group(0)  # Get the full key=value pair
            
    #         # Replace old TSf172a88f027 in the current cookie
    #         cookie_next = re.sub(r"TSf172a88f027=[^;]+", new_ts_value, cookie_first)
    #         print("Updated cookie:", cookie_next)
    #     else:
    #         print("TSf172a88f027 not found in the new cookie.")
    # else:
    #     print("No new cookie received.")

    # # You can now use the updated `current_cookie` for the next request
    # headers["cookie"] = cookie_next
   


finally:
    driver.quit()
