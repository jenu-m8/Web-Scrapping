import requests
from bs4 import BeautifulSoup
import json

def login():
    with requests.Session() as session:
        login_page_response = session.get("http://www.edudept.np.gov.lk/schoolacc/schoolsignin.php")
        if login_page_response.ok:
            csrf_token = session.cookies.get_dict().get("csrftoken")

            login_data = {
                "csrfmiddlewaretoken": csrf_token,
                "username": "1001019",
                "password": "II93xh72",
            }
            login_response = session.post("http://www.edudept.np.gov.lk/schoolacc/loginchksch.php", data=login_data)
            if "http://www.edudept.np.gov.lk/schoolacc/search-sch.php" in login_response.url:
                print("Login successful")
                return session
            else:
                print("Login failed")
        else:
            print(f"Failed to access the login page. Status code: {login_page_response.status_code}")

def scrape_student_details(student_id):
    url = f"http://www.edudept.np.gov.lk/schoolacc/StudentDetails/dbstudenteditlistSch.php?StudentID={student_id}&selectins=1&selectinsd=All&selectinsy=All"
    requests_session = login()

    if requests_session:
        response = requests_session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            student_id_element = soup.find("input", {"name": "StudentID1", "id": "StudentID"})
            student_id_value = student_id_element.get("value")

            fullname_element = soup.find("input", {"name": "StFullName"})
            fullname_value = fullname_element.get("value")

            dob_element = soup.find("input", {"name": "DateofBirth"})
            dob_value = dob_element.get("value")

            academic_year_element = soup.find("input", {"name": "yearofstudy"})
            academic_year_value = academic_year_element.get("value")

            address_element = soup.find("input", {"name": "StHomeAddress"})
            address_value = address_element.get("value")

            father_first_name_element = soup.find("input", {"name": "FatherFName"})
            father_first_name_value = father_first_name_element.get("value")

            father_last_name_element = soup.find("input", {"name": "FatherLName"})
            father_last_name_value = father_last_name_element.get("value")

            father_nic_element = soup.find("input", {"name": "FatherNIC"})
            father_nic_value = father_nic_element.get("value")

            father_phone_element = soup.find("input", {"name": "FatherContactNo"})
            father_phone_value = father_phone_element.get("value")

            mother_first_name_element = soup.find("input", {"name": "MotherFName"})
            mother_first_name_value = mother_first_name_element.get("value")

            mother_last_name_element = soup.find("input", {"name": "MotherLName"})
            mother_last_name_value = mother_last_name_element.get("value")

            mother_nic_element = soup.find("input", {"name": "MotherNIC"})
            mother_nic_value = mother_nic_element.get("value")

            mother_phone_element = soup.find("input", {"name": "MotherContactNo"})
            mother_phone_value = mother_phone_element.get("value")

            student_details = {
                "Id": student_id_value,
                "FullName": fullname_value,
                "Dob": dob_value,
                "AcademicYear": academic_year_value,
                "Address": address_value,
                "FatherFirstName": father_first_name_value,
                "FatherLastName": father_last_name_value,
                "FatherNIC": father_nic_value,
                "FatherContactNo": father_phone_value,
                "MotherFName": mother_first_name_value,
                "MotherLName": mother_last_name_value,
                "MotherNIC": mother_nic_value,
                "MotherContactNo": mother_phone_value
            }

            return student_details

        except AttributeError:
            print(f"No student details found for ID: {student_id}")
            return None

def scrape_grade1_students():
    all_students_details = []

    for student_id in range(94750013447, 94750013450):  # Adjust the range accordingly
        print(f"Scraping details for ID {student_id}...")
        student_details = scrape_student_details(student_id)
        if student_details:
            all_students_details.append(student_details)

    with open("grade_1_students_details.json", "w") as json_file:
        json.dump(all_students_details, json_file, indent=4)

    print(f"Total grade 1 students: {len(all_students_details)}")

if __name__ == '__main__':
    scrape_grade1_students()
