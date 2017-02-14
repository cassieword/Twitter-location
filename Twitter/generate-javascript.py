#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('/Users/xinyu/Desktop/twitter.sqlite')

c = conn.cursor()

import codecs

file = codecs.open("/Users/xinyu/Desktop/geo.js", "w", "utf-8")

file.write("var addressPoints = [")

for row in c.execute('SELECT * FROM twitters'):
	text = "\"" + row[4] + "\""
	text = text.replace('\n', '')
	file.write('[' + ', '.join([str(row[3]), str(row[2]), text, "\"" + str(row[1]) + "\"" ]) + '],\n')

file.write("];")

file.close()
