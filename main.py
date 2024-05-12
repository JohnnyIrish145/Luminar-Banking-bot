# This code was written by Johnnyirish (On Discord), or JohnnyIrish145 (On Github)

# To anyone reading this code, I can wish you the best of luck.
import discord
from datetime import datetime
import pytz
from responses import response_balance
from responses import payment
import json
import math
import asyncio
import calendar
import time

intents = discord.Intents.all()
client = discord.ext.commands.Bot(command_prefix="$", intents=intents, sync_commands=True) # Syncs up commands and sets ctx command up with "$" as caller

TOKEN = "" # Discord bot token, get your discord bot token here: https://discord.com/developers/applications

# Settings
OWNER = # Owner discord id goes here (int)
co_OWNER = # Co owner discord id goes here (int)
bank_name = "Bank of Luminar"
interest_rate = 2.5 # Set the interest rate %
withdraw_fee = 2.3 # Set the withdraw fee %
emoji = "✅" # Emoji used to mark withdrawls for easier withdrawl tracking
colour_stripe = discord.Colour.dark_teal() # Embed stripe color 
# Channels
withdraws = # Withraw channel id (int)
log = # Logs channel id (int)
allbal = # All balance command channel id (int)
server_id = # Discord server id (int)
Console_channel = # Console channel id (int)
interest_channel = # Interest channel id (int)
error_channel = # Errors channel id (int)


# Starting the bot up
@client.event
async def on_ready():
    newYorkTz = pytz.timezone("America/New_York") 
    timeInNewYork = datetime.now(newYorkTz)
    current_time = timeInNewYork.strftime("%a:%H:%M:%S")
    print("-----")
    print(f"{client.user} is now running")
    print("Time: ", current_time)
    await client.tree.sync()
    embed = discord.Embed(
        colour=colour_stripe,
        description="Bank console",
        title=f"{client.user} is now running")
    embed.set_author(name=bank_name)
    await client.get_channel(Console_channel).send(embed=embed)

# Sends new member that joins the server a welcome message
@client.event 
async def on_member_join(member):
    if member.guild.id == server_id:
        embed = discord.Embed(
                colour=colour_stripe,
                description=bank_name,
                title='To make an account do "/bal"')
        embed.set_author(name=f'Thank you for joining the {bank_name} server!')
        await member.send(embed=embed)
    return

# Catches all errors and sends them to error channel for debugging
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    embed = discord.Embed(
            colour=colour_stripe,
            description=bank_name,
            title="An error occurred")
    embed.set_author(name=f'We are very sorry, the {bank_name} is having troubles.')
    await ctx.send(embed=embed)
    await client.get_channel(error_channel).send(error)

# All balance ctx command, sums up all balances, except for the owner's balance, and gives an entire bank balance amount
@client.command()
async def allbalance(ctx):
    user_id = int(ctx.message.author.id)
    if user_id == OWNER or user_id == co_OWNER:
        newYorkTz = pytz.timezone("America/New_York")
        timeInNewYork = datetime.now(newYorkTz)
        currentTimeInNewYork = timeInNewYork.strftime("%a:%H:%M:%S")
        filename = "Bal.json"
        with open(filename, 'r') as f:
            data = json.load(f)
        f.close()
        accounts = data.get('accounts', [])
        entry = data["accounts"]
        data_length = len(entry)
        i = 0
        bank_balance = 0
        while True:
            entry = data["accounts"]
            entry = entry[i]
            user_id = entry["user_id"]
            user_balance = entry["balance"]
            if user_id == OWNER or user_id == co_OWNER:
                i+=1
            else:
                i+=1
                bank_balance = user_balance + bank_balance
            if data_length <= i:
                bank_balance = float(round(bank_balance, 2))
                bank_balance = format(float(bank_balance),",")
                colour_stripe = discord.Colour.dark_teal()
                embed = discord.Embed(
                colour=colour_stripe,
                description="Bank balance interface",
                title=f"Bank balance is ${bank_balance}")
                print("-----")
                print(f"Time: ", currentTimeInNewYork)
                print(f'Allbalance: ${bank_balance}')
                embed.set_author(name=bank_name)
                await client.get_channel(allbal).send(embed=embed)
                break
    else:
        pass

