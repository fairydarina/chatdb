import sqlite3
from time import gmtime, strftime
from flask import Flask, redirect, render_template, request, session
import random


app = Flask(__name__)



class DB:
    def __init__(self):
        conn = sqlite3.connect('chatdb2.db', check_same_thread=False)
        self.conn = conn
 
    def get_connection(self):
        return self.conn
 
    def __del__(self):
        self.conn.close()


class Messages:
    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        color_list = ['#F08080', '#DC143C', '#8B0000', '#FF69B4', '#DB7093', '#FF7F50', '#FF8C00', '#F0E68C', '#4B0082', '#DDA0DD', '#F4A460', '#CD853F', '#D2691E', '#228B22', '#808000', '#7B68EE', '#20B2AA', '#00FFFF', '#FFFFF0', '#C0C0C0', '#F5F5F5'] 
        cursor = self.connection.cursor()
        cursor.execute('''SELECT t.user_name, t.text_message 
FROM
(SELECT m.user_name, m.text_message, m.date_message
FROM messages m ORDER BY date_message DESC LIMIT 10) t
ORDER BY t.date_message'''
        )
        rows = cursor.fetchall()
        rows2 = [] 
        for i in rows: 
            rows2.append((i[0], i[1], color_list[random.randrange(0, len(color_list))])) 
        return rows2         


    def insert(self, user_name, text_message):
        dt = strftime("%Y%m%d%H%M%S", gmtime())

        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO messages 
                        (user_name, date_message, text_message) 
                        VALUES (?,?,?)''', (user_name, dt, text_message))
        cursor.close()
        self.connection.commit()



db = DB()
m = Messages(db.get_connection())



@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        message_all_list = m.get_all()
        return render_template('index.html', title='Сообщение доставлено', message_all=message_all_list)
    elif request.method == 'POST':
        user_name = request.form['user_name']
        text_message = request.form['text_message']
        m.insert(user_name, text_message)
        return '''<!DOCTYPE html> 
<html lang="en"> 
<head> 
    <meta charset="UTF-8"> 
    <META HTTP-EQUIV="refresh" CONTENT="2"> 
    <title>Сообщение добавлено</title> 
</head> 
<body> 
    <h1>Сообщение добавлено</h1> 
</body> 
</html>'''


        
    


#print(u.get('geron', 'geron'))
#u.insert('geron', 'geron')
#m.insert(2, 'qweqwelkjqwe')
#a = m.get_all()
#print(a)





if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)