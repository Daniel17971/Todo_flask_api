from api import app, db

with app.app_context(): #create the instance folder with database.db (the command py create_db.py will create the database.db file)
    db.create_all()