#discord.__version__ = 1.0.0a
client_id_file 		= open("./private_data/client_id.txt", "r")
token_file 			= open("./private_data/token.txt", "r")
server_id_file 		= open("./private_data/my_server_id.txt", "r")
# admin_secret_file	= open("./private_data/my_admin_secret.txt", "r")
client_id 			= int(client_id_file.read())
server_id 			= int(server_id_file.read())
# admin_secret 		= admin_secret_file.read()
token 				= token_file.read()
permissions 		= 68608

# https://discordapp.com/oauth2/authorize?client_id={CLIENT_ID}&scope=bot&permissions={PERMISSIONSINT}
add_to_server_url = f"https://discordapp.com/oauth2/authorize?client_id={client_id}&scope=bot&permissions={permissions}"
print(add_to_server_url)

import discord
import currency
# from Crypto.Hash import SHA256

# initiates client
client = discord.Client()
currency_lastbench = None

@client.event 	# decorator/wrapper
async def on_ready(currency=currency):

	global currency_lastbench

	# server = client.get_guild(id=server_id) # Eishhtimulation
	
	currency_lastbench = currency.Currency()
	# currency_lastbench.show_balance()

# @bot.command()
# async def getuser(ctx, userid: int):
#     user = bot.get_user(userid)
#     await ctx.send(user.name)

@client.event
async def on_message(message):
	print(f"#{message.channel} : {message.author} : {message.author.name} : {message.content}")

	if "!btctip xxstop" in message.content.lower():
		print("byeeee")
		currency_lastbench.close_file()
		await client.close()
		return
	if "!btctip show my balance" in message.content.lower() and message.author.name!="bitcoin-tip-bot":
		await message.channel.send(f"you have {currency_lastbench.show_balance(str(message.author.id))}sats")
		return
	if "!btctip help" in message.content.lower() and message.author.name!="bitcoin-tip-bot" :
		await message.channel.send("hey hey heyyyyy I'm a bitcoin bot you can use to tip people within this server with some bitcoin. My creator has envisoned me to work with bitcoin's lightning network so you can do microtransaction instantly.\n\nRight now you can only send bitcoin already in circulation but my creator will soon add the feature to withdraw (and deposit) your bitcoin which you can receive on any bitcoin wallet.\n\nTo send money:`!btctip <mention-username-of-receiver> <amt-in-satoshi>`\nExample: `!btctip @ParmuSingh#5099 50` This will send 50 satoshis from your wallet to ParmuSingh's wallet.\n\nTo see your balances:\n`!btctip show my balance`\n\n\nps: 1 satoshi is 0.00000001 bitcoin 		|		 I may not be online all the time.\n\nbeep beep boop boop - created by a smart ass.")
		return
	if "!btctip" in message.content.lower() and message.author.name!="bitcoin-tip-bot":
		try:
			words = message.content.lower().split(' ')
			# print(words)
			# sometimes mentioning user adds another empty char which could fuck things up so I'm removing any spaces registered as words:
			for i in range(len(words)):
				if words[i] == '':
					words.pop(i)
					break
			# print(words)
			# sender_name = message.author.name
			for i in range(len(words)):
				if words[i] == "!btctip":
					recipient = words[i+1]
					amount = words[i+2]
					break
					# not returning if invalid after invoke command cuz it raises exception and program goes on
			# print(f"userID = {recipient[2:len(recipient) - 1]}")
			# print(f"username = {client.get_user(int(recipient[2:len(recipient) - 1]))}")
			
			sender_id = str(message.author.id)
			sender_name = message.author.name
			recipient_id = str(recipient[2:len(recipient) - 1])
			recipient_name = client.get_user(recipient_id)

			print(f"sender_name = {sender_name} | sender_id = {sender_id} | recipient_name = {recipient_name} | recipient_id = {recipient_id}")

			if sender_id == recipient_id:
				await message.channel.send("why would you tip yourself...?")
				return
			# sender_tag = message.author.tag
			# recipient = words[1]
			# amount = words[2]
			success, err = currency_lastbench.do_transaction(sender_name, sender_id, recipient_name, recipient_id, amount)
			if success:
				await message.channel.send(f"hey heyy heyyy\n{amount} satoshis sent to {str(recipient_name).split('#')[0]} from {sender_name}\n\n1 satoshi = 0.00000001 bitcoin")
			else:
				await message.channel.send(f"problem: {err}")

		except ValueError as e:
			print(e)
			await message.channel.send("ay check again")

client.run(token)

