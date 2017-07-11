#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Класс для работы с объектами, создание, изменение, удаление

class obj:
	def __init__ (self,columns=[],val=[]):
		self.values=[]			# values[h_pos][w_pos]
		self.h=0 # Высота и ширина объектов
		self.w=0
		self.topdebug=0 #Отобразить объект на печать перед выводом контента

		self.columns=columns 	# инициализация колонок
		self.w=len(columns)		# ширина объекта
		self.error = 0

		if len(val)!=0 and val!=[[]]:
			if self.w!=len(val[0]):
				raise Exception('You try to create values with diferent weight from columns list='+str(self.w)+' values weight='+str(len(values)))
			self.values=val
			self.h=len(val)
	
	def setError(self,code,msg):
		self.error=1
		self.error_msg=msg
		self.error_code=code
			
	def __str__(self):
		out="w="+str(self.w)+" h="+str(self.h)+" topdebug="+str(self.topdebug)+"\n"
		for i in range(len(self.columns)):
			out+=" "+str(self.columns[i])+":\t"
			if self.h!=0:	
				for j in self.values:
					out+=str(j[i])+"\t"
			out+="\n"
		return out
	
	def __repr__(self):
		return "w="+str(self.w)+" h="+str(self.h)+" topdebug="+str(self.topdebug)+"\nCOL="+str(self.columns)+"\nVAL="+str(self.values)+"\n"
	
	def webout(self,name=""):
		out="<br><table cellspacing='0' cellpadding='3' style='border: 1  dotted #808080; font-family: Georgia; font-size: 12px;'><tr>"
		if name:
			out+="<th style='padding:5px;' bgcolor=#FFDDFF>Obj: "+name+"</th></tr><tr>"
		for i in self.columns:
			out+="<th style='padding:5px;'>"+str(i)+"</th>"
		out+="</tr>"

		for i in range(len(self.values)):
			out+="<tr"; 
			if i%2==0: out+=" bgcolor=#DDDDFF";
			out+=">"
			for j in self.values[i]:
				out+="<td style='padding:5px;'>"+str(j)+"</td>"
			out+="</tr>"
		out+="</table><br>"						
		return out		 


	def insert_column(self,column_name,column_values=[]):
		if self.w==0:
			self.h=len(column_values);
		elif len(column_values)!=self.h:
			raise Exception('You can not insert column with different height. newColumn height='+str(len(column_values))+' current columns height='+str(self.h));
		try:
		    self._get_w_pos(str(column_name))
		except Exception:
			self.columns.append(column_name);
		else:
			return -1

		for i in range(len(column_values)):
			if self.w==0:
				self.values.append([])			
			self.values[i].append(column_values[i]);

		self.w+=1;
		return self.w          	

	def _get_w_pos(self,column_name_or_num):
		if type(column_name_or_num)==type(0):
			w_pos=column_name_or_num;
		else:
			try:
				w_pos=self.columns.index(column_name_or_num)
			except ValueError:
				raise Exception("Don't found column with name="+column_name_or_num);
		if w_pos>self.w:
			raise Exception('You try to get values outside values array your_pos='+str(w_pos)+' max pos='+str(self.w))
		return w_pos

	def modify(self,column_name_or_num,h_pos,new_value):
		self.values[h_pos][self._get_w_pos(column_name_or_num)]=new_value
		return new_value


	def get(self,column_name_or_num,h_pos=0):
		try:
			return self.values[h_pos][self._get_w_pos(column_name_or_num)]
		except IndexError as details:
			raise Exception(details)

	def insert(self,new_values):
		if len(new_values)!=self.w:
			raise Exception('You can not insert values with different lenth. newValues len='+str(len(new_values))+' curValues len='+str(self.w));
		else:
			self.h+=1
			self.values.append(new_values)
			return self.h

# 	def delete(self,h_pos=0):
# 		"""
# 		�������������� h_pos �������������� ���� ������������
# 		"""
# 		del self.values[h_pos:h_pos+1]
# 		self.h-=1;



# 	def remove_column(self,column_name_or_num):
# 		"""
# 		�������������� �������������� �� ������ ������ ����������������
# 		"""	
# 		w_pos=self._get_w_pos(column_name_or_num)
# 		del self.columns[w_pos:w_pos+1]
# 		for i in range(self.h):
# 			del self.values[i][w_pos]
# 		self.w-=1;