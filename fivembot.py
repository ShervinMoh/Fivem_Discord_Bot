import discord
import re
from discord.ext import tasks
import requests


intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

'''In this function, it is possible to use the available commands by mentioning the user'''
def get_member_by_mention(guild, mention):
    user_id = int(re.findall(r'\d+', mention)[0])
    return guild.get_member(user_id)

async def remove_role(message, role_mention, target_user):
    
    '''This command can only be executed in the channel you specify here'''
    if message.channel.id == 'YOUR CHANNEL ID': 
        guild = message.guild
        
        # Extract the role ID from the mention
        role_id = int(role_mention.replace("<@&", "").replace(">", ""))
        
        # Get the role object from the ID
        role = discord.utils.get(guild.roles, id=role_id)

        '''This condition checks whether the desired role exists or not''' 
        if not role:
            await message.channel.send("Role not found.")
            return

        role_name = role.name

        required_roles = {"Roles that can use this command"}

        '''This condition checks that only the roles defined inside the code can use this command'''
        if any(role.name in required_roles for role in message.author.roles):
            
            '''Checks if there is a user or not'''
            if not target_user:
                await message.channel.send("User not found.")
                return

            '''Those who have the role specified in the code cannot take roles from each other'''
            if role.name in required_roles:
                await message.channel.send("You can't remove high ranks role.") 
                return  
            '''Those who have the role specified in the code cannot take a role from themselves'''
            if role in target_user.roles:
                if target_user == message.author:
                    await message.channel.send("You can't remove a role from yourself.")
                    return         
            '''It checks whether the user has the role or not'''
            if role in target_user.roles:
                try:
                    await target_user.remove_roles(role)
                    await message.channel.send(f"Role '{role_name}' has been removed from {target_user.mention}")

                    '''
                    If this command is used, a report message will be sent to the specified channel. 
                    This report contains information such as the ID of the person from whom the 
                    roll was taken, the ID of the person who used the command, 
                    details about the command used and the roll removed from the user.
                    '''
                    log_channel_name = "YOUR LOG CHANNEL IN DISCORD"
                    log_channel = discord.utils.get(message.guild.channels, name=log_channel_name)
                    log_message = f"User ID: {message.author.mention} | Command: !removerole | Role Name: {role_mention} | Target User: {target_user.mention}"
                    await log_channel.send(log_message)

                except discord.Forbidden:
                    await message.channel.send("I don't have permission to remove roles.")
                except discord.HTTPException:
                    await message.channel.send("An error occurred while removing the role.")
            else:
                await message.channel.send(f"{target_user.mention} does not have the role '{role_name}'.")
        else:
            await message.channel.send("You don't have the required role to execute this command.")
    else:
        await message.channel.send("This command can only be used in the workspace channel.")


async def add_role(message, role_mention, target_user):
    
    '''This command can only be executed in the channel you specify here'''
    if message.channel.id == 'YOUR CHANNEL ID':
        guild = message.guild

        # Extract the role ID from the mention
        role_id = int(role_mention.replace("<@&", "").replace(">", ""))

        # Get the role object from the ID
        role = discord.utils.get(guild.roles, id=role_id)
        
        '''This condition checks whether the desired role exists or not''' 
        if not role:
            await message.channel.send("Role not found.")
            return
        
        '''Those who have the role specified in the code cannot add a role for themselves'''
        if role not in target_user.roles:
            if target_user == message.author:
                await message.channel.send("You can't add a role for yourself.")
                return  

        role_name = role.name

        required_roles = {"Roles that can use this command"}

        '''This condition checks that only the roles defined inside the code can use this command'''
        if any(role.name in required_roles for role in message.author.roles):
            
            '''Checks if there is a user or not'''
            if not target_user:
                await message.channel.send("User not found.")
                return

            '''
            Those who have the role specified in the code cannot add 
            another role for someone with the same role. 
            Only Founder can add roles to them through Discord
            '''
            if role.name in required_roles:
                await message.channel.send("Only the Founder can add roles for high ranks.")
                return

            '''This condition checks whether the user has the desired role or not'''
            if role not in target_user.roles:
                try:
                    await target_user.add_roles(role)
                    await message.channel.send(f"Role '{role_name}' has been added to {target_user.mention}.")

                    '''
                    If this command is used, a report message will be sent to the specified channel. 
                    This report contains information such as the ID of the person from whom the 
                    roll was given, the ID of the person who used the command, 
                    details about the command used and the roll adde to the user.
                    '''
                    log_channel_name = "discord-bot"
                    log_channel = discord.utils.get(message.guild.channels, name=log_channel_name)
                    log_message = f"User ID: {message.author.mention} | Command: !addrole | Role Name: {role_mention} | Target User: {target_user.mention}"
                    await log_channel.send(log_message)
                    
                except discord.Forbidden:
                    await message.channel.send("I don't have permission to add roles.")
                except discord.HTTPException:
                    await message.channel.send("An error occurred while adding the role.")
            else:
                await message.channel.send(f"{target_user.mention} already has the role '{role_name}'.")
        
        
        else:
            await message.channel.send("You don't have the required role to execute this command.")
    else:
        await message.channel.send("This command can only be used in the workspace channel.")


