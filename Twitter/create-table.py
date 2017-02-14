import sqlite3
conn = sqlite3.connect('/Users/xinyu/Desktop/twitter.sqlite')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE twitters
			 (userID text, date date, leo real, geo real, content text)''')

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()