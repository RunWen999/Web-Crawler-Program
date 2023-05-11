import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
output_directory = "pdf_downloads"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

url = "https://www.fda.gov/regulatory-information/search-fda-guidance-documents"
base_url = "https://www.fda.gov"

driver = webdriver.Chrome(executable_path = 'chromedriver')
driver.get('https://www.fda.gov/regulatory-information/search-fda-guidance-documents')
driver.execute_script('window.scrollTo(0, document.body.scrollHeight) ;')
time.sleep(3)

text = driver.page_source


soup = BeautifulSoup(text,'lxml')
pdf_list_odd = []
pdf_name_odd = []
pdf_list_even = []
pdf_names_even = []
tt = soup.findAll('tr', {'class' : 'odd'})
tt_even = soup.findAll('tr',{'class':'even'})

for te in tt_even:
    for a_even in te.findAll('a'):
        href_even = a_even.get('href')
        pdf_link_even = ''
        pdf_name_even = ''
        if href_even.startswith('/media/'):
            pdf_link_even = href_even
            pdf_list_even.append(pdf_link_even)
        if href_even.startswith('/regulatory'):
            pdf_name_even = a_even.text.strip()
            pdf_names_even.append(pdf_name_even)

for t in tt:
    for a in t.findAll('a'):
        href = a.get('href')
        pdf_link = ''
        pdf_name = ''
        if href.startswith('/media/'):
            pdf_link = href
            pdf_list_odd.append(pdf_link)
        if href.startswith('/regulatory'):
            pdf_name = a.text.strip()
            pdf_name_odd.append(pdf_name)

for i in range(len(pdf_list_odd)):
    full_url = base_url + pdf_list_odd[i]
    try:
        # get the PDF file content from the URL
        response = requests.get(full_url)
        # save the PDF file with the desired name in the pdf_downloads folder
        with open('pdf_downloads/{}.pdf'.format(pdf_name_odd[i][:100]), 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f"Error downloading {pdf_name_odd[i]}: {e}")

for i in range(len(pdf_list_even)):
    full_url_even = base_url + pdf_list_even[i]
    try:
        # get the PDF file content from the URL
        response_even = requests.get(full_url_even)
        # save the PDF file with the desired name in the pdf_downloads folder
        with open('pdf_downloads/{}.pdf'.format(pdf_names_even[i][:100]), 'wb') as f:
            f.write(response_even.content)
    except Exception as e:
        print(f"Error downloading {pdf_names_even[i]}: {e}")





