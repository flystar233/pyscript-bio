import requests
import argparse
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import pandas as pd
from pypinyin import lazy_pinyin

def get_temperature(url):
	header = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
	req = requests.get(url, headers=header)
	req.encoding = 'utf-8'
	soup = BeautifulSoup(req.text, "html5lib")
	ul_tag1 = soup.find_all('div',class_='th200') # date tag
	date = []
	for i in ul_tag1:
		result = re.findall(r'>(.*)</div>',str(i))[0]
		date.append(result)

	ul_tag2 = soup.find_all('div',class_='th140') # temperature tag
	tianqi = []
	tmp = []
	for i in ul_tag2:
		result = re.findall(r'>(.*)</div>',str(i))[0]
		tmp.append(result)
		if len(tmp)==4:
			tianqi.append(tmp)
			tmp = []
	return date,tianqi

def make_plot(city,time):
	city_pinyin = ''.join(lazy_pinyin(city))
	year_date = ['0'+str(i) if i <10 else str(i) for i in range(1,13)]
	mydict = {}
	for y in time:
		for i in year_date:
			url = f'http://lishi.tianqi.com/{city_pinyin}/{y}{i}.html'
			date,tianqi = get_temperature(url)
			for res in zip(date,tianqi):
				if res[0] == '日期': #remove header
					pass
				else:
					mydict[res[0][0:10]] = [int(i.rstrip('℃')) for i in res[1][0:2]] #cut year and temperature

	df = pd.DataFrame(mydict).T
	df.columns = ['the high','the low']
	fig, ax = plt.subplots(figsize=(12, 6))
	df.plot(ax =ax,title=f"{city} {list(time)[0]}-{list(time)[-1]} 温度变化",lw=1)
	plt.rcParams['font.sans-serif']=['SimHei']
	plt.rcParams['axes.unicode_minus']=False
	plt.grid(axis='y')
	plt.savefig('weather.pdf')

def main():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("-c", "--city", action="store", dest="city", required=True,help="the city")
	parser.add_argument("-s", "--start", type =int, dest="start",required=True,help="start year")
	parser.add_argument("-e", "--end", type =int, dest="end",required=True,help="end year")
	args = parser.parse_args()
	city = args.city
	start = args.start
	end = args.end
	assert start>=2011,"Start time should't less than 2010"
	assert end>=start,"Start time bigger than end time!"
	make_plot(city,range(start,end+1))
if __name__ == "__main__":
    main()
