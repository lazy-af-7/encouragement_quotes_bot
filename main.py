import os
import requests
import discord
from dotenv import load_dotenv
import json
import random
from replit import db
from web_server import keep_alive


load_dotenv()
TOKEN = os.getenv('TOKEN')

client = discord.Client()

sad_words=["sad","lonely","heartbroken","gloomy","disappointed","hopeless","grieved","unhappy","lost","troubled","resigned","miserable"]
starter_encouragements=["Yo! Cheer up!","Hang in there little one.","You are the best /bot!"]

if "responding" not in db.keys():
  db['responding']=True


def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q']+" - "+json_data[0]['a']
  return quote

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements=db['encouragements']
    encouragements.append(encouraging_message)
    db['encouragements']=encouragements
  else:
    db['encouragements']=encouraging_message


def delete_encouragement(index):
  encouragements=db['encouragements']
  if len(encouragements)>index:
    del encouragements[index]
    db['encouragements']=encouragements

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
  if message.author==client.user:
    return

  msg=message.content

  if message.content.startswith('!encourage'):
    quote=get_quote()
    await message.channel.send(quote)

  if db['responding']:
    options=starter_encouragements
    if "encouragements" in db.keys():
      options=options+db['encouragements']
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))


  if msg.startswith('!new'):
    encouraging_message=msg.split('!new ',1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added!")

  if msg.startswith('!del'):
    encouragements=[]
    if "encouragements" in db.keys():
      index=int(msg.split('!del ',1)[1])
      encouragements=delete_encouragement(index)
    await message.channel.send(encouragements)

  if msg.startswith('!list'):
    encouragements=[]
    if "encouragements" in db.keys():
      encouragements=db['encouragements']
    await message.channel.send(encouragements)


  if msg.startswith('!responding'):
    value=msg.split('!responding ',1)[1]
    if value.lower()=='true':
      db['responding']=True
      await message.channel.send("Responding is ON!")
    else:
      db['responding']=False
      await message.channel.send("Responding is OFF!")
    

keep_alive()
client.run(TOKEN)