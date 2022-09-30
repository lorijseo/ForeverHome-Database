from bs4 import BeautifulSoup
import requests

import pandas as pd

# get url and save as html
url = "https://github.com/topics"
response = requests.get(url)  # checks internet speed, if url is correct, if we can access the page
# print(response)
data = response.text  # text: sees url in bytes of memory, content: sees url with unicode
parsed_doc = BeautifulSoup(data, 'html.parser')
with open('website.html', 'w', encoding='utf-8') as f:  # must add encoding
    f.write(data)  # opens html as local hosts

title_selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
topic_title_tags = parsed_doc.find_all('p', {'class': title_selection_class})  # same thing as class_= selection_class

# obtain list of topics in a list
topic_titles = []
for tag in topic_title_tags:
    topic_titles.append(tag.text)
# print(topic_titles)


description_selection_class = 'f5 color-fg-muted mb-0 mt-1'
topic_description_tags = parsed_doc.find_all('p', {'class': description_selection_class})
# print(topic_description_tags[:5])

# list of descriptions
topic_description = []
for tag in topic_description_tags:
    topic_description.append(tag.text.strip())  # removes whitespace and next line character before and after
# print(topic_description)

topic_title_tag0 = topic_title_tags[0]  # use index to get first url title tag

# list of urls
base_url = "http://github.com"
topic_urls = []
for tag in topic_title_tags:
    topic_urls.append(base_url + tag.parent.get('href'))

# print(topic_urls)

# creates spreadsheet given dictionary
topics_dict = {
    'title': topic_titles,
    'url': topic_urls,
    'description': topic_description,
    'url again': topic_urls  # it doesn't save the last data into csv??
}
topics_df = pd.DataFrame(topics_dict)  # automatically includes row num
# print(topics_df)

# save as csv
topics_df.to_csv('topics.csv')

# next page - redo the steps from beginning
topic_page_url = topic_urls[0]
response = requests.get(topic_page_url)
data_url = response.text
parsed_url = BeautifulSoup(data_url, 'html.parser')

with open('url.html', 'w', encoding='utf-8') as f:
    f.write(data_url)

# if there is no class, look for a parent with a class
h3_selection_class = 'f3 color-fg-muted text-normal lh-condensed'
repo_tag = parsed_url.find_all('h3', {'class': h3_selection_class})  # get all the h3 tags
a_tag = repo_tag[0].find_all('a')  # get all the a tags in the first h3 tag
# print(a_tag[0].text.strip())                # get the first a tag and grab the text
url_tag = a_tag[0].get('href')  # get url
# print(base_url + url_tag)                   # print url

star_selection_class = 'Counter js-social-count'
star_tags = parsed_url.find_all('span', {'class': star_selection_class})
star_count = star_tags[0].text  # get the first star rating for this page. this is mrdoob's star


def parse_star_count(star_str):
    star_str = star_str.strip()
    if star_str[-1] == 'k':
        star_int = int(float(star_str[:-1]) * 1000)
    else:
        star_int = int(star_str)
    return star_int
