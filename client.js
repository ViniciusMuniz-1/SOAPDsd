const soap = require('soap');
const url = 'http://localhost:8000/?wsdl';

function createAvatar(client, name) {
    client.createAvatar({name: name}, function(err, result) {
        if (err) throw err;
        console.log(result);
    });
}

function getAvatarInfo(client, name) {
    client.getAvatarInfo({name: name}, function(err, result) {
        if (err) throw err;
        console.log(`Avatar Info: Name: ${result.name}, Level: ${result.level}, XP: ${result.xp}, Current Mission: ${result.current_mission}, Mission Progress: ${result.mission_progress * 100}%`);
    });
}

function startMission(client, name) {
    client.startMission({name: name}, function(err, result) {
        if (err) throw err;
        console.log(result);
    });
}

function completeMission(client, name, progress) {
    client.completeMission({name: name, progress: progress}, function(err, result) {
        if (err) throw err;
        console.log(result);
    });
}

soap.createClient(url, function(err, client) {
    if (err) throw err;

    const avatarName = 'Hero';
    
    // Create an avatar
    createAvatar(client, avatarName);
    
    // Start a mission
    startMission(client, avatarName);
    
    // Complete the mission in steps
    completeMission(client, avatarName, 0.5);  // 50% progress
    completeMission(client, avatarName, 0.5);  // 100% progress

    // Get avatar info
    getAvatarInfo(client, avatarName);
});
