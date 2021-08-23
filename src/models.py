import os
import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import exc
import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(250), unique=True,nullable=False)
    assign_tasks = db.relationship('Task', lazy=True)


    def __repr__(self):
        return f'Account: {self.id}, user: {self.nick}'


    def to_dict(self):
        print(self.assign_tasks)
        return {
            "id": self.id,
            "nick": self.nick,
        }


    def create(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        users_list = cls.query.all()
        return [user.to_dict() for user in users_list]


    @classmethod
    def get_by_id(cls,id):
        account = cls.query.filter_by(id = id).one_or_none()
        return account

    def update(slef, nick):
        self.nick = nick
        db.session.commit()

    
    @classmethod
    def get_by_nick(cls,nick):
        account = cls.query.filter_by(nick = nick).one_or_none()
        return account 
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Task(db.Model): 
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column (db.String(250),nullable=False)
    status = db.Column (db.Boolean(True), default=False )
    account_id = db.Column (db.Integer, db.ForeignKey("account.id"))


    def __repr__(self):
        return f'Task: {self.id}, label: {self.label}, status: {self.status} from user: {self.account_id}'
    

    def to_dict(self):
        account = Account.get_by_id(self.account_id)
        return{
            "task_id":self.id,
            "label":self.label,
            "status":self.status,
            "account": account.nick
        }


    def add_new(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_tasks(cls):
        tasks = cls.query.all()
        return [task.to_dict() for task in tasks]


    @classmethod
    def get_task_by_user(cls, id):
        specific_task_list = cls.query.filter_by(account_id = id, status =False)
        return [element.to_dict() for element in specific_task_list]


    @classmethod
    def get_one_task(cls, position):
        one_task = cls.query.get(position)
        return one_task

#NO DEVOLVER one_task.dict; eso lo devolverá en main

    def delete(self):
        db.session.delete(self)
        db.session.commit()