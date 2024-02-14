import requests
from bs4 import BeautifulSoup

def properties():
    url = "https://www.kwurbain.ca/en/listings/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    elements = soup.find_all('div', class_="card-body")

    for element in elements:
        address_element = element.find('h5', class_='card-body')
        address = address_element.text.strip()
        print(f"Address: {address}")

        # price_element = element.find('div', class_='card-title').find('span')
        # price = price_element.text.strip()
        #
        # location_element = element.find('h6', class_='card-subtitle')
        # location = location_element.text.strip()
        #
        # mls_element = element.find('div', class_='card-footer')
        # mls = mls_element.text.strip().split(':')[1].strip()
        #
        # print(f"Price: {price}")
        # print(f"Location: {location}")
        # print(f"MLS: {mls}")
        print()

        print(f"Elements : {len(elements)}")



if __name__ == '__main__':
    properties()