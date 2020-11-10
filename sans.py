# The first 30ish lines are based on
# realpython.com/how-to-make-a-discord-bot-python/

import os
import ffmpeg
import discord
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

sans = discord.Client()

# on_ready
@sans.event
async def on_ready():
    print(f'{sans.user} has successfully connected to Discord.')
    
    print('\nMember of the following:')
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
		
# sans join command
async def sans_join_vc(message):

	# user is in voice channel -- join them
	if message.author.voice:
		await message.author.voice.channel.connect()
		await message.channel.send(f'connected to {message.author.voice.channel} by {message.author.mention}.')
		
		# successful join! Let sans introduce himself
		await sans_say('hello aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa                   a',message.author.voice.channel)

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

async def sans_say(what, the_channel):

	# check for channel match
	voice_client_to_use = False
	
	for client in sans.voice_clients:
		if client.channel == the_channel:
			voice_client_to_use = client

	if(voice_client_to_use):

		eh = voice_client_to_use

		for a_character in what:
			# play "eh" for a nonspace character in message
			if a_character != ' ':
				eh.play(discord.FFmpegPCMAudio('vc.mp3'))
				while eh.is_playing():
					1 == 1
			# pause for a space
			else:
				await asyncio.sleep(0.3)

def sans_say_global_message():
	print("Not implemented.")

sans.run(TOKEN)
