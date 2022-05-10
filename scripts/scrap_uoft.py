import requests
from bs4 import BeautifulSoup



for i in range(2, 21):
  url = "https://future.utoronto.ca/academics/undergraduate-programs/?sf_paged=" + str(i)
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
  result = requests.get(url, headers=headers)

  with open('/Users/rahul/Documents/main/projects/personal_learning_projects/uoftroom/uoft_programs.txt', 'a') as f:
    soup = BeautifulSoup(result.content, "html.parser")
    main_div = soup.find('div', class_='program')
    program_rows = main_div.find('div', class_='row')
    all_programs = program_rows.findAll('div')
    for elem in all_programs[:-1]:
      program_name = elem.find('h3').text.strip()
      f.write(program_name + '\n')



