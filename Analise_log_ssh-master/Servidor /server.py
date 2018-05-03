#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pygtail.core import Pygtail
from datetime import datetime
import socket
from lxml import etree
import lxml.builder as lb
from bottle import Bottle, run



mes = ["Unk", "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

server = Bottle()

@server.route('/ssh')
def read_log():
    da = datetime.now()
    data = da.strftime('%Y-%m-%dT%H:%M:%f')
    filename = '/var/log/auth.log'
    nome = socket.getfqdn()
    ip = socket.gethostbyname(socket.gethostname())
    mensagem = etree.Element('message')
    hostXML = etree.Element('host', name=nome, ip=ip)
    mensagem.append(hostXML)
    reportXML = etree.Element('report', date=data)
    mensagem.append(reportXML)
    payload = etree.Element('payload')
    for l in Pygtail(filename):
        
        if "sshd" and "Accepted" in l:
            dia = l[0:6]
            hora = l[7:15]
            day = dia.split()[0]
            dia = dia.split()[1]
            datalog = ("%d-%02d-%02sT%s" % (datetime.now().year, mes.index(day), dia, hora))
            entrada = lb.E.entry(service='ssh', user=eval('l.split()[8]'), ip_address=eval('l.split()[10]'),
                                 connect_date=datalog,
                                 access='success')
            payload.append(entrada)
    mensagem.append(payload)
    xml = etree.tostring(mensagem, encoding='utf-8', xml_declaration=True)

    return (xml).decode('utf-8')



if __name__== '__main__':
    run(server,host='localhost', port=8081, debug=True)