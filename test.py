import requests

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bot"
}

stuff = requests.post('https://discordapp.com/api/v6/channels/376384220857106434/messages/510120060409479198',
                       headers=headers)
