import requests
from bs4 import BeautifulSoup
import json


def properties():
    global bed_count, bath_count, powder_room, municipality_tax, property_info
    properties_list = []

    start_page = 1
    end_page = 2
    start_pos = 1
    end_pos = 1
    school_tax = "Not available"
    condo_fees = "Condo fees not available"
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
                address, location, centris_number = desc_text.split('<br>')
                sold = False
                if sold_element and sold_element.find('img')['src'] == '/images/en/ic_sold.png':
                    sold = True

                centris_no = centris_number.split(': ')[-1]

                detail_url = f"https://www.londonogroup.com/property/viewProperty.php?id={centris_no}&pos={pos_number}"
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
                                bed_count = type_element.select_one('li:-soup-contains("Bedrooms")')
                                bath_count = type_element.select_one('li:-soup-contains("Bathrooms")')
                                if len(type_element.select('li')) > 3:
                                    powder_room = type_element.select_one('li:-soup-contains("Powder Room")')
                                    if powder_room:
                                        powder_room = powder_room.select_one('strong').text
                                    else:
                                        powder_room = "No Powder Room"
                                    municipality_tax = type_element.select_one('li:-soup-contains("Municipality Tax")')
                                    if municipality_tax:
                                        municipality_tax = municipality_tax.select_one('strong').text
                                    else:
                                        municipality_tax = "Not show"
                                    school_tax = type_element.select_one('li:-soup-contains("School Tax")')
                                    if school_tax:
                                        school_tax = school_tax.select_one('strong').text
                                    else:
                                        school_tax = "Not show"
                                    condo_fees_element = type_element.select_one('li:-soup-contains("Condo Fees")')
                                    if condo_fees_element:
                                        condo_fees = condo_fees_element.select_one('strong').text
                                    else:
                                        condo_fees = "Condo fees not available"
                                else:
                                    municipality_tax = "N/A"
                                    powder_room = "N/A"
                            except ValueError:
                                title = type_price_text
                                price = None

                            if "Rental Price" in title:
                                title = "Rental"
                            else:
                                title = "Sales"

                            property_info = {
                                'title': title,
                                'address': address if address else "Not available",
                                'location': location if location else "Not available",
                                'sold': sold,
                                'price': price if price else "Price not available",
                                'bed_count': bed_count.text if bed_count else "Not available",
                                'bath_count': bath_count.text if bath_count else "Not available",
                                'powder_room': powder_room if powder_room else "Not available",
                                "municipality_tax": municipality_tax if municipality_tax else "Not available",
                                "school_tax": school_tax if school_tax else "Not available",
                                'centris_number': centris_number.split(': ')[-1],
                                'condo_fees': condo_fees if condo_fees else "Condo fees not available",
                            }


                properties_list.append(property_info)

    with open("properties-details.json", "w") as json_file:
        json.dump(properties_list, json_file, indent=4)

    print(f"Number of properties: {len(properties_list)}")


if __name__ == '__main__':
    properties()
