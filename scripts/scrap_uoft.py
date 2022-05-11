import requests
from bs4 import BeautifulSoup


# https://www.utoronto.ca/academics/programs-directory?field_degrees_value=2&keys=&page=1
# https://www.utoronto.ca/academics/programs-directory?field_degrees_value=2&keys=&page=11
for i in range(0, 12):
  # url = "https://future.utoronto.ca/academics/undergraduate-programs/?sf_paged=" + str(i)
  url = 'https://www.utoronto.ca/academics/programs-directory?field_degrees_value=2&keys=&page=' + str(i)
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
  result = requests.get(url, headers=headers)

  with open('/Users/rahul/Documents/main/projects/personal_learning_projects/uoftroom/uoft_programs.txt', 'a') as f:
    soup = BeautifulSoup(result.content, "html.parser")

    ## grad 
    main_div = soup.find('div', class_='region region-content')
    programs_div = main_div.find('div').find('div')
    programs_list = programs_div.findAll('p', class_='name')
    for elem in programs_list:
      program_name = elem.text.replace('\n', '').strip()
      f.write(program_name + '\n')

    ## undergrad
    # main_div = soup.find('div', class_='program')
    # program_rows = main_div.find('div', class_='row')
    # all_programs = program_rows.findAll('div')
    # for elem in all_programs[:-1]:
    #   program_name = elem.find('h3').text.strip()
    #   f.write(program_name + '\n')



