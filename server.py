from flask import Flask, request, Response, send_from_directory
import random
from lxml import etree

app = Flask(__name__)

class Avatar:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.xp = 0
        self.current_mission = ""
        self.mission_progress = 0.0

avatars = {}

def create_avatar(name):
    if name in avatars:
        return "Avatar already exists!"
    avatars[name] = Avatar(name)
    return f"Avatar '{name}' created successfully!"

def get_avatar_info(name):
    if name in avatars:
        avatar = avatars[name]
        return {
            'name': avatar.name,
            'level': avatar.level,
            'xp': avatar.xp,
            'current_mission': avatar.current_mission,
            'mission_progress': avatar.mission_progress
        }
    return None

def start_mission(name):
    if name in avatars:
        avatar = avatars[name]
        if avatar.current_mission:
            return f"Avatar is already on a mission: {avatar.current_mission}"
        mission_name = f"Mission {random.randint(1, 100)}"
        avatar.current_mission = mission_name
        avatar.mission_progress = 0.0
        return f"Mission '{mission_name}' started!"
    return "Avatar not found!"

def complete_mission(name, progress):
    if name in avatars:
        avatar = avatars[name]
        if not avatar.current_mission:
            return "Avatar is not on a mission!"
        avatar.mission_progress += progress
        if avatar.mission_progress >= 1.0:
            avatar.xp += 50  # Award XP for completing the mission
            avatar.current_mission = ""
            avatar.mission_progress = 0.0
            if avatar.xp >= 100:
                avatar.level += 1
                avatar.xp -= 100
            return f"Mission completed! Avatar leveled up to {avatar.level}, XP: {avatar.xp}"
        return f"Mission progress: {avatar.mission_progress*100:.2f}%"
    return "Avatar not found!"

@app.route('/soap/', methods=['POST'])
def soap():
    envelope = etree.fromstring(request.data)
    operation = envelope.find('{http://schemas.xmlsoap.org/soap/envelope/}Body').getchildren()[0].tag.split('}')[1]

    if operation == "createAvatar":
        name = envelope.find('.//name').text
        result = create_avatar(name)
        response = f"<result>{result}</result>"
    elif operation == "getAvatarInfo":
        name = envelope.find('.//name').text
        avatar_info = get_avatar_info(name)
        if avatar_info:
            response = f"""
            <Avatar>
                <name>{avatar_info['name']}</name>
                <level>{avatar_info['level']}</level>
                <xp>{avatar_info['xp']}</xp>
                <current_mission>{avatar_info['current_mission']}</current_mission>
                <mission_progress>{avatar_info['mission_progress']}</mission_progress>
            </Avatar>
            """
        else:
            response = "<Avatar><name>Unknown</name><level>0</level><xp>0</xp><current_mission>None</current_mission><mission_progress>0.0</mission_progress></Avatar>"
    elif operation == "startMission":
        name = envelope.find('.//name').text
        result = start_mission(name)
        response = f"<result>{result}</result>"
    elif operation == "completeMission":
        name = envelope.find('.//name').text
        progress = float(envelope.find('.//progress').text)
        result = complete_mission(name, progress)
        response = f"<result>{result}</result>"
    else:
        response = "<error>Unknown operation</error>"

    soap_response = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://localhost:8000/soap/">
       <soapenv:Header/>
       <soapenv:Body>
          {response}
       </soapenv:Body>
    </soapenv:Envelope>
    """

    return Response(soap_response, mimetype='text/xml')

@app.route('/wsdl/', methods=['GET'])
def serve_wsdl():
    return send_from_directory(directory='.', path='avatar_service.wsdl', mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
