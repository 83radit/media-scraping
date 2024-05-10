# Get all the news data from the page

# ---------
#  LIBRARY
# ---------

import pandas as pd
import time
import sys
import os
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# -----------
#  PARAMETER
# -----------

# news_portal = 'CNNINDONESIACOM'
# news_portal = 'KUMPARANCOM'
# news_portal = 'LIPUTAN6COM'
# news_portal = 'METROTVNEWSCOM-MEDCOMID'
# news_portal = 'OKEZONECOM'
# news_portal = 'TEMPOCO'
# news_portal = 'TRIBUNNEWSCOM'
news_portal = 'TVONENEWSCOM-VIVACOID'
filename = (f'scraped_news_links_{news_portal}.csv')
output_file = (f'scraped_news_page_{news_portal}.csv')

news_index_num = [] # index number in the file
news_links = []
news_titles = []
news_authors = []
news_dates = []
news_texts = []
full_text = ''

chromedriver_path = "C:\\Users\\lenovo\\Downloads\\chromedriver\\chromedriver.exe"
chrome_service = Service(chromedriver_path)
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless=new") # headless mode
chrome_options.add_argument("--user-data-dir=C:\\Users\\lenovo\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
driver = uc.Chrome(driver_executable_path=chromedriver_path,
                   service=chrome_service,
                   options=chrome_options)

# ----------
#  FUNCTION
# ----------

# Read the csv file
def read_csv(the_csv):
    global df
    df = pd.read_csv(the_csv)

# Make the link list
def make_link():
    global link_list
    link_list = df['news_link'].tolist()

# Open a webpage from an url in a browser
def open_page(url):
    driver.get(url)

# Scroll the page to the max
def scroll_page():
    previous_height = driver.execute_script("return document.body.scrollHeight")
    total_scroll = 0
    scroll_multiplier = 5
    scroll_counter = 1
    while True:
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight/{scroll_multiplier}*{scroll_counter});")
        scroll_height = driver.execute_script(f"return document.body.scrollHeight/{scroll_multiplier}*{scroll_counter}")
        scroll_counter = scroll_counter + 1
        # total_scroll += scroll_height
        # print(f"scroll height = {scroll_height}")
        # driver.execute_script('window.stop();')
        time.sleep(0.5)
        last_height = driver.execute_script("return document.body.scrollHeight")
        # print(f"last height = {last_height}")
        if previous_height < last_height:
            previous_height = last_height
            scroll_counter = 1
        if scroll_height >= last_height:
            break
        # else:
        #     last_height = new_height

# Pause the process before exit
def pause():
    input("\nPAUSED. Press ENTER to continue.")


# Remove unwanted texts
text_to_remove_list = []

def replace_text(text, text_list):
  """Replaces all text from the list a space."""
  #return text.replace('\n', ' ')
  text = str(text)
  # print(text)
  # print(text_list)
  text = text.replace(text_list, '')
  # return text.replace(text_list, '')
  return text


# Get the news data
def get_news_data():
    # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, title_class)))
    try:
        news_title = driver.find_element(By.CLASS_NAME, 'main-content-title').text
    except:
        pass
    print(news_title)
    news_titles.append(news_title)

    try:
        news_author = driver.find_element(By.CLASS_NAME, 'main-content-author').text
    except:
        pass
    print(news_author)
    news_authors.append(news_author)

    try:
        news_date = driver.find_element(By.CLASS_NAME, 'main-content-date').text
    except:
        pass
    print(news_date)
    news_dates.append(news_date)

# Get the news text
def get_news_text():
    try:
        news_container = driver.find_element(By.CLASS_NAME, 'main-content-detail')
        # print(f"news_container: {news_container.text}")
    except:
        pass
    # dirty_text = news_container.text
    # clean_text = dirty_text
    # for text_to_remove in text_to_remove_list:
    #     # print(f"text to remove: {text_to_remove}")
    #     clean_text = replace_text(clean_text, text_to_remove)
    #     # print(f"clean text: {clean_text}")
    # print(f"clean_text: {clean_text}")
    container = news_container.find_elements(By.TAG_NAME, 'p')
    # print(f'container = {container}')
    # if len(container) == 1:
    #     container.append(driver.find_element(By.CLASS_NAME, 'article-content-body__item-content'))
        # print(f'container = {container.text}')

    for container_text in container: # container[0:-1]
        dirty_text = container_text.text
        # print(f"dirty text: {dirty_text}")
        # global text_to_remove_list
        clean_text = dirty_text
        # print(f'clean text: {clean_text}')
        for text_to_remove in text_to_remove_list:
            # print(f"text to remove: {text_to_remove}")
            clean_text = replace_text(clean_text, text_to_remove)
            # print(f"clean text 1: {clean_text}")
        # print(f"clean text: {clean_text}\n")
        global full_text
        full_text += (f"{clean_text} ")
    #     # soup = BeautifulSoup(news_text, 'html.parser')
    #     # clean_news_text = soup.get_text(strip=True, separator='\n')
    #     print(clean_text)
    # full_text = clean_text
    print(f'full_text: {full_text}')
    news_texts.append(full_text)
    full_text = ''