async def send_message(message, channel_mention, content):
    
    '''This command can only be executed in the channel you specify here'''
    if message.channel.id == 'YOUR CHANNEL ID':
        guild = message.guild
        
        required_roles = {"Roles that can use this command"}

        '''This condition checks that only the roles defined inside the code can use this command'''
        if any(role.name in required_roles for role in message.author.roles):
            channel_id = int(re.findall(r'\d+', channel_mention)[0])
            target_channel = guild.get_channel(channel_id)

            '''
            This condition checks whether the desired channel is available 
            for sending the message or not
            '''
            if not target_channel:
                await message.channel.send("Channel not found.")
                return

            # Create and configure the embed
            embed = discord.Embed(
                title="\U0001F4E2 ONE Community Announcement:",
                description=content,
                color=discord.Color(0xf04a10)
            )

            try:
                await target_channel.send(embed=embed)
                await message.channel.send(f"Message sent to {target_channel.mention}")
                
                '''
                If this command is used, a report message will be sent to the specified channel. 
                This report contains information such as the ID of the person who used the command, 
                details about the command used and and the details of the channel to which the message was sent.
                '''
                log_channel_name = "discord-bot"
                log_channel = discord.utils.get(message.guild.channels, name=log_channel_name)
                log_message = f"User ID: {message.author.mention} | Command: !sendmessage | Channel Name:  {target_channel.mention}"
                await log_channel.send(log_message)

            except discord.Forbidden:
                await message.channel.send("I don't have permission to send messages.")
            except discord.HTTPException:
                await message.channel.send("An error occurred while sending the message.")
        else:
            await message.channel.send("You don't have the required role to execute this command.")
    else:
        await message.channel.send("This command can only be used in the workspace channel.")


async def kick_user(message, target_user):
    
    '''This command can only be executed in the channel you specify here'''
    if message.channel.id == 'YOUR CHANNEL ID':
        try:
            user_id_or_mention, *kick_reason = message.content.split()[1:]  # Extract the target user ID or mention and the kick reason
            kick_reason = ' '.join(kick_reason)

            guild = message.guild  # Get the guild object

            required_roles = {"Roles that can use this command"}

            '''This condition checks that only the roles defined inside the code can use this command'''
            if any(role.name in required_roles for role in message.author.roles):

                if re.match(r'<@!?(\d+)>', user_id_or_mention):

                    target_user_id = int(re.findall(r'\d+', user_id_or_mention)[0])
                else:

                    target_user_id = int(user_id_or_mention)

                target_user = guild.get_member(target_user_id) 

                if target_user:
                    
                    '''No one can kick themselves'''
                    if target_user.id == message.author.id:
                        await message.channel.send("You cannot kick yourself.")
                    
                    else:
                        await target_user.kick(reason=kick_reason)
                        await message.channel.send(f"{target_user.mention} has been kicked from the server | Reason: {kick_reason}")
                        
                        '''
                        If this command is used, a report message will be sent to the specified channel. 
                        This report contains information such as the ID of the person who used the command, 
                        details about the command used and the details of the person who was kicked.
                        '''
                        log_channel_name = "discord-bot"
                        log_channel = discord.utils.get(message.guild.channels, name=log_channel_name)
                        log_message = f"User ID: {message.author.mention} | Command: !kick | Target User: {target_user.mention} | Reason: {kick_reason}"
                        await log_channel.send(log_message)

                else:
                    await message.channel.send("User not found.")
            else:
                await message.channel.send("You don't have the required role to execute this command.")
        except IndexError:
            await message.channel.send("Please enter User ID/Mention and kick reason.")
    else:
        await message.channel.send("This command can only be used in the workspace channel.")


