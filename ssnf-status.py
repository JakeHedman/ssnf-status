#coding: utf-8
import datetime
import requests
import xml.etree.ElementTree as ET
from flask import Flask
app = Flask(__name__)

def pretty_dt(unix_ts):
    return datetime.datetime.fromtimestamp(int(unix_ts)/1000).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
@app.route('/<isp_id>')
def hello_world(isp_id=1003):
    url = 'http://194.0.217.143/WebServices/PublicFunction'
    headers = {
        'Content-Type': 'text/xml',
    }
    body = """
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <SOAP-ENV:Body>
            <tns:getDisturbancesByCitynetCode xmlns:tns="http://publicfunction.services.glu.ws.ssnf.org/">
                <arg0>{isp_id}</arg0>
            </tns:getDisturbancesByCitynetCode>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>
    """.format(isp_id=int(isp_id))

    res = requests.post(url, headers=headers, data=body)

    tree = ET.fromstring(res.content)

    tree = ET.fromstring(tree.find('.//return').text.encode('utf-8'))
    html = ""
    for obj in tree.findall('.//object/id/..'):
        issue_id = obj.find('id/integer').text
        cause = obj.find('cause/string').text
        start = obj.find('startDate/date').text
        end = obj.find('endDate/date').text
        affected = obj.find('numberOfAffectedCustomers/integer').text

        html += (u"""
            <h2>Störning #{issue_id}</h2>
            <strong>Ärende: </strong><pre>{issue_id}</pre>
            <strong>Beskrivning: </strong><pre>{cause}</pre>
            <strong>Inträffat: </strong><pre>{start}</pre>
            <strong>Beräknas klart: </strong><pre>{end}</pre>
            <strong>Berörda kunder: </strong><pre>{affected} st</pre>
        """.format(
            issue_id=issue_id,
            cause=cause,
            start=pretty_dt(start),
            end=pretty_dt(end),
            affected=affected
        ).encode('utf-8'))

    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
