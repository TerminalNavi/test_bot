from peewee import SqliteDatabase, Model, ForeignKeyField, TextField  
 
 
db = SqliteDatabase('sqlite.db') 
 
class DB(Model): 
 
    class Meta: 
        database = db 
 
class User(DB): 
    user_id = TextField() 
    anime_url = TextField(default='None')


db.connect()
db.create_tables([User], safe=True)
db.close()