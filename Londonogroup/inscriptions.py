import requests
from bs4 import BeautifulSoup
import json


def properties():
    global type_price_text, bed_count, bath_count, municipality_tax, school_tax
    properties_list = []

    start_page = 1
    end_page = 1
    start_pos = 1
    end_pos = 1
    for page_number in range(start_page, end_page + 1):
        for pos_number in range(start_pos, end_pos + 1):
            url = f'https://www.londonogroup.com/property/search.php?id=&district=any&prop_type=any&broker=any&project=any&price_range=any&sales=1&rentals=1&subSearch=submit&page={page_number}&sort=recent'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            elements = soup.find_all('a', class_="project-item")

            for element in elements:
                desc_element = element.find('div', class_='desc')
                desc_text = desc_element.get_text(separator='<br>').strip()
                sold_element = element.find('div', class_='tag')
                address, location, centrish_number = desc_text.split('<br>')
                sold = False
                if sold_element and sold_element.find('img')['src'] == '/images/en/ic_sold.png':
                    sold = True

                centrish_no = centrish_number.split(': ')[-1]
                property_info = {
                    # 'centrish_number': centrish_number.split(': ')[-1],
                    # 'sold': sold,
                    # 'address': address,
                    # 'location': location
                }

                detail_url = f"https://www.londonogroup.com/property/viewProperty.php?id={centrish_no}&pos={pos_number}"
                response = requests.get(detail_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                details = soup.find_all('div', class_="content-tab")
                for detail in details:
                    type_price_element = detail.find_all('ul', class_='total-price')
                    for type_element in type_price_element:
                        if type_element.text != '':
                            type_price_text = type_element.text.strip()
                            try:
                                title, price = type_price_text.split(': ', 1)
                                price = type_element.select('li')[0].select_one('strong').text
                                bed_count = type_element.select('li')[1].select_one('strong').text
                                bath_count = type_element.select('li')[2].select_one('strong').text
                                if len(type_element.select('li')) > 3:
                                    municipality_tax = type_element.select('li')[3].select_one('strong').text
                                    if len(type_element.select('li')) > 4:
                                        school_tax = type_element.select('li')[4].select_one('strong').text
                                else:
                                    municipality_tax = "N/A"
                                    school_tax = "N/A"

                            except ValueError:
                                title = type_price_text
                                price = None

                            if "Rental Price" in title:
                                title = "Rental"
                            else:
                                title = "Sales"

                            property_info = {
                                'title': title,
                                'price': price if price else "Price not available",
                                'bed_count': bed_count if bed_count else "Price not available",
                                'bath_count': bath_count if bath_count else "Price not available",
                                "municipality_tax": municipality_tax if municipality_tax else "Price not available",
                                "school_tax": school_tax if school_tax else "Price not available",
                                'address': address if address else "Price not available",
                                'location': location if location else "Price not available",
                                'sold': sold,
                                'centrish_number': centrish_number.split(': ')[-1],

                            }

                properties_list.append(property_info)

    with open("properties-details.json", "w") as json_file:
        json.dump(properties_list, json_file, indent=4)

    print(f"Number of properties: {len(properties_list)}")


if __name__ == '__main__':
    properties()