async def ban_user(message):
        
    '''This command can only be executed in the channel you specify here'''
    if message.channel.id == 'YOUR CHANNEL ID':
        try:
            _, target_user_input, *ban_reason = message.content.split()
            ban_reason = ' '.join(ban_reason)

            guild = message.guild

            required_roles = {"Roles that can use this command"}

            # Check if the author is a guild member
            if isinstance(message.author, discord.Member):
                author_roles = set(role.name for role in message.author.roles)
                
                '''This condition checks that only the roles defined inside the code can use this command'''
                if author_roles.intersection(required_roles):
                    if re.match(r'<@!?(\d+)>', target_user_input):

                        target_user_id = int(re.findall(r'\d+', target_user_input)[0])
                    else:

                        target_user_id = int(target_user_input)

                    target_user = guild.get_member(target_user_id)

                    '''No one can ban themselves'''
                    if target_user:
                        if target_user.id == message.author.id:
                            await message.channel.send("You cannot ban yourself.")

                        else:
                            await target_user.ban(reason=ban_reason)  # Provide the ban reason
                            await message.channel.send(f"{target_user.mention} has been banned from the server | Reason: {ban_reason}")

                            '''
                            If this command is used, a report message will be sent to the specified channel. 
                            This report contains information such as the ID of the person who used the command, 
                            details about the command used and the details of the person who was banned.
                            '''
                            log_channel_name = "discord-bot"
                            log_channel = discord.utils.get(message.guild.channels, name=log_channel_name)
                            log_message = f"User ID: {message.author.mention} | Command: !ban | Target User: {target_user.mention} | Reason: {ban_reason}"
                            await log_channel.send(log_message)

                    else:
                        await message.channel.send("User not found.")
                else:
                    await message.channel.send("You don't have the required role to execute this command.")
            else:
                await message.channel.send("Message author is not a guild member.")
        except IndexError:
            await message.channel.send("Please enter User ID/Mention and ban reason.")
    else:
        await message.channel.send("This command can only be used in the workspace channel.")



async def add_member_to_channel(message, channel_mention, user_mention):

    '''This command can only be executed in the channel you specify here'''
    if message.channel.id == 'YOUR CHANNEL ID':
        guild = message.guild
        
        required_roles = {"Roles that can use this command"}

        '''This condition checks that only the roles defined inside the code can use this command'''
        if any(role.name in required_roles for role in message.author.roles):
            channel_id = int(re.findall(r'\d+', channel_mention)[0])
            
            '''You must specify the categories in which you want to add a user'''
            target_category = [
                guild.get_channel('YOUR CATEGORY ID')
            ]

            '''Checks whether users can be added to this category or not'''
            if not any(target_category):
                await message.channel.send("Channel not found or not in the ticket category")
                return

            '''Gets the ID of the categories in the list'''
            target_channel = None
            for category in target_category:
                if category is not None:  # Check if category is not None
                    target_channel = discord.utils.get(category.channels, id=channel_id)
                    if target_channel:
                        break
            

            member = get_member_by_mention(guild, user_mention)
            if not member:
                await message.channel.send("User not found.")
                return
            
            if target_channel.permissions_for(member).read_messages:
                await message.channel.send(f"{member.mention} can see {target_channel.mention}!")
                return

            await target_channel.set_permissions(member, read_messages=True, send_messages=True)
            await message.channel.send(f"{member.mention} has been added to the channel.")

            '''
            If this command is used, a report message will be sent to the specified channel. 
            This report contains information such as the ID of the person who used the command, 
            details about the command used and the details of the person who was added to channel.
            '''
            log_channel_name = "discord-bot"
            log_channel = discord.utils.get(message.guild.channels, name=log_channel_name)
            log_message = f"User ID: {message.author.mention} | Command: !addmember | Target Channel: {target_channel.mention} | Target User: {member.mention}"
            await log_channel.send(log_message)
            
        else:
            await message.channel.send("You don't have the required role to execute this command.")
    else:
        await message.channel.send("This command can only be used in the workspace channel.")


