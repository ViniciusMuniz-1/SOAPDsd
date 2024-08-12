import fetch from 'node-fetch';
import { parseStringPromise } from 'xml2js';
import readlineSync from 'readline-sync';

async function determineCharacter() {
    // Perguntas simples para o teste
    const question1 = readlineSync.keyInYNStrict('Voce se considera um bom lider?');
    const question2 = readlineSync.keyInYNStrict('Voce gosta de aprender novas habilidades?');

    // Construindo o corpo da solicitação SOAP com as respostas
    const soapRequest = `
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                          xmlns:exam="http://example.com/soap">
            <soapenv:Header/>
            <soapenv:Body>
                <exam:DetermineCharacterRequest>
                    <exam:answers>
                        <question1>${question1 ? 'yes' : 'no'}</question1>
                        <question2>${question2 ? 'yes' : 'no'}</question2>
                    </exam:answers>
                </exam:DetermineCharacterRequest>
            </soapenv:Body>
        </soapenv:Envelope>
    `;

    try {                            //MUDAR ISSO DAQUI PARA O ENDEREÇO DO SERVIDOR DITO!!!!! :D
        const response = await fetch('http://localhost:5000/soap', {
            method: 'POST',
            headers: {
                'Content-Type': 'text/xml',
            },
            body: soapRequest,
        });

        const text = await response.text();

        // Parse XML response
        const result = await parseStringPromise(text);
        const character = result['soapenv:Envelope']['soapenv:Body'][0]['exam:DetermineCharacterResponse'][0]['exam:character'][0];
        
        console.log(`Você é ${character}!`);
    } catch (error) {
        console.error('Erro:', error);
    }
}

determineCharacter();
