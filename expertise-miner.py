import csv
from selenium import webdriver
from retry import retry
import urllib.request
from bs4 import BeautifulSoup
from time import sleep

#----------------
# retry decorator
#----------------
@retry(urllib.error.URLError, tries=4, delay=3, backoff=2)
def urlopen_with_retry(url):
    return urllib.request.urlopen(url)

driver = webdriver.Chrome(executable_path = 'C:\chromedriver.exe')

with open('input.csv', 'r', encoding = 'utf-8') as csvfile:

    csvreader = csv.reader(csvfile, delimiter = '\t', quotechar = '"')

    for row in csvreader:
        staff_id = row[0]
        links = row[1].split(';')
        links = [i.strip() for i in links]
        expertises = []

        for link in links:
            driver.get(link)

            # attempt to extract expertise
            try:
                e = driver.find_element_by_xpath('//*[@id="gsc_prf_int"]')
                expertises_ = e.find_elements_by_tag_name('a')
                expertises_ = [i.text.lower() for i in expertises_]

                for i in expertises_:
                    if i not in expertises:
                        expertises.append(i)
                
            except:
                expertises.append('-NA-')
                
        expertises = '; '.join(expertises)
        print('\t'.join([staff_id, expertises]))
        sleep(10)

driver.close()
driver.quit()
