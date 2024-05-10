# Get all the news links from Google search results for KOMPAS.com

'''
The process:
------------
1. Open the page
------------
'''

# ---------
#  LIBRARY
# ---------
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
import re



# -----------
#  PARAMETER
# -----------

news_portal = "KOMPASCOM"
webpage = 'https://www.google.com/search?hl=en&as_q=investasi+pariwisata&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=kompas.com&as_occt=title&as_filetype=&tbs='
# news_portal = "DETIKCOM"
# webpage = 'https://www.google.com/search?q=allintitle%3A+investasi+pariwisata+site%3Adetik.com&lr=&sca_esv=558984878&hl=en&as_qdr=all&biw=1536&bih=747&ei=ipLkZO6_Lbru4-EPuIiEuAI&ved=0ahUKEwjurLboi_CAAxU69zgGHTgEAScQ4dUDCA8&uact=5&oq=allintitle%3A+investasi+pariwisata+site%3Adetik.com&gs_lp=Egxnd3Mtd2l6LXNlcnAiL2FsbGludGl0bGU6IGludmVzdGFzaSBwYXJpd2lzYXRhIHNpdGU6ZGV0aWsuY29tSJ8PUPAFWK8KcAF4AJABAJgBZKABugKqAQM0LjG4AQPIAQD4AQHiAwQYASBBiAYB&sclient=gws-wiz-serp'
# news_portal = "CNNINDONESIACOM"
# webpage = 'https://www.google.com/search?hl=en&as_q=investasi+pariwisata&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=cnnindonesia.com&as_occt=title&as_filetype=&tbs='
# news_portal = "TRIBUNNEWSCOM"
# webpage = 'https://www.google.com/search?hl=en&as_q=investasi+pariwisata&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=tribunnews.com&as_occt=title&as_filetype=&tbs='
# news_portal = "TVONENEWSCOM-VIVACOID"
# webpage = 'https://www.google.com/search?q=allintitle%3A+investasi+pariwisata+site%3Aviva.co.id&lr=&sca_esv=559325667&hl=en&as_qdr=all&sxsrf=AB5stBj9RrArrfcF81tw-UCLauSszyDnLA%3A1692775028563&ei=dLLlZMDzId684-EPnf62kA4&ved=0ahUKEwjA_YuynvKAAxVe3jgGHR2_DeIQ4dUDCBA&oq=allintitle%3A+investasi+pariwisata+site%3Aviva.co.id&gs_lp=Egxnd3Mtd2l6LXNlcnAiMGFsbGludGl0bGU6IGludmVzdGFzaSBwYXJpd2lzYXRhIHNpdGU6dml2YS5jby5pZEgAUABYAHAAeACQAQCYAQCgAQCqAQC4AQzIAQDiAwQYACBB&sclient=gws-wiz-serp#ip=1'
# news_portal = "METROTVNEWSCOM-MEDCOMID"
# webpage = 'https://www.google.com/search?hl=en&as_q=investasi+pariwisata&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=medcom.id&as_occt=title&as_filetype=&tbs=#ip=1'
# news_portal = "LIPUTAN6COM"
# webpage = 'https://www.google.com/search?q=allintitle%3A+investasi+pariwisata+site%3Aliputan6.com&lr=&sca_esv=559325667&hl=en&as_qdr=all&sxsrf=AB5stBgfJrc9dzhBV5JWZaTJ6bBC-n6Xsw%3A1692775042096&ei=grLlZLGzBZ7w4-EP55GDGA&ved=0ahUKEwix_MW4nvKAAxUe-DgGHefIAAMQ4dUDCBA&uact=5&oq=allintitle%3A+investasi+pariwisata+site%3Aliputan6.com&gs_lp=Egxnd3Mtd2l6LXNlcnAiMmFsbGludGl0bGU6IGludmVzdGFzaSBwYXJpd2lzYXRhIHNpdGU6bGlwdXRhbjYuY29tSMWLBVCNgAVYp4MFcAJ4AJABAJgBiwGgAa8CqgEDMS4yuAEDyAEA-AEB-AECwgIFECEYoAHiAwQYASBBiAYB&sclient=gws-wiz-serp#ip=1'
# news_portal = "OKEZONECOM"
# webpage = 'https://www.google.com/search?hl=en&as_q=investasi+pariwisata&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=okezone.com&as_occt=title&as_filetype=&tbs='
# news_portal = "KUMPARANCOM"
# webpage = 'https://www.google.com/search?hl=en&as_q=investasi+pariwisata&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=kumparan.com&as_occt=title&as_filetype=&tbs='
# news_portal = "TEMPOCO"
# webpage = 'https://www.google.com/search?hl=en&as_q=investasi+pariwisata&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=tempo.co&as_occt=title&as_filetype=&tbs='