# Close the browser
def close_page():
    driver.quit()

# Check if the file exist
def delete_file_if_exist(the_file):
    if os.path.exists(the_file):
        os.remove(the_file)

# Write links to a file
def write_link_file(the_file):
    print('news index num: ' + str(len(news_index_num)))
    print('news links: ' + str(len(news_links)))
    print('news titles: ' + str(len(news_titles)))
    print('news authors: ' + str(len(news_authors)))
    print('news dates: ' + str(len(news_dates)))
    print('news texts: ' + str(len(news_texts)))
    df_news_titles = pd.DataFrame({"No.": news_index_num,
                                   "news_link": news_links,
                                   "news_title": news_titles,
                                   "news_author": news_authors,
                                   "news_date": news_dates,
                                   "news_text": news_texts})
    df_news_titles.to_csv(the_file, index=False, sep=",")

next_page_link = ''
# Check if the pagination exit
def is_pagination_exist():
    try:
        pagination = driver.find_element(By.CLASS_NAME, 'pagination').text
        # print(f'pagination: {pagination}')
    except:
        pagination = ''
        # print("\nThe next button doesn't exist or this is the last page.\n")
    return pagination


# ---------
#  PROCESS
# ---------

if __name__=='__main__':
    read_csv(filename)
    make_link()
    news_num = 1
    for link in link_list: # link_list[60:80]: <- for testing smaller samples
        start_time = time.time()
        print(news_num)
        # news_index_num.append(news_num)
        print(link)
        # news_links.append(link)
        open_page(link)
        time.sleep(1)
        driver.maximize_window()
        scroll_page()
        time.sleep(1)

        # list the texts to remove here:
        try:
            text_to_remove_3 = driver.find_elements(By.CLASS_NAME, 'baca')
            for text_inbacajuga in text_to_remove_3:
                text_to_remove_list.append(text_inbacajuga.text.replace("\n", ""))
        except:
            pass
        try:
            text_to_remove_31 = driver.find_elements(By.CLASS_NAME, 'baca')
            for text_inbacajuga in text_to_remove_31:
                text_to_remove_list.append(text_inbacajuga.text)
        except:
            pass
        try:
            text_to_remove_4 = driver.find_elements(By.TAG_NAME, 'strong')
            for text_inbacajuga in text_to_remove_4:
                text_to_remove_list.append(text_inbacajuga.text.replace("\n", ""))
        except:
            pass
        text_to_remove_list.append('Baca juga Berita TribunBatam.id lainnya di Google')
        # text_to_remove_list.append('Baca juga:')
        # text_to_remove_list.append('Selanjutnya:')
        # text_to_remove_list.append('Baca juga Berita TribunBatam.id lainnya di Google')

        if is_pagination_exist() != '':
            # number_of_page = driver.find_element(By.CLASS_NAME, 'paging').find_elements(By.TAG_NAME, 'a')[-1]
            # print(f'number_of_page: {number_of_page.text}')
            try:
                button_selanjutnya = driver.find_elements(By.CLASS_NAME, 'pagination-button')[-1]
            except:
                button_selanjutnya = ''
            while button_selanjutnya.text != 'TAMPILKAN SEMUA':
                next_page_link = button_selanjutnya.get_attribute('href')
                open_page(next_page_link)
                time.sleep(1)
                scroll_page()
                time.sleep(1)
                button_selanjutnya = driver.find_elements(By.CLASS_NAME, 'pagination-button')[-1]
                # print(f'button_selanjutnya: {button_selanjutnya.text}')

            next_page_link = button_selanjutnya.get_attribute('href')
            open_page(next_page_link)
            time.sleep(1)
            scroll_page()
            time.sleep(1)

            # list the texts to remove here:
            try:
                text_to_remove_5 = driver.find_elements(By.CLASS_NAME, 'baca')
                for text_inbacajuga in text_to_remove_5:
                    text_to_remove_list.append(text_inbacajuga.text.replace("\n", ""))
            except:
                pass
            try:
                text_to_remove_51 = driver.find_elements(By.CLASS_NAME, 'baca')
                for text_inbacajuga in text_to_remove_51:
                    text_to_remove_list.append(text_inbacajuga.text)
            except:
                pass
            try:
                text_to_remove_6 = driver.find_elements(By.TAG_NAME, 'strong')
                for text_inbacajuga in text_to_remove_6:
                    text_to_remove_list.append(text_inbacajuga.text.replace("\n", ""))
            except:
                pass

            news_index_num.append(news_num)
            news_links.append(link)
            get_news_data()
            get_news_text()

        else:
            news_index_num.append(news_num)
            news_links.append(link)
            get_news_data()
            get_news_text()

        # get_loading_time(link)
        elapsed_time = time.time() - start_time
        print(f"Page loaded in {elapsed_time:.2f} seconds\n")
        text_to_remove_list = []
        news_num = news_num + 1
        # pause()
        # close_page()

    # pause()
    delete_file_if_exist(output_file)
    print("delete file OK")
    write_link_file(output_file)
    print("write file OK")
    close_page()
    print("close page OK")
    sys.exit()