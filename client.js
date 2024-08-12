const soap = require('soap');
const readline = require('readline');
const url = 'http://localhost:8000/wsdl/';  // URL do WSDL

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

soap.createClient(url, function(err, client) {
    if (err) throw err;

    function ask(question) {
        return new Promise((resolve) => {
            rl.question(question, (answer) => resolve(answer));
        });
    }

    async function interact() {
        const avatarName = await ask('Enter avatar name: ');

        // Create an avatar
        client.createAvatar({name: avatarName}, function(err, result) {
            if (err) {
                console.error('Error creating avatar:', err);
                rl.close();
                return;
            }
            console.log('Avatar Creation Result:', result);

            (async function missionFlow() {
                const action = await ask('Choose action: (startMission/completeMission/getAvatarInfo): ');

                if (action === 'startMission') {
                    client.startMission({name: avatarName}, function(err, result) {
                        if (err) {
                            console.error('Error starting mission:', err);
                            rl.close();
                            return;
                        }
                        console.log('Mission Start Result:', result);
                        missionFlow();  // Prompt for next action
                    });
                } else if (action === 'completeMission') {
                    const progress = parseFloat(await ask('Enter mission progress (0-1): '));
                    client.completeMission({name: avatarName, progress: progress}, function(err, result) {
                        if (err) {
                            console.error('Error completing mission:', err);
                            rl.close();
                            return;
                        }
                        console.log('Mission Completion Result:', result);
                        missionFlow();  // Prompt for next action
                    });
                } else if (action === 'getAvatarInfo') {
                    client.getAvatarInfo({name: avatarName}, function(err, result) {
                        if (err) {
                            console.error('Error getting avatar info:', err);
                            rl.close();
                            return;
                        }
                        console.log('Avatar Info Result:', result);
                        missionFlow();  // Prompt for next action
                    });
                } else {
                    console.log('Unknown action. Exiting...');
                    rl.close();
                }
            })();
        });
    }

    interact();
});
