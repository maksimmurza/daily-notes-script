#!/usr/bin/python

import os
import sys
import calendar
import subprocess
from datetime import date
import platform

diaryPath = os.environ.get('DAILY_NOTES_PATH')
editorPath = os.environ.get('DAILY_NOTES_EDITOR')
shellPath = os.environ.get('SHELL')
path = name = ""

if diaryPath == None or os.path.exists(diaryPath) == False:
	if os.path.exists(diaryPath) == False:
		print('Diary path is not exist. Path will be set on default (Desktop)\n')

	if 'linux' in sys.platform:
		# If on wsl
		if 'Microsoft' in platform.uname()[3]:
			command = 'cmd.exe /c "echo %USERNAME%"'
			winUsername = subprocess.check_output(command, shell=True)
			winUsername = winUsername.strip()
			diaryPath = '/mnt/c/Users/' + winUsername + '/Desktop/'
			print(diaryPath)
		else:
			diaryPath = '~/Desktop/'
	# elif 'win' in sys.platform:
	# 	diaryPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
	else:
		print('Unsupportable platform')

if editorPath == None:
	if os.environ.get('VISUAL') != None:
		editorPath = os.environ.get('VISUAL')
	elif os.environ.get('EDITOR') != None:
		editorPath = os.environ.get('EDITOR')
	else:
		print('Cannot detect editor')


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





