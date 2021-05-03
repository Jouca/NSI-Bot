import discord,json,asyncio,time,traceback,sys,os,base64,gd,io,datetime,secrets,logging
from discord.utils import *
from itertools import chain
from urllib.request import urlopen
import mysql.connector as MC
from mysql.connector import errorcode
from urllib.parse import unquote
from re import search
from PIL import Image,ImageFont,ImageDraw

#########################

# Configs for database :

dbhost = "localhost"
dbdatabase = "nsi"
dbuser = "root"
dbpassword = "password"

#########################

# Configs in globally :

pic_ext = ['.jpg','.png','.jpeg']

jouca = 216708683290247168

nsi_channel = 818859248477536286
logs = 819976240617226320

classeliste = ["S11SNT","S11MATHS","S3SNT","PNSI1","PNSI2"]
roleclasseliste = [["S11SNT",821393232750968862],["S11MATHS",821393373709467679],["S3SNT",821393410425356298],["PNSI1",821393434539458570],["PNSI2",821393611567530035]]
chatclasseliste = [["S11SNT",828938993122148393],["S11MATHS",828938993122148393],["S3SNT",828938952353906769],["PNSI1",828938871752491008],["PNSI2",828938907554152488]]

student_role = 819966009087098881

TOKEN = "TOKEN OF THE BOT"
prefix = "nsi!"

#########################

# When loading the bot :

client = discord.Client(
	status="online",
	chunk_guilds_at_startup=False,
	heartbeat_timeout=60)

try:
	conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
	cursor = conn.cursor()
except MC.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is not right with your username or your password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
finally:
	if(conn.is_connected()):
		cursor.close()
		conn.close()
		print("Connection to the database established !")

conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
cursor = conn.cursor(buffered=True)

ready = True

#########################

