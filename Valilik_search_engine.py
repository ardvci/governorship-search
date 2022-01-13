import tkinter as tk 
from googlesearch import search
from tkinter import messagebox
import webbrowser
from bs4 import BeautifulSoup
import requests
from PIL import Image, ImageTk
import time
import xlsxwriter
import pandas as pd
from tkinter import messagebox as mb 

from tkinter import filedialog 
import os
websites = []
global x
global excel_df
excel_df = pd.DataFrame(columns=['Anahtar Kelime İçerme Durumu','Şehir','Başlık','Link'])
keywords = []
comparison_list_adana = []
comparison_list_adana2 = []
comparison_list_batman = []
comparison_list_elazığ = []
comparison_list_gaziantep = []
comparison_list_hakkari = []
comparison_list_mardin = []
comparison_list_muğla = []
comparison_list_muş = []
comparison_list_şanlıurfa = []
comparison_list_şırnak = []
comparison_list_tunceli = []
comparison_list_van = []


def get():
	global res
	final_keywords = []
	guess = Entry.get()
	keywords.append(guess)
	global label3
	label3=tk.Label(lower_frame,text="İstediğiniz iletilmiştir",bg="#ECECF2")
	root.after(4000,label3.destroy)
	label3.pack()
	Entry.delete(0,tk.END)
	N=""
	res = [ele for ele in keywords if ele != N]
	print(res)
	return res

def network_control():
	try:
		requests.get('https://www.google.com/').status_code
		return True
	except:
		messagebox.showerror("UYARI","internet Bağlantınızı kontrol edip uygulamaya tekrardan Girin")
		exit()
def adana_check(): 
    res = mb.askquestion('Adana Arama',  
                         'Adana Valiliğinde Aramaya Devam Edilsin mi ?') 
      
    if res == 'yes' :
    	root.after(1000,lambda:adana_web_scraping())   
    else : 
        mb.showinfo('Return', 'Returning to main application')
def adana_check_2(): 
    res = mb.askquestion('Adana Arama',  
                         'Adana Valiliğinde Aramaya Devam Edilsin mi ?') 
      
    if res == 'yes' :
    	root.after(1000,lambda:adana_press_scraping())   
    else : 
        mb.showinfo('Return', 'Returning to main application')
