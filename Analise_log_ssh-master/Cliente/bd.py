#!/usr/bin/env python3
import os
#import logging
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
#import xml.etree.cElementTree  as ET
#import dateutil.parser


Base = declarative_base()


basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///'+ os.path.join(basedir,'xml.db'),
                       echo=True)
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    def __repr__(self):
        return '<User {}>'.format(self.name)

class Clients(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    ip = Column(String(15), unique=True, nullable=False)
    def __repr__(self):
        return '<Client {}>'.format(self.ip)

class Servers(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    ip = Column(String(15), unique=True, nullable=False)
    def __repr__(self):
        return '<Server {}>'.format(self.name, self.ip)


class Services(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    def __repr__(self):
        return '<Service {}>'.format(self.name)

class Reports(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    date = datetime
    def __repr__(self):
        return '<Report {}>'.format(self.date)

class Connections(Base):
    __tablename__ = 'connections'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.isoformat)
    action = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    server_id = Column(Integer, ForeignKey('servers.id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    report_id = Column(Integer, ForeignKey('reports.id'))
    def __repr__(self):
        return '<Connection {}>'.format(self.date, self.action)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()
