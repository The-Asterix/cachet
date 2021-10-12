import discord
from discord.ext import commands
import random
import datetime
import urllib

from urllib import parse, request
import re

token='ODI5MDQ5NDE4MzEyNzEyMTkz.YGyecA.b8Lm1g3RzaJ6AhFQpZwLuvYujAs'

client = commands.Bot(command_prefix='>')

@client.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}", inline=True)
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}", inline=True)
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}", inline=True)
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}", inline=True)
    embed.add_field(name="Member Count", value=f"{ctx.guild.member_count}", inline=True)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)

@client.command()
async def userinfo(ctx, member:discord.Member = None):
    roles = [role for role in member.roles]

    embed = discord.Embed(title=f"{member}", colour=discord.Colour.dark_gold(), timestamp=ctx.message.created_at)
    embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
    embed.set_author(name="User Info: ")
    embed.add_field(name="ID:", value=member.id, inline=False)
    embed.add_field(name="User Name:", value=member.display_name, inline=False)
    embed.add_field(name="Discriminator:", value=member.discriminator, inline=False)
    embed.add_field(name="Current Activity:",
                    value=f'{member.activities[0].name}' if member.activity is not None else "None",
                    inline=False)
    embed.add_field(name="Created At:", value=member.created_at.strftime("%a, %d, %B, %Y, %I, %M, %p UTC"),
                    inline=False)
    embed.add_field(name="Joined At:", value=member.joined_at.strftime("%a, %d, %B, %Y, %I, %M, %p UTC"), inline=False)
    embed.add_field(name=f"Roles [{len(roles)}]", value=" **|** ".join([role.mention for role in roles]), inline=False)
    embed.add_field(name="Top Role:", value=member.top_role, inline=False)
    embed.add_field(name="Bot:", value=member.bot, inline=False)
    await ctx.send(embed=embed)

@client.command()
async def avatar(ctx, member: discord.Member):
    await ctx.send(member.avatar_url)

@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(title="Kicked", description=f"{member.mention} was kicked.", colour=discord.Colour.green())
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(title="Banned", description=f"{member.mention} was banned.", colour=discord.Colour.dark_purple())
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_user = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_user:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(title="Unbanned", description=f"{member} was unbanned.",
                                  colour=discord.Colour.dark_orange())
            await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="Muted", description=f"{member.mention} was muted.", colour=discord.Colour.light_gray())
    embed.add_field(name="Reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)

@client.command()
async def meme(ctx):
    images = ['https://i.pinimg.com/474x/98/9f/36/989f3606fbd5f96a2e6d99d86113937f.jpg',
              'https://pics.me.me/thumb_study-to-get-high-gpa-study-to-understand-and-make-41096081.png']
    embed = discord.Embed(color=discord.Colour.dark_magenta())
    random_link = random.choice((images))
    embed.set_image(url = random_link)
    await ctx.send(embed=embed)

@client.command()
async def youtube(ctx, *, search):
        query_string = parse.urlencode({'search_query': search})
        html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
        search_content = html_content.read().decode()
        search_results = re.findall(r'\/watch\?v=\w+', search_content)
        await ctx.send('https://www.youtube.com' + search_results[0])

@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=20):
    await ctx.channel.purge(limit=amount)

@client.event
async def on_ready():
    servers = len(client.guilds)
    members = 0
    for guild in client.guilds:
        members += guild.member_count - 1
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Activity(
                                     type=discord.ActivityType.playing,
                                     name=f'>help | Serving {members} users in {servers} servers'))
    print('Bot is ready')

client.run(token)
