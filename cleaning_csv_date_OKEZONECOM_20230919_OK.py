# Clean the csv column and convert into a standard date type

# ---------
#  LIBRARY
# ---------

import pandas as pd
import datetime
import re
import os

# -----------
#  PARAMETER
# -----------

# news_portal = 'CNNINDONESIACOM'
# news_portal = 'KUMPARANCOM'
# news_portal = 'METROTVNEWSCOM-MEDCOMID'
# news_portal = 'OKEZONECOM'
# news_portal = 'TRIBUNNEWSCOM-GABUNG'
news_portal = 'TVONENEWSCOM-VIVACOID'
filename = (f'scraped_news_page_{news_portal}.csv')
date_list = []
new_date_list = []
text_to_remove_list = ['Kompas.com',
                       ',',
                       ' WIB',
                       'Jumat',
                       "Jum'at",
                       'Sabtu',
                       'Minggu',
                       'Senin',
                       'Selasa',
                       'Rabu',
                       'Kamis',
                       ' -',
                       '/',
                       # 'Annisa ayu artanti',
                       # ' • ',
                       # 'Antara',
                       # 'Husen Miftahudin',
                       # 'Eko Nordiansyah',
                       # 'Ilham wibowo',
                       # 'Insi Nantika Jelita',
                       # 'Irene Harty',
                       # 'Dian Ihsan Siregar',
                       # 'Meilikhah',
                       # 'Putri Rosmala',
                       'Diperbarui ']

# ----------
#  FUNCTION
# ----------

# Read the csv file
def read_csv(the_csv):
    global df
    df = pd.read_csv(the_csv)

# Make the date list
def make_date_list():
    global date_list
    date_list = df['news_date'].tolist()

# Get the text to remove
def get_text_to_remove(input_text_to_remove):
    regex = "[A-Za-z ]+ • "
    matches = re.findall(regex, input_text_to_remove)
    for match in matches:
        print(f'get text to remove: {match}')
        text_to_remove_list.append(match)

# Remove and replace texts with a space
def replace_text(text, text_list):
  """Replaces all text from the list a space."""
  #return text.replace('\n', ' ')
  text = str(text)
  # print(text)
  # print(text_list)
  # text = text.replace(' Oktober ', '/10/')
  return text.replace(text_list, '')

# Remove time from the date
def remove_time(text):
  """Replaces all occurrences of a time string with a replacement."""
  regex = "[0-9]+:[0-9]{2}"
  matches = re.findall(regex, text)
  for match in matches:
    text = text.replace(match, '')
  return text

# Convert string to date
def convert_str_to_date(str_date):
    date_format = "%d %m %Y" #For Kompas.com "%d/%m/%Y", CNNIndonesia.com "%d %m %Y"
    date = datetime.datetime.strptime(str_date, date_format)
    # try:
    #     date_format = "%d %m %Y"
    #     date = datetime.datetime.strptime(str_date, date_format)
    # except:
    #     pass
    # print(date)
    return date

# Convert month to number
def month_to_num(str_month):
    regex = '[ ]{1}[A-Z]{1}[a-z]+[ ]{1}' #'[ ]{1}[A-Z]{1}[a-z]{2}[ ]{1}'
    matches = re.findall(regex, str_month)
    for match in matches:
        match = match.strip()
        # print(match)
        num_month = ''
        if match == 'Jan' or match == 'Januari':
            num_month = '01'
        elif match == 'Feb' or match == 'Februari':
            num_month = '02'
        elif match == 'Mar' or match == 'Maret':
            num_month = '03'
        elif match == 'Apr' or match == 'April':
            num_month = '04'
        elif match == 'Mei':
            num_month = '05'
        elif match == 'Jun' or match == 'Juni':
            num_month = '06'
        elif match == 'Jul' or match == 'Juli':
            num_month = '07'
        elif match == 'Agu' or match == 'Agustus':
            num_month = '08'
        elif match == 'Sep' or match == 'September':
            num_month = '09'
        elif match == 'Okt' or match == 'Oktober':
            num_month = '10'
        elif match == 'Nov' or match == 'November':
            num_month = '11'
        elif match == 'Des' or match == 'Desember':
            num_month = '12'
        # print(num_month)
        str_month = str_month.replace(match, num_month)
        # print(str_month)
    return str_month

# Formatting a datetime
def format_date(date_time):
    format_string = "%d-%b-%Y"
    formatted_datetime = date_time.strftime(format_string)
    return formatted_datetime

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
make_date_list()
print(f'{date_list}\n')
for date in date_list:
    print(date)
    # get_text_to_remove(date)
    for text_to_remove in text_to_remove_list:
        print(f'text to remove: {text_to_remove}')
        new_date = replace_text(date,text_to_remove)
        print(f'new date after text removal: {new_date}')
        date = new_date
    # print(new_date)
    new_date = remove_time(new_date)
    # print(new_date)
    new_date = month_to_num(new_date)
    # print(new_date)
    new_date = new_date.strip()
    print(new_date)
    new_date = convert_str_to_date(new_date)
    # print(new_date)
    new_date = format_date(new_date)
    print(f'new formatted date: {new_date}')
    new_date_list.append(new_date)
# print(f'{new_date_list}\n')
# print(df)
df["new_news_date"] = new_date_list
# print(df)
delete_file_if_exist(filename)
write_link_file(filename)