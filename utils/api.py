import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup


async def get_schedule(faculty, course, group):
    url = "https://dekanat.lnu.edu.ua/cgi-bin/timetable.cgi?n=700"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    payload = {
        "faculty": faculty,
        "teacher": "",
        "course": course,
        "group": group,
        "sdate": "",
        "edate": "",
        "n": "700"
    }

    payload_encoded = urlencode(payload, encoding='windows-1251')

    response = requests.post(url, headers=headers, data=payload_encoded.encode('windows-1251'))
    response.encoding = 'windows-1251'
    return await parse_page(response.text)


async def get_group(faculty, course, group):
    import requests

    url = f"https://dekanat.lnu.edu.ua/cgi-bin/timetable.cgi?n=701&lev=142&faculty={faculty}&course={course}&query={group}"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    try:
        json_response = response.json()["suggestions"]
    except requests.exceptions.JSONDecodeError:
        return None
    return json_response


async def parse_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    container = soup.find_all('div', class_='container')
    row3 = container[1].find_all('div', class_='row', recursive=False)

    json_data = {}
    for row in row3:
        col_md_6_first = row.find('div', class_="col-md-6")

        count_td = len(col_md_6_first.find_all('td'))
        if count_td == 3:
            date_header = col_md_6_first.find('h4').text.strip()
            date_parts = date_header.split()
            date = date_parts[0]
            day = date_parts[1].strip('()')
            rows_child = row.find_all('div', class_='row')
            day_schedule = []
            for row_child in rows_child:
                cells = row_child.find_all('td')
                if len(cells) == 3:
                    lesson_number = cells[0].text.strip()

                    td = cells[1]
                    text_segments = [str(segment).strip() for segment in td if
                                     isinstance(segment, str) or segment.name == 'br']
                    text_segments = [segment for segment in text_segments if segment]
                    text_segments = [item for item in text_segments if item != '<br/>']
                    time = text_segments

                    td = cells[2]
                    text_segments2 = [str(segment).strip() for segment in td if
                                      isinstance(segment, str) or segment.name == 'br']
                    text_segments2 = [segment for segment in text_segments2 if segment]
                    text_segments2 = [item for item in text_segments2 if item != '<br/>']

                    details = text_segments2
                    if len(details) > 0:
                        subject = details[0]
                        lecturer = details[1]
                        if len(details) > 2:
                            audience = details[2]
                        else:
                            audience = None

                        schedule_entry = {
                            'lesson_number': lesson_number,
                            'time': time,
                            'lecturer': lecturer,
                            'subject': subject,
                            'audience': audience,
                        }
                        day_schedule.append(schedule_entry)

                    json_data[date] = {
                        'day': day,
                        'schedule': day_schedule
                    }

        col_md_6_second = row.find('div', class_="col-md-6").find_next('div', class_="col-md-6")
        if col_md_6_second is not None:

            # Знаходимо дату та день тижня
            date_header = col_md_6_second.find('h4').text.strip()
            date_parts = date_header.split()
            date = date_parts[0]
            day = date_parts[1].strip('()')

            # Знаходимо всі рядки в таблиці розкладу
            table_rows = col_md_6_second.find_all('tr')
            day_schedule = []

            for row in table_rows:
                cells = row.find_all('td')
                if len(cells) == 3:
                    lesson_number = cells[0].text.strip()

                    td = cells[1]
                    text_segments = [str(segment).strip() for segment in td if
                                     isinstance(segment, str) or segment.name == 'br']
                    text_segments = [segment for segment in text_segments if segment]
                    text_segments = [item for item in text_segments if item != '<br/>']
                    time = text_segments

                    td = cells[2]
                    text_segments2 = [str(segment).strip() for segment in td if
                                      isinstance(segment, str) or segment.name == 'br']
                    text_segments2 = [segment for segment in text_segments2 if segment]
                    text_segments2 = [item for item in text_segments2 if item != '<br/>']

                    details = text_segments2
                    if len(details) > 1:
                        subject = details[0]
                        lecturer = details[1]
                        if len(details) > 2:
                            audience = details[2]
                        else:
                            audience = None

                        schedule_entry = {
                            'lesson_number': lesson_number,
                            'time': time,
                            'lecturer': lecturer,
                            'subject': subject,
                            'audience': audience,
                        }
                        day_schedule.append(schedule_entry)

            json_data[date] = {
                'day': day,
                'schedule': day_schedule
            }
    return json_data