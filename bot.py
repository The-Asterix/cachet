import discord

TOKEN = 'ODI5MDQ5NDE4MzEyNzEyMTkz.YGyecA.1U_4ZeW4wQG3MiQXQt-Xlrp_Efs'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hi'):
        msg = 'Hi {0.author.mention}'.format(message)
        await message.channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