chromedriver_path = "C:\\Users\\lenovo\\Downloads\\chromedriver\\chromedriver.exe"
chrome_service = Service(chromedriver_path)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--user-data-dir=C:\\Users\\lenovo\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
driver = uc.Chrome(driver_executable_path=chromedriver_path, service=chrome_service, options=chrome_options)
# driver = webdriver.Chrome(service=chrome_service)

wait_time = 1
number_of_pages = 1 # Change the number of pages to scrape
output_file_name = f"scraped_news_links_{news_portal}.csv"
news_index_num = [] # index number in the file
news_links = []

# ----------
#  FUNCTION
# ----------

# Get the links
news_num = 1
def get_link():
    global news_num
    # containers = driver.find_element(By.ID, 'result-stats')
    containers = driver.find_elements(By.CLASS_NAME, 'yuRUbf')
    # yuRUbf
    # MjjYud
    for container in containers:
        # try:
        link = container.find_element(By.TAG_NAME, 'a').get_attribute('href')
        print(news_num)
        print(link)
        news_index_num.append(news_num)
        news_num += 1
        news_links.append(link)
        # except:
        #     pass

# Checking the next button exist
def is_next_button_exist():
    try:
        next_button = driver.find_element(By.ID, 'pnnext')
    except:
        next_button = ''
        print("\nThe next button doesn't exist or this is the last page.")
    return next_button

# Click the next page link
def next_button_click(button):
    button.click()

# Sleep process
def sleep(sleep_time):
    time.sleep(sleep_time)

# Scroll the page to the bottom
def scroll_page():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # driver.execute_script('window.stop();')
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        else:
            last_height = new_height

# Write links to a file
def write_link_file(the_file):
    df_news_titles = pd.DataFrame({"No.": news_index_num, "news_link": news_links})
    df_news_titles.to_csv(the_file, index=False)

# Check if the file exist
def delete_file_if_exist(the_file):
    if os.path.exists(the_file):
        os.remove(the_file)

# Check and solve the CAPTCHA before continue
def check_captcha():
    captcha_container = driver.find_element(By.TAG_NAME, 'body').text
    captcha_pattern = re.compile('detected unusual traffic')
    captcha_matched = captcha_pattern.search(captcha_container)
    if str(captcha_matched) != 'None':
        input("\nSolve the CAPTCHA and press ENTER to continue.")
    # else:
    #     print("\nThis is not a CAPTCHA page. Press ENTER to continue.")

# ---------
#  PROCESS
# ---------
if __name__=='__main__':
    driver.get(webpage)
    sleep(wait_time)
    driver.maximize_window()
    check_captcha()
    scroll_page()
    input("Press ENTER to continue")
    page_num = 1
    while page_num < (number_of_pages + 1):
        sleep(wait_time)
        check_captcha()
        scroll_page()
        print(f"page: {page_num}")
        get_link()
        button = is_next_button_exist()
        try:
            next_button_click(button)
        except:
            pass
        page_num += 1
    input("Press ENTER to continue")
    driver.quit()
    delete_file_if_exist(output_file_name)
    write_link_file(output_file_name)