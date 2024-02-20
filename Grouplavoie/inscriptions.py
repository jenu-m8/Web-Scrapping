import requests
from bs4 import BeautifulSoup
import json


def properties():
    properties_list = []

    url = 'https://groupelavoie.com/en/houses-for-sale/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    elements = soup.find_all('a', class_='c-property-summary wow fadeInUp')

    for element in elements:
        property_info = {}

        price_element = element.find('span', class_='c-property-summary__price')
        property_info['price'] = price_element.text.strip()

        name_element = element.find('span', class_='c-property-summary__name')
        property_info['name'] = name_element.text.strip()

        bathrooms = element.find('i', class_='c-property-summary__bathrooms fa fa-bath')
        if bathrooms:
            bathrooms_text = bathrooms.find_next_sibling('span', class_='c-property-summary__number').get_text(strip=True)
            property_info['bathrooms'] = bathrooms_text
        else:
            property_info['bathrooms'] = "Bathrooms not found"

        bedrooms = element.find('i', class_='c-property-summary__bedrooms fa fa-bed')
        if bedrooms:
            bedrooms_text = bedrooms.find_next_sibling('span', class_='c-property-summary__number').get_text(strip=True)
            property_info['bedrooms'] = bedrooms_text
        else:
            property_info['bedrooms'] = "Bedrooms not found"

        properties_list.append(property_info)

    with open("properties-details.json", "w") as json_file:
        json.dump(properties_list, json_file, indent=4)

    print(f"Number of properties: {len(elements)}")


if __name__ == '__main__':
    properties()