# Logging ctx command, for logging the Bal.json file manually, it is logged automaticlly every week before and after interest payment
@client.command()
async def logs(ctx):
    user_id = int(ctx.message.author.id)
    if user_id == OWNER or user_id == co_OWNER:
        newYorkTz = pytz.timezone("America/New_York")
        timeInNewYork = datetime.now(newYorkTz)
        currentTimeInNewYork = timeInNewYork.strftime("%a:%H:%M:%S")
        filename = "Bal.json"
        print("-----")
        print(f"Time: ", currentTimeInNewYork)
        print(f'{filename} has been logged!')
        await client.get_channel(log).send(file=discord.File(fp=filename, filename=filename, spoiler=True))
    else:
        pass

# Paying interest ctx command, for mannually paying interest, it is done automaticlly every week
# Interest rate is set at 2.5% currentlly, you can change it by chaning the "interest_rate" varible
@client.command()
async def pay_interest(ctx):
    newYorkTz = pytz.timezone("America/New_York")
    timeInNewYork = datetime.now(newYorkTz)
    currentTimeInNewYork = timeInNewYork.strftime("%a:%H:%M:%S")
    filename = "Bal.json"
    print("-----")
    print(f"Time: ", currentTimeInNewYork)
    print(f'{filename} has been logged!')
    await client.get_channel(log).send(file=discord.File(fp=filename, filename=filename, spoiler=True)) # Auto logging file before hand
    
    user_id = int(ctx.message.author.id)
    if user_id == OWNER or user_id == co_OWNER:
        newYorkTz = pytz.timezone("America/New_York")
        timeInNewYork = datetime.now(newYorkTz)
        currentTimeInNewYork = timeInNewYork.strftime("%a:%H:%M:%S")
        print("-----")
        print("Time: ", currentTimeInNewYork)
        print('Interest has been paid!')
        print(f'Interest rate is {interest_rate}%!')
        filename = "Bal.json"
        with open(filename, 'r') as f:
            data = json.load(f)
        f.close()
        accounts = data.get('accounts', [])

        entry = data["accounts"]
        data_length = len(entry) - 1
        i = -1
        while True:
            i+=1
            entry = data["accounts"]
            entry = entry[i]
            user_id = entry["user_id"]
            user_old_balance = entry["balance"]
            user_new_balance = user_old_balance + user_old_balance * (interest_rate/100)
            user_new_balance = float(round(user_new_balance, 2))
            entry["balance"] = user_new_balance
            if user_new_balance > 10:
                user_old_balance = format(float(user_old_balance),",")
                user_new_balance = format(float(user_new_balance),",")
                colour_stripe = discord.Colour.dark_teal()
                bank_name = "Bank of bank"
                embed = discord.Embed(
                colour=colour_stripe,
                description="Interest interface",
                title=f"Interest has been paid:\nyour new balance is ${user_new_balance}, \nyour balance was ${user_old_balance}")
                embed.set_author(name=bank_name)
                try:
                    if OWNER != user_id:
                        user = client.get_user(user_id)
                        await user.send(embed=embed, silent=True)
                except:
                    pass

            if data_length <= i:
                with open(filename, 'w') as f:
                    accounts = {"accounts": accounts}
                    json.dump(accounts, f, indent=4)
                    embed = discord.Embed(
                    colour=colour_stripe,
                    description="Interest interface",
                    title=f"Interest payed!")
                embed.set_author(name=bank_name)
                await client.get_channel(interest_channel).send(embed=embed)
                
                newYorkTz = pytz.timezone("America/New_York")
                timeInNewYork = datetime.now(newYorkTz)
                currentTimeInNewYork = timeInNewYork.strftime("%a:%H:%M:%S")
                filename = "Bal.json"
                print("-----")
                print(f"Time: ", currentTimeInNewYork)
                print(f'{filename} has been logged!')
                await client.get_channel(log).send(file=discord.File(fp=filename, filename=filename, spoiler=True)) # Auto logging file after paying interest
                break
    else:
        pass

