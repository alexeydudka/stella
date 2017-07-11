#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Файл для создания поключение к БД

import mysql.connector
import st_config

class Database:
	def __init__(self):
		self.db = mysql.connector.Connect(**st_config.config)
		self.db.autocommit = True
		self.cursor = self.db.cursor()

	def executequery(self, query):
		self.cursor.execute(query)
		try:
			return self.cursor.column_names, self.cursor.fetchall()
		except:
			return "", ""

	def getlastquery(self):
		return "<br><br>"+str(self.cursor.statement)+"<br><br>"

	def closeconnection(self):
		self.cursor.close()
		self.db.close()