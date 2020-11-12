# The first 30ish lines are based on
# realpython.com/how-to-make-a-discord-bot-python/

from flask import Flask
from threading import Threading

import os
import ffmpeg
import discord
import asyncio
from dotenv import load_dotenv

# keeping the server up
app = Flask('')

@app.route('/')
def route_return():
	return 'Alive.'
	
def run_app():
    hport = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=hport)
    
def keep_alive():
    server = Thread(target=run_app)
    server.start()

# discord code	
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

sans = discord.Client()

# on_ready
@sans.event
async def on_ready():
    print(f'{sans.user} has successfully connected to Discord.')
    
    print('\nMember of the following as of ready:')
    print(f'GUILD \t\t\t\t ID ')
    print('-----------------------------------------------------------------')
    
    # Connect to and display guilds
    for guild in sans.guilds:
    	print(f'{guild.name} \t\t\t\t {guild.id}')
    	
    print('\n')
    	
# detect a message command
@sans.event
async def on_message(message):
	
	# voice channel join command
	if message.content == 'sans join':
		await sans_join_vc(message)

	# voice channel leave command
	if message.content == 'sans leave':
		await sans_leave_vc(message)
		
	if message.content[0:9] == 'sans tts ':
		await sans_tts(message)
		
	if message.content == 'sans help':
		await sans_display_help(message)

async def sans_display_help(message):
	await message.channel.send('```Commands:\n' +
						 	   'join      : join the same voice channel as user\n' +
						 	   'leave     : leave the voice channel the user is in\n' +
						 	   'tts <msg> : repeat text in current voice channel of user\n' +
						 	   'help      : display this help message```')
# sans join command
async def sans_join_vc(message):

	# user is in voice channel -- join them
	if message.author.voice:
		await message.author.voice.channel.connect()
		await message.channel.send(f'connected to {message.author.voice.channel} by {message.author.mention}.')
		
		# successful join! Let sans introduce himself
		await sans_say('hello',message.author.voice.channel)

	# voice channel join fail
	else:
		await message.channel.send(f'hey {message.author.mention}, i can\'t find the voice channel you\'re in. sorry.')

# sans leave command
async def sans_leave_vc(message):

	user_channel = message.author.voice.channel

	# check for channel match
	voice_client_to_close = False
	
	for client in sans.voice_clients:
		if client.channel == user_channel:
			voice_client_to_close = client

	# cases 1 & 2: make sure sans is connected to the guild first
	if(sans.voice_clients and voice_client_to_close):
		
		# case 1: user and sans are in same channel ; proceed with disconnect
		if voice_client_to_close:
			await voice_client_to_close.disconnect()
			await message.channel.send('goodbye friend.')
		else:
			await message.channel.send(f'hey {message.author.mention}, you can\'t disconnect me unless you are in the same voice channel as me. nothing personal, kid.')

	# case 3: sans isn't in a voice channel at all
	else:
		await message.channel.send(f'i\'m not in a voice channel here at all {message.author.mention}...')

async def sans_tts(message):

	user_channel = message.author.voice.channel
	
	# check for channel match
	voice_client_to_use = False
	
	for client in sans.voice_clients:
		if client.channel == user_channel:
			voice_client_to_use = client

	if voice_client_to_use:
		await sans_say(message.content.strip('sans tts '), user_channel)
		
	else:
		await message.channel.send('you must be in the same voice channel as me to use this command.')
		
			
	

async def sans_say(what, the_channel):

	# check for channel match
	voice_client_to_use = False
	
	for client in sans.voice_clients:
		if client.channel == the_channel:
			voice_client_to_use = client

	if(voice_client_to_use):

		eh = voice_client_to_use

		# a generic speaking-time length
		speak_time = len(what) * 60 * 0.1 / 160

		# recording is only 122 seconds long;
		# for anything longer, loop through the recording until done
		while speak_time > 122:
			eh.play(discord.FFmpegPCMAudio('vc.mp3'))
			# one second of leeway
			await asyncio.sleep(123)
			speak_time -= 122;

		# one second of leeway
		eh.play(discord.FFmpegPCMAudio('vc.mp3'))
		await asyncio.sleep(speak_time + 1)
		eh.stop()
		
run_app()
sans.run(TOKEN)