# Slash command, allows users to calculate the current withdraw fee
# Current rate is set at 2.3% currentlly, you can change it by chaning the "withdraw_fee" varible
@client.tree.command(name = "fee", description="Calculate the fee for withdraws, current fee is {withdraw_fee}%")
async def fee(interaction : discord.Interaction, amount: float):
    username = str(interaction.user)
    user_id = str(interaction.user.id)
    channel = str(interaction.channel)

    print("---")
    print(f"User: {username}")
    print(f"User_id: {user_id}")
    newYorkTz = pytz.timezone("America/New_York")
    timeInNewYork = datetime.now(newYorkTz)
    current_time = timeInNewYork.strftime("%a:%H:%M:%S")
    print("Time: ", current_time)
    if amount <= 1:
        embed = discord.Embed(
        colour=colour_stripe,
        description="Fee calculation interface",
        title=f"Please put in an amount that is more than $1")
        embed.set_author(name=bank_name)
        print("Tried to find the fee for less than $1")
        Hidden = True
    else:
        amount_fee = amount - amount * (withdraw_fee/100)
        amount_fee = float(amount_fee * 100)
        amount_fee = math.floor(amount_fee)
        amount_fee = float(amount_fee / 100)

        amount = format(float(amount),",")
        amount_fee = format(float(amount_fee),",")
        print(f"Command: /fee")
        print(f"Amount: ${amount}")
        print(f"After fee: ${amount_fee}")

        if channel == f"Direct Message with {username}":
            Hidden = False
            print(f"{channel}")
        else:
            Hidden = True
            print(f"In channel: #{channel}")

        embed = discord.Embed(
                colour=colour_stripe,
                description="Fee calculation interface",
                title=f"Fees after ${amount} is ${amount_fee}")
        embed.set_author(name=bank_name)
    await interaction.response.send_message(embed=embed, ephemeral=Hidden)

# Slash command, allows users to calculate the current interest rate
# Interest rate is set at 2.5% currentlly, you can change it by chaning the "interest_rate" varible
@client.tree.command(name = "interest", description="Calculate compound interest, current interest rate is {interest_rate}%")
async def interest(interaction : discord.Interaction, amount: float, weeks: int):
    username = str(interaction.user)
    user_id = str(interaction.user.id)
    channel = str(interaction.channel)

    print("---")
    print(f"User: {username}")
    print(f"User_id: {user_id}")
    newYorkTz = pytz.timezone("America/New_York")
    timeInNewYork = datetime.now(newYorkTz)
    current_time = timeInNewYork.strftime("%a:%H:%M:%S")
    print("Time: ", current_time)
    if amount <= 1:
        embed = discord.Embed(
        colour=colour_stripe,
        description="Interest calculation interface",
        title=f"Please put in an amount that is more than $1")
        embed.set_author(name=bank_name)
        print("Tried to find the interest for less than $1")
    elif weeks <= 0:
        embed = discord.Embed(
        colour=colour_stripe,
        description="Interest calculation interface",
        title=f"Please put in a time period of more than 1 week")
        embed.set_author(name=bank_name)
        print("Tried to find the interest for less than 1 week")
    else:
        interest_amount = amount
        for i in range(weeks):
            interest_amount = interest_amount + interest_amount * (interest_rate/100)
        interest_amount = float(interest_amount * 100)
        interest_amount = math.floor(interest_amount)
        interest_amount = float(interest_amount / 100)
        
        
        
        amount = format(float(amount),",")
        interest_amount = format(float(interest_amount),",")
        print(f"Command: /interest")
        print(f"Amount: ${amount}")
        print(f"Weeks: {weeks}")
        print(f"After weeks: ${interest_amount}")
        if channel == f"Direct Message with {username}":
            Hidden = False
            print(f"{channel}")
        else:
            Hidden = True
            print(f"In channel: #{channel}")

        embed = discord.Embed(
                colour=colour_stripe,
                description="Interest calculation interface",
                title=f"Interest for ${amount} after {weeks} weeks is ${interest_amount}")
        embed.set_author(name=bank_name)
    await interaction.response.send_message(embed=embed, ephemeral=Hidden)