@client.event
async def on_message(message):
	try:
		def senderror(content):
			"""
			Permet de crée un embed qui crée un message d'erreur.
			content (str)

			>>> senderror("Vous n'avez pas accès à cette commande.")
			"""
			embed400 = discord.Embed(title="", color=0xff0000)
			embed400.add_field(name=f'Erreur :x:', value=f"{content}")
			return embed400

		def sendsuccess(content):
			"""
			Permet de crée un embed qui crée un message de succès.
			content (str)

			>>> sendsuccess("La commande a bien été mise à jour.")
			"""
			embed1 = discord.Embed(title="", color=0x00ff00)
			embed1.add_field(name=f'Succès :white_check_mark:', value=f"{content}")
			return embed1

		def sendlog(content):
			"""
			Permet de crée un embed qui crée un message de log.
			content (str)

			>>> sendlog("Compte de l'utilisateur Jouca supprimé.")
			"""
			embed123 = discord.Embed(title="", color=0x0000ff)
			embed123.add_field(name=f'LOG :envelope_with_arrow:', value=f"{content}")
			return embed123

		await client.change_presence(activity=discord.Streaming(name="nsi!help", url="https://monlycee.net"))
		
		if message.author.id == client.user.id:
			return

		if not message.content.startswith(prefix):
			return

		msg = message.content.split(prefix)[1]
		args = msg.split(" ")
		
		datetime_object = datetime.datetime.now()

		if msg.startswith("help"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)
				author = message.author.id

				pagehome = embed=discord.Embed(title="Aides", 
                	description="Bievenue sur la page d'aide par rapport au bot !\nRéagisser avec les réactions pour naviguer sur les pages :\n\n:student: = Commandes élèves\n:teacher: = Commandes professeur\n:information_source: = Informations", 
                	color=0x00ff08
            		)
				pageeleve = embed=discord.Embed(title="__Élèves__", 
                	description=f"- `{prefix}help` : Permet de pouvoir voir la liste des commandes du robot.\n- `{prefix}code (code)` : Permet d'avoir accès au serveur avec un code donnée par le professeur.", 
                	color=0x00ff08
            		)
				pageprof = embed=discord.Embed(title="__Professeurs__", 
                	description=f"- `{prefix}open (classe)` : Permet d'ouvrir le salon vocal __Cours__ afin de pouvoir laisser l'accès aux élèves étant dans la classe spécifiée pour se connecter.\n- `{prefix}close (classe)` : Permet de fermer le salon vocal __Cours__ et ainsi faire exclure tout le monde étant connecté à ce salon + ferme l'accès aux élèves d'une classe spécifié pour se connecter dessus.\n- `{prefix}appel (classe)` : Permet de connaître le noms des élèves d'une classe étant connecté au salon vocal __Cours__ et également les élèves d'une classe n'étant pas connecté au salon.\n- `{prefix}code create (code) (Prénom) (classe)` : Permet de crée un code pour qu'un élève puisse accéder au serveur.\n- `{prefix}code list` : Permet d'afficher la liste des élèves avec leurs codes, leurs prénom et si le code a été utilisé.\n -`{prefix}code remove (code)` : Permet de supprimer un utilisateur spécifique.", 
                	color=0x00ff08
            		)
				pageinfo = embed=discord.Embed(title="__Informations__", 
                	description=f"**Ce robot a été crée par Diego (Jouca) et utilise le module Discord.py pour interagir avec Discord.**\n\n**Liste des classes du serveur :**\n{classeliste}", 
                	color=0x00ff08
            		)

				embed.set_author(name="NSI Bot", icon_url="https://banner2.cleanpng.com/20181128/cbr/kisspng-python-programming-basics-for-absolute-beginners-michigan-python-user-group-5-jul-2-18-5bfef921c53528.7857216715434365778078.jpg")
				embed.set_author(name="NSI Bot", icon_url="https://banner2.cleanpng.com/20181128/cbr/kisspng-python-programming-basics-for-absolute-beginners-michigan-python-user-group-5-jul-2-18-5bfef921c53528.7857216715434365778078.jpg")

				pages = [pagehome, pageeleve, pageprof, pageinfo]

				msg1 = await message.channel.send(embed=pagehome)

				await msg1.add_reaction('👨‍🎓')
				await msg1.add_reaction('👨‍🏫')
				await msg1.add_reaction('ℹ️')

				def check(reaction, user):
					return user == message.author

				i = 0
				reaction = None

				while True:
					if str(reaction) == '👨‍🎓':
						i = 1
						await msg1.edit(embed = pages[i])
					if str(reaction) == '👨‍🏫':
						i = 2
						await msg1.edit(embed = pages[i])
					if str(reaction) == 'ℹ️':
						i = 3
						await msg1.edit(embed = pages[i])

					if i > 0:
						i = -1
						await msg1.clear_reactions()
						await msg1.add_reaction('⬆️')

					if str(reaction) == '⬆️':
						i = 0
						await msg1.clear_reactions()
						await msg1.edit(embed = pages[i])
						await msg1.add_reaction('👨‍🎓')
						await msg1.add_reaction('👨‍🏫')
						await msg1.add_reaction('ℹ️')

					try:
						reaction, user = await client.wait_for('reaction_add', timeout = 10.0, check = check)
						await msg1.remove_reaction(reaction, user)
					except:
						break
				await msg1.clear_reactions()
				return

		if msg.startswith("open"):
			guild = message.guild
			if message.author.guild_permissions.administrator:
				try:
					classe = args[1].upper()
				except IndexError as error:
					embed400 = senderror("Aucune classe n'a été sélectionné.")
					msg2 = await message.channel.send(embed=embed400)
					time.sleep(3)
					await msg2.delete()
					return
				if classe not in classeliste:
					embed400 = senderror("Cette classe n'existe pas.")
					msg2 = await message.channel.send(embed=embed400)
					time.sleep(3)
					await msg2.delete()
					return

				channelperm = client.get_channel(int(nsi_channel))
				for k in roleclasseliste:
					for o in range(len(roleclasseliste)):
						if roleclasseliste[o][0] == classe:
							chatclasse = chatclasseliste[o][1]
							classerole = guild.get_role(roleclasseliste[o][1])
				await channelperm.set_permissions(classerole, connect=True,speak=True,stream=True,use_voice_activation=True)
				chatchannelperm = client.get_channel(int(chatclasse))
				await chatchannelperm.set_permissions(classerole, 
					send_messages=True,
					read_messages=True,
					attach_files=True,
					external_emojis=True,
					add_reactions=True
				)
				embed1 = sendsuccess(f"__**La salle de NSI est maintenant ouverte et accessible aux autres utilisateurs de la classe {classe}. Le chat est également accessible pour les élèves.**__")
				msg2 = await message.channel.send(embed=embed1)
				return
			embed400 = senderror("Vous n'avez pas accès à cette commande.")
			msg2 = await message.channel.send(embed=embed400)
			time.sleep(3)
			await msg2.delete()
			return

		if msg.startswith("close"):
			guild = message.guild
			if message.author.guild_permissions.administrator:
				try:
					classe = args[1].upper()
				except IndexError as error:
					embed400 = senderror("Aucune classe n'a été sélectionné.")
					msg2 = await message.channel.send(embed=embed400)
					time.sleep(3)
					await msg2.delete()
					return
				if classe not in classeliste:
					embed400 = senderror("Cette classe n'existe pas.")
					msg2 = await message.channel.send(embed=embed400)
					time.sleep(3)
					await msg2.delete()
					return
				
				channelperm = client.get_channel(int(nsi_channel))
				for k in roleclasseliste:
					for o in range(len(roleclasseliste)):
						if roleclasseliste[o][0] == classe:
							chatclasse = chatclasseliste[o][1]
							classerole = guild.get_role(roleclasseliste[o][1])
				await channelperm.set_permissions(classerole, connect=False,speak=False,stream=False,use_voice_activation=False)
				chatchannelperm = client.get_channel(int(chatclasse))
				await chatchannelperm.set_permissions(classerole, 
					send_messages=False,
					read_messages=False,
					attach_files=False,
					external_emojis=False,
					add_reactions=False
				)
				members = channelperm.members
				members_to_kick = []
				for x in members:
					members_to_kick.append(x)
					await x.move_to(None)
				embed1 = sendsuccess(f"__**La salle de NSI est maintenant fermé pour la classe {classe}. Tout les utilisateurs du salon vocal ont été déconnecté.**__")
				msg2 = await message.channel.send(embed=embed1)
				return
			embed400 = senderror("Vous n'avez pas accès à cette commande.")
			msg2 = await message.channel.send(embed=embed400)
			time.sleep(3)
			await msg2.delete()
			return

		if msg.startswith("code"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor()

				author = message.author
				guild = message.guild
				try:
					code = args[1]
				except IndexError as error:
					embed400 = senderror("Aucun code n'a été entré dans la commande ou le format du code est invalide.")
					msg2 = await message.channel.send(embed=embed400)
					time.sleep(3)
					await msg2.delete()
					return

				if code == "list":
					if message.author.guild_permissions.administrator:
						try:
							classe = args[2].upper()
						except IndexError as error:
							embed400 = senderror("Aucune classe n'a été sélectionné.")
							msg2 = await message.channel.send(embed=embed400)
							time.sleep(3)
							await msg2.delete()
							return
						if classe not in classeliste:
							embed400 = senderror("Cette classe n'existe pas.")
							msg2 = await message.channel.send(embed=embed400)
							time.sleep(3)
							await msg2.delete()
							return
						
						cursor.execute(f"SELECT code,prenom,checked FROM codes WHERE classe = '{classe}'")
						classes = cursor.fetchall()

						finalstr = ""
						for i in classes:
							if i[2] == 1:
								finalstr = finalstr+f"> - **{i[1]}**, Code : `{i[0]}`, Validation du code : **Oui**\n"
							else:
								finalstr = finalstr+f"> - **{i[1]}**, Code : `{i[0]}`, Validation du code : **Non**\n"
						if len(finalstr) == 0:
							finalstr = "Personne."
						
						embed1 = discord.Embed(title=f":scroll: Liste des élèves de la classe {classe}",description=finalstr,color=0x00ff00)
						msg = await message.channel.send(embed=embed1)
						return
					else:
						embed400 = senderror("Vous n'avez pas accès à cette commande.")
						msg2 = await message.channel.send(embed=embed400)
						time.sleep(3)
						await msg2.delete()
						return
				if code == "remove":
					if message.author.guild_permissions.administrator:
						try:
							code = int(args[2])
						except IndexError as error:
							embed400 = senderror("Aucun code n'a été sélectionné.")
							msg2 = await message.channel.send(embed=embed400)
							time.sleep(3)
							await msg2.delete()
							return

						cursor.execute(f"SELECT code FROM codes WHERE code = {code}")
						try:
							codetest = cursor.fetchone()[0]
						except:
							embed400 = senderror(f"Aucun utilisateur n'est assigné avec le code `{code}`.")
							msg2 = await message.channel.send(embed=embed400)
							time.sleep(3)
							await msg2.delete()
							return
						cursor.execute(f"SELECT prenom FROM codes WHERE code = {code}")
						prenom = cursor.fetchone()[0]

						cursor.execute(f"DELETE FROM codes WHERE code = {code}")
						conn.commit()

						embed1 = sendsuccess(f"L'utilisateur **{prenom}** contenant le code `{code}` a été supprimé.")
						msg2 = await message.channel.send(embed=embed1)

						channellog = client.get_channel(logs)
						embed123 = sendlog(f"Code `{code}` supprimé de l'utilisateur **{prenom}**.")
						msg2 = await channellog.send(embed=embed123)
						return
					else:
						embed400 = senderror("Vous n'avez pas accès à cette commande.")
						msg2 = await message.channel.send(embed=embed400)
						time.sleep(3)
						await msg2.delete()
						return
				if code == "create":
					if message.author.guild_permissions.administrator:
						try:
							code = int(args[2])
						except IndexError as error:
							embed400 = senderror("Aucun code n'a été sélectionné.")
							msg2 = await message.channel.send(embed=embed400)
							time.sleep(3)
							await msg2.delete()
							return
						
						try:
							prenom = args[3]
						except IndexError as error:
							embed400 = senderror("Aucun prénom n'a été assigné.")
							msg2 = await message.channel.send(embed=embed400)
							time.sleep(3)
							await msg2.delete()
							return

						try:
							classe = args[4].upper()
						except IndexError as error:
							embed400 = senderror("Aucune classe n'a été sélectionné.")
							msg2 = await message.channel.send(embed=embed400)
							time.sleep(3)
							await msg2.delete()
							return

						if classe not in classeliste:
							embed400 = senderror("Cette classe n'existe pas.")
							msg2 = await message.channel.send(embed=embed400)
							time.sleep(3)
							await msg2.delete()
							return

						cursor.execute(f"SELECT code FROM codes WHERE code = {code} AND checked = 0")
						try:
							testcode = cursor.fetchone()[0]
						except:
							testcode = None
						if testcode != code:
							sql = "INSERT INTO codes (code,prenom,checked,discordid,classe) VALUES (%s, %s, %s, %s, %s)"
							val = (code, prenom, 0, 0, classe)
							cursor.execute(sql, val)
							conn.commit()
							embed1 = sendsuccess(f"Le code `{code}` a été crée pour l'utilisateur **{prenom}** dans la classe **{classe}**.")
							msg2 = await message.channel.send(embed=embed1)
							channellog = client.get_channel(logs)
							embed123 = sendlog(f"Code `{code}` crée pour l'utilisateur **{prenom}** dans la classe **{classe}**.")
							msg2 = await channellog.send(embed=embed123)
							return
						else:
							embed400 = senderror("Ce code est actuellement en cours d'utilisation pour un autre utilisateur, veuillez utiliser un autre code.")
							msg2 = await message.channel.send(embed=embed400)
							time.sleep(3)
							await msg2.delete()
							return
					else:
						embed400 = senderror("Vous n'avez pas accès à cette commande.")
						msg2 = await message.channel.send(embed=embed400)
						time.sleep(3)
						await msg2.delete()
						return
				
				cursor.execute(f"SELECT code FROM codes WHERE discordid = {author.id}")
				try:
					alreadychecked = cursor.fetchone()[0]
				except:
					alreadychecked = None
				if alreadychecked is not None:
					embed400 = senderror("Vous vous êtes déjà enregistré avec un compte.")
					msg2 = await message.channel.send(embed=embed400)
					time.sleep(3)
					await msg2.delete()
					return
				
				code = int(code)
				cursor.execute(f"SELECT code FROM codes WHERE code = {code} AND checked = 0")
				try:
					testcode = cursor.fetchone()[0]
				except:
					testcode = None
				if testcode == code:
					channellog = client.get_channel(logs)
					cursor.execute(f"SELECT prenom FROM codes WHERE code = {code} AND checked = 0")
					prenom = cursor.fetchone()[0]
					cursor.execute(f"UPDATE codes SET discordid = {author.id} WHERE code = {code} AND checked = 0")
					conn.commit()
					rolestudent = guild.get_role(student_role)
					await author.add_roles(rolestudent)

					cursor.execute(f"SELECT classe FROM codes WHERE code = {code} AND checked = 0")
					classe = cursor.fetchone()[0]
					for k in roleclasseliste:
						for o in range(len(roleclasseliste)):
							if roleclasseliste[o][0] == classe:
								if roleclasseliste[o][0] == "S11SNT" or roleclasseliste[o][0] == "S11MATHS":
									classerole = guild.get_role(roleclasseliste[0][1])
									await author.add_roles(classerole)
									classerole = guild.get_role(roleclasseliste[1][1])
									await author.add_roles(classerole)
									done=True
									break
								elif roleclasseliste[o][0] != "S11SNT" or roleclasseliste[o][0] != "S11MATHS":
									classerole = guild.get_role(roleclasseliste[o][1])
									print(classerole)
									await author.add_roles(classerole)
						try:
							if done:
								break
						except:
							pass


					await author.edit(nick=prenom)

					embed123 = sendlog(f"**{prenom}** a rejoint le serveur.")
					msg2 = await channellog.send(embed=embed123)
					cursor.execute(f"UPDATE codes SET checked = 1 WHERE code = {code} AND checked = 0")
					conn.commit()
					return
				else:
					embed400 = senderror("Code invalide.")
					msg2 = await message.channel.send(embed=embed400)
					time.sleep(3)
					await msg2.delete()
					return

		if msg.startswith("appel"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor(buffered=True)
				guild = message.guild
				if message.author.guild_permissions.administrator:
					try:
						classe = args[1].upper()
					except IndexError as error:
						embed400 = senderror("Aucune classe n'a été sélectionné.")
						msg2 = await message.channel.send(embed=embed400)
						time.sleep(3)
						await msg2.delete()
						return
					if classe not in classeliste:
						embed400 = senderror("Cette classe n'existe pas.")
						msg2 = await message.channel.send(embed=embed400)
						time.sleep(3)
						await msg2.delete()
						return

					channelperm = client.get_channel(int(nsi_channel))
					rolestudent = guild.get_role(student_role)
					for k in roleclasseliste:
						for o in range(len(roleclasseliste)):
							if roleclasseliste[o][0] == classe:
								classerole = guild.get_role(roleclasseliste[o][1])

					members = channelperm.members
					connected_members = []
					offline_members = []
					prenoms_connected = []
					prenoms_offline = []
					for x in members:
						connected_members.append(x)

					for i in message.guild.members:
						if rolestudent in i.roles:
							if classerole in i.roles:
								if i not in connected_members:
									offline_members.append(i.id)

					for l in connected_members:
						cursor.execute(f"SELECT prenom FROM codes WHERE discordid = %s AND classe = %s AND checked = 1 LIMIT 1", (l.id, classe))
						try:
							prenomtempo = cursor.fetchone()[0]
							prenoms_connected.append(prenomtempo)
						except:
							pass

					for l in offline_members:
						cursor.execute(f"SELECT prenom FROM codes WHERE discordid = %s AND classe = %s AND checked = 1 LIMIT 1", (l, classe))
						try:
							prenomtempo = cursor.fetchone()[0]
							prenoms_offline.append(prenomtempo)
						except:
							pass
					
					prenoms_connected_final,prenoms_offline_final = prenoms_connected,prenoms_offline

					if len(prenoms_connected) == 0:
						prenoms_connected_final = "Aucun ¯\_(ツ)_/¯"

					if len(prenoms_offline) == 0:
						prenoms_offline_final = "Aucun ¯\_(ツ)_/¯"

					embed1 = discord.Embed(title="", color=0x00ff00)
					embed1.add_field(name=f'Appel terminé :white_check_mark:', value=f"**:speaker: Élèves connectés au salon vocal :**\n`{prenoms_connected_final}`\n\n**:mute: Élèves hors-lignes au salon vocal :**\n`{prenoms_offline_final}`")
					textfinal1 = ""
					textfinal2 = ""
					for m in prenoms_connected:
						textfinal1 = textfinal1+"- "+m+"\n"
					if len(prenoms_connected) == 0:
						textfinal1 = "Aucun ¯\_(ツ)_/¯"
					for m in prenoms_offline:
						textfinal2 = textfinal2+"- "+m+"\n"
					if len(prenoms_offline) == 0:
						textfinal1 = "Aucun ¯\_(ツ)_/¯"
					text_file = open("appel.txt", "w+")
					text_file.write(f"Personnes connectés :\n\n{textfinal1}\n\nPersonnes hors-lignes :\n\n{textfinal2}")
					text_file.close()
					msg = await message.channel.send(embed=embed1)
					today = datetime.date.today()
					datefinal = today.strftime("%d-%m-%Y")
					with open("appel.txt", "rb") as file:
						msg = await message.channel.send(file=discord.File(file, f"appel-{classe}-{datefinal}.txt"))
					if os.path.exists("appel.txt"):
						os.remove("appel.txt")
					return
				else:
					embed400 = senderror("Vous n'avez pas accès à cette commande.")
					msg2 = await message.channel.send(embed=embed400)
					time.sleep(3)
					await msg2.delete()
					return

		if msg.startswith("eval"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor()
				
				args = [x for ar in args for x in ar.split('\n')]

				embed3 = discord.Embed(title="Loading...", color=0xffce08)
				embed3.add_field(name='Loading... Please wait a little moment', value="\u200b")
				loading	= await message.channel.send(embed=embed3)
				server = message.guild.name
				var = message.guild.id
				author = message.author.id
				channel = message.channel.id

				query = " ".join(msg.split(" ")[1:])
				if author != jouca:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name='Error.', value="You are not Jouca.")
					await message.channel.send(embed=embed)
					await loading.delete()
					return

				if len(query) == 0:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name='Error.', value="You need to input a query.")
					await message.channel.send(embed=embed)
					await loading.delete()
					return

				try:
					cursor.execute(query)
				except MC.Error as error:
					embed = discord.Embed(title="Error.", color=0xff0000)
					embed.add_field(name='Input :inbox_tray:', value=f"```{query}```")
					embed.add_field(name='Output :outbox_tray:', value=error, inline=False)
					await loading.delete()
					await message.channel.send(embed=embed)
					return
				commitlist = ["INSERT","UPDATE","DELETE"]
				embed = discord.Embed(title='Success!', color=0x00ff00)
				embed.add_field(name='Input :inbox_tray:', value=f"```{query}```")
				if query.split(" ")[0] in commitlist:
					conn.commit()
					embed.add_field(name='Output :outbox_tray:', value="OK!", inline=False)
					await loading.delete()
					await message.channel.send(embed=embed)
					return
				else:
					result = cursor.fetchall()
					embed.add_field(name='Output :outbox_tray:', value=f"```{result}```", inline=False)
					await loading.delete()
					await message.channel.send(embed=embed)
					return

		if msg.startswith("exec"):
			try:
				conn = MC.connect(host = dbhost, database = dbdatabase, user = dbuser, password = dbpassword)
				cursor = conn.cursor()
			except MC.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is not right with your username or your password")
					return
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
					return
				else:
					print(err)
					return
			else:
				conn.cursor()
				args = [x for ar in args for x in ar.split('\n')]

				embed3 = discord.Embed(title="Loading...", color=0xffce08)
				embed3.add_field(name='Loading... Please wait a little moment', value="\u200b")
				loading	= await message.channel.send(embed=embed3)
				server = message.guild.name
				var = message.guild.id
				author = message.author.id
				channel = message.channel.id
				query = " ".join(msg.split(" ")[1:])
				if author != jouca: #553971625679126549
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name='Error. <:error:472907618386575370>', value="You are not Jouca.")
					await message.channel.send(embed=embed)
					await loading.delete()
					return
				if len(query) == 0:
					embed = discord.Embed(title="", color=0xff0000)
					embed.add_field(name='Error. <:error:472907618386575370>', value="You need to input code.")
					await message.channel.send(embed=embed)
					await loading.delete()
					return
				try:
					embed = discord.Embed(title='Success! <:success:472908961176092702>', color=0x00ff00)
					embed.add_field(name='Input :inbox_tray:', value=f"```{query}```")
					env = {
						"message": message,
						"cursor": cursor,
						"conn": conn
					}
					res = exec(query, env);
					embed.add_field(name='Output :outbox_tray:', value=f"```{res}```", inline=False)
					await loading.delete()
					await message.channel.send(embed=embed)
				except Exception as error:
					embed = discord.Embed(title="Error. <:error:472907618386575370>", color=0xff0000)
					embed.add_field(name='Input :inbox_tray:', value=f"```{query}```")
					embed.add_field(name='Output :outbox_tray:', value=error, inline=False)
					await loading.delete()
					await message.channel.send(embed=embed)
					return
				return
			return;

	except Exception as error:
		args2 = prefix,' '.join(args)
		msg404 = traceback.format_exc()
		channel2 = client.get_channel(int(818903417622757436))
		embed = discord.Embed(title="", color=0xff0000)
		embed.add_field(name='Une erreur est survenue. <:error:472907618386575370>', value=f"Input :```{args2}```Output :```{msg404}```\n**L'équipe d'assistance du robot a été informé.**")
		embed.set_footer(text=f"{message.guild.name} --- {message.author}")
		embed2 = discord.Embed(title="", color=0xff0000)
		embed2.add_field(name='Une erreur est survenue. <:error:472907618386575370>', value=f'Input :```{args2}```Output :```{msg404}```')
		embed2.set_footer(text=f"{message.guild.name} --- {message.author}")
		await message.channel.send(embed=embed)
		await channel2.send(f"<@{jouca}>",embed=embed2)
		return

@client.event
async def on_member_join(member):
	channelwelcome = client.get_channel(819965636851531816)
	embed200 = discord.Embed(title="", color=0x0000ff)
	embed200.add_field(name=f'Annonce', value=f"__**Bienvenue {member.name} sur le serveur Discord consacré à la spécialité NSI !**__\n\nAfin de pouvoir avoir les permissions d'accéder au serveur, veuillez entrer le code que vous avez reçu via la boite de messagerie de l'ENT avec la commande :\n\n`nsi!code (le code juste ici)`")
	msg = await channelwelcome.send(embed=embed200)
	

@client.event
async def on_ready():
	print('Connecté avec :')
	print(client.user.name)
	print(client.user.id)
	print('------')
	datetime_object = datetime.datetime.now()

client.run(TOKEN)