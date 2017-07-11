#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Файл всех системных функций stella project
import re

def do(st):
    res = []

    skindex = st.find("(")
    funcname = st[0:skindex]
    funcparam = st[skindex+1:-1]
    n=0
    while n<1:
        if funcname == "strescape": # эранирует все специальные символы в строке
            res.append(re.escape(funcparam))
            break

        if funcname == "strunescape": # убирает экранирование в строке
            res.append(re.sub(r'\\(.)', r'\1', funcparam))
            break

        if funcname == "tostring": # заворачивает строку в одинарные кавычки и выполняет экранирование одинарных кавычек внутри
            res.append("'"+funcparam.replace("'", "\\'")+"'")
            break

        if funcname == "strempty": # проверяет пустая ли строка, если да то возвращает 1, нет 0, tostring делать не нужно
            if funcparam=="":
                res.append("1")
            else:
                res.append("0")
            break
        
        n=n+1
    
    if n==1:
        raise Exception("Function " + funcname + " not found")

    return res