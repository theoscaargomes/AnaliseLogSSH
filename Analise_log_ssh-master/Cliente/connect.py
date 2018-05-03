#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import logging
from sqlalchemy.orm import sessionmaker
from bd import Users, Clients, Connections, Services, Servers, Reports
from bd import Base, engine
import xml.etree.cElementTree as ET
import dateutil.parser


class connect:
    def __init__(self):
          self.file_log = 'get.log'
          self.url = 'http://localhost:8081/ssh'
          self.logger = logging.getLogger(__name__)

    def get(self):
        
         try:
           return(urllib.request.urlopen(self.url)).read().decode('utf-8')
         except Exception as e:
             self.logger.critical ("%s %s" % (self.url,e))
             return ''

def xml_inserebd(xml):
    tree = ET.ElementTree(ET.fromstring(xml))
    for element in tree.iter():
        if 'entry' in element.tag:
            if not session.query(Users.name).filter(Users.name==
                                element.attrib['user']).count():
                user = Users()
                user.name = element.attrib['user']
                session.add(user)
                session.commit()
            else:
                user = session.query(Users.id, Users.name).filter(Users.name==
                                    element.attrib['user']).first()
                print("ID do usuario: ", user.id)
            if not session.query(Services.name).filter(Services.name==
                                element.attrib['service']).count():
                service = Services()
                service.name = element.attrib['service']
                session.add(service)
                session.commit()
            else:
                service = Services()
                service = session.query(Services.id,
                                        Services.name).filter(Services.name==
                                                     element.attrib['service']
                                                     ).first()
                print("ID servico: ", service.id)
            if not session.query(Clients.ip).filter(Clients.ip==
                                element.attrib['ip_address']).count():
                client = Clients()
                client.ip = element.attrib['ip_address']
                session.add(client)
                session.commit()
            else:
                client = Clients()
                client = session.query(Clients.id,
                                       Clients.ip).filter(Clients.ip==
                                                          element.attrib['ip_address']
                                                          ).first()
                print("ID do cliente: ", client.id)
            con = Connections()
            con.date = dateutil.parser.parse(element.attrib['connect_date'])
            con.action = element.attrib['access']
            con.user_id = user.id
            con.server_id = server.id
            con.service_id = service.id
            con.client_id = client.id
            con.report_id = report.id
            session.add(con)
            session.commit()
        elif 'host' in element.tag:
            if not session.query(Servers.name).filter(Servers.name==
                                 element.attrib['name']).count():
                server = Servers()
                server.name = element.attrib['name']
                server.ip = element.attrib['ip']
                session.add(server)
                session.commit()
            else:
                server = Servers()
                server = session.query(Servers.id, Servers.ip,
                                       Servers.name).filter(Servers.name==
                                                   element.attrib['name']).first()
                print("ID do servidor:",  server.id)
        elif 'report' in element.tag:
            if not session.query(Reports.date).filter(Reports.date==
                                 element.attrib['date']).count():
                report = Reports()
                report.date = dateutil.parser.parse(element.attrib['date'])
                session.add(report)
                session.commit()
    session.close()

conectar = connect()
xml = conectar.get()

if len(xml)>190:
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    xml_inserebd(xml)
else:
    print("Vazio")