async def remove_member_from_channel(message, channel_mention, user_mention):
    
    '''This command can only be executed in the channel you specify here'''    
    if message.channel.id == 'YOUR CHANNEL ID':
        guild = message.guild

        required_roles = {"Roles that can use this command"}

        '''This condition checks that only the roles defined inside the code can use this command'''        
        if any(role.name in required_roles for role in message.author.roles):
            channel_id = int(re.findall(r'\d+', channel_mention)[0])
            
            '''You must specify the categories in which you want to remove a user'''
            target_category = [
                guild.get_channel('YOUR CATEGORY ID')
            ]

            '''Checks whether users can be removed from this category or not'''
            if not any(target_category):
                await message.channel.send("Channel not found or not in the ticket category.")
                return

            '''Gets the ID of the categories in the list'''
            target_channel = None
            for category in target_category:
                if category is not None:  # Check if category is not None
                    target_channel = discord.utils.get(category.channels, id=channel_id)
                    if target_channel:
                        break


            member = get_member_by_mention(guild, user_mention)
            if not member:
                await message.channel.send("User not found.")
                return
            
            if not target_channel.permissions_for(member).read_messages:
                await message.channel.send(f"{member.mention} cannot see {target_channel.mention}!")
                return

            await target_channel.set_permissions(member, read_messages=False, send_messages=False)
            await message.channel.send(f"{member.mention} has been removed from the channel.")

            '''
            If this command is used, a report message will be sent to the specified channel. 
            This report contains information such as the ID of the person who used the command, 
            details about the command used and the details of the person who was removed from channel.
            '''
            log_channel_name = "discord-bot"
            log_channel = discord.utils.get(message.guild.channels, name=log_channel_name)
            log_message = f"User ID: {message.author.mention} | Command: !removemember | Target Channel: {target_channel.mention} | Target User: {member.mention}"
            await log_channel.send(log_message)

        else:
            await message.channel.send("You don't have the required role to execute this command.")
    else:
        await message.channel.send("This command can only be used in the workspace channel.")


async def rename_channel(message, channel_mention, new_name):
    
    '''This command can only be executed in the channel you specify here'''    
    if message.channel.id == 'YOUR CHANNEL ID':
        guild = message.guild
        
        required_roles = {"Roles that can use this command"}

        '''This condition checks that only the roles defined inside the code can use this command'''        
        if any(role.name in required_roles for role in message.author.roles):
            channel_id = int(re.findall(r'\d+', channel_mention)[0])
            
            '''You must specify the categories in which you want to rename the channels'''
            target_category = [
                guild.get_channel('YOUR CATEGORY ID')
            ]

            '''Gets the ID of the categories in the list'''
            target_channel = None
            for category in target_category:
                if category is not None:  # Check if category is not None
                    target_channel = discord.utils.get(category.channels, id=channel_id)
                    if target_channel:
                        break

            '''Checks whether channel can be renamed or not'''
            if not target_channel:
                await message.channel.send("Channel not found or not in the ticket category.")
                return

            await target_channel.edit(name=new_name)
            await message.channel.send(f"The channel has been renamed to {target_channel.mention}.")

            '''
            If this command is used, a report message will be sent to the specified channel. 
            This report contains information such as the ID of the person who used the command, 
            details about the command used and the details of the channel was renamed.
            '''
            log_channel_name = "discord-bot"
            log_channel = discord.utils.get(message.guild.channels, name=log_channel_name)
            log_message = f"User ID: {message.author.mention} | Command: !renamechannel | Target Channel: {target_channel.mention}"
            await log_channel.send(log_message)

        else:
            await message.channel.send("You don't have the required role to execute this command.")
    else:
        await message.channel.send("This command can only be used in the workspace channel.")

