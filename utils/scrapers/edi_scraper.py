from bs4 import BeautifulSoup
import requests
import json
import sys
import stat

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options




url = sys.argv[1]

chrome_options = Options()  
chrome_options.add_argument("--headless") # Opens the browser up in background

with Chrome(options=chrome_options) as browser:
	browser.get(url)
	response = browser.page_source


# response = requests.get(url)
# print(response)
soup = BeautifulSoup(response, 'html.parser')

if soup.text == "Just a moment...Enable JavaScript and cookies to continue":
	print("Bypassing anti-scrap protection...")
	scr = soup.findAll("script")[-1].string
	scr = scr[scr.index("var a=toNumbers"):].split(';')
	line = scr[0]
	abc = []
	while "toNumbers" in line:
		i = line.index("toNumbers")
		line = line[i+11:]
		abc.append(line[:line.index('"')])
	from Crypto.Cipher import AES
	def to_numbers(x):
		return bytes(int(x[i:i+2], 16) for i in range(0, len(x), 2))
	key, iv, cipher = map(to_numbers, abc)
	aes = AES.new(key, AES.MODE_CBC, iv)
	rcpc = aes.decrypt(cipher).hex()
	print(f"RCPC = {rcpc}")
	url = scr[-2]
	url = url[url.index('"')+1:-1]
	r = requests.get(url, cookies={"RCPC": rcpc})
	s = r.text
	soup = BeautifulSoup(s, "html.parser")

soup = soup.find_all(class_='content')[0] # .find_all(class_ = 'spoiler')



while soup.pre != None:
	soup.pre.decompose()

import pickle


# res=(soup.prettify().split('<a href="'))

edi = []

on = False

problem = 'contest/1979/problem/F'

for tag in soup.find_all(['p', 'h2', 'h3']):
	
	

	links = tag.find_all(href=True)

	if (len(links) > 0 and tag.name != 'p' and problem in links[0].prettify()):
		on=True
	elif len(links) > 0 and tag.name != 'p':
		on = False
	elif on:
		latex_content = ""

		for elem in tag.descendants:

			if (elem.find_parent().name != 'p'):
				continue

			if isinstance(elem, str):
				latex_content += elem
			elif elem.name == "script" and elem.get("type") == "math/tex":
				latex_content += "$" + elem.string + "$"

			

		edi.append(latex_content)


print('\n'.join(edi))





