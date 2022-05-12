import requests
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
url = 'https://www.artsci.utoronto.ca/current/academics/course-planning/course-list'
result = requests.get(url, headers=headers)
soup = BeautifulSoup(result.content, "html.parser")
primary_div = soup.find('div', class_='field-items')
main_div = primary_div.find('div')
all_course_divs = main_div.findAll('div', class_='table-responsive')

all_courses = []
with open('/Users/rahul/Documents/main/projects/personal_learning_projects/uoftroom/uoft_all_courses.txt', 'a') as f:
  for course_div in all_course_divs:
    course_table = course_div.find('table').find('tbody')
    course_rows = course_table.findAll('tr')
    for row in course_rows:
      course_txt = row.find('td').text
      course_name = ''
      if 'H1' in course_txt:
        course_name = course_txt.split('H1')[0]
      else:
        course_name = course_txt.split('Y1')[0]

      if course_name not in all_courses:
        all_courses.append(course_name)
        f.write(course_name + '\n')



 