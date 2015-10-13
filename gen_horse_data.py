#-*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import random
if len(sys.argv) < 2:
	print "usage : python gen_horse_data.py 1000"
	exit()

fname = 'horse_'
gen_count = int(sys.argv[1])
print gen_count

def gen_row():
	rt = ['win']
	row = []
	row.append(1.0 + round(random.random(),2))
	row.append(random.choice(["male","female"])) 	
	row.append(random.randrange(1,6))
	row.append(random.randrange(100,140))
	row.append(random.choice(["steadily","spurt","gambling"]))
	row.append(random.randrange(1,6))
	row.append(random.randrange(1,6))
	row.append(random.randrange(1,6))
	row.append(random.randrange(1,6))
	if ((row[5] > row[6]) and (row[7] > row[8])) and (row[0] < 1.2 or row[3] > 120):
		rt[0] = 'win'
	else:
		rt[0] = 'lose'
	rt.extend(row)
	return rt

f = open(fname + str(gen_count)+'.dat','w')
for i in range(gen_count):
	row = gen_row()
	print row
	for col in row:
		f.write(str(col)+'\t')
	f.write('\n')
f.close()

'''
펜 > 문 & 검 > 펙 이고, 평균이 1.2 밑 이거나 훈련 시간이 120 이상시   win 으로 한다 나머지는 lose


참조::
http://sports.chosun.com/news/html/life/horse/20150919s.htm


성적    평균  성별 나이 훈련 성격 팬 문 검 펙
win     1.33    1   2   120 추입    5   4   2   2
lose    1.32    2   3   110 선행    4   4   3   1
lose    1.32    2   3   110 도박    4   4   3   1

'''