def adana_web_scraping():
	comparison_string= ["",""]
	comparison_list=[]
	a = []
	hrefs=[]
	arr= []
	page_arr = []
	urls= []
	final_urls = []
	word = get()
	url = "http://adana.gov.tr/duyurular"
	page = requests.get(url)
	data = page.text
	soup = BeautifulSoup(data, 'html.parser')
	text = soup.find_all('a',class_='announce-text')
	for line in soup.find_all('a',class_='announce-text'):
		a.append(line.get_text())
	for line in soup.find_all('a',class_='announce-text'):
		hrefs.append(line.get('href'))
	word=[y.lower() for y in word]
	k = [x.replace(' ', '') for x in a]
	k2= k = [x.replace('\r', '') for x in k]
	k3 = k = [x.replace('\n', '') for x in k2]
	k3=[x.lower() for x in k3]
	hrefs = list(dict.fromkeys(hrefs))

	for i in word:
		all_titles = [p for p in k3 if i in p]
		arr.append(all_titles)
	for i in comparison_string:
		all_titles = [p for p in k3 if i in p]
		comparison_list.append(all_titles)
	arr=tuple(filter(lambda x:x!=[], arr))
	mytuplelist = [tuple(item) for item in arr]
	mylist = list(set(mytuplelist))
	comparison_list_new = [elem for elem in arr if elem not in comparison_list ]
	# index=k3.index(comparison_list_new[0][0])
	num1= int(len(comparison_list_new))
	num2 = int(len(comparison_list_adana))
	adana_count = 0
	
	if num1 > num2:
		for i in range(len(comparison_list_new)):
			comparison_list_adana.append(comparison_list_new[i])
			index=k3.index(comparison_list_new[i][0])
			length=len(excel_df)
			urls.append(index)	
		url=hrefs[index]
		for i in urls:
			final_urls.append(hrefs[i])
		page = requests.get("http:"+url)
		data = page.text
		soup_text = BeautifulSoup(data, 'html.parser')
		for line in soup_text.find_all('div',class_='icerik'):
			page_arr.append(line.get_text())
		page_arr = [x.replace('\xa0', '') for x in page_arr]
		page_arr = [x.replace('\r', '') for x in page_arr]
		page_arr = [x.replace('\n', '') for x in page_arr]
		page_arr = [x.replace(' ', '') for x in page_arr]
		page_arr = [x.replace('/', '') for x in page_arr]
		page_arr=[x.lower() for x in page_arr]
		for i in page_arr:
			page_substring = [p for p in page_arr if ("2911" or "5944") in p]
			print(page_substring)
		if len(page_substring) != 0:
			messagebox.showinfo("Adana","Yeni Duyuru Yayınlandı !!!!")
			label_pos_adana = tk.Label(lower_frame,text="Adana Valiliğinde yeni bildiri yayınlandı")
			label_pos_adana.pack()
			root.after(60000,label_pos_adana.destroy)
			city = "Adana"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) ==1:
				for i in range(len(comparison_list_new[0])):
					index=k3.index(comparison_list_new[0][i])
					length=len(excel_df)
					urls.append(index)
				url=hrefs[index]
				for i in urls:
					final_urls.append(hrefs[i])
				final_urls = list(dict.fromkeys(final_urls))
				print(final_urls)
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["+",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["+",city,comparison_list_new[-1:][0],url]
			
			print(num1," ",num2)
			num2+=1
			print(num1," ",num2)
			adana_check()
		else:
			messagebox.showinfo("Adana","Yeni Duyuru Yayınlandı !!!!")
			label_pos_adana = tk.Label(lower_frame,text="Adana Valiliğinde yeni bildiri yayınlandı")
			city = "Adana"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) == 1:
				for i in range(len(comparison_list_new[0])):
					for i in range(len(comparison_list_new[0])):
						index=k3.index(comparison_list_new[0][i])
						length=len(excel_df)
						urls.append(index)
					url=hrefs[index]
					for i in urls:
						final_urls.append(hrefs[i])
					final_urls = list(dict.fromkeys(final_urls))
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["-",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["x",city,comparison_list_new[-1:][0],url]
			adana_check()
	else:
		label_negative_adana = tk.Label(lower_frame,text="Adana valiliğinde 5 dakika sonra tekrardan arama yapılacak")
		label_negative_adana.pack()
		root.after(60000,label_negative_adana.destroy)
		root.after(60000,lambda:adana_web_scraping())
def adana_press_scraping():
	comparison_string= ["",""]
	comparison_list=[]
	a = []
	hrefs=[]
	arr= []
	page_arr = []
	word =get()
	url = "http://adana.gov.tr/basin-aciklamalari"
	page = requests.get(url)
	data = page.text
	soup = BeautifulSoup(data, 'html.parser')
	text = soup.find_all('a',class_='announce-text')
	for line in soup.find_all('a',class_='announce-text'):
		a.append(line.get_text())
	for line in soup.find_all('a',class_='announce-text'):
		hrefs.append(line.get('href'))
	word=[y.lower() for y in word]
	k = [x.replace(' ', '') for x in a]
	k2= k = [x.replace('\r', '') for x in k]
	k3 = k = [x.replace('\n', '') for x in k2]
	k3=[x.lower() for x in k3]
	hrefs = list(dict.fromkeys(hrefs))
	for i in word:
		all_titles = [p for p in k3 if i in p]
		arr.append(all_titles)
	for i in comparison_string:
		all_titles = [p for p in k3 if i in p]
		comparison_list.append(all_titles)
	arr=tuple(filter(lambda x:x!=[], arr))
	mytuplelist = [tuple(item) for item in arr]
	mylist = list(set(mytuplelist))
	comparison_list_new = [elem for elem in arr if elem not in comparison_list ]
	# index=k3.index(comparison_list_new[0][0])
	num1= int(len(comparison_list_new))
	num2 = int(len(comparison_list_adana2))
	stringg = comparison_list_new[-1:]
	if num1 > num2:
		for i in range(len(comparison_list_new)):
			comparison_list_adana2.append(comparison_list_new[i])
			index=k3.index(comparison_list_new[i][0])
		length=len(excel_df)
		url=hrefs[index]
		page = requests.get("http:"+url)
		data = page.text
		soup_text = BeautifulSoup(data, 'html.parser')
		for line in soup_text.find_all('div',class_='icerik'):
			page_arr.append(line.get_text())
		page_arr =  [x.replace('\xa0', '') for x in page_arr]
		page_arr =  [x.replace('\r', '') for x in page_arr]
		page_arr =  [x.replace('\n', '') for x in page_arr]
		page_arr =  [x.replace(' ', '') for x in page_arr]
		page_arr =  [x.replace('/', '') for x in page_arr]
		page_arr =  [x.lower() for x in page_arr]
		for i in page_arr:
			page_substring = [p for p in page_arr if ("2911" or "5944") in p]
			print(page_substring)
		if len(page_substring) != 0:	
			messagebox.showinfo("Adana","Yeni Duyuru Yayınlandı !!!!")
			label_pos_adana = tk.Label(lower_frame,text="Adana Valiliğinde yeni bildiri yayınlandı")
			label_pos_adana.pack()
			root.after(60000,label_pos_adana.destroy)
			city = "Adana"
			excel_df.loc[length+1] = ["🗸",city,comparison_list_new[-1:][0],url]
			print(num1," ",num2)
			num2+=1
			print(num1," ",num2)
			adana_check_2()
		else:
			messagebox.showinfo("Adana","Yeni Duyuru Yayınlandı !!!!")
			label_pos_adana = tk.Label(lower_frame,text="Adana Valiliğinde yeni bildiri yayınlandı")
			city = "Adana"
			excel_df.loc[length+1] = ["X",city,comparison_list_new[-1:][0],url]
			adana_check_2()
	
		

	else:
		label_negative_adana = tk.Label(lower_frame,text="Adana valiliğinde 5 dakika sonra tekrardan arama yapılacak")
		label_negative_adana.pack()
		root.after(60000,label_negative_adana.destroy)
		root.after(60000,lambda:adana_press_scraping())


def batman_check(): 
    res = mb.askquestion('batman Arama',  
                         'batman Valiliğinde Aramaya Devam Edilsin mi ?') 
      
    if res == 'yes' :
    	root.after(1000,lambda:batman_web_scraping())   
    else : 
        mb.showinfo('Return', 'Returning to main application')

def batman_web_scraping():
	comparison_string= ["",""]
	comparison_list=[]
	a = []
	hrefs=[]
	arr= []
	page_arr = []
	urls= []
	final_urls = []
	word = get()
	url = "http://batman.gov.tr/duyurular"
	page = requests.get(url)
	data = page.text
	soup = BeautifulSoup(data, 'html.parser')
	text = soup.find_all('a',class_='announce-text')
	for line in soup.find_all('a',class_='announce-text'):
		a.append(line.get_text())
	for line in soup.find_all('a',class_='announce-text'):
		hrefs.append(line.get('href'))
	word=[y.lower() for y in word]
	k = [x.replace(' ', '') for x in a]
	k2= k = [x.replace('\r', '') for x in k]
	k3 = k = [x.replace('\n', '') for x in k2]
	k3=[x.lower() for x in k3]
	hrefs = list(dict.fromkeys(hrefs))

	for i in word:
		all_titles = [p for p in k3 if i in p]
		arr.append(all_titles)
	for i in comparison_string:
		all_titles = [p for p in k3 if i in p]
		comparison_list.append(all_titles)
	arr=tuple(filter(lambda x:x!=[], arr))
	mytuplelist = [tuple(item) for item in arr]
	mylist = list(set(mytuplelist))
	comparison_list_new = [elem for elem in arr if elem not in comparison_list ]
	# index=k3.index(comparison_list_new[0][0])
	num1= int(len(comparison_list_new))
	num2 = int(len(comparison_list_batman))
	batman_count = 0
	
	if num1 > num2:
		for i in range(len(comparison_list_new)):
			comparison_list_batman.append(comparison_list_new[i])
			index=k3.index(comparison_list_new[i][0])
			length=len(excel_df)
			urls.append(index)	
		url=hrefs[index]
		for i in urls:
			final_urls.append(hrefs[i])

		page = requests.get("http:"+url)
		data = page.text
		soup_text = BeautifulSoup(data, 'html.parser')
		for line in soup_text.find_all('div',class_='icerik'):
			page_arr.append(line.get_text())
		page_arr = [x.replace('\xa0', '') for x in page_arr]
		page_arr = [x.replace('\r', '') for x in page_arr]
		page_arr = [x.replace('\n', '') for x in page_arr]
		page_arr = [x.replace(' ', '') for x in page_arr]
		page_arr = [x.replace('/', '') for x in page_arr]
		page_arr=[x.lower() for x in page_arr]
		for i in page_arr:
			page_substring = [p for p in page_arr if ("2911" or "5944") in p]
			print(page_substring)
		if len(page_substring) != 0:
			messagebox.showinfo("Batman","Yeni Duyuru Yayınlandı !!!!")
			label_pos_batman = tk.Label(lower_frame,text="Batman Valiliğinde yeni bildiri yayınlandı")
			label_pos_batman.pack()
			root.after(60000,label_pos_batman.destroy)
			city = "Batman"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) ==1:
				for i in range(len(comparison_list_new[0])):
					index=k3.index(comparison_list_new[0][i])
					length=len(excel_df)
					urls.append(index)
				url=hrefs[index]
				for i in urls:
					final_urls.append(hrefs[i])
				final_urls = list(dict.fromkeys(final_urls))
				print(final_urls)
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["+",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["+",city,comparison_list_new[-1:][0],url]
			
			print(num1," ",num2)
			num2+=1
			print(num1," ",num2)
			batman_check()
		else:
			messagebox.showinfo("Batman","Yeni Duyuru Yayınlandı !!!!")
			label_pos_batman = tk.Label(lower_frame,text="Batman Valiliğinde yeni bildiri yayınlandı")
			city = "Batman"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) == 1:
				for i in range(len(comparison_list_new[0])):
					for i in range(len(comparison_list_new[0])):
						index=k3.index(comparison_list_new[0][i])
						length=len(excel_df)
						urls.append(index)
					url=hrefs[index]
					for i in urls:
						final_urls.append(hrefs[i])
					final_urls = list(dict.fromkeys(final_urls))
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["-",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["x",city,comparison_list_new[-1:][0],url]
			batman_check()
		

	else:
		label_negative_batman = tk.Label(lower_frame,text="Batman valiliğinde 5 dakika sonra tekrardan arama yapılacak")
		label_negative_batman.pack()
		root.after(60000,label_negative_batman.destroy)
		root.after(60000,lambda:batman_web_scraping())

def elazığ_check(): 
    res = mb.askquestion('Elazığ Arama',  
                         'Elazığ Valiliğinde Aramaya Devam Edilsin mi ?') 
      
    if res == 'yes' :
    	root.after(1000,lambda:elazığ_web_scraping())   
    else : 
        mb.showinfo('Return', 'Returning to main application')
def elazığ_web_scraping():
	comparison_string= ["",""]
	comparison_list=[]
	a = []
	hrefs=[]
	arr= []
	page_arr = []
	urls= []
	final_urls = []
	word =get()
	url = "http://www.elazig.gov.tr/duyurular"
	page = requests.get(url)
	data = page.text
	soup = BeautifulSoup(data, 'html.parser')
	text = soup.find_all('a',class_='announce-text')
	for line in soup.find_all('a',class_='announce-text'):
		a.append(line.get_text())
	for line in soup.find_all('a',class_='announce-text'):
		hrefs.append(line.get('href'))
	word=[y.lower() for y in word]
	k = [x.replace(' ', '') for x in a]
	k2= k = [x.replace('\r', '') for x in k]
	k3 = k = [x.replace('\n', '') for x in k2]
	k3=[x.lower() for x in k3]
	hrefs = list(dict.fromkeys(hrefs))

	for i in word:
		all_titles = [p for p in k3 if i in p]
		arr.append(all_titles)
	for i in comparison_string:
		all_titles = [p for p in k3 if i in p]
		comparison_list.append(all_titles)
	arr=tuple(filter(lambda x:x!=[], arr))
	mytuplelist = [tuple(item) for item in arr]
	mylist = list(set(mytuplelist))
	comparison_list_new = [elem for elem in arr if elem not in comparison_list ]
	# index=k3.index(comparison_list_new[0][0])
	num1= int(len(comparison_list_new))
	num2 = int(len(comparison_list_elazığ))
	elazığ_count = 0
	
	if num1 > num2:
		for i in range(len(comparison_list_new)):
			comparison_list_elazığ.append(comparison_list_new[i])
			index=k3.index(comparison_list_new[i][0])
			length=len(excel_df)
			urls.append(index)	
		url=hrefs[index]
		for i in urls:
			final_urls.append(hrefs[i])

		page = requests.get("http:"+url)
		data = page.text
		soup_text = BeautifulSoup(data, 'html.parser')
		for line in soup_text.find_all('div',class_='icerik'):
			page_arr.append(line.get_text())
		page_arr = [x.replace('\xa0', '') for x in page_arr]
		page_arr = [x.replace('\r', '') for x in page_arr]
		page_arr = [x.replace('\n', '') for x in page_arr]
		page_arr = [x.replace(' ', '') for x in page_arr]
		page_arr = [x.replace('/', '') for x in page_arr]
		page_arr=[x.lower() for x in page_arr]
		for i in page_arr:
			page_substring = [p for p in page_arr if ("2911" or "5944") in p]
			print(page_substring)
		if len(page_substring) != 0:
			messagebox.showinfo("Elazığ","Yeni Duyuru Yayınlandı !!!!")
			label_pos_elazığ = tk.Label(lower_frame,text="Elazığ Valiliğinde yeni bildiri yayınlandı")
			label_pos_elazığ.pack()
			root.after(60000,label_pos_elazığ.destroy)
			city = "Elazığ"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) ==1:
				for i in range(len(comparison_list_new[0])):
					index=k3.index(comparison_list_new[0][i])
					length=len(excel_df)
					urls.append(index)
				url=hrefs[index]
				for i in urls:
					final_urls.append(hrefs[i])
				final_urls = list(dict.fromkeys(final_urls))
				print(final_urls)
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["+",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["+",city,comparison_list_new[-1:][0],url]
			
			print(num1," ",num2)
			num2+=1
			print(num1," ",num2)
			elazığ_check()
		else:
			messagebox.showinfo("Elazığ","Yeni Duyuru Yayınlandı !!!!")
			label_pos_elazığ = tk.Label(lower_frame,text="Elazığ Valiliğinde yeni bildiri yayınlandı")
			city = "Elazığ"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) == 1:
				for i in range(len(comparison_list_new[0])):
					for i in range(len(comparison_list_new[0])):
						index=k3.index(comparison_list_new[0][i])
						length=len(excel_df)
						urls.append(index)
					url=hrefs[index]
					for i in urls:
						final_urls.append(hrefs[i])
					final_urls = list(dict.fromkeys(final_urls))
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["-",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["x",city,comparison_list_new[-1:][0],url]
			elazığ_check()
		

	else:
		label_negative_elazığ = tk.Label(lower_frame,text="Elazığ valiliğinde 5 dakika sonra tekrardan arama yapılacak")
		label_negative_elazığ.pack()
		root.after(60000,label_negative_elazığ.destroy)
		root.after(60000,lambda:elazığ_web_scraping())
def gaziantep_check(): 
    res = mb.askquestion('Gaziantep Arama',  
                         'Gaziantep Valiliğinde Aramaya Devam Edilsin mi ?') 
      
    if res == 'yes' :
    	root.after(1000,lambda:gaziantep_web_scraping())   
    else : 
        mb.showinfo('Return', 'Returning to main application')
def gaziantep_web_scraping():
	comparison_string= ["",""]
	comparison_list=[]
	a = []
	hrefs=[]
	arr= []
	page_arr = []
	urls= []
	final_urls = []
	word =get()
	url = "http://gaziantep.gov.tr/duyurular"
	page = requests.get(url)
	data = page.text
	soup = BeautifulSoup(data, 'html.parser')
	text = soup.find_all('a',class_='announce-text')
	for line in soup.find_all('a',class_='announce-text'):
		a.append(line.get_text())
	for line in soup.find_all('a',class_='announce-text'):
		hrefs.append(line.get('href'))
	word=[y.lower() for y in word]
	k = [x.replace(' ', '') for x in a]
	k2= k = [x.replace('\r', '') for x in k]
	k3 = k = [x.replace('\n', '') for x in k2]
	k3=[x.lower() for x in k3]
	hrefs = list(dict.fromkeys(hrefs))

	for i in word:
		all_titles = [p for p in k3 if i in p]
		arr.append(all_titles)
	for i in comparison_string:
		all_titles = [p for p in k3 if i in p]
		comparison_list.append(all_titles)
	arr=tuple(filter(lambda x:x!=[], arr))
	mytuplelist = [tuple(item) for item in arr]
	mylist = list(set(mytuplelist))
	comparison_list_new = [elem for elem in arr if elem not in comparison_list ]
	# index=k3.index(comparison_list_new[0][0])
	num1= int(len(comparison_list_new))
	num2 = int(len(comparison_list_gaziantep))
	gaziantep_count = 0
	
	if num1 > num2:
		for i in range(len(comparison_list_new)):
			comparison_list_gaziantep.append(comparison_list_new[i])
			index=k3.index(comparison_list_new[i][0])
			length=len(excel_df)
			urls.append(index)	
		url=hrefs[index]
		for i in urls:
			final_urls.append(hrefs[i])

		page = requests.get("http:"+url)
		data = page.text
		soup_text = BeautifulSoup(data, 'html.parser')
		for line in soup_text.find_all('div',class_='icerik'):
			page_arr.append(line.get_text())
		page_arr = [x.replace('\xa0', '') for x in page_arr]
		page_arr = [x.replace('\r', '') for x in page_arr]
		page_arr = [x.replace('\n', '') for x in page_arr]
		page_arr = [x.replace(' ', '') for x in page_arr]
		page_arr = [x.replace('/', '') for x in page_arr]
		page_arr=[x.lower() for x in page_arr]
		for i in page_arr:
			page_substring = [p for p in page_arr if ("2911" or "5944") in p]
			print(page_substring)
		if len(page_substring) != 0:
			messagebox.showinfo("Gaziantep","Yeni Duyuru Yayınlandı !!!!")
			label_pos_gaziantep = tk.Label(lower_frame,text="Gaziantep Valiliğinde yeni bildiri yayınlandı")
			label_pos_gaziantep.pack()
			root.after(60000,label_pos_gaziantep.destroy)
			city = "Gaziantep"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) ==1:
				for i in range(len(comparison_list_new[0])):
					index=k3.index(comparison_list_new[0][i])
					length=len(excel_df)
					urls.append(index)
				url=hrefs[index]
				for i in urls:
					final_urls.append(hrefs[i])
				final_urls = list(dict.fromkeys(final_urls))
				print(final_urls)
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["+",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["+",city,comparison_list_new[-1:][0],url]
			
			print(num1," ",num2)
			num2+=1
			print(num1," ",num2)
			gaziantep_check()
		else:
			messagebox.showinfo("Gaziantep","Yeni Duyuru Yayınlandı !!!!")
			label_pos_gaziantep = tk.Label(lower_frame,text="Gaziantep Valiliğinde yeni bildiri yayınlandı")
			city = "Gaziantep"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) == 1:
				for i in range(len(comparison_list_new[0])):
					for i in range(len(comparison_list_new[0])):
						index=k3.index(comparison_list_new[0][i])
						length=len(excel_df)
						urls.append(index)
					url=hrefs[index]
					for i in urls:
						final_urls.append(hrefs[i])
					final_urls = list(dict.fromkeys(final_urls))
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["-",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["x",city,comparison_list_new[-1:][0],url]
			gaziantep_check()
		

	else:
		label_negative_gaziantep = tk.Label(lower_frame,text="Gaziantep valiliğinde 5 dakika sonra tekrardan arama yapılacak")
		label_negative_gaziantep.pack()
		root.after(60000,label_negative_gaziantep.destroy)
		root.after(60000,lambda:gaziantep_web_scraping())
def hakkari_check(): 
    res = mb.askquestion('Hakkari Arama',  
                         'Hakkari Valiliğinde Aramaya Devam Edilsin mi ?') 
      
    if res == 'yes' :
    	root.after(1000,lambda:hakkari_web_scraping())   
    else : 
        mb.showinfo('Return', 'Returning to main application')
def hakkari_web_scraping():
	comparison_string= ["",""]
	comparison_list=[]
	a = []
	hrefs=[]
	arr= []
	page_arr = []
	urls= []
	final_urls = []
	word =get()
	url = "http://hakkari.gov.tr/duyurular"
	page = requests.get(url)
	data = page.text
	soup = BeautifulSoup(data, 'html.parser')
	text = soup.find_all('a',class_='announce-text')
	for line in soup.find_all('a',class_='announce-text'):
		a.append(line.get_text())
	for line in soup.find_all('a',class_='announce-text'):
		hrefs.append(line.get('href'))
	word=[y.lower() for y in word]
	k = [x.replace(' ', '') for x in a]
	k2= k = [x.replace('\r', '') for x in k]
	k3 = k = [x.replace('\n', '') for x in k2]
	k3=[x.lower() for x in k3]
	hrefs = list(dict.fromkeys(hrefs))

	for i in word:
		all_titles = [p for p in k3 if i in p]
		arr.append(all_titles)
	for i in comparison_string:
		all_titles = [p for p in k3 if i in p]
		comparison_list.append(all_titles)
	arr=tuple(filter(lambda x:x!=[], arr))
	mytuplelist = [tuple(item) for item in arr]
	mylist = list(set(mytuplelist))
	comparison_list_new = [elem for elem in arr if elem not in comparison_list ]
	# index=k3.index(comparison_list_new[0][0])
	num1= int(len(comparison_list_new))
	num2 = int(len(comparison_list_hakkari))
	hakkari_count = 0
	
	if num1 > num2:
		for i in range(len(comparison_list_new)):
			comparison_list_hakkari.append(comparison_list_new[i])
			index=k3.index(comparison_list_new[i][0])
			length=len(excel_df)
			urls.append(index)	
		url=hrefs[index]
		for i in urls:
			final_urls.append(hrefs[i])

		page = requests.get("http:"+url)
		data = page.text
		soup_text = BeautifulSoup(data, 'html.parser')
		for line in soup_text.find_all('div',class_='icerik'):
			page_arr.append(line.get_text())
		page_arr = [x.replace('\xa0', '') for x in page_arr]
		page_arr = [x.replace('\r', '') for x in page_arr]
		page_arr = [x.replace('\n', '') for x in page_arr]
		page_arr = [x.replace(' ', '') for x in page_arr]
		page_arr = [x.replace('/', '') for x in page_arr]
		page_arr=[x.lower() for x in page_arr]
		for i in page_arr:
			page_substring = [p for p in page_arr if ("2911" or "5944") in p]
			print(page_substring)
		if len(page_substring) != 0:
			messagebox.showinfo("Hakkari","Yeni Duyuru Yayınlandı !!!!")
			label_pos_hakkari = tk.Label(lower_frame,text="Hakkari Valiliğinde yeni bildiri yayınlandı")
			label_pos_hakkari.pack()
			root.after(60000,label_pos_hakkari.destroy)
			city = "Hakkari"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) ==1:
				for i in range(len(comparison_list_new[0])):
					index=k3.index(comparison_list_new[0][i])
					length=len(excel_df)
					urls.append(index)
				url=hrefs[index]
				for i in urls:
					final_urls.append(hrefs[i])
				final_urls = list(dict.fromkeys(final_urls))
				print(final_urls)
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["+",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["+",city,comparison_list_new[-1:][0],url]
			
			print(num1," ",num2)
			num2+=1
			print(num1," ",num2)
			hakkari_check()
		else:
			messagebox.showinfo("Hakkari","Yeni Duyuru Yayınlandı !!!!")
			label_pos_hakkari = tk.Label(lower_frame,text="Hakkari Valiliğinde yeni bildiri yayınlandı")
			city = "Hakkari"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) == 1:
				for i in range(len(comparison_list_new[0])):
					for i in range(len(comparison_list_new[0])):
						index=k3.index(comparison_list_new[0][i])
						length=len(excel_df)
						urls.append(index)
					url=hrefs[index]
					for i in urls:
						final_urls.append(hrefs[i])
					final_urls = list(dict.fromkeys(final_urls))
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["-",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["x",city,comparison_list_new[-1:][0],url]
			hakkari_check()
		

	else:
		label_negative_hakkari = tk.Label(lower_frame,text="Hakkari valiliğinde 5 dakika sonra tekrardan arama yapılacak")
		label_negative_hakkari.pack()
		root.after(60000,label_negative_hakkari.destroy)
		root.after(60000,lambda:hakkari_web_scraping())
def mardin_check(): 
    res = mb.askquestion('Mardin Arama',  
                         'Mardin Valiliğinde Aramaya Devam Edilsin mi ?') 
      
    if res == 'yes' :
    	root.after(1000,lambda:mardin_web_scraping())   
    else : 
        mb.showinfo('Return', 'Returning to the main application')
def mardin_web_scraping():
	comparison_string= ["",""]
	comparison_list=[]
	a = []
	hrefs=[]
	arr= []
	page_arr = []
	urls= []
	final_urls = []
	word =get()
	url = "http://mardin.gov.tr/duyurular"
	page = requests.get(url)
	data = page.text
	soup = BeautifulSoup(data, 'html.parser')
	text = soup.find_all('a',class_='announce-text')
	for line in soup.find_all('a',class_='announce-text'):
		a.append(line.get_text())
	for line in soup.find_all('a',class_='announce-text'):
		hrefs.append(line.get('href'))
	word=[y.lower() for y in word]
	k = [x.replace(' ', '') for x in a]
	k2= k = [x.replace('\r', '') for x in k]
	k3 = k = [x.replace('\n', '') for x in k2]
	k3=[x.lower() for x in k3]
	hrefs = list(dict.fromkeys(hrefs))

	for i in word:
		all_titles = [p for p in k3 if i in p]
		arr.append(all_titles)
	for i in comparison_string:
		all_titles = [p for p in k3 if i in p]
		comparison_list.append(all_titles)
	arr=tuple(filter(lambda x:x!=[], arr))
	mytuplelist = [tuple(item) for item in arr]
	mylist = list(set(mytuplelist))
	comparison_list_new = [elem for elem in arr if elem not in comparison_list ]
	# index=k3.index(comparison_list_new[0][0])
	num1= int(len(comparison_list_new))
	num2 = int(len(comparison_list_mardin))
	mardin_count = 0
	
	if num1 > num2:
		for i in range(len(comparison_list_new)):
			comparison_list_mardin.append(comparison_list_new[i])
			index=k3.index(comparison_list_new[i][0])
			length=len(excel_df)
			urls.append(index)	
		url=hrefs[index]
		for i in urls:
			final_urls.append(hrefs[i])

		page = requests.get("http:"+url)
		data = page.text
		soup_text = BeautifulSoup(data, 'html.parser')
		for line in soup_text.find_all('div',class_='icerik'):
			page_arr.append(line.get_text())
		page_arr = [x.replace('\xa0', '') for x in page_arr]
		page_arr = [x.replace('\r', '') for x in page_arr]
		page_arr = [x.replace('\n', '') for x in page_arr]
		page_arr = [x.replace(' ', '') for x in page_arr]
		page_arr = [x.replace('/', '') for x in page_arr]
		page_arr=[x.lower() for x in page_arr]
		for i in page_arr:
			page_substring = [p for p in page_arr if ("2911" or "5944") in p]
			print(page_substring)
		if len(page_substring) != 0:
			messagebox.showinfo("Mardin","Yeni Duyuru Yayınlandı !!!!")
			label_pos_mardin = tk.Label(lower_frame,text="Mardin Valiliğinde yeni bildiri yayınlandı")
			label_pos_mardin.pack()
			root.after(60000,label_pos_mardin.destroy)
			city = "Mardin"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) ==1:
				for i in range(len(comparison_list_new[0])):
					index=k3.index(comparison_list_new[0][i])
					length=len(excel_df)
					urls.append(index)
				url=hrefs[index]
				for i in urls:
					final_urls.append(hrefs[i])
				final_urls = list(dict.fromkeys(final_urls))
				print(final_urls)
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["+",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["+",city,comparison_list_new[-1:][0],url]
			
			print(num1," ",num2)
			num2+=1
			print(num1," ",num2)
			mardin_check()
		else:
			messagebox.showinfo("Mardin","Yeni Duyuru Yayınlandı !!!!")
			label_pos_mardin = tk.Label(lower_frame,text="Mardin Valiliğinde yeni bildiri yayınlandı")
			city = "Mardin"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) == 1:
				for i in range(len(comparison_list_new[0])):
					for i in range(len(comparison_list_new[0])):
						index=k3.index(comparison_list_new[0][i])
						length=len(excel_df)
						urls.append(index)
					url=hrefs[index]
					for i in urls:
						final_urls.append(hrefs[i])
					final_urls = list(dict.fromkeys(final_urls))
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["-",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["x",city,comparison_list_new[-1:][0],url]
			mardin_check()
		

	else:
		label_negative_mardin = tk.Label(lower_frame,text="Mardin valiliğinde 5 dakika sonra tekrardan arama yapılacak")
		label_negative_mardin.pack()
		root.after(60000,label_negative_mardin.destroy)
		root.after(60000,lambda:mardin_web_scraping())
def muğla_check(): 
    res = mb.askquestion('Muğla Arama',  
                         'Muğla Valiliğinde Aramaya Devam Edilsin mi ?') 
      
    if res == 'yes' :
    	root.after(1000,lambda:muğla_web_scraping())   
    else : 
        mb.showinfo('Return', 'Returning to the main application')
def muğla_web_scraping():
	comparison_string= ["",""]
	comparison_list=[]
	a = []
	hrefs=[]
	arr= []
	page_arr = []
	urls= []
	final_urls = []
	word =get()
	url = "http://mugla.gov.tr/duyurular"
	page = requests.get(url)
	data = page.text
	soup = BeautifulSoup(data, 'html.parser')
	text = soup.find_all('a',class_='announce-text')
	for line in soup.find_all('a',class_='announce-text'):
		a.append(line.get_text())
	for line in soup.find_all('a',class_='announce-text'):
		hrefs.append(line.get('href'))
	word=[y.lower() for y in word]
	k = [x.replace(' ', '') for x in a]
	k2= k = [x.replace('\r', '') for x in k]
	k3 = k = [x.replace('\n', '') for x in k2]
	k3=[x.lower() for x in k3]
	hrefs = list(dict.fromkeys(hrefs))

	for i in word:
		all_titles = [p for p in k3 if i in p]
		arr.append(all_titles)
	for i in comparison_string:
		all_titles = [p for p in k3 if i in p]
		comparison_list.append(all_titles)
	arr=tuple(filter(lambda x:x!=[], arr))
	mytuplelist = [tuple(item) for item in arr]
	mylist = list(set(mytuplelist))
	comparison_list_new = [elem for elem in arr if elem not in comparison_list ]
	# index=k3.index(comparison_list_new[0][0])
	num1= int(len(comparison_list_new))
	num2 = int(len(comparison_list_muğla))
	muğla_count = 0
	
	if num1 > num2:
		for i in range(len(comparison_list_new)):
			comparison_list_muğla.append(comparison_list_new[i])
			index=k3.index(comparison_list_new[i][0])
			length=len(excel_df)
			urls.append(index)	
		url=hrefs[index]
		for i in urls:
			final_urls.append(hrefs[i])

		page = requests.get("http:"+url)
		data = page.text
		soup_text = BeautifulSoup(data, 'html.parser')
		for line in soup_text.find_all('div',class_='icerik'):
			page_arr.append(line.get_text())
		page_arr = [x.replace('\xa0', '') for x in page_arr]
		page_arr = [x.replace('\r', '') for x in page_arr]
		page_arr = [x.replace('\n', '') for x in page_arr]
		page_arr = [x.replace(' ', '') for x in page_arr]
		page_arr = [x.replace('/', '') for x in page_arr]
		page_arr=[x.lower() for x in page_arr]
		for i in page_arr:
			page_substring = [p for p in page_arr if ("2911" or "5944") in p]
			print(page_substring)
		if len(page_substring) != 0:
			messagebox.showinfo("Muğla","Yeni Duyuru Yayınlandı !!!!")
			label_pos_muğla = tk.Label(lower_frame,text="Muğla Valiliğinde yeni bildiri yayınlandı")
			label_pos_muğla.pack()
			root.after(60000,label_pos_muğla.destroy)
			city = "Muğla"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) ==1:
				for i in range(len(comparison_list_new[0])):
					index=k3.index(comparison_list_new[0][i])
					length=len(excel_df)
					urls.append(index)
				url=hrefs[index]
				for i in urls:
					final_urls.append(hrefs[i])
				final_urls = list(dict.fromkeys(final_urls))
				print(final_urls)
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["+",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["+",city,comparison_list_new[-1:][0],url]
			
			print(num1," ",num2)
			num2+=1
			print(num1," ",num2)
			muğla_check()
		else:
			messagebox.showinfo("Muğla","Yeni Duyuru Yayınlandı !!!!")
			label_pos_muğla = tk.Label(lower_frame,text="Muğla Valiliğinde yeni bildiri yayınlandı")
			city = "Muğla"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) == 1:
				for i in range(len(comparison_list_new[0])):
					for i in range(len(comparison_list_new[0])):
						index=k3.index(comparison_list_new[0][i])
						length=len(excel_df)
						urls.append(index)
					url=hrefs[index]
					for i in urls:
						final_urls.append(hrefs[i])
					final_urls = list(dict.fromkeys(final_urls))
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["-",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["x",city,comparison_list_new[-1:][0],url]
			muğla_check()
		

	else:
		label_negative_muğla = tk.Label(lower_frame,text="Muğla valiliğinde 5 dakika sonra tekrardan arama yapılacak")
		label_negative_muğla.pack()
		root.after(60000,label_negative_muğla.destroy)
		root.after(60000,lambda:muğla_web_scraping())

def muş_check(): 
    res = mb.askquestion('Muş Arama',  
                         'Muş Valiliğinde Aramaya Devam Edilsin mi ?') 
      
    if res == 'yes' :
    	root.after(1000,lambda:muş_web_scraping())   
    else : 
        mb.showinfo('Return', 'Returning to the main application')
def muş_web_scraping():
	comparison_string= ["",""]
	comparison_list=[]
	a = []
	hrefs=[]
	arr= []
	page_arr = []
	urls= []
	final_urls = []
	word =get()
	url = "http://mus.gov.tr/duyurular"
	page = requests.get(url)
	data = page.text
	soup = BeautifulSoup(data, 'html.parser')
	text = soup.find_all('a',class_='announce-text')
	for line in soup.find_all('a',class_='announce-text'):
		a.append(line.get_text())
	for line in soup.find_all('a',class_='announce-text'):
		hrefs.append(line.get('href'))
	word=[y.lower() for y in word]
	k = [x.replace(' ', '') for x in a]
	k2= k = [x.replace('\r', '') for x in k]
	k3 = k = [x.replace('\n', '') for x in k2]
	k3=[x.lower() for x in k3]
	hrefs = list(dict.fromkeys(hrefs))

	for i in word:
		all_titles = [p for p in k3 if i in p]
		arr.append(all_titles)
	for i in comparison_string:
		all_titles = [p for p in k3 if i in p]
		comparison_list.append(all_titles)
	arr=tuple(filter(lambda x:x!=[], arr))
	mytuplelist = [tuple(item) for item in arr]
	mylist = list(set(mytuplelist))
	comparison_list_new = [elem for elem in arr if elem not in comparison_list ]
	# index=k3.index(comparison_list_new[0][0])
	num1= int(len(comparison_list_new))
	num2 = int(len(comparison_list_muş))
	muş_count = 0
	
	if num1 > num2:
		for i in range(len(comparison_list_new)):
			comparison_list_muş.append(comparison_list_new[i])
			index=k3.index(comparison_list_new[i][0])
			length=len(excel_df)
			urls.append(index)	
		url=hrefs[index]
		for i in urls:
			final_urls.append(hrefs[i])

		page = requests.get("http:"+url)
		data = page.text
		soup_text = BeautifulSoup(data, 'html.parser')
		for line in soup_text.find_all('div',class_='icerik'):
			page_arr.append(line.get_text())
		page_arr = [x.replace('\xa0', '') for x in page_arr]
		page_arr = [x.replace('\r', '') for x in page_arr]
		page_arr = [x.replace('\n', '') for x in page_arr]
		page_arr = [x.replace(' ', '') for x in page_arr]
		page_arr = [x.replace('/', '') for x in page_arr]
		page_arr=[x.lower() for x in page_arr]
		for i in page_arr:
			page_substring = [p for p in page_arr if ("2911" or "5944") in p]
			print(page_substring)
		if len(page_substring) != 0:
			messagebox.showinfo("Muş","Yeni Duyuru Yayınlandı !!!!")
			label_pos_muş = tk.Label(lower_frame,text="Muş Valiliğinde yeni bildiri yayınlandı")
			label_pos_muş.pack()
			root.after(60000,label_pos_muş.destroy)
			city = "Muş"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) ==1:
				for i in range(len(comparison_list_new[0])):
					index=k3.index(comparison_list_new[0][i])
					length=len(excel_df)
					urls.append(index)
				url=hrefs[index]
				for i in urls:
					final_urls.append(hrefs[i])
				final_urls = list(dict.fromkeys(final_urls))
				print(final_urls)
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["+",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["+",city,comparison_list_new[-1:][0],url]
			
			print(num1," ",num2)
			num2+=1
			print(num1," ",num2)
			muş_check()
		else:
			messagebox.showinfo("Muş","Yeni Duyuru Yayınlandı !!!!")
			label_pos_muş = tk.Label(lower_frame,text="Muş Valiliğinde yeni bildiri yayınlandı")
			city = "Muş"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) == 1:
				for i in range(len(comparison_list_new[0])):
					for i in range(len(comparison_list_new[0])):
						index=k3.index(comparison_list_new[0][i])
						length=len(excel_df)
						urls.append(index)
					url=hrefs[index]
					for i in urls:
						final_urls.append(hrefs[i])
					final_urls = list(dict.fromkeys(final_urls))
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["-",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["x",city,comparison_list_new[-1:][0],url]
			muş_check()
		

	else:
		label_negative_muş = tk.Label(lower_frame,text="Muş valiliğinde 5 dakika sonra tekrardan arama yapılacak")
		label_negative_muş.pack()
		root.after(60000,label_negative_muş.destroy)
		root.after(60000,lambda:muş_web_scraping())
def şanlıurfa_check(): 
    res = mb.askquestion('Şanlıurfa Arama',  
                         'Şanlıurfa Valiliğinde Aramaya Devam Edilsin mi ?') 
      
    if res == 'yes' :
    	root.after(1000,lambda:şanlıurfa_web_scraping())   
    else : 
        mb.showinfo('Return', 'Returning to the main application')
def şanlıurfa_web_scraping():
	comparison_string= ["",""]
	comparison_list=[]
	a = []
	hrefs=[]
	arr= []
	page_arr = []
	urls= []
	final_urls = []
	word =get()
	url = "http://sanliurfa.gov.tr/duyurular"
	page = requests.get(url)
	data = page.text
	soup = BeautifulSoup(data, 'html.parser')
	text = soup.find_all('a',class_='announce-text')
	for line in soup.find_all('a',class_='announce-text'):
		a.append(line.get_text())
	for line in soup.find_all('a',class_='announce-text'):
		hrefs.append(line.get('href'))
	word=[y.lower() for y in word]
	k = [x.replace(' ', '') for x in a]
	k2= k = [x.replace('\r', '') for x in k]
	k3 = k = [x.replace('\n', '') for x in k2]
	k3=[x.lower() for x in k3]
	hrefs = list(dict.fromkeys(hrefs))

	for i in word:
		all_titles = [p for p in k3 if i in p]
		arr.append(all_titles)
	for i in comparison_string:
		all_titles = [p for p in k3 if i in p]
		comparison_list.append(all_titles)
	arr=tuple(filter(lambda x:x!=[], arr))
	mytuplelist = [tuple(item) for item in arr]
	mylist = list(set(mytuplelist))
	comparison_list_new = [elem for elem in arr if elem not in comparison_list ]
	# index=k3.index(comparison_list_new[0][0])
	num1= int(len(comparison_list_new))
	num2 = int(len(comparison_list_şanlıurfa))
	şanlıurfa_count = 0
	
	if num1 > num2:
		for i in range(len(comparison_list_new)):
			comparison_list_şanlıurfa.append(comparison_list_new[i])
			index=k3.index(comparison_list_new[i][0])
			length=len(excel_df)
			urls.append(index)	
		url=hrefs[index]
		for i in urls:
			final_urls.append(hrefs[i])

		page = requests.get("http:"+url)
		data = page.text
		soup_text = BeautifulSoup(data, 'html.parser')
		for line in soup_text.find_all('div',class_='icerik'):
			page_arr.append(line.get_text())
		page_arr = [x.replace('\xa0', '') for x in page_arr]
		page_arr = [x.replace('\r', '') for x in page_arr]
		page_arr = [x.replace('\n', '') for x in page_arr]
		page_arr = [x.replace(' ', '') for x in page_arr]
		page_arr = [x.replace('/', '') for x in page_arr]
		page_arr=[x.lower() for x in page_arr]
		for i in page_arr:
			page_substring = [p for p in page_arr if ("2911" or "5944") in p]
			print(page_substring)
		if len(page_substring) != 0:
			messagebox.showinfo("Şanlıurfa","Yeni Duyuru Yayınlandı !!!!")
			label_pos_şanlıurfa = tk.Label(lower_frame,text="Şanlıurfa Valiliğinde yeni bildiri yayınlandı")
			label_pos_şanlıurfa.pack()
			root.after(60000,label_pos_şanlıurfa.destroy)
			city = "Şanlıurfa"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) ==1:
				for i in range(len(comparison_list_new[0])):
					index=k3.index(comparison_list_new[0][i])
					length=len(excel_df)
					urls.append(index)
				url=hrefs[index]
				for i in urls:
					final_urls.append(hrefs[i])
				final_urls = list(dict.fromkeys(final_urls))
				print(final_urls)
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["+",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["+",city,comparison_list_new[-1:][0],url]
			
			print(num1," ",num2)
			num2+=1
			print(num1," ",num2)
			şanlıurfa_check()
		else:
			messagebox.showinfo("Şanlıurfa","Yeni Duyuru Yayınlandı !!!!")
			label_pos_şanlıurfa = tk.Label(lower_frame,text="Şanlıurfa Valiliğinde yeni bildiri yayınlandı")
			city = "Şanlıurfa"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) == 1:
				for i in range(len(comparison_list_new[0])):
					for i in range(len(comparison_list_new[0])):
						index=k3.index(comparison_list_new[0][i])
						length=len(excel_df)
						urls.append(index)
					url=hrefs[index]
					for i in urls:
						final_urls.append(hrefs[i])
					final_urls = list(dict.fromkeys(final_urls))
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["-",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["x",city,comparison_list_new[-1:][0],url]
			şanlıurfa_check()
		

	else:
		label_negative_şanlıurfa = tk.Label(lower_frame,text="Şanlıurfa valiliğinde 5 dakika sonra tekrardan arama yapılacak")
		label_negative_şanlıurfa.pack()
		root.after(60000,label_negative_şanlıurfa.destroy)
		root.after(60000,lambda:şanlıurfa_web_scraping())
def şırnak_check(): 
    res = mb.askquestion('Şırnak Arama',  
                         'Şırnak Valiliğinde Aramaya Devam Edilsin mi ?') 
      
    if res == 'yes' :
    	root.after(1000,lambda:şırnak_web_scraping())   
    else : 
        mb.showinfo('Return', 'Returning to the main application')
def şırnak_web_scraping():
	comparison_string= ["",""]
	comparison_list=[]
	a = []
	hrefs=[]
	arr= []
	page_arr = []
	urls= []
	final_urls = []
	word =get()
	url = "http://www.sirnak.gov.tr/basin-aciklamalari"
	page = requests.get(url)
	data = page.text
	soup = BeautifulSoup(data, 'html.parser')
	text = soup.find_all('a',class_='announce-text')
	for line in soup.find_all('a',class_='announce-text'):
		a.append(line.get_text())
	for line in soup.find_all('a',class_='announce-text'):
		hrefs.append(line.get('href'))
	word=[y.lower() for y in word]
	k = [x.replace(' ', '') for x in a]
	k2= k = [x.replace('\r', '') for x in k]
	k3 = k = [x.replace('\n', '') for x in k2]
	k3=[x.lower() for x in k3]
	hrefs = list(dict.fromkeys(hrefs))

	for i in word:
		all_titles = [p for p in k3 if i in p]
		arr.append(all_titles)
	for i in comparison_string:
		all_titles = [p for p in k3 if i in p]
		comparison_list.append(all_titles)
	arr=tuple(filter(lambda x:x!=[], arr))
	mytuplelist = [tuple(item) for item in arr]
	mylist = list(set(mytuplelist))
	comparison_list_new = [elem for elem in arr if elem not in comparison_list ]
	# index=k3.index(comparison_list_new[0][0])
	num1= int(len(comparison_list_new))
	num2 = int(len(comparison_list_şırnak))
	şırnak_count = 0
	
	if num1 > num2:
		for i in range(len(comparison_list_new)):
			comparison_list_şırnak.append(comparison_list_new[i])
			index=k3.index(comparison_list_new[i][0])
			length=len(excel_df)
			urls.append(index)	
		url=hrefs[index]
		for i in urls:
			final_urls.append(hrefs[i])

		page = requests.get("http:"+url)
		data = page.text
		soup_text = BeautifulSoup(data, 'html.parser')
		for line in soup_text.find_all('div',class_='icerik'):
			page_arr.append(line.get_text())
		page_arr = [x.replace('\xa0', '') for x in page_arr]
		page_arr = [x.replace('\r', '') for x in page_arr]
		page_arr = [x.replace('\n', '') for x in page_arr]
		page_arr = [x.replace(' ', '') for x in page_arr]
		page_arr = [x.replace('/', '') for x in page_arr]
		page_arr=[x.lower() for x in page_arr]
		for i in page_arr:
			page_substring = [p for p in page_arr if ("2911" or "5944") in p]
			print(page_substring)
		if len(page_substring) != 0:
			messagebox.showinfo("Şırnak","Yeni Duyuru Yayınlandı !!!!")
			label_pos_şırnak = tk.Label(lower_frame,text="Şırnak Valiliğinde yeni bildiri yayınlandı")
			label_pos_şırnak.pack()
			root.after(60000,label_pos_şırnak.destroy)
			city = "Şırnak"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) ==1:
				for i in range(len(comparison_list_new[0])):
					index=k3.index(comparison_list_new[0][i])
					length=len(excel_df)
					urls.append(index)
				url=hrefs[index]
				for i in urls:
					final_urls.append(hrefs[i])
				final_urls = list(dict.fromkeys(final_urls))
				print(final_urls)
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["+",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["+",city,comparison_list_new[-1:][0],url]
			
			print(num1," ",num2)
			num2+=1
			print(num1," ",num2)
			şırnak_check()
		else:
			messagebox.showinfo("Şırnak","Yeni Duyuru Yayınlandı !!!!")
			label_pos_şırnak = tk.Label(lower_frame,text="Şırnak Valiliğinde yeni bildiri yayınlandı")
			city = "Şırnak"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) == 1:
				for i in range(len(comparison_list_new[0])):
					for i in range(len(comparison_list_new[0])):
						index=k3.index(comparison_list_new[0][i])
						length=len(excel_df)
						urls.append(index)
					url=hrefs[index]
					for i in urls:
						final_urls.append(hrefs[i])
					final_urls = list(dict.fromkeys(final_urls))
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["-",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["x",city,comparison_list_new[-1:][0],url]
			şırnak_check()
		

	else:
		label_negative_şırnak = tk.Label(lower_frame,text="Şırnak valiliğinde 5 dakika sonra tekrardan arama yapılacak")
		label_negative_şırnak.pack()
		root.after(60000,label_negative_şırnak.destroy)
		root.after(60000,lambda:şırnak_web_scraping())
def tunceli_check(): 
    res = mb.askquestion('Tunceli Arama',  
                         'Tunceli Valiliğinde Aramaya Devam Edilsin mi ?') 
      
    if res == 'yes' :
    	root.after(1000,lambda:tunceli_web_scraping())   
    else : 
        mb.showinfo('Return', 'Returning to the main application')
def tunceli_web_scraping():
	comparison_string= ["",""]
	comparison_list=[]
	a = []
	hrefs=[]
	arr= []
	page_arr = []
	urls= []
	final_urls = []
	word =get()
	url = "http://tunceli.gov.tr/duyurular"
	page = requests.get(url)
	data = page.text
	soup = BeautifulSoup(data, 'html.parser')
	text = soup.find_all('a',class_='announce-text')
	for line in soup.find_all('a',class_='announce-text'):
		a.append(line.get_text())
	for line in soup.find_all('a',class_='announce-text'):
		hrefs.append(line.get('href'))
	word=[y.lower() for y in word]
	k = [x.replace(' ', '') for x in a]
	k2= k = [x.replace('\r', '') for x in k]
	k3 = k = [x.replace('\n', '') for x in k2]
	k3=[x.lower() for x in k3]
	hrefs = list(dict.fromkeys(hrefs))

	for i in word:
		all_titles = [p for p in k3 if i in p]
		arr.append(all_titles)
	for i in comparison_string:
		all_titles = [p for p in k3 if i in p]
		comparison_list.append(all_titles)
	arr=tuple(filter(lambda x:x!=[], arr))
	mytuplelist = [tuple(item) for item in arr]
	mylist = list(set(mytuplelist))
	comparison_list_new = [elem for elem in arr if elem not in comparison_list ]
	# index=k3.index(comparison_list_new[0][0])
	num1= int(len(comparison_list_new))
	num2 = int(len(comparison_list_tunceli))
	tunceli_count = 0
	
	if num1 > num2:
		for i in range(len(comparison_list_new)):
			comparison_list_tunceli.append(comparison_list_new[i])
			index=k3.index(comparison_list_new[i][0])
			length=len(excel_df)
			urls.append(index)	
		url=hrefs[index]
		for i in urls:
			final_urls.append(hrefs[i])

		page = requests.get("http:"+url)
		data = page.text
		soup_text = BeautifulSoup(data, 'html.parser')
		for line in soup_text.find_all('div',class_='icerik'):
			page_arr.append(line.get_text())
		page_arr = [x.replace('\xa0', '') for x in page_arr]
		page_arr = [x.replace('\r', '') for x in page_arr]
		page_arr = [x.replace('\n', '') for x in page_arr]
		page_arr = [x.replace(' ', '') for x in page_arr]
		page_arr = [x.replace('/', '') for x in page_arr]
		page_arr=[x.lower() for x in page_arr]
		for i in page_arr:
			page_substring = [p for p in page_arr if ("2911" or "5944") in p]
			print(page_substring)
		if len(page_substring) != 0:
			messagebox.showinfo("Tunceli","Yeni Duyuru Yayınlandı !!!!")
			label_pos_tunceli = tk.Label(lower_frame,text="Tunceli Valiliğinde yeni bildiri yayınlandı")
			label_pos_tunceli.pack()
			root.after(60000,label_pos_tunceli.destroy)
			city = "Tunceli"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) ==1:
				for i in range(len(comparison_list_new[0])):
					index=k3.index(comparison_list_new[0][i])
					length=len(excel_df)
					urls.append(index)
				url=hrefs[index]
				for i in urls:
					final_urls.append(hrefs[i])
				final_urls = list(dict.fromkeys(final_urls))
				print(final_urls)
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["+",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["+",city,comparison_list_new[-1:][0],url]
			
			print(num1," ",num2)
			num2+=1
			print(num1," ",num2)
			tunceli_check()
		else:
			messagebox.showinfo("Tunceli","Yeni Duyuru Yayınlandı !!!!")
			label_pos_tunceli = tk.Label(lower_frame,text="Tunceli Valiliğinde yeni bildiri yayınlandı")
			city = "Tunceli"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) == 1:
				for i in range(len(comparison_list_new[0])):
					for i in range(len(comparison_list_new[0])):
						index=k3.index(comparison_list_new[0][i])
						length=len(excel_df)
						urls.append(index)
					url=hrefs[index]
					for i in urls:
						final_urls.append(hrefs[i])
					final_urls = list(dict.fromkeys(final_urls))
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["-",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["x",city,comparison_list_new[-1:][0],url]
			tunceli_check()
		

	else:
		label_negative_tunceli = tk.Label(lower_frame,text="Tunceli valiliğinde 5 dakika sonra tekrardan arama yapılacak")
		label_negative_tunceli.pack()
		root.after(60000,label_negative_tunceli.destroy)
		root.after(60000,lambda:tunceli_web_scraping())
def van_check(): 
    res = mb.askquestion('Van Arama',  
                         'Van Valiliğinde Aramaya Devam Edilsin mi ?') 
      
    if res == 'yes' :
    	root.after(1000,lambda:van_web_scraping())   
    else : 
        mb.showinfo('Return', 'Returning to the main application')
def van_web_scraping():
	comparison_string= ["",""]
	comparison_list=[]
	a = []
	hrefs=[]
	arr= []
	page_arr = []
	urls= []
	final_urls = []
	word =get()
	url = "http://van.gov.tr/duyurular"
	page = requests.get(url)
	data = page.text
	soup = BeautifulSoup(data, 'html.parser')
	text = soup.find_all('a',class_='announce-text')
	for line in soup.find_all('a',class_='announce-text'):
		a.append(line.get_text())
	for line in soup.find_all('a',class_='announce-text'):
		hrefs.append(line.get('href'))
	word=[y.lower() for y in word]
	k = [x.replace(' ', '') for x in a]
	k2= k = [x.replace('\r', '') for x in k]
	k3 = k = [x.replace('\n', '') for x in k2]
	k3=[x.lower() for x in k3]
	hrefs = list(dict.fromkeys(hrefs))

	for i in word:
		all_titles = [p for p in k3 if i in p]
		arr.append(all_titles)
	for i in comparison_string:
		all_titles = [p for p in k3 if i in p]
		comparison_list.append(all_titles)
	arr=tuple(filter(lambda x:x!=[], arr))
	mytuplelist = [tuple(item) for item in arr]
	mylist = list(set(mytuplelist))
	comparison_list_new = [elem for elem in arr if elem not in comparison_list ]
	# index=k3.index(comparison_list_new[0][0])
	num1= int(len(comparison_list_new))
	num2 = int(len(comparison_list_van))
	van_count = 0
	
	if num1 > num2:
		for i in range(len(comparison_list_new)):
			comparison_list_van.append(comparison_list_new[i])
			index=k3.index(comparison_list_new[i][0])
			length=len(excel_df)
			urls.append(index)	
		url=hrefs[index]
		for i in urls:
			final_urls.append(hrefs[i])

		page = requests.get("http:"+url)
		data = page.text
		soup_text = BeautifulSoup(data, 'html.parser')
		for line in soup_text.find_all('div',class_='icerik'):
			page_arr.append(line.get_text())
		page_arr = [x.replace('\xa0', '') for x in page_arr]
		page_arr = [x.replace('\r', '') for x in page_arr]
		page_arr = [x.replace('\n', '') for x in page_arr]
		page_arr = [x.replace(' ', '') for x in page_arr]
		page_arr = [x.replace('/', '') for x in page_arr]
		page_arr=[x.lower() for x in page_arr]
		for i in page_arr:
			page_substring = [p for p in page_arr if ("2911" or "5944") in p]
			print(page_substring)
		if len(page_substring) != 0:
			messagebox.showinfo("Van","Yeni Duyuru Yayınlandı !!!!")
			label_pos_van = tk.Label(lower_frame,text="Van Valiliğinde yeni bildiri yayınlandı")
			label_pos_van.pack()
			root.after(60000,label_pos_van.destroy)
			city = "Van"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) ==1:
				for i in range(len(comparison_list_new[0])):
					index=k3.index(comparison_list_new[0][i])
					length=len(excel_df)
					urls.append(index)
				url=hrefs[index]
				for i in urls:
					final_urls.append(hrefs[i])
				final_urls = list(dict.fromkeys(final_urls))
				print(final_urls)
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["+",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["+",city,comparison_list_new[-1:][0],url]
			
			print(num1," ",num2)
			num2+=1
			print(num1," ",num2)
			van_check()
		else:
			messagebox.showinfo("Van","Yeni Duyuru Yayınlandı !!!!")
			label_pos_van = tk.Label(lower_frame,text="Van Valiliğinde yeni bildiri yayınlandı")
			city = "Van"
			if(len(comparison_list_new[0]) >= 2)and len(comparison_list_new) == 1:
				for i in range(len(comparison_list_new[0])):
					for i in range(len(comparison_list_new[0])):
						index=k3.index(comparison_list_new[0][i])
						length=len(excel_df)
						urls.append(index)
					url=hrefs[index]
					for i in urls:
						final_urls.append(hrefs[i])
					final_urls = list(dict.fromkeys(final_urls))
				for i in range(len(comparison_list_new[0])):
					length=len(excel_df)	
					excel_df.loc[length+1] = ["-",city,comparison_list_new[0][i],final_urls[i]]
					print(excel_df)
			else:
				length=len(excel_df)
				excel_df.loc[length+1] = ["x",city,comparison_list_new[-1:][0],url]
			van_check()
		

	else:
		label_negative_van = tk.Label(lower_frame,text="Van valiliğinde 5 dakika sonra tekrardan arama yapılacak")
		label_negative_van.pack()
		root.after(60000,label_negative_van.destroy)
		root.after(60000,lambda:van_web_scraping())


def google():
	webbrowser.open("www.Google.com")
	

def helpmenu():
	os.system('start Valilik_Arama_Kullanım_Kılavuzu.docx')



def searching_displaying_websites():
	# for url in keywords:
	# 	webbrowser.open(url)
	if len(keywords) == 0:
		global label_send
		label_send = tk.Label(lower_frame,text="Bir Anahtar Kelime Yazıp Yazdıklarımı ilete tıklayıp Tekrar Deneyiniz",font=30,bg="#ECECF2")
		label_send.pack()
	else:
		for term in keywords:
			url = "https://www.google.com.tr/search?q={}".format(keywords)
		webbrowser.open_new_tab(url)
		

def iterating_google_search():
	query = keywords
	if len(keywords) == 0:
		global label1
		label1= tk.Label(lower_frame,text="Aranacak Kelimeyi ekleyin.",font=60,bg="#ECECF2")
		label1.pack()
	else:
		for i in range(len(keywords)):
			for j in search(keywords[i], num=20, stop=10):
				websites.append(j)
		
		global scrollbar
		scrollbar=tk.Scrollbar(lower_frame,orient=tk.VERTICAL)
		
		scrollbar.pack(side=tk.RIGHT, fill= tk.Y)
		global T
		T=tk.Text(lower_frame,bg="#ECECF2",yscrollcommand = scrollbar.set)
		scrollbar.config(command=T.yview)
		T.pack()

		
		for display in websites:
			T.insert(tk.END,display+"\n")
			

def deleting_Screen():
	try:
		T
	except NameError:
		print("do nothing")
	else:
		T.destroy()
		scrollbar.destroy()
	try:
		label1
	except NameError:
		print("do nothing")
	else:
		label1.destroy()
	try:
		label
	except NameError:
		print("do nothing")
	else:
		label.destroy()
	try:
		label3
	except NameError:
		print("do nothing")
	else:
		label3.destroy()
	try:
		label_send
	except NameError:
		print("do nothing")
	else:
		label_send.destroy()
	try:
		label_excel
	except NameError:
		print("do nothing")
	else:
		label_excel.destroy()


def deleting_keywords():
	res.clear()
	print(res)

def saving_excel():
	export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
	excel_df.to_excel (export_file_path, index = False)
def displaying_excel():
	global label_excel
	label_excel=tk.Label(lower_frame,text=excel_df)
	label_excel.pack()

def start_search_all():
	adana_web_scraping()
	root.after(30000,lambda:batman_web_scraping())
	root.after(45000,lambda:elazığ_web_scraping())
	root.after(60000,lambda:gaziantep_web_scraping())
	root.after(75000,lambda:hakkari_web_scraping())
	root.after(90000,lambda:mardin_web_scraping())
	root.after(105000,lambda:muğla_web_scraping())
	root.after(120000,lambda:muş_web_scraping())
	root.after(135000,lambda:şanlıurfa_web_scraping())
	root.after(150000,lambda:şırnak_web_scraping())
	root.after(165000,lambda:tunceli_web_scraping())
	root.after(180000,lambda:van_web_scraping())
	root.after(195000,lambda:adana_press_scraping())
root = tk.Tk()
root.wm_iconbitmap('eshid.ico')
root.wm_title('Title')
root.geometry("700x500")
root.title("EŞHİD GOOGLE TARAMA")
root.configure(bg="#E5E6E2")
network_control()
img  = Image.open("eshidd.png") 
photo=ImageTk.PhotoImage(img)
lab=tk.Label(image=photo).place(x=0,y=0)
 
label = tk.Label(root,text="Eşhid Google Tarama",bg="#E5E6E2",font=40)
label.pack()



Frame=tk.Frame(root,bg="#4784BC",bd=5)
Frame.place(relx=0.5,rely=0.1,relwidth=0.75,relheight=0.132,anchor="n")

Entry=tk.Entry(Frame,font=40,bd=4)
Entry.place(relwidth=0.5,relheight=0.5,relx=0.01)



Keyentry=tk.Entry(Frame,font=40,bd=4)
Keyentry.place(relx=0.01,rely=0.82,anchor="w",relwidth=0.50,relheight=0.50)


buttonstart = tk.Button(Frame,text="Kelimeleri Google'da Ara",font=40,command =lambda:searching_displaying_websites())
buttonstart.place(relx = 0.60,rely=0.27,anchor='w',relwidth=0.38,relheight=0.50)



Buttonstop=tk.Button(Frame,text="Yazdıklarını İlet",font=40,command=lambda:get())
Buttonstop.place(relx=0.60,rely=0.85,anchor="w",relwidth=0.38,relheight=0.50)

lower_frame=tk.Entry(root,bg="#ECECF2",bd=5)
lower_frame.place(relx=0.5,rely=0.4,relwidth=0.8,relheight=0.5,anchor="n")


			

my_menu=tk.Menu(root)
root.config(menu=my_menu)

file_menu = tk.Menu(my_menu)
my_menu.add_cascade(label="Menü",menu=file_menu)
file_menu.add_command(label="Google'ı Aç",command=lambda:google())
file_menu.add_command(label="Google Sonuç Tarama",command=lambda:iterating_google_search())
file_menu.add_command(label="Google'da Arama",command=lambda:searching_displaying_websites())
file_menu.add_separator()
file_menu.add_command(label="Çıkış",command= root.quit)

################################################################################


website_menu=tk.Menu(my_menu)
my_menu.add_cascade(label="Duyurularda Arama",menu=website_menu)
website_menu.add_command(label="Tüm Valiliklerde Arama",command=lambda:start_search_all())
website_menu.add_command(label="Adana",command=lambda:adana_web_scraping())
website_menu.add_command(label="Adana2",command=lambda:adana_press_scraping())
website_menu.add_command(label="Batman",command=lambda:batman_web_scraping())
website_menu.add_command(label="Elazığ",command=lambda:elazığ_web_scraping())
website_menu.add_command(label="Gaziantep",command=lambda:gaziantep_web_scraping())
website_menu.add_command(label="Hakkari",command=lambda:hakkari_web_scraping())
website_menu.add_command(label="Mardin",command=lambda:mardin_web_scraping())
website_menu.add_command(label="Muğla",command=lambda:muğla_web_scraping())
website_menu.add_command(label="Muş",command=lambda:muş_web_scraping())
website_menu.add_command(label="Şanlıurfa",command=lambda:şanlıurfa_web_scraping())
website_menu.add_command(label="Şırnak",command=lambda:şırnak_web_scraping())
website_menu.add_command(label="Tunceli",command=lambda:tunceli_web_scraping())
website_menu.add_command(label="Van",command=lambda:van_web_scraping())


################################################################################

edit_menu = tk.Menu(my_menu)
my_menu.add_cascade(label="Belgeler",menu=edit_menu)
edit_menu.add_command(label="Kaydedilen Valilikleri Göster",command=lambda:displaying_excel())
edit_menu.add_command(label="Bulunan Siteleri Excel dosyasına aktar",command=lambda:saving_excel())

###############################################################################

delete_menu = tk.Menu(my_menu)
my_menu.add_cascade(label="Yazılanları Sil",menu=delete_menu)
delete_menu.add_command(label="Ekrandaki Yazıları Temizle",command=lambda:deleting_Screen())
delete_menu.add_command(label="Gönderilen Yazıları Temizle",command=lambda:deleting_keywords())

##############################################################################


help_menu = tk.Menu(my_menu)
my_menu.add_cascade(label="Help",menu=help_menu)
help_menu.add_command(label="Help",command=lambda:helpmenu())




# for j in search(query, tld="co.in", num=10, stop=10):
# 	websites.append(j) 
# print(websites)



root.mainloop()


