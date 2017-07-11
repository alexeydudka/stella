#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi, os, sys, re
from time import *
from st_object import * #импорт класса для работы с объектами
import st_functions #Импорт файла функций
from st_sql import *

htmlheader = ['Cache-control: private', 'Content-type: text/html; charset=utf-8\n\n'] #стандартные хедеры для инициализации страницы

db = Database() #Инициализация базы данных
objs = {} #Глобальная переменная хранящая все обьекты

def e_print(string='', encoding='utf8'): #Функция для вывода в браузер контента в utf-8
	sys.stdout.buffer.write(string.encode(encoding) + b'\n')

def do(path): #Главная функция работы парсера, вызывается в cgi
	global objs
	try:
		st = read_file(path) #Чтение данных из файла
		init_header() #Инициализация хедеров для страницы
		e_print(str(os.environ))
		objs = initobjects() #Инициализация системных объектов e,f,c,data
		res = main(st)
		db.closeconnection() #Отключение от БД
		e_print(res)
	except Exception as e:
		e_print("Error: "+str(e))

def read_file(file_name): #Функция чтения контента из файлов
	f = open(file_name, "r", encoding="utf8")
	databuf="";
	for line in f:
		databuf+=line;
	f.close();
	return databuf

def init_header(): #Функция инициализации хедеров
	for headerLine in htmlheader:
		e_print(headerLine)

def initobjects(): #Функция инициализации объектов
	gobjs = {}

	# Создание объекта data, используется для хранение всех переменных
	gobjs['var'] = obj([])
	
	# Создание объекта e из environ
	keys = sorted(os.environ.keys())
	nk = []
	for i in keys:
		td = os.environ[i]
		nk.append(td)
	gobjs['e'] = obj(keys, [nk])

	# Создание объекта f from cgi-forms
	form = cgi.FieldStorage();
	try:
		keys = sorted(form.keys())
	except:
		keys = []	
	dict = {}
	nk = []
	for i in keys[:]:  # просматриваем копию keys потому что в процессе file_upload добовляет свои ключи
		try:        	
			if form[i].filename: # Это загрузка файла (ов)
				lines = ""
				while 1:
					line = form[i].file.readline()
					if not line: break
					else: lines = lines + line;
				filesize = len(lines);
				filetype = form[i].headers['Content-Type']
				filename = string.split(form[i].filename, "\\")[-1]
				nk.append(lines)
				keys.insert(keys.index(i) + 1, i + "_filesize")
				keys.insert(keys.index(i) + 1, i + "_filetype")
				keys.insert(keys.index(i) + 1, i + "_filename")
				nk.append(filename)
				nk.append(filetype)
				nk.append(filesize)
				continue;
		except:
			pass;

		if type(form[i]) != type([]):
			td = form[i].value
		else:
			td = ""
			for z in form[i]:
				if td == "":
					td = td + z.value
				else:
					td = td + flag_multiple_separate + z.value
		nk.append(td)

	gobjs['f'] = obj(keys, [nk]);

	#Создание объекта c (cookies)
	try:
		c_arr = sorted(os.environ['HTTP_COOKIE'].split("; "))
	except KeyError:
		c_arr = []
	c_keys = []
	c_vals = []
	for c in c_arr:
		c_keys.append(c.split("=")[0])
		c_vals.append(c.split("=")[1])
	gobjs['c'] = obj(c_keys, [c_vals])
	
	return gobjs

def unpack(str):
	#  распаковывает стринг в лист и бъет его по квадратным скобкам.
	rst=[];cur="";inside=0;
	for s in str:
		ch = s
		if s=="[": 
			inside+=1;
			if inside==1 and cur: #c первой скобки начинаем новый блок
				if cur.strip() != "":
					rst.append(cur)
				cur=s;
				continue;
		if s=="]": 
			inside-=1;		
			if not inside and cur: # все скобки закрылись - начинаем новый блок
				if (cur+s).strip() != "":
					rst.append(cur+s);
				cur="";
				continue;
		cur+=s
	if cur:
		rst.append(cur) # последний кусок добовляем		
	return rst

def err(e):
	raise Exception(str(e))

def main(st):
	rst = st
	if type(rst)!=type([]):
		rst = unpack(st) #Раcпаковковка st
	result = ""
	while rst:	# основный цикл перебора строк
		cur = str(rst.pop(0));

		if not cur: 
			continue

		if cur[0] != "[": #Это не синтаксис stella, просто вывод на экран
			result += cur
			continue

		if cur[-1] != "]":
			err("Un-closed tag: " + cur)

		if cur[0:5] == '[get ': #Показывание темплейта
			query = re.sub(r"\s"," ",cur[5:-1])
			result += str(query)
			
			continue
		
		result += str(cur) #Если синтаксис не поппал ни под одно условие, то добавлется он тоже, возможно, например, это js массив

	return result