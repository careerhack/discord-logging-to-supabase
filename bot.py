# This example requires the 'members' privileged intents

import discord
import random
import uuid
import time
import datetime

# get command line args
import sys
CONFIGFILE = sys.argv[1]

# get configuration file
import json
CONFIG = json.load(open(CONFIGFILE,'r'))
AUTHORIZATION_TOKEN = CONFIG['token']

# create database connection
from supabase import create_client, Client
supabase_url: str = CONFIG['supabase_url']
supabase_token: str = CONFIG['supabase_service_token']
supabase: Client = create_client(supabase_url, supabase_token)
TABLE_NAME = 'posts'
SOURCE_NAME = ''
SOURCE_TYPE = 'discord'

########################################################################
#
# FUNCTION: sinkData(data)
# sends data to Supabase. Assumes you are inputting correct schema 
# as a dict object.
#
########################################################################
def sinkData(data: dict):
    try:
        data = supabase.table(TABLE_NAME).insert(data).execute()
        return 200
    except:
        return 400

########################################################################
#
# FUNCTION: getActiveChannels
# gets active channels
#
########################################################################
def getActiveChannels():
    data = supabase.table('sources').select('source_name').eq('active', '1').execute()
    channel_dict_list = data[0]
    channel_list = []
    for row in channel_dict_list:
        channel_list.append(row['source_name'])
    return channel_list

########################################################################
#
# FUNCTION: discordMessageToDict
# function to extract the data from the raw message class to a dict
#
########################################################################
def discordMessageToDict(message):
    # init variables
    message_id = None
    channel_name = None
    channel_id = None
    category_id = None
    author_name = None
    author_id = None
    author_bot = None
    guild_name = None
    guild_id = None
    guild_size = None
    message_body = None

    # exception handling for each variable
    try:
        message_id  = message.id
    except:
        pass
    try:
        channel  = message.channel.name
    except:
        pass
    try:
        channel_id = message.channel.id
    except:
        pass
    try:
        category_id = message.channel.category_id
    except:
        pass
    try:
        author_name = message.author.name
    except:
        pass
    try:
        author_id = message.author.id
    except:
        pass
    try:
        author_bot = message.author.bot
    except:
        pass
    try:
        guild_name = message.guild.name
    except:
        pass
    try:
        guild_id  = message.guild.id
    except:
        pass
    try:
        guild_size = message.guild.member_count
    except:
        pass
    try:
        message_body = message.content
    except:
        pass
    try:
        # data with no errors
        return {
            'status':200,
            'status_message':'success',
            'message_id' : message_id,
            'channel' : channel,
            'channel_id': channel_id,
            'category_id': category_id,
            'author_name': author_name,
            'author_id': author_id,
            'author_bot': author_bot,
            'guild_name': guild_name,
            'guild_id' : guild_id,
            'guild_size': guild_size,
            'message_body': message_body
        }
    except Exception as e:
        # data if there is an error
        return {
            'status':400,
            'status_message':str(e),
            'message_id' : message_id,
            'channel' : channel,
            'channel_id': channel_id,
            'category_id': category_id,
            'author_name': author_name,
            'author_id': author_id,
            'author_bot': author_bot,
            'guild_name': guild_name,
            'guild_id' : guild_id,
            'guild_size': guild_size,
            'message_body': message_body
        }

########################################################################
#
# HANDLERS
#
########################################################################

# initialize discord client
client = discord.Client()

# handler for when connected to server
@client.event
async def on_ready():
    print('[DSC] logged into Discord as {0.user}'.format(client))




# handler for ANY MESSAGE sent to the server on ANY CHANNEL.
# ToDo: have users direct the bot to only grab data from specific channels.
@client.event
async def on_message(message):
    CHANNEL_ID = str(message.channel.id)

    # ignore bot's own messages
    bot_id = client.user.id
    if message.author.id == bot_id:
        exit
    # activechannel command
    elif message.content.startswith(f'<@!{bot_id}> activechannels'):
        active_channels = getActiveChannels()
        dataJSON = json.dumps(active_channels,indent=4)
        await message.channel.send(f'```\n{dataJSON}\n```')

    # only run if in approved channel list
    elif CHANNEL_ID in getActiveChannels():

        # generate data
        raw = discordMessageToDict(message)
        rawJSON = json.dumps(raw)

        # message body
        message_body = raw['message_body']

        # source name
        SOURCE_NAME = str(CHANNEL_ID)
        
        # construct data
        DATA = {
            'source_name':SOURCE_NAME,
            'source_type':SOURCE_TYPE,
            'post':message_body,
            'raw':rawJSON
        }
        sinkData(DATA)


# main runtime
client.run(AUTHORIZATION_TOKEN)