
uoft_undergrad_programs_fp = '/Users/rahul/Documents/main/projects/personal_learning_projects/uoftroom/uoft_programs.txt'
f = open(uoft_undergrad_programs_fp, 'r')
ug_lines = f.readlines()
undergrad_programs = [line.replace('\n', '').strip() for line in ug_lines]

uoft_grad_programs_fp = '/Users/rahul/Documents/main/projects/personal_learning_projects/uoftroom/uoft_grad.txt'
f = open(uoft_grad_programs_fp, 'r')
g_lines = f.readlines()
grad_programs = [line.replace('\n', '').strip() for line in g_lines]

final_list = []
with open('/Users/rahul/Documents/main/projects/personal_learning_projects/uoftroom/final_programs_list.txt', 'a') as f:
  for program in undergrad_programs:
    final_list.append(program)
    f.write(program + '\n')

  for program in grad_programs:
    if program not in final_list:
      final_list.append(program)
      f.write(program + '\n')



