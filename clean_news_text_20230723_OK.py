# Remove all the new lines and replace with spaces

# ---------
#  LIBRARY
# ---------

import pandas as pd
import os


# -----------
#  PARAMETER
# -----------

# news_portal = 'CNNINDONESIACOM'
# news_portal = 'KUMPARANCOM'
# news_portal = 'LIPUTAN6COM'
# news_portal = 'METROTVNEWSCOM-MEDCOMID'
# news_portal = 'OKEZONECOM'
# news_portal = 'TRIBUNNEWSCOM-GABUNG'
news_portal = 'CNNINDONESIACOM'
# filename = 'scraped_news_page_DETIKCOM.csv'
filename = (f'scraped_news_page_{news_portal}.csv')
title_list = []
text_list = []
new_text_list = []

# ----------
#  FUNCTION
# ----------

# Read the csv file
def read_csv(the_csv):
    global df
    df = pd.read_csv(the_csv)

# Make the text list
def make_text_list():
    global title_list
    global text_list
    title_list = df['news_title'].tolist()
    text_list = df['news_text'].tolist()

# Remove and replace newlines with a space
def replace_newline(text):
  return text.replace('\n', ' ')

# Check if the file exist
def delete_file_if_exist(the_file):
    if os.path.exists(the_file):
        os.remove(the_file)

# Write links to a file
def write_link_file(the_file):
    # print(len(news_index_num))
    # print(len(news_links))
    # print(len(news_titles))
    # print(len(news_authors))
    # print(len(news_dates))
    # print(len(news_texts))
    df.to_csv(the_file, index=False, sep=",")


# ---------
#  PROCESS
# ---------

read_csv(filename)
make_text_list()
text_list = [ x + ' ' + y for x,y in zip(title_list, text_list)]
print(text_list)
for text in text_list:
    # print(f'{text}\n')
    text = replace_newline(text)
    print(f'new text: {text}\n')
    new_text_list.append(text)
df["new_news_text"] = new_text_list
delete_file_if_exist(filename)
write_link_file(filename)