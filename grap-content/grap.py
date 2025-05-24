from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

CHROME_CONFIG={
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.265 Safari/537.36",
    "headless":True,
    "disable_gpu":True,
    "ignore_certificate_errors":True
}

TARGET_CONFIG={
    "naukrigulf":{
        "url":"https://www.naukrigulf.com/top-jobs-by-designation",
        "wait_for":{"by":By.CLASS_NAME,"value":"soft-link"},
        "selectors":{
            "job_title":{"tag":"a","class":"soft-link darker"}
        },
        "max_items":20
    },
    #etc
}

class WebScraper:
    def __init__(self,site_config):
        self.driver=self._init_browser()
        self.config=site_config
    
    def _init_browser(self):
        chrome_options=Options()
        chrome_options.add_argument(f"user-agent={CHROME_CONFIG['user_agent']}")
        if CHROME_CONFIG["headless"]:
            chrome_options.add_argument("--headless")
        if CHROME_CONFIG["disable_gpu"]:
            chrome_options.add_argument("--disable-gpu")
        if  CHROME_CONFIG['ignore_certificate_errors']:
            chrome_options.add_argument("ignore-certificate-errors")

        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  
        service=Service("D:\google chrome\chromedriver-win64\chromedriver.exe")
        return webdriver.Chrome(service=service,options=chrome_options)
    
    def _wait_for_page_load(self):
        WebDriverWait(self.driver,30).until(EC.presence_of_element_located((
            self.config["wait_for"]["by"],
            self.config["wait_for"]["value"]
        )))
    def _get_page_content(self):
        self.driver.get(self.config["url"])
        self._wait_for_page_load()
        return  BeautifulSoup(self.driver.page_source,"html.parser")
    def extract_data(self):
        soup=self._get_page_content()
        max_items=self.config.get("max_items",20) 
        results={}
        for key,selector in self.config["selectors"].items():
            elements=soup.find_all(selector["tag"],class_=selector.get("class"))
            results[key]=[element.text.strip() for element in elements[:max_items]]
        return results
    def close(self):
        self.driver.close()
if  __name__=="__main__":
    scraper = None  # 提前声明
    try:
        scraper=WebScraper(TARGET_CONFIG["naukrigulf"])
        data=scraper.extract_data()
        print("Top of job data:")
        for i,job in enumerate(data["job_title"],start=1):
            print(f"{i}.{job}")
    finally:
        if scraper:
            scraper.close()