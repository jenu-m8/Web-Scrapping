import requests
from bs4 import BeautifulSoup


def properties():
    url = 'https://www.kwurbain.ca/inscriptions'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    elements = soup.find_all('div', class_='card-body')

    for element in elements:
        name_element = element.find('h5')
        name = name_element.text.strip()
        print(f"Name: {name}")

        price_element = element.find('span')
        price = price_element.text.strip()
        print(f"Price: {price}")

        location_element = element.find('h6', class_='card-subtitle')
        location = location_element.text.strip()
        print(f"Location: {location}")

        icons = element.find_all('div', class_='icon')
        if len(icons) >= 3:
            bedrooms = icons[0].text.strip()
            bathrooms = icons[1].text.strip()
            size = icons[2].text.strip()
            print(f"Bedrooms: {bedrooms}, Bathrooms: {bathrooms}, Size: {size}")
        else:
            print("Bedrooms, Bathrooms, or Size not found")

        print()

    print(f"Number of properties: {len(elements)}")


if __name__ == '__main__':
    properties()
