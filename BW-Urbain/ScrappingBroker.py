import requests
from bs4 import BeautifulSoup

def scrape():
    url = 'https://www.kwurbain.ca/en/our-brokers/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    elements = soup.find_all('div', class_="card-body px-0")

    for element in elements:
        name_element = element.find('h4', class_="card-title no-border")
        name = name_element.text.strip()
        print(f"Name: {name}")
        link = name_element['data-href']
        print(f"Link: {link}")
        phone_element = element.find('a', href=True)
        phone = phone_element.text.strip()
        print(f"Phone: {phone}")
        print()

    print(f"Elements : {len(elements)}")


if __name__ == '__main__':
    scrape()
