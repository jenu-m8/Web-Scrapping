import requests
from bs4 import BeautifulSoup


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


def students(grade):
    url = f"http://www.edudept.np.gov.lk/schoolacc/StudentDetails/studenteditlist.php?in={grade}&ind=All&iny=All"
    requests_session = login()

    if requests_session:
        response = requests_session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            students_table = soup.select_one(".TFtable")
            student_details = []
            for student_row in students_table.find_all("tr"):
                student_detail = [column.get_text(strip=True) for column in student_row.find_all("td")]
                if student_detail and student_detail[0] != "S.No.":
                    student_details.append({
                        "Id": student_detail[1],
                        "Name": student_detail[2],
                        "DOB": student_detail[3],
                        "Grade": student_detail[4],
                        "Division": student_detail[5],
                        "Year": student_detail[6]
                    })
            for student in student_details:
                print(student)
            print(f"Elements: {len(student_details)}")

        except AttributeError:
            print(f"No student table found on the page: {url}")


if __name__ == '__main__':
    for grade in range(1, 6):
        print(f"Scraping Grade {grade}...")
        students(grade)