'''This function calculates the number of players on the 
server and displays this number in the bot game activity section'''
def get_player_count():
    try:
        response = requests.get('YOUR FIVEM SERVER IP')  # Replace with your FiveM server IP
        if response.status_code == 200:
            player_data = response.json()
            return len(player_data) 
    except:
        pass
    return 'Server is Off'

'''Update game activity'''
@tasks.loop(seconds=30)
async def update_game_activity():
    player_count = get_player_count()
    await client.change_presence(activity=discord.Game(f'Players: {player_count}'))

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    update_game_activity.start()

# Code execution
if __name__ == "__main__":

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return


        if message.content.startswith('!addrole'):
            await message.delete()
            args = message.content.split(' ')
            if len(args) < 3:
                await message.channel.send("Invalid command format. Use `!addrole @role_name @user`.")
                return

            role_name = args[1]
            target_user = get_member_by_mention(message.guild, args[2])
            await add_role(message, role_name, target_user)

        
        elif message.content.startswith('!removerole'):
            await message.delete()
            args = message.content.split(' ')
            if len(args) < 3:
                await message.channel.send("Invalid command format. Use `!removerole @role_name @user`.")
                return

            role_name = args[1]
            target_user = get_member_by_mention(message.guild, args[2])
            await remove_role(message, role_name, target_user)

        
        elif message.content.startswith('!sendmessage'):
            await message.delete()
            args = message.content.split(' ', 2)
            if len(args) < 3:
                await message.channel.send("Invalid command format. Use `!sendmessage #channel <content>`.")
                return

            channel_mention = args[1]
            content = args[2]
            await send_message(message, channel_mention, content)

        
        elif message.content.startswith('!kick'):
            await message.delete()
            args = message.content.split(' ')
            if len(args) < 2:
                await message.channel.send("Invalid command format. Use `!kick @user`.")
                return

            target_user = get_member_by_mention(message.guild, args[1])
            await kick_user(message, target_user)

        
        elif message.content.startswith('!ban'):
            await message.delete()
            args = message.content.split(' ')
            if len(args) < 2:
                await message.channel.send("Invalid command format. Use `!ban @user`.")
                return
            
            await ban_user(message)

        
        elif message.content.startswith('!addmember'):
            await message.delete()
            args = message.content.split(' ')
            if len(args) < 3:
                await message.channel.send("Invalid command format. Use `!addmember #channel @user`.")
                return

            channel_mention = args[1]
            user_mention = args[2]
            await add_member_to_channel(message, channel_mention, user_mention)

        
        elif message.content.startswith('!removemember'):
            await message.delete()
            args = message.content.split(' ')
            if len(args) < 3:
                await message.channel.send("Invalid command format. Use `!removemember #channel @user`.")
                return

            channel_mention = args[1]
            user_mention = args[2]
            await remove_member_from_channel(message, channel_mention, user_mention)


        elif message.content.startswith('!renamechannel'):
            await message.delete()
            args = message.content.split(' ')
            if len(args) < 3:
                await message.channel.send("Invalid command format. Use `!renamechannel #channel new_name`.")
                return
            
            channel_mention = args[1]
            new_name = ' '.join(args[2:])
            await rename_channel(message, channel_mention, new_name)
        
    # Replace 'YOUR_TOKEN' with your Discord bot token
    client.run('YOUR_TOKEN')