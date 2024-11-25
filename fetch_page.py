from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import urllib3

# Login credentials
username = "guadalupe.tunon@gmail.com"
password = "47234228"
page_number = 4193

# Path to the Chrome extension folder
extension_path = "D:\work\python task\Arquivo Nacional\INFDCENBDOIBCACOGKNKJLECLHNJDMFH_1_0_2_0.crx"
# Path to the ChromeDriver executable
chromedriver_path = "D:\chromedriver-win64\chromedriver.exe"

# Set up Chrome options to load the extension
chrome_options = Options()

# Set up the WebDriver with Chrome options
driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

try:
    # Open the login page
    driver.get("https://sian.an.gov.br/sianex/consulta/login-novo-com-cadastro.asp")
    # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # Wait for the login page to load

    # Find and fill in the username and password fields
    driver.find_element(By.ID, "login").send_keys(username)
    driver.find_element(By.ID, "senha").send_keys(password)
    # Find and click the login button
    login_button = driver.find_element(By.ID, "botao_entrar_estilizado")
    input('Continue: ')
    login_button.click()

    input('Waiting...')

    for i in range(page_number):
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

        print("Cookies:")
        print(send_cookie)
        
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
            "ID":"1816403",
            "Dir":"BR DFANBSB V8.MIC, GNC.AAA.64095453",
            "niv":"4"
        }

        url = "https://sian.an.gov.br/sianex/consulta/Pesquisa_Livre_Controle.asp?Dir="
        response = requests.post(url, data=body, headers=headers, verify=False)

        # Save the content to a file
        with open(f"page{i}.html", "w", encoding="utf-8") as file:
            file.write(response.text)
            print("Success")

        next_page = driver.find_element(By.XPATH, "//a[@class='page-link next' and text()='Próximo']")
        next_page.click()
        time.sleep(2)
    # soup = BeautifulSoup(driver.page_source, "html.parser")
    # html = str(soup)
    # with open('result.html', 'w', encoding='utf-8') as file:
    #     file.write(html)

    # Wait for the login process to complete and the page to redirect


finally:
    driver.quit()