# Slash command, shows user his personal balance
# This command is hidden to everyone, unless the user dms the bot privately, which it then sends as a normal response
@client.tree.command(name = "bal", description="Shows your current balance")
async def bal(interaction : discord.Interaction):
    username = str(interaction.user)
    user_id = str(interaction.user.id)
    channel = str(interaction.channel)
    
    print("---")
    print(f"User: {username}")
    print(f"User_id: {user_id}")
    newYorkTz = pytz.timezone("America/New_York") 
    timeInNewYork = datetime.now(newYorkTz)
    current_time = timeInNewYork.strftime("%a:%H:%M:%S")
    print("Time: ", current_time)
    responses = response_balance(user_id)
    
    if channel == f"Direct Message with {username}":
        Hidden = False
        print(f"{channel}")
    else:
        Hidden = True
        print(f"In channel: #{channel}")
    print(f"Command: /bal")
    
    if responses == "null":
        print(f"New account made for {username}")
        embed = discord.Embed(
                colour=colour_stripe,
                description="Account balance interface",
                title=f"Your account has been made! Thank you for choosing {bank_name}!")
        embed.set_author(name=bank_name)
        if channel == f"Direct Message with {username}":
            pass
        else:
            await interaction.user.send(embed=embed)
            
    else:
        print(f"Balance: {responses}")
        responses_format = str(responses)
        responses_format = format(float(responses_format),",")
        resp = "$" + responses_format
        
        embed = discord.Embed(
                colour=colour_stripe,
                description="Account balance interface",
                title=resp)
        embed.set_author(name=bank_name)
    await interaction.response.send_message(embed=embed, ephemeral=Hidden)

# Slash command, shows users his personal balance and his username along side it
# This command is not hidden from everyone, it shows the users balance to everyone in that channel
@client.tree.command(name = "flex", description="Show everyone how rich you are!")
async def flex(interaction : discord.Interaction):
    username = str(interaction.user)
    user_id = str(interaction.user.id)
    channel = str(interaction.channel)    
    print("---")
    print(f"User: {username}")
    print(f"User_id: {user_id}")
    newYorkTz = pytz.timezone("America/New_York") 
    timeInNewYork = datetime.now(newYorkTz)
    current_time = timeInNewYork.strftime("%a:%H:%M:%S")
    print("Time: ", current_time)
    responses = response_balance(user_id)
    
    if channel == f"Direct Message with {username}":
        print(f"{channel}")
    else:
        print(f"In channel: #{channel}")
    
    print(f"Command: /flex")
    
    if responses == "null":
        print(f"New account made for {username}")
        if channel == f"Direct Message with {username}":
            embed = discord.Embed(
                colour=colour_stripe,
                description="Account balance interface",
                title=f"Your account has been made! Thank you for choosing {bank_name}!")
            embed.set_author(name=bank_name)
        else:
            embed = discord.Embed(
                colour=colour_stripe,
                description="Account balance interface",
                title=f"Your account has been made! Thank you for choosing {bank_name}!")
            embed.set_author(name=bank_name)
        
        
            await interaction.user.send(embed=embed)
            embed = discord.Embed(
                colour=colour_stripe,
                description="Account balance interface",
                title=f"New account made for {username}! Thank you for choosing {bank_name}!")
            embed.set_author(name=bank_name)
    else:
        print(f"Balance: {responses}")
        responses_format = str(responses)
        responses_format = format(float(responses_format),",")
        resp = f"Balance of {username} is $" + responses_format
        embed = discord.Embed(
                colour=colour_stripe,
                description="Account balance interface",
                title=resp)
        embed.set_author(name=bank_name)
    
    await interaction.response.send_message(embed=embed, ephemeral=False)

