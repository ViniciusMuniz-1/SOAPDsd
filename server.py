from flask import Flask, request
from lxml import etree
from zeep import Client, Settings
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin

app = Flask(__name__)

# Define the WSDL schema
wsdl = '''
<definitions xmlns="http://schemas.xmlsoap.org/wsdl/"
             xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
             xmlns:xsd="http://www.w3.org/2001/XMLSchema"
             targetNamespace="http://example.com/soap">
    <message name="DetermineCharacterRequest">
        <part name="answers" type="xsd:string"/>
    </message>
    <message name="DetermineCharacterResponse">
        <part name="character" type="xsd:string"/>
    </message>
    <portType name="CharacterPortType">
        <operation name="DetermineCharacter">
            <input message="tns:DetermineCharacterRequest"/>
            <output message="tns:DetermineCharacterResponse"/>
        </operation>
    </portType>
    <binding name="CharacterBinding" type="tns:CharacterPortType">
        <soap:binding transport="http://schemas.xmlsoap.org/soap/http"/>
        <operation name="DetermineCharacter">
            <soap:operation soapAction="urn:DetermineCharacter"/>
            <input>
                <soap:body use="literal"/>
            </input>
            <output>
                <soap:body use="literal"/>
            </output>
        </operation>
    </binding>
    <service name="CharacterService">
        <port name="CharacterPort" binding="tns:CharacterBinding">
            <soap:address location="http://localhost:5000/soap"/>
        </port>
    </service>
</definitions>
'''

@app.route('/soap', methods=['POST'])
def soap():
    soap_envelope = request.data
    root = etree.fromstring(soap_envelope)
    
    answers = {}
    for elem in root.xpath('//exam:answers', namespaces={'exam': 'http://example.com/soap'}):
        for child in elem:
            answers[child.tag] = child.text

    character = determine_character(answers)
    
    response = f'''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:exam="http://example.com/soap">
        <soapenv:Header/>
        <soapenv:Body>
            <exam:DetermineCharacterResponse>
                <exam:character>{character}</exam:character>
            </exam:DetermineCharacterResponse>
        </soapenv:Body>
    </soapenv:Envelope>
    '''
    return response, {'Content-Type': 'text/xml'}

def determine_character(answers):
    if answers.get('question1') == 'yes':
        return 'Aang'
    elif answers.get('question2') == 'yes':
        return 'Katara'
    else:
        return 'Zuko'

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
