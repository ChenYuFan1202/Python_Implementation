from wtforms import Form, StringField, TextAreaField, validators
from wtforms.fields import EmailField
import sqlite3

def sqlite_insert(title, username, email, message_text):
    connect = sqlite3.connect("database.sqlite")
    connect.execute("INSERT INTO message_board(title, username, email, message_text, date) VALUES(?, ?, ?, ?, DATETIME('now'))", 
                    (title, username, email, message_text))
    connect.commit()
    connect.close()

def sqlite_read():
    conn = sqlite3.connect("database.sqlite")
    create_sql = """create table if not exists message_board(
                    'title' TEXT, 'username' TEXT, 'email' TEXT, 
                    'message_text' TEXT, 'date' TEXT)"""
    conn.execute(create_sql)
    read_sql = "select * from message_board"
    read_data = conn.execute(read_sql)
    dataset = read_data.fetchall()
    conn.close()
    return list(dataset)

class ReviewForm(Form):
    title = StringField("標題:", validators = [validators.DataRequired()])
    username = StringField("作者:", validators = [validators.DataRequired()])
    email = EmailField("email:", validators = [validators.DataRequired()])
    message_text = TextAreaField("留言:", validators = [validators.DataRequired()])
    