# Slash command, allows user to pay another user via there username
# They will also need to provide a private message to the user, an amount and should the payment be hidden or not
@client.tree.command(name = "pay", description="Pay someone")
async def pay(interaction : discord.Interaction, amount: float, user: discord.User, message: str, hidden: bool):
    username = str(interaction.user)
    user_id = str(interaction.user.id)
    channel = str(interaction.channel)
    amount = float(amount * 100)
    amount = math.floor(amount)
    amount = float(amount / 100)
    print("---")
    print(f"User: {username}")
    print(f"User_id: {user_id}")
    newYorkTz = pytz.timezone("America/New_York")
    timeInNewYork = datetime.now(newYorkTz)
    current_time = timeInNewYork.strftime("%a:%H:%M:%S")
    print("Time:", current_time)
    responses = response_balance(user_id)
    if channel == f"Direct Message with {username}":
        print(f"{channel}")
    else:
        print(f"In channel: #{channel}")
    print(f"Command: /pay")
    receiver = int(user.id)
    sender = int(user_id)
    if responses == "null":
        print(f"New account made for {username}")
        if channel == f"Direct Message with {username}":
            embed = discord.Embed(
                colour=colour_stripe,
                description="Account balance interface",
                title=f"Your account has been made! Thank you for choosing {bank_name}!")
            embed.set_author(name=bank_name)
            hidden = False
        else:
            embed = discord.Embed(
                colour=colour_stripe,
                description="Account balance interface",
                title=f"Your account has been made! Thank you for choosing {bank_name}!")
            embed.set_author(name=bank_name)


            await interaction.user.send(embed=embed)
            embed = discord.Embed(
                colour=colour_stripe,
                description="Account balance interface",
                title=f"New account made for {username}! Thank you for choosing {bank_name}!")
            embed.set_author(name=bank_name)
            hidden = False
    else:
        responses = float(responses)
        if sender == receiver:
            embed = discord.Embed(
                colour=colour_stripe,
                description="Payment interface",
                title=f"Sorry, you can not send funds to yourself")
            embed.set_author(name=bank_name)
            print("Sent funds to himself")
            hidden = True
        elif receiver == 557628352828014614 or receiver == 720351927581278219 or receiver == 1193283628709462097:
            embed = discord.Embed(
                colour=colour_stripe,
                description="Payment interface",
                title=f"Sorry, you can not send funds to bots")
            embed.set_author(name=bank_name)
            hidden = True
            print("Sent funds to a bot")
        else:
            if amount <= 0:
                embed = discord.Embed(
                colour=colour_stripe,
                description="Payment interface",
                title=f"Please put in an amount that is more than $0")
                embed.set_author(name=bank_name)
                print("Sent less than $1")
                hidden = True
            elif amount > responses:
                embed = discord.Embed(
                colour=colour_stripe,
                description="Payment interface",
                title=f"You do not have sufficient funds")
                embed.set_author(name=bank_name)
                print("Insufficient funds")
                hidden = True
            else:               
                exsists = payment(sender, receiver, amount, responses)
                receiver_old_balance = float(exsists[1])
                exsists = exsists[0]
                receiver_new_balance = receiver_old_balance + float(amount)
                sender_new_balance = responses - float(amount)
                if sender == OWNER or sender == co_OWNER:
                    if exsists == False:
                        responses = response_balance(receiver)
                        if responses == "null":
                            print(f"New account made for {user}")
                            embed = discord.Embed(
                            colour=colour_stripe,
                            description="Account balance interface",
                            title=f"Your account has been made! Thank you for choosing {bank_name}!")
                            embed.set_author(name=bank_name)

                            await user.send(embed=embed)

                            responses = response_balance(user_id)
                            receiver = int(user.id)
                            exsists = payment(sender, receiver, amount, responses)
                            receiver_old_balance = float(exsists[1])
                            exsists = exsists[0]
                            receiver_new_balance = receiver_old_balance + float(amount)
                            sender_new_balance = responses - float(amount)
                if exsists == False:
                    embed = discord.Embed(
                    colour=colour_stripe,
                    description="Payment interface",
                    title=f"Sorry, but {user} does not have an account")
                    embed.set_author(name=bank_name)
                    hidden = True
                if exsists == True:
                    sender_new_balance = float(responses) - amount
                    print(f"Sender: {sender}")
                    print(f"Sender old balance: {responses}")
                    print(f"Sender new balance: {sender_new_balance}")
                    print(f"Amount sent: {amount}")
                    print(f"Receiver: {receiver}")
                    print(f"Receiver old balance {receiver_old_balance}")
                    print(f"Receiver new balance {receiver_new_balance}")
                    sender_bal = format(float(sender_new_balance),",")
                    sender_bal_old = format(float(responses),",")
                    amount = format(float(amount),",")
                    receiver_old_balance = format(float(receiver_old_balance),",")
                    receiver_new_balance = format(float(receiver_new_balance),",")
                    timestamp = calendar.timegm(time.gmtime())
                    embed = discord.Embed(
                        colour=colour_stripe,
                        description="Payment interface",
                        title=f'User {username} has sent you ${amount} with a message,\n"{message}". \nYour old balance ${receiver_old_balance}, \nyour new balance ${receiver_new_balance}.\nTime: <t:{timestamp}:F>')
                    embed.set_author(name=bank_name)

                    await user.send(embed=embed)

                    embed = discord.Embed(
                        colour=colour_stripe,
                        description="Bank console",
                        title=f"Sender {username},\nSender old balance: {sender_bal_old},\nSender new balance: {sender_bal},\nReceiver {user},\nReceiver old balance {receiver_old_balance},\nReceiver new balance {receiver_new_balance},\nAmount sent: {amount},\nTimestamp: <t:{timestamp}:F>")
                    embed.set_author(name=bank_name)
                    await client.get_channel(Console_channel).send(embed=embed)
                    if channel == f"Direct Message with {username}":
                        embed = discord.Embed(
                        colour=colour_stripe,
                        description="Payment interface",
                        title=f"You successfully paid {user} ${amount}, \nyour new balance is ${sender_bal}.\nTime: <t:{timestamp}:F>")
                        embed.set_author(name=bank_name)
                        hidden = False
                    else:
                        if hidden == False:
                            resp = f"{username} paid ${amount} to {user} at <t:{timestamp}:F>"
                        else:
                            resp = f"You paid {user} ${amount}, \nyour new balance is ${sender_bal}.\nTime: <t:{timestamp}:F>"
                        embed = discord.Embed(
                        colour=colour_stripe,
                        description="Payment interface",
                        title=f"You successfully paid {user} ${amount}, \nyour new balance is ${sender_bal}.\nTime: <t:{timestamp}:F>")
                        embed.set_author(name=bank_name)


                        await interaction.user.send(embed=embed, silent=True)
                        embed = discord.Embed(
                        colour=colour_stripe,
                        description="Payment interface",
                        title=resp)
                        embed.set_author(name=bank_name)
                    print(f"Hidden: {hidden}")
    await interaction.response.send_message(embed=embed, ephemeral=hidden)

