from datetime import datetime
import sys
import os, errno
import time
from PyQt5.QtWidgets import *
from PyQt5 import uic

# GUI 구현
form_class = uic.loadUiType("version1.0.ui")[0]

class MyWindow(QMainWindow, from_class):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	myWindow = MyWindow()
	myWindow.show()
	app.exec_()

# time check
def date_titme(number):
	year = datetime.today().year
	month = datetime.today().month
	day = datetime.today().day
	year = str(year)[2:]
	
	if month < 10 : 
		month = "0" + str(month)

	if day < 10 :
		day = day - 1
		day = "0" + str(day)

	if number == 1:
		return str(year) + '.' + str(month) + '.' + str(day)
	else:
		return str(year) + str(month) + str(day)

# select function
def select_function(site_name, movie_name, func_number):
	select_site(site_name) 
	select_number(func_number)

# cralwer function
def select_number(func_number):
	if func_number == 1:
		return 1
	elif func_number == 2:
		return 2
	elif func_number == 3:
		return 3

# select site
def select_site(site_name):
	if site_name == "네이버":
		return 1
	elif site_name == "다음":
		return 2
	elif site_name == "CGV":
		return 3
	elif site_name == "롯데시네마":
		return 4
	elif site_name == "메가박스":
		return 5
	elif site_name == "rotten":
		return 6
	elif site_name == "IMDB":
		return 7
	else:
		return 8

# 해당 위치에 데이터 저장할 폴더 생성 
def create_forder(forder_name, path):
	result = ""
	try:
		if not (os.path.isdir(path + "/" + forder_name)):
			os.mkdir(os.path.join(path + "/" + forder_name))
		result = path + forder_name
	except OSError as e:
		if e.errno != errno.EEXIST:
			print("Failed to Create Directory")
	return result

# 파일 오류 발생 체크
def is_checked_filesize(path, forder_name, file_name):
	flag = False

	result = os.path.getsize(path+forder_name+"/"+file_name)
	result = math.ceil(result / 1024) # math 올림 함수

	if result >= 1:
		flag = True
	else:
		flag = False

	return flag


# 문제 발생으로 인한 크롤링 실패 시 체크 후 5분 후 다시 크롤링
def insert_info(moviecode, forder_name, movie_name):
	URL_naver = "https://movie.naver.com/movie/point/af/list.nhn?st=mcode&sword="+moviecode+"&target=after&page=" #네이버 리뷰 URL
	path = "D:/project/movie_date/" # 데이터를 저장할 폴더 경로
	file_name = "movie_review_" + moviecode + "_" + date_time(2) + ".txt"  # 저장될 파일 이름

	result = create_forder(forder_name, path)
	
	flag = is_checked_filesize(URL_naver, path, file_name)
	while True:
		if flag == True:
			print("정상적으로 완료됨")
			break
		else:
			review_naver(result, URL_naver, file_name)
			time.sleep(300)

# 
def review_naver(URL_naver, path, file_name):
	f = open(path+"/"+ file_name, "w", encoding='utf-8')
	page = 0
	tmp = 0
	while True:
		page = page + 1
		URL = URL_naver + "{0}".format(page)
		html = requests.get(URL).content

		soup = BeautifulSoup(html, "html.parser")
		table = soup.find("table", {"class": "list_netizen"})
		tbody = table.find("tbody")
		tr_date = tbody.find("tr")
		tr_tags = tbody.find_all("tr")

		date_t = list(tr_date.strings)
		
		for info in tr_tags:
			storeDate = list(info.strings)
			no = storeDate[1].strip()
			point = storeDate[4].strip()
			review = storeDate[9].strip()
			date = storeDate[14].strip()
			f.write(no + ',')
			f.write(date + ',')
			f.write(point + ',')
			f.write(review + '\n')
