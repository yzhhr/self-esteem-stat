import pandas as pd
import matplotlib.pyplot as plt
file = r'goodorder.xlsx'
df = pd.read_excel(file, sheet_name='Sheet1', header=0)
print('head!!', df.head(0))
print(df.head(0).columns[1])
print('values!!', df.values)
data = df.values

# 0: id
# 1: gender
# 2: grade
# 3 - 22: specific questions

conv = {}
revmap = {}
for j in range(1, 22 + 1):
  item = data[0][j]
  style = 0
  qid = 0
  if (type(item) == int):
    if (item <= 0):
      style = 0
    else:
      style = 1
    qid = item
  else:
    style = -1
    qid = int(item[:-1:])
  conv[item] = (df.head(0).columns[j], qid, style)
  revmap[qid] = item
  print(item, conv[item])
  # (name, questionid, type(1, -1, 0))
  del item
  del style
  del qid

L = 2 # no 2 - 144
R = 144

users = []

for i in range(L, R + 1):
  row = data[i - 1]
  user = {'gender': row[1], 'grade': row[2]}
  for j in range(3, 22 + 1):
    key = data[0][j]
    user[conv[key][1]] = row[j]
  users.append(user)
  del row
  del user

print(users[0])

def tri(cond, yes = 1, no = 0):
  if (cond):
    return yes
  else:
    return no
def sum_over(iterable, f):
  sum = 0
  for x in iterable:
    sum += f(x)
  return sum

males = []
females = []
for user in users:
  if (user['gender'] == 1):
    males.append(user)
  else:
    females.append(user)

def rosenberg(user):
  score = 0
  for i in range(1, 11):
    # print(user[i], ' ', end = '')
    if conv[revmap[i]][2] == 1:
      score += user[i]
      # print(i, 'in positive')
    elif conv[revmap[i]][2] == -1:
      score += 5 - user[i]
      # print(i, 'in negative')
    else:
      pass
      # print('strange', user)
  return score
def sgn(x):
  return tri(x > 0, 1, tri(x < 0, -1, 0))
def kendall_tau_c(x, y):
  n = len(x)
  if (len(x) != len(y)):
    print('Nopes')
  sum = 0
  for i in range(0, n):
    for j in range(i + 1, n):
      sum += sgn(x[i] - x[j]) * sgn(y[i] - y[j])
  return sum * 2 / n / (n - 1)

report = open('./report/report.txt', 'w', encoding='utf-8')
report.write('male count = {}\n'.format(len(males)))
report.write('female count = {}\n'.format(len(females)))
report.write('male rosenberg ave = {}\n'.format(sum_over(males, rosenberg) / len(males) / 10))
report.write('female rosenberg ave = {}\n'.format(sum_over(females, rosenberg) / len(females) / 10))

# consider the following questions

orig_serif = plt.rcParams['font.sans-serif']

def extract(users):
  ses = []
  score = []
  for user in users:
    ses.append(rosenberg(user) / 10)
    score.append(user[i])
  return ses, score

import scipy
import scipy.stats

for i in range(1, 20 + 1):
  report.write('Question #{}: {}\n'.format(i, conv[revmap[i]][0]))

  ses, score = extract(males)
  plt.scatter(ses, score, color='#0000ff77')
  report.write('male relevance = {}\n'.format(scipy.stats.kendalltau(ses, score)))
  report.write('mean = {}\n'.format(sum(score) / len(score)))

  ses, score = extract(females)
  plt.scatter(ses, score, color='#ff000077')
  report.write('female relevance = {}\n'.format(scipy.stats.kendalltau(ses, score)))
  report.write('mean = {}\n'.format(sum(score) / len(score)))


  # plt.scatter(ses, score, color='r', alpha=0.5)
  ses, score = extract(users)
  report.write('overall relevance = {}\n'.format(scipy.stats.kendalltau(ses, score)))
  report.write('mean = {}\n'.format(sum(score) / len(score)))

  plt.xlabel('SES Score')
  plt.ylabel('This Question')
  plt.rcParams['font.sans-serif'] = ['SimHei']
  plt.rcParams['axes.unicode_minus'] = False
  plt.title(str(i) + '.' + conv[revmap[i]][0])
  # plt.savefig('./report/{}cn.png'.format(i))
  plt.rcParams['font.sans-serif'] = ['Times New Roman']
  plt.rcParams['axes.unicode_minus'] = True
  plt.title('Figure {}'.format(i))
  plt.savefig('./report/{}en.png'.format(i))
  print(i, 'done')
  # plt.show()
  plt.clf()

report.close()



# print(sorted(males[0].items()))
# print(males[0])
# print(rosenberg(males[0]))
# print(conv)





# print(df.head(0).iloc[0].values)

