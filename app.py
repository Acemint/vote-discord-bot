import hikari
import json
import re
import requests
from hikari.emojis import Emoji

API_ENDPOINT = 'https://discord.com/api/v8'
TOKEN = json.loads(open('./bot_token.json', "r").read())['token']
CLIENT_ID = json.loads(open('./bot_token.json', "r").read())['client_id']
CLIENT_SECRET =  json.loads(open('./bot_token.json', "r").read())['client_secret']
COINMARKET_SECRET = json.loads(open('./bot_token.json', "r").read())['coin_market_cap']
OPENEMOJI_SECRET = json.loads(open('./bot_token.json', "r").read())['open_emoji']
PREFIX = "$"

class VoteBot(hikari.GatewayBot):
    def __init__(self, token):
        super().__init__(token)

app = VoteBot(TOKEN)

@app.listen()
async def receiveMessage(event: hikari.GuildMessageCreateEvent) -> None:
    # to read the message from the server
    if(event.is_bot or not event.content):
        return
    
    if(event.content.startswith(PREFIX + "help")):
        clientMessage = event.content.strip(PREFIX)
        list_of_commands = ["help"]
        await event.message.respond(clientMessage)

    if(event.content.startswith(PREFIX + "vote")):
        validCustomEmojis = await app.rest.fetch_guild_emojis(event.guild_id)
        validCustomEmojis = [ emoji.id for emoji in validCustomEmojis]
        print(validCustomEmojis)
        clientMessage = event.content.strip(" ").lstrip(PREFIX + "vote")
        clientMessage = clientMessage.split(" ")

        customEmojis = re.findall("<:[\S]*:[0-9]*>", event.content)
        unicodeEmojis = re.findall(":[\S]*:", event.content)

        validVote = 0
        # custom emoji uses the format <:emojiName:emojiNum>
        for emoji in customEmojis:
            emoji = emoji.strip("<").strip(">")
            emojiName = emoji.split(":")[-2]
            emojiNumber = emoji.split(":")[-1]
            print(emojiNumber, validCustomEmojis[0])
            if(emojiNumber in validCustomEmojis): 
                print("VALID")
                validVote += 1
            else:
                print("INVALID")


            # if(emojiNumber is in unicodeEmojis)
        # unicode emoji uses the format :[emojiName]: 
        for emoji in unicodeEmojis:
            emojiName = emoji.strip(":")
            baseUrlEmojiChecker = f"https://emoji-api.com/emojis?search={emojiName}&access_key={OPENEMOJI_SECRET}"
            print(baseUrlEmojiChecker)
            emojiExist = requests.get(baseUrlEmojiChecker)
            emojiExist = emojiExist.json()
            
            if(emojiExist == None):
                print("NOT EXIST")
            else:
                print(emojiExist)



        if(len(clientMessage) != 3):
            text = "Please use the format: $vote [content] [emoji1] [emoji2]"
            await event.message.respond(text)
        elif(validVote != 2):
            text = "Please use valid emojis"
            await event.message.respond(text)
        else:
            content_to_vote = "React below to vote\n" + clientMessage[0] + "\n" + f"{clientMessage[-2]}\n{clientMessage[-1]}"
            await event.message.respond(content_to_vote)

app.run()
