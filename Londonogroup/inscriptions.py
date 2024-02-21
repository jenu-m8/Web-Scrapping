import requests
from bs4 import BeautifulSoup
import json


def properties():
    properties_list = []

    start_page = 1
    end_page = 29
    for page_number in range(start_page, end_page + 1):
        url = f'https://www.londonogroup.com/property/search.php?id=&district=any&prop_type=any&broker=any&project=any&price_range=any&sales=1&rentals=1&subSearch=submit&page={page_number}&sort=recent'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        elements = soup.find_all('a', class_="project-item")

        for element in elements:
            type_price_element = element.find_all('div', class_='title')
            for type_element in type_price_element:
                if type_element.text != '':
                    type_price_text = type_element.text.strip()
            try:
                title, price = type_price_text.split(': ', 1)
            except ValueError:
                title = type_price_text
                price = None
            desc_element = element.find('div', class_='desc')
            sold_element = element.find('div', class_='tag')

            desc_text = desc_element.get_text(separator='<br>').strip()
            address, location, centrish_number = desc_text.split('<br>')

            sold = False
            if sold_element and sold_element.find('img')['src'] == '/images/en/ic_sold.png':
                sold = True

            property_info = {
                'title': title,
                'price': price.strip() if price else "Price not available",
                'address': address,
                'location': location,
                'centrish_number': centrish_number.split(': ')[-1],
                'sold': sold
            }

            properties_list.append(property_info)

    with open("properties-details.json", "w") as json_file:
        json.dump(properties_list, json_file, indent=4)

    print(f"Number of properties: {len(properties_list)}")


if __name__ == '__main__':
    properties()
