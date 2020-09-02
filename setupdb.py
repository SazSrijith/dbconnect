from models import  Project,Employee,Skill,Score,User,db
from __init__ import app,db

db.create_all()
admin=User('admin@admin.com','admin','admin')
db.session.add(admin)
db.session.commit()
