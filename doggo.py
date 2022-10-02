from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.adoptapet.com/pet-search?radius=50&postalCode=90024&speciesId=1'
response = requests.get(url)

data = response.text
parsed_doc = BeautifulSoup(data, 'html.parser')

# fetch dog names
# DEBUG: name - location
# DEBUG: name - bonded - location
name_class = 'font-bold truncate truncate-15 text-blue text-h4 leading-h5 tablet:leading-h4-sm name tablet:truncate-24'
get_name_tag = parsed_doc.find_all('p', {'class': name_class})
for tag in get_name_tag:
    print(tag.text.strip())


# fetch dog breed

breed_class = 'font-bold truncate breed text-h5 leading-h5-sm mb-15 truncate-15 tablet:mb-10 tablet:truncate-24'
get_breed_tag = parsed_doc.find_all('p', {'class': breed_class})
breed_list = []

for tag in get_breed_tag:
    print(tag.text.strip())

# obtains list of descriptions for dog
description_class = 'flex flex-wrap'
get_description_tag = parsed_doc.find_all('div', {'class': description_class})

description_list = []

for tags in get_description_tag[0]:
    description = tags.text.split(',')
    for ele in description:
        ele = ele.strip()
        if ele != '':
            description_list.append(ele)

# print(description_list) # DEBUG

location_class = 'mt-5'
get_location_tag = parsed_doc.find_all('div', {'class': location_class})
for tags in get_location_tag[:5]:
    print(tags.text.strip())


# next page
next_page_class = 'ml-5 pagination-arrow desktop:h-40 desktop:w-40 desktop:ml-20'
get_page_tag = parsed_doc.find_all('a', {'class': next_page_class})
next_page_list = []
for tag in get_page_tag:
    next_page = next_page_list.append(tag.get('href'))


# create next page with different page number
page = next_page_list[0]
print(page[:-1]+"3")