# Slash command, allows user to withraw
# It sends the funds to the Owner's balance and sends a message to the withdrawl channel
@client.tree.command(name = "withdraw", description="Withdraw your cash")
async def withdraw(interaction : discord.Interaction, amount: float, ign: str, hidden: bool):
    username = str(interaction.user)
    user_id = str(interaction.user.id)
    channel = str(interaction.channel)
    amount = float(amount * 100)
    amount = math.floor(amount)
    amount = float(amount / 100)
    print("---")
    print(f"User: {username}")
    print(f"User_id: {user_id}")
    newYorkTz = pytz.timezone("America/New_York") 
    timeInNewYork = datetime.now(newYorkTz)
    current_time = timeInNewYork.strftime("%a:%H:%M:%S")
    print("Time:", current_time)
    responses = response_balance(user_id)
    
    if channel == f"Direct Message with {username}":
        print(f"{channel}")
    else:
        print(f"In channel: #{channel}")
    print(f"Command: /withdraw")
    receiver = OWNER
    user = client.get_user(receiver)
    sender = int(user_id)
    amount_fee = amount - amount * (withdraw_fee/100)
    amount_fee = float(amount_fee * 100)
    amount_fee = math.floor(amount_fee)
    amount_fee = float(amount_fee / 100)
    if responses == "null":
        print(f"New account made for {username}")
        if channel == f"Direct Message with {username}":
            embed = discord.Embed(
                colour=colour_stripe,
                description="Account balance interface",
                title=f"Your account has been made! Thank you for choosing {bank_name}!")
            embed.set_author(name=bank_name)
            hidden = False
        else:
            embed = discord.Embed(
                colour=colour_stripe,
                description="Account balance interface",
                title=f"Your account has been made! Thank you for choosing {bank_name}!")
            embed.set_author(name=bank_name)
        
        
            await interaction.user.send(embed=embed)
            embed = discord.Embed(
                colour=colour_stripe,
                description="Account balance interface",
                title=f"New account made for {username}! Thank you for choosing {bank_name}!")
            embed.set_author(name=bank_name)
            hidden = False
    else:
        responses_format = format(float(responses),",")
        responses = float(responses)
        if sender == receiver:
            embed = discord.Embed(
                colour=colour_stripe,
                description="Withdraw dashboard",
                title=f"Sorry, you can not send funds to yourself")
            embed.set_author(name=bank_name)
            print("Sent funds to himself")
            hidden = True
        else:
            if amount <= 10:
                embed = discord.Embed(
                colour=colour_stripe,
                description="Withdraw dashboard",
                title=f"Please put in an amount that is more than $10")
                embed.set_author(name=bank_name)
                print("Tried to withdraw less than $10")
                hidden = True
            elif amount > responses:
                embed = discord.Embed(
                colour=colour_stripe,
                description="Withdraw dashboard",
                title=f"Insufficient funds, please put in an amount that is under ${responses}")
                embed.set_author(name=bank_name)
                print("Insufficient funds")
                hidden = True
            else:
                exsists = payment(sender, receiver, amount, responses)
                exsists = exsists[0]
                sender_new_balance = responses - float(amount)
                
                
                if exsists == False:
                    embed = discord.Embed(
                    colour=colour_stripe,
                    description="Withdraw dashboard",
                    title=f"We are very sorry {username}, The {bank_name} is having troubles.")
                    embed.set_author(name=bank_name)
                    hidden = True
                else:
                    sender_new_balance = float(responses) - amount
                    print(f"Withdrawer old balance: {responses}")
                    print(f"Withdrawer new balance: {sender_new_balance}")
                    print(f"Amount withdrawn: {amount}")
                    print(f"After fees: {amount_fee}")
                    sender_bal = format(float(sender_new_balance),",")
                    amount2 = amount
                    amount = format(float(amount),",")
                    timestamp = calendar.timegm(time.gmtime())
                    embed = discord.Embed(
                        colour=colour_stripe,
                        description="Bank console",
                        title=f'User {username} has withdrawn ${amount},\nafter fees ${amount_fee},\nWithdrawer old balance: {responses},\nWithdrawer new balance: {sender_new_balance},\nthere ign: {ign},\ntimestamp: <t:{timestamp}:F>')
                    embed.set_author(name=bank_name)
                    await client.get_channel(Console_channel).send(embed=embed)
                    embed = discord.Embed(
                        colour=colour_stripe,
                        description="Withdraw dashboard",
                        title=f'User {username} has withdrawn ${amount},\nafter fees ${amount_fee},\nthere ign: {ign},\ntimestamp: <t:{timestamp}:F>')
                    embed.set_author(name=bank_name)
                    withdraws_message = await client.get_channel(withdraws).send(embed=embed)
                    
                    await withdraws_message.add_reaction(emoji)
                    amount_fee = format(float(amount_fee),",")
                    if channel == f"Direct Message with {username}":
                        embed = discord.Embed(
                        colour=colour_stripe,
                        description="Withdraw dashboard",
                        title=f"You have successfully withdrawn ${amount}, after fee ${amount_fee}, \nyour new balance is ${sender_bal}.\nTime: <t:{timestamp}:F>")
                        embed.set_author(name=bank_name)
                        hidden = False
                    else:
                        if hidden == False:
                            resp = f"{username} has withdrawn ${amount}, after fee ${amount_fee}.\nTime: <t:{timestamp}:F>"
                        else:
                            resp = f"You have successfully withdrawn ${amount}, after fee ${amount_fee},\nyour new balance is ${sender_bal}.\nTime: <t:{timestamp}:F>"
                        embed = discord.Embed(
                        colour=colour_stripe,
                        description="Withdraw dashboard",
                        title=f"You have successfully withdrawn ${amount}, after fee ${amount_fee},\nyour new balance is ${sender_bal}.\nTime: <t:{timestamp}:F>")
                        embed.set_author(name=bank_name)
        
                        
                        await interaction.user.send(embed=embed, silent=True)
                        embed = discord.Embed(
                        colour=colour_stripe,
                        description="Withdraw dashboard",
                        title=resp)
                        embed.set_author(name=bank_name)
                    print(f"Hidden: {hidden}")
                    print(f"Ign: {ign}")
    await interaction.response.send_message(embed=embed, ephemeral=hidden)

# Reconnection loop, makes sure the bot is always online
async def reconnect_loop():
    while True:
        await asyncio.sleep(1)
        if client.is_closed():
            print('Bot is disconnected, attempting to reconnect...')
            try:
                await client.start(TOKEN)
                print('Reconnect successful.')
                break
            except Exception as e:
                print(f'Reconnect failed, {e}, retrying in 5 seconds...')
                await asyncio.sleep(5)

async def main():
    try:
        await client.start(TOKEN)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Fatal exception {e}, running reconnect loop.")
        await reconnect_loop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
