#!/usr/bin/python

import os
import sys
import calendar
import subprocess
from datetime import date

diaryPath = os.environ.get('DIARY')
editorPath = os.environ.get('SUBL')
shellPath = os.environ.get('SHELL')
path = name = ""

def getDateStr(date):
	s = str(date)
	if date < 10: return "0" + s 
	else: return s

def format(str):
	arr = [" ", "(", ")"]
	for i in arr:
		str = str.replace(i, "\\"+i)
	return str

def createDiaryNote(day, month, year):
	os.chdir(diaryPath)

	monthFolder = month + ". " + calendar.month_name[int(month)]
	yearFolder = year

	if not os.path.isdir(yearFolder):
		os.mkdir(yearFolder)

	os.chdir(diaryPath + yearFolder)

	if not os.path.isdir(monthFolder):
		os.mkdir(monthFolder)

	os.chdir(diaryPath + yearFolder + "/" + monthFolder)
	path = diaryPath + yearFolder + "/" + monthFolder + "/"
	name = day + "." + month + "." + year + ".md"

	if os.path.isfile(name):
		if len(sys.argv) == 1:
			command = format(editorPath) + " " + name
			subprocess.call(command, shell=True, executable=shellPath)
		return

	command = "touch " + format(path) + name
	subprocess.call(command, shell=True, executable=shellPath)

	file = open(path + name, "w")
	file.write("# " + name[:-3])
	file.close()

	if len(sys.argv) == 1:
		command = format(editorPath) + " " + name
		subprocess.call(command, shell=True, executable=shellPath)


if len(sys.argv) > 1:
	for i in range(len(sys.argv)):
		if i!=0:
			createDiaryNote(sys.argv[i][0:2],sys.argv[i][3:5],sys.argv[i][6:10])
else:
	today = date.today()
	createDiaryNote(getDateStr(today.day), getDateStr(today.month), str(today.year))





