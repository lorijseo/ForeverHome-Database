from bs4 import BeautifulSoup
import requests
import pandas as pd
import json


def get_page(url):
    """returns parsed html page given url"""
    response = requests.get(url)
    data = response.text
    parsed_page = BeautifulSoup(data, 'html.parser')
    return parsed_page


def get_name(parsed_doc, num):
    """returns name of dog given parsed page and index number"""
    name_class = 'font-bold truncate truncate-15 text-blue text-h4 leading-h5 tablet:' \
                 'leading-h4-sm name tablet:truncate-24'
    get_name_tag = parsed_doc.find_all('p', {'class': name_class})
    for tag in get_name_tag[num]:
        return tag.text.strip()


def get_breed(parsed_doc, num):
    """returns breed of dog given parsed page and index number"""
    breed_class = 'font-bold truncate breed text-h5 leading-h5-sm mb-15 truncate-15 tablet:mb-10 tablet:truncate-24'
    get_breed_tag = parsed_doc.find_all('p', {'class': breed_class})

    for tag in get_breed_tag[num]:
        return tag.text.strip()


def get_description(parsed_doc, num):
    """returns description of dog given parsed page and index number"""
    description_class = 'flex flex-wrap'
    get_description_tag = parsed_doc.find_all('div', {'class': description_class})

    dog_descriptions_list = []
    for tags in get_description_tag[num]:
        description = tags.text.split(',')
        for ele in description:
            ele = ele.strip()
            if ele != '':
                dog_descriptions_list.append(ele)

    return dog_descriptions_list


def get_location(parsed_doc, num):
    """returns location of dog given parsed page and index number"""
    location_class = 'mt-5'
    get_location_tag = parsed_doc.find_all('div', {'class': location_class})
    for tags in get_location_tag[:num]:
        if tags != '':
            return tags.text.strip()
        return "NA"


def get_next_page(parsed_doc, page_num):
    """returns url of the next page given parsed page and index number"""
    next_page_class = 'ml-5 pagination-arrow desktop:h-40 desktop:w-40 desktop:ml-20'
    get_page_tag = parsed_doc.find_all('a', {'class': next_page_class})
    for tag in get_page_tag:
        next_url = tag.get('href')
        return next_url[:-1] + str(page_num)


def scrape_web(home_page):
    """returns list of dictionaries with dog's profile given url"""
    total_dog_list = []

    for pages in range(1, 5):
        doc = get_page(home_page)
        if pages != 1:
            doc = get_page(get_next_page(doc, pages))
        for num in range(0, 8):
            dog_dict = {
                'Name': get_name(doc, num),
                'Breed': get_breed(doc, num),
                'Gender': get_description(doc, num)[0],
                'Age Info': get_description(doc, num)[1],
                'Location': get_location(doc, num),
                'Empty': get_location(doc, num)
            }
            total_dog_list.append(dog_dict)

    return total_dog_list


def write_csv(website, name):
    """given a scraped website, saves all data as csv file"""
    dogs_df = pd.DataFrame(website)
    custom_url = name + '.csv'
    dogs_df.to_csv(custom_url)


def write_json(website, name):
    """given a scraped website, saves all data as json file"""
    custom_url = name + '.json'
    with open(custom_url, 'w') as f:
        json.dump(website, f)


# Main page
main_url = 'https://www.adoptapet.com/pet-search?radius=50&postalCode=90024&speciesId=1'

# Intro
print("Find your forever friend")

# Menu Option
print("What type of forever friend are you looking for?")
print("1. Dog \n2. Cat \n3. Rabbit \n4. Hamster/Guinea Pig \n5. Bird/Chicken/Goose \n6. Horse \n7. Turtle \n8. Pig")
animal_type = input('Input the corresponding number to choose: ')

# First filter: Specific animal page
type_url = main_url[:-1] + str(animal_type)


# Save data into file decided by user
print("How would you like to save your file as? \n1. CSV \n2. JSON")
file_type = input("Input the corresponding number to choose: ")

if file_type == '1':
    name_csv = input('Save CSV file as: ')
    write_csv(scrape_web(type_url), name_csv)
elif file_type == '2':
    name_json = input('Save JSON file as: ')
    write_json(scrape_web(main_url), name_json)
else:
    print("Please choose a number from the menu options.")
