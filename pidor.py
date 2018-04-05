import telebot

#from telebot import apihelper

import config

import mysql.connector

import datetime

import time

import random

import re

#help(apihelper)
#telebot.apihelper.proxy = {'http':'n.ivanovskiy:345ERT6y@10.5.0.9:3128'}

#s = requests.session()
#s.proxies = {"http":"n.ivanovskiy:345ERT6y@10.5.0.9:3128"}
#r = s.get("http://www.google.com")
#print(r.text)

#Proxy = {'host':"10.5.0.9","port":"3128","username":"n.ivanovskiy","password"}
bot = telebot.TeleBot(config.token)

idutvibori = []

@bot.message_handler(commands=['alkopidor'])
def repeat_all_messages(message: object): 
	global idutvibori
	if config.chats_id.count(message.chat.id) == 0:
		#print(message.chat)
		if idutvibori.count(message.chat.id) > 0:
			bot.send_message(message.chat.id, "збс")
			idutvibori.pop(idutvibori.index(message.chat.id))
		elif idutvibori.count(message.chat.id) == 0:
			bot.send_message(message.chat.id, "ахтыж блять")
			idutvibori.append(message.chat.id)
		time.sleep(1)
		bot.send_message(message.chat.id, "Ок. ты пидор @" + message.from_user.username)
		#idutvibori = 0
		return None
	if idutvibori.count(message.chat.id) > 0:
		bot.send_message(message.chat.id, "Ну ты и пидор @"+message.from_user.username+" идут выборы, не лезь.", None, message.message_id)
		return None
	cnx = mysql.connector.connect(user='root', password='auban', host='127.0.0.1', database='pidor')
	cursor = cnx.cursor(buffered=True)
	cursor1 = cnx.cursor(buffered=True)
	query = "select pday.member, mbr.username from pidor_of_day as pday inner join members as mbr on pday.member=mbr.id " \
			"and pday.day=%s and pday.chat_id=%s"
	sedni = datetime.date.today()
	#print(sedni)
	cursor.execute(query,(sedni.strftime('%Y-%m-%d %H:%M:%S'),str(message.chat.id)))
	if cursor.rowcount == 0:
		idutvibori.append(message.chat.id)
		bot.send_message(message.chat.id, 'Итак уважаемые пидоры, ща будут выборы')
		NewMonth = False
		if datetime.date.today().strftime("%d") == '01':
			NewMonth = True
		time.sleep(1)
		if NewMonth:
			bot.send_message(message.chat.id, 'Статистика за месяц!')
		else:
			bot.send_message(message.chat.id, 'Немного предвыборной статистики за вчера')
		time.sleep(1)
		
		vchera = sedni - datetime.timedelta(days=1)
		query = ("select mbr.username, v2.mb, v1.m_count, v1. m_type from (Select Max(grupen_msg.c_msg) as m_count, grupen_msg.msg_t as m_type "
		"from (SELECT t1.member_id as mb, count(t1.message_id) as c_msg, t1.message_type as msg_t FROM pidor.messages t1 "
		"where t1.chat_id = %s and t1.message_datetime >= %s "
		"group by t1.member_id, t1.message_type) as grupen_msg "
		"group by grupen_msg.msg_t) v1 "
		"join (SELECT t1.member_id as mb, count(t1.message_id) as c_msg, t1.message_type as msg_t FROM pidor.messages t1 "
		"where t1.chat_id = %s and t1.message_datetime >= %s "
		"group by t1.member_id, t1.message_type) v2 "
		"on v1.m_type = v2.msg_t and v1.m_count = v2.c_msg "
		"join (select id, username from members) mbr "
		"on v2.mb = mbr.id")
		if NewMonth:
			origin_date = sedni
			day = origin_date.day
			month = origin_date.month
			year = origin_date.year
			if origin_date.month == 1:
				delta = datetime.date(year - 1, 12, day)
			else:
				delta = datetime.date(year, month - 1, day)
			cursor.execute(query,(str(message.chat.id),delta.strftime('%Y-%m-%d %H:%M:%S'),str(message.chat.id),delta.strftime('%Y-%m-%d %H:%M:%S')))
		else:
			cursor.execute(query,(str(message.chat.id),vchera.strftime('%Y-%m-%d %H:%M:%S'),str(message.chat.id),vchera.strftime('%Y-%m-%d %H:%M:%S')))
		for (user_name, user_id, msg_count, msg_type) in cursor:
			if msg_type == "text":
				bot.send_message(message.chat.id, 'Самый быстрый палец и самый занятой работник - @'+user_name + ' набрал ' + str(msg_count) + ' сообщений')
			if msg_type == "location":
				bot.send_message(message.chat.id, 'Сусанин, епта, - @'+user_name + ' кинул ' + str(msg_count) + ' location')
			if msg_type == "audio":
				bot.send_message(message.chat.id, 'Аудиофил с большими ушами - @'+user_name + ' заставил слушать ' + str(msg_count) + ' audio')
			if msg_type == "document":
				bot.send_message(message.chat.id, 'Алярм, Сноуден в чате - @'+user_name + ' cлил ' + str(msg_count) + ' document')
			if msg_type == "sticker":
				bot.send_message(message.chat.id, 'Стикеролюб - @'+user_name + ' c ' + str(msg_count) + ' sticker')
			if msg_type == "video":
				bot.send_message(message.chat.id, 'Вуаерист - @'+user_name + ' c ' + str(msg_count) + ' video')
			if msg_type == "voice":
				bot.send_message(message.chat.id, 'Голосящий кивин - @'+user_name + ' напиздел ' + str(msg_count) + ' voice')
			if msg_type == "photo":
				bot.send_message(message.chat.id, 'Надеюсь эксгибиционистка - @'+user_name + ' выложила ' + str(msg_count) + ' photo своих сск')
			time.sleep(1)
			
		
		bot.send_message(message.chat.id, 'Выбираем 10 кандидатов в пидоры')
		
		query = ("SELECT distinct mbr.id, mbr.username FROM pidor.messages as msg "
				 "inner join pidor.members as mbr"
				 " on msg.member_id = mbr.id "
				 "where msg.chat_id = %s and msg.message_datetime > %s and mbr.username is not null "
				 "order by rand() limit 10")
			#"SELECT id, username FROM members where chat_id="+str(message.chat.id)+" order by rand() limit 1"
		cursor.execute(query,(str(message.chat.id),vchera.strftime('%Y-%m-%d %H:%M:%S')))
		i = 1
		for (user_id, user_name) in cursor:
			time.sleep(1)
			bot.send_message(message.chat.id, 'Кандидат № '+str(i)+ ' @'+user_name)
			i+=1
			query = "insert into vibori (user_id, username, tur, date,chat_id) values (%s,%s,%s,%s,%s)"
			data_q = (user_id,user_name, 1, sedni.strftime('%Y-%m-%d %H:%M:%S'),str(message.chat.id))
			cursor1.execute(query,data_q)
			cnx.commit()

		bot.send_message(message.chat.id, 'Аплодисменты счастливчикам')
		time.sleep(1)
		bot.send_message(message.chat.id, 'Начинаем второй тур. Выбираем троих счастливчиков')
		query = ("SELECT distinct user_id, username FROM pidor.vibori "
					"where chat_id = %s and tur = 1 and date >= %s"
					"order by rand() limit 3")
			# "SELECT id, username FROM members where chat_id="+str(message.chat.id)+" order by rand() limit 1"
		cursor.execute(query, (str(message.chat.id), sedni.strftime('%Y-%m-%d %H:%M:%S')))
		i = 1
		for (user_id, user_name) in cursor:
			time.sleep(1)
			bot.send_message(message.chat.id, 'Финалист № ' + str(i) + ' @' + user_name)
			query = "insert into vibori (user_id, username, tur, date,chat_id) values (%s,%s,%s,%s,%s)"
			data_q = (user_id, user_name, 2, sedni.strftime('%Y-%m-%d %H:%M:%S'), str(message.chat.id))
			cursor1.execute(query, data_q)
			cnx.commit()
			i=i+1
		time.sleep(1)
		bot.send_message(message.chat.id, 'Определились финалисты')
		time.sleep(2)
		bot.send_message(message.chat.id, 'Барабанная дробь')
		#time.sleep(2)
		bot.send_message(message.chat.id, 'Кто же алкопидор? 10 секунд на ваши ставки')
		#time.sleep(10)
		query = ("SELECT distinct user_id, username FROM pidor.vibori "
					"where chat_id = %s and tur = 2 and date >= %s"
					"order by rand() limit 1")
			# "SELECT id, username FROM members where chat_id="+str(message.chat.id)+" order by rand() limit 1"
		cursor.execute(query, (str(message.chat.id), sedni.strftime('%Y-%m-%d %H:%M:%S')))
		for (user_id, user_name) in cursor:
			query = "insert into pidor_of_day (day,member,chat_id) values (%s,%s,%s)"
			data_q = (sedni.strftime('%Y-%m-%d %H:%M:%S'),user_id,str(message.chat.id))
			cursor.execute(query,data_q)
			cnx.commit()
			t1 = '∟( ͠° ͜ʖ ͠°)ง/☆'
			t2 = '╰( ͡° ͜ʖ ͡°)つ──☆*:►'
			msg = bot.send_message(message.chat.id, t2)
			
			while i <= 11:
				bot.edit_message_text(t1, msg.chat.id, msg.message_id)
				time.sleep(1)
				bot.edit_message_text(t2, msg.chat.id, msg.message_id)
				i += 1
			
			bot.edit_message_text(t1, msg.chat.id, msg.message_id)
			bot.edit_message_text('.\n\n?╰( ͡° ͜ʖ ͡°)つ──☆*:► ты пидор @' + user_name, msg.chat.id, msg.message_id)
			idutvibori.pop(idutvibori.index(message.chat.id))
			bot.send_message(message.chat.id, '.\n\n?╰( ͡° ͜ʖ ͡°)つ──☆*:► ты пидор @' + user_name)
			# time.sleep(1)
			# bot.send_message(message.chat.id, 'Хотя... хуй с ним с барабаном. будут у нас выборы в 3 этапа')
			# bot.send_message(message.chat.id, 'Этап первый. выбираем 10 кандидатов в пидоры')
			#
			# msg = bot.send_message(message.chat.id, '.')
			# s = ''
			# while i <= 5:
			#	 bot.edit_message_text(s + '|', msg.chat.id, msg.message_id)
			#	 bot.edit_message_text(s + '/', msg.chat.id, msg.message_id)
			#	 bot.edit_message_text(s + '-', msg.chat.id, msg.message_id)
			#	 bot.edit_message_text(s + '\\', msg.chat.id, msg.message_id)
			#	 #s = s + '|'
			#	 i += 1
			# bot.edit_message_text('|', msg.chat.id, msg.message_id)
			# s = '.\n.???\n( ????)????*?\n?. ? ...??+.\n???...°?+ *??)\n..........· ??.·*??) ?.·*?)\n..........(?.·? (?.·''* ? ВЖУХ ?'
			# bot.send_message(message.chat.id, s)
			# bot.send_message(message.chat.id, '.\n\n?( ?° ?? ?° )?──?*:?? ты пидор @'+user_name)
			# message_text = 'Асалама алейкум.'
			# bot.send_message(message.chat.id, message_text, message.message_id)
			# time.sleep(2)
			# message_text = "Захады дарагой вибирай поп любой"
			# bot.send_message(message.chat.id, message_text)
			# time.sleep(3)
			# message_text = "Поп сладкий как пэрсык, упругий как баран"
			#
			# bot.send_message(message.chat.id, message_text)
			# # time.sleep(5)
			# # message_text = "Хочу обратить внимание всех. Я встречался со многими пидорами, которые погибли, с людьми и демонстрантами, которые погибли, и все задают вопрос:"
			# # bot.send_message(message.chat.id, message_text)
			# time.sleep(3)
			# message_text = "Вибор сделан "
			# bot.send_message(message.chat.id, message_text)
			# time.sleep(3)
			# message_text = "Лючший поп у @" + user_name
			# bot.send_message(message.chat.id, message_text)
			# time.sleep(2)
			#message_text = "Пидоры идут! Пидоры идут!" \
			#			   "\n@{} пьяного несут.".format(user_name)
			#bot.send_message(message.chat.id, message_text)
			# time.sleep(1)
			# message_text = "Вобщем гордись и наслаждайся @"+user_name+" пидор"
			# bot.send_message(message.chat.id, message_text)
			# time.sleep(1)
			# message_text = "Всем он знаком, кто угостит хуйком?"
			# bot.send_message(message.chat.id, message_text)
			# time.sleep(300)
			# message_text = "Чо пидор @"+user_name+" трави анекдот"#"Ахаха. ты пидор @"+user_name+" . Все слышали?  @"+user_name+" то пидор оказывается."
			# bot.send_message(message.chat.id, message_text)
			#time.sleep(3)

			#query = 'update members set username=%s where id=$s'
			print(user_name)
			idutvibori = []
			#data_user = (message.from_user.username, message.from_user.id)
			#cursor.execute(query, data_user)
			#cnx.commit()
	else:
		for (member,user_name) in cursor:
			message_text = "А Алкопидор дня сегодня "+user_name+"\nсодомировать тебя кочергой, длинной и короткой\n\nА книга теперь пьет, топает и ...\nНу вы понели"
			bot.send_message(message.chat.id, message_text)

	#print(message.chat.id)
	#message_text = 'Бхх, я научился читать все ваши сообщения. Скоро научусь отправлять куда следует и вам пизда.'
	#bot.send_message(message.chat.id,  message_text, message.message_id)

@bot.message_handler(commands=['knigapedeg'])
def knigapedeg(message: object):
	if message.chat.id == config.chat_id:
		if message.from_user.id == 424429201:
			bot.send_message(message.chat.id, "nero иди нахуй. ©Rarebook ", None, message.message_id)
			return None
		rnd = random.randrange(1,10,1)
		if rnd <= 3:
			bot.send_message(message.chat.id, "@Rarebook тебя кличут")
		else:
			bot.send_message(message.chat.id, "Сам ты педег, какбы отвечает книга", None, message.message_id)
	else:
		try:
			print(message.chat)
		except:
			print("смайлы в названии чата")
		try:
			print(message.text)
		except:
			print("смайлы боя")

@bot.message_handler(commands=['start'])
def startue(message: object):
	bot.send_message(message.chat.id, "Хуярт, спецом для одного чата сделано")
	print(message.chat)
	print(message.from_user)

@bot.message_handler(commands=['help'])
def helpue(message: object):
	if message.chat.id == config.chat_id:
		bot.send_message(message.chat.id, "Хэлп", None, message.message_id)
		#time.sleep(1)
		bot.send_message(message.chat.id, "Ай нид сом бади", None, message.message_id)
		bot.send_message(message.chat.id, "Хэлп", None, message.message_id)
		#time.sleep(1)
		bot.send_message(message.chat.id, "Нот джаст эни бадиии", None, message.message_id)
		bot.send_message(message.chat.id, "Хэлп", None, message.message_id)
		bot.send_message(message.chat.id, "Ю ноу ай нид сомуон", None, message.message_id)
		bot.send_message(message.chat.id, "Хээээлп", None, message.message_id)
	else:
		bot.send_message(message.chat.id, "Хуелп, спецом для одного чата сделано")
		try:
			print(message.chat)
		except:
			print("смайлы в названии чата")
		try:
			print(message.text)
		except:
			print("смайлы боя")
		
@bot.message_handler(commands=['do_it_vjuh'])
def doit(message: object):
	print(message.chat)
	t1 = '∟( ͠° ͜ʖ ͠°)ง/☆'
	t2 = '╰( ͡° ͜ʖ ͡°)つ──☆*:►'
	msg = bot.send_message(message.chat.id, t2)
	i=0
	while i <= 11:
		bot.edit_message_text(t1, msg.chat.id, msg.message_id)
		time.sleep(1)
		bot.edit_message_text(t2, msg.chat.id, msg.message_id)
		time.sleep(1)
		i += 1
	
	bot.edit_message_text(t1, msg.chat.id, msg.message_id)
	bot.edit_message_text('?( ?° ?? ?° )?──?*:?? на те вжух @' + message.from_user.username, msg.chat.id, msg.message_id)
	
@bot.message_handler(commands=['fuck_you'])
def fuck(message: object):
	if message.reply_to_message != None:
		print(message.chat)
		t1 = '╭п╮(︶︿︶)╭∩╮'
		t2 = '╭∩╮(︶︿︶)╭п╮'
		t3 = '╭∩╮(︶︿︶)╭∩╮'
		msg = bot.send_message(message.chat.id, t2, None, message.reply_to_message.message_id)
		i=0
		while i <= 11:
			bot.edit_message_text(t1, msg.chat.id, msg.message_id)
			time.sleep(1)
			bot.edit_message_text(t2, msg.chat.id, msg.message_id)
			time.sleep(1)
			i += 1
	
		bot.edit_message_text(t3, msg.chat.id, msg.message_id)
		#bot.edit_message_text('?( ?° ?? ?° )?──?*:?? на те вжух @' + message.from_user.username, msg.chat.id, msg.message_id)
	

@bot.message_handler(commands=['go_v_sche'])
def gogogo(message: object):
	if message.chat.id == config.chat_id:
		s = message.text
		s = s.replace('/go_v_sche@alkopidor_bot','')
		s = s.replace('/go_v_sche ','')
		s = s.replace('/go_v_sche','')
		if s == '':
			bot.send_message(message.chat.id, "@Albertusss555 го в щ")
		else:
			s = s.replace('@', '')
			bot.send_message(message.chat.id, "@"+s+" го в щ")
	else:
		try:
			print(message.chat)
		except:
			print("смайлы в названии чата")
		try:
			print(message.text)
		except:
			print("смайлы боя")

@bot.message_handler(commands=['nahuy_sche'])
def gogogo(message: object):
	if message.chat.id == config.chat_id:
		s = message.text
		s = s.replace('/nahuy_sche@alkopidor_bot','')
		s = s.replace('/nahuy_sche ','')
		s = s.replace('/nahuy_sche','')
		if s == '':
			bot.send_message(message.chat.id, "@Albertusss555 нахуй щ. го в кран.")
		else:
			s = s.replace('@', '')
			bot.send_message(message.chat.id, "@"+s+" нахуй щ. го в кран.")
	else:
		try:
			print(message.chat)
		except:
			print("смайлы в названии чата")
		try:
			print(message.text)
		except:
			print("смайлы боя")

@bot.message_handler(commands=['obyava'])
def obyava(message: object):
	s = config.obyava
	if s != '':
		bot.send_message(message.chat.id, config.obyava)


@bot.message_handler(commands=['kto_v_sche'])
def ktovsche(message: object):
	# if message.chat.id == config.chat_id:
	cnx = mysql.connector.connect(user='root', password='auban', host='127.0.0.1', database='pidor')
	cursor = cnx.cursor(buffered=True)
	sedni = datetime.date.today()
	# print(sedni)
	query = "select username, voskok from ktovsche where voskok>='"+sedni.strftime('%Y-%m-%d %H:%M:%S')+"' order by voskok"
	cursor.execute(query)
	if cursor.rowcount > 0:
		s=''
		for (username,voskok) in cursor:
			s=s+""+username+" будет в "+voskok.strftime('%H:%M:%S')+'\n'
		bot.send_message(message.chat.id, s)
	else:
		bot.send_message(message.chat.id, "Никого")
	# else:
		# try:
			# print(message.chat)
		# except:
			# print("смайлы в названии чата")
		# try:
			# print(message.text)
		# except:
			# print("смайлы боя")

@bot.message_handler(commands=['pedik'])
def pedik(message: object):
	if message.chat.id == config.chat_id:
		sedni = datetime.date.today()
		cnx = mysql.connector.connect(user='root', password='auban', host='127.0.0.1', database='pidor')
		cursor = cnx.cursor(buffered=True)
		query = "delete from ktovsche where username = '" + message.from_user.username + "' and voskok>='" + sedni.strftime(
			'%Y-%m-%d %H:%M:%S') + "'"
		cursor.execute(query)
		cnx.commit()
		bot.send_message(message.chat.id, "@" + message.from_user.username + " - педик. в Щ не придет")
	else:
		try:
			print(message.chat)
		except:
			print("смайлы в названии чата")
		try:
			print(message.text)
		except:
			print("смайлы боя")

@bot.message_handler(commands=['anon'])
def anon(message: object):
	if isinstance(message.text,str) == True and config.admins.count(message.chat.id) > 0:
		s = message.text
		s = s.replace('/anon@alkopidor_bot','')
		s = s.replace('/anon ','')
		s = s.replace('/anon','')
		print(message.chat)
		print(message.text)
		bot.send_message(config.chat_id, 'Нам анонимно сообщают:\n'+s)
			
@bot.message_handler(commands=['safe'])
def safe(message: object):
	if isinstance(message.text,str) == True and config.admins.count(message.chat.id) > 0:
		s = message.text
		s = s.replace('/safe@alkopidor_bot','')
		s = s.replace('/safe ','')
		s = s.replace('/safe','')
		print(message.chat)
		print(message.text)
		bot.send_message(config.chat_id, 'Из надежных источников стало известно:\n'+s)
			
@bot.message_handler(commands=['budu'])
def ktovsche(message: object):
	#if message.chat.id == config.chat_id:

	sedni = datetime.date.today()
	chas = message.text.replace("@alkopidor_bot","")
	chas = chas.replace("/budu ", "")
	chas = chas.replace("/budu", "")
	if chas.lower() == "через 2 дня":
		bot.send_message(message.chat.id, "ой, та не пизди", None, message.message_id)
		return None
	chas = chas.replace(" ", ":")
	chas = chas.replace(".", ":")
	chas = chas.replace(",", ":")
	#print(chas)
	if len(chas) == 0:
		chas = chas+"00:00:00"
	if len(chas) == 2:
		chas = chas+":00:00"
	if len(chas) == 5:
		chas = chas+":00"
	# print(chas)
	try:
		voskok = datetime.datetime.strptime(sedni.strftime('%Y-%m-%d')+' '+chas[0:8],'%Y-%m-%d %H:%M:%S')
	except:
		bot.send_message(message.chat.id, "нхнп во скок", None, message.message_id)
		return None
	# print(sedni)
	cnx = mysql.connector.connect(user='root', password='auban', host='127.0.0.1', database='pidor')
	cursor = cnx.cursor(buffered=True)
	query = "delete from ktovsche where username = '"+message.from_user.username+"' and voskok>='"+sedni.strftime('%Y-%m-%d %H:%M:%S')+"'"
	cursor.execute(query)
	cnx.commit()
	# cursor.close()
	# cnx.close()
	# cnx = mysql.connector.connect(user='root', password='auban', host='127.0.0.1', database='pidor')
	# cursor = cnx.cursor()
	query = "insert into ktovsche (username, voskok) values('"+message.from_user.username+"','"+voskok.strftime('%Y-%m-%d %H:%M:%S')+"')"
	cursor.execute(query)
	cnx.commit()
	cursor.close()
	cnx.close()
	bot.send_message(message.chat.id, "@"+message.from_user.username+" будет в "+voskok.strftime('%H:%M:%S'))
		# if cursor.rowcount > 0:
		#	 for (username,voskok) in cursor:
		#		 bot.send_message(message.chat.id, "@"+username+" будет в "+voskok.strftime('%H:%M:%S'))
		# else:
		#	 bot.send_message(message.chat.id, "Никого")
	# else:
		# try:
			# print(message.chat)
		# except:
			# print("смайлы в названии чата")
		# try:
			# print(message.text)
		# except:
			# print("смайлы боя")

@bot.message_handler(func=lambda message: True, content_types=['text', 'audio', 'document', 'photo', 'sticker','video', 'voice', 'location', 'contact', 'new\_chat\_participant','left\_chat\_participant', 'new\_chat\_title', 'new\_chat\_photo','delete\_chat\_photo', 'group\_chat\_created'])
def read_all_message(message:object):
	if config.chats_id.count(message.chat.id) > 0:
		if isinstance(message.text,str) == True and message.text.find('го') != -1 and (message.text.lower().find('пиго') != -1 or message.text.lower().find('пиво') != -1 or message.text.lower().find('пв ') != -1) and message.text.find('в щ') != -1:
			bot.send_message(message.chat.id, "боя боч", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "нет":
			bot.send_message(message.chat.id, "пидора ответ", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "нeт":
			bot.send_message(message.chat.id, "пидора otvet", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "heт":
			bot.send_message(message.chat.id, "pidora otvet", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "неть":
			bot.send_message(message.chat.id, "пiдоров геть", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "нетъ":
			bot.send_message(message.chat.id, "пидора ответъ", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "не":
			bot.send_message(message.chat.id, "пидора отве", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "нит":
			bot.send_message(message.chat.id, "пидора ретвит", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "ни":
			bot.send_message(message.chat.id, "пидора ретви", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "ниет":
			bot.send_message(message.chat.id, "Пидору миниет ©Лллома", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "нихт":
			bot.send_message(message.chat.id, "пидор пидорихт", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "найн":
			bot.send_message(message.chat.id, "ну, девять. и чо?", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "нэт":
			bot.send_message(message.chat.id, "Эээ, захады, дарагой", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "ноу":
			bot.send_message(message.chat.id, "пидора о-оу", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "н":
			bot.send_message(message.chat.id, "пдр отв", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "да нет":
			bot.send_message(message.chat.id, "двух пидоров ответ", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "нетушки":
			bot.send_message(message.chat.id, "Хуетушки. Ну чо @Rarebook довольна?", None, message.message_id)
		if isinstance(message.text,str) == True and message.text.lower() == "h":
			bot.send_message(message.chat.id, "Лови пятюню, хитрожоп. H - Хэ в английской расскладке ввел. Усех ноебал", None, message.message_id)
		if isinstance(message.text,str) == True and (re.match('[0-9\+\-\*\/\(\)\.\,\^%]+$',message.text) is not None and re.match('[0-9]+$',message.text) is None) and message.reply_to_message == None:
			try:
				if config.ignor_id.count(message.from_user.id) > 0:
					bot.send_message(message.chat.id, "Мама сказала ты хулиган и мне нельзя с тобой дружить", None, message.message_id)
				else:
					if message.text.count('**') > 0 or message.text.count('*') > 10 or len(message.text) > 50:
						bot.send_message(message.chat.id, "хуй тебе", None, message.message_id)
					else:
						rnd = random.randrange(1,10,1)
						if rnd <= 3:
							bot.send_message(message.chat.id, "ну "+str(eval(message.text)), None, message.message_id)
						elif rnd > 3 and rnd <=6:
							bot.send_message(message.chat.id, str(eval(message.text))+" и чо?", None, message.message_id)
						elif rnd > 6 and rnd <=9:
							bot.send_message(message.chat.id, "вроде "+str(eval(message.text)), None, message.message_id)
						else:
							bot.send_message(message.chat.id, "да заебал. на "+str(eval(message.text)), None, message.message_id)
					
			except:
				bot.send_message(message.chat.id, "Хуйня какая то", None, message.message_id)
		if isinstance(message.text,str) == True and (message.text.lower() == "баян" or message.text.lower() == "боян"):
			bot.send_message(message.chat.id, "хуян", None, message.message_id)
		if isinstance(message.text,str) == True and message.text[0] == '+' and message.reply_to_message != None:
			cnt = message.text.count('+')
			if cnt == 1:
				bot.send_message(message.chat.id, "От души, брат. говорит @"+message.from_user.username, None, message.reply_to_message.message_id)
			else:
				sMsg = ''
				i=1
				for i in range(cnt):
					sMsg = sMsg + 'пэ-'
				bot.send_message(message.chat.id, sMsg + "люс тебе от @"+message.from_user.username, None, message.reply_to_message.message_id)
		if isinstance(message.text,str) == True and message.text[0] == '-' and message.reply_to_message != None:
			cnt = message.text.count('-')
			if cnt == 1:
				bot.send_message(message.chat.id, "Харам, медик. говорит @"+message.from_user.username, None, message.reply_to_message.message_id)
			else:
				sMsg = ''
				i=1
				for i in range(cnt):
					sMsg = sMsg + 'мэ-'
				bot.send_message(message.chat.id, sMsg + "медик  ты. говорит @"+message.from_user.username, None, message.reply_to_message.message_id)
		if message.content_type == 'voice':
			bot.send_message(message.chat.id, "Чо писать не умеешь? Распизделся тут, медик, боя.", None,message.message_id)
		cnx = mysql.connector.connect(user='root', password='auban', host='127.0.0.1', database='pidor')
		cursor = cnx.cursor(buffered=True)
		query = ('select username, first_name, last_name from members where id='+str(message.from_user.id)+' and chat_id='+str(message.chat.id))
		cursor.execute(query)
		if cursor.rowcount > 0:
			for (user_name, first_name, last_name) in cursor:
				if user_name != message.from_user.username:
					query = 'update members set username=%s where id=%s'
					#print(user_name)
					data_user = (message.from_user.username, message.from_user.id)
					cursor.execute(query, data_user)
					cnx.commit()

		else:
			query = 'insert into members (id,username,chat_id) VALUES (%s,%s,%s)'
			#print(query)
			data_user = (message.from_user.id, message.from_user.username,str(message.chat.id))
			cursor.execute(query, data_user)
			cnx.commit()


		#print(message.from_user.id)
		query = "insert into messages (message_id,member_id,message_date_time,message_text,message_type,message_datetime,chat_id) VALUES (%s,%s,%s,%s,%s,%s,%s)"
		#print(query)
		message_datetime = datetime.datetime.fromtimestamp(int(message.date))
		
		if message.chat.id == config.chat_id:
			msg_txt = str(message.text)
		else:
			msg_txt = "q"
		data_user = (message.message_id, message.from_user.id,message.date,msg_txt,message.content_type,message_datetime,str(message.chat.id))
		try:
			cursor.execute(query, data_user)
		except:
			data_user = (message.message_id, message.from_user.id, message.date, '', message.content_type,message_datetime,str(message.chat.id))
			cursor.execute(query, data_user)
		cnx.commit()
		cursor.close()
		cnx.close()
	else:
		i=1
		if isinstance(message.text,str) == True:
			#print(message.chat)
			try:
				print(message.chat)
			except:
				print("смайлы в названии чата")
			try:
				print(message.text)
			except:
				print("смайлы боя")
			bot.send_message(message.chat.id, "Бот работает только в одном чате.", None, message.message_id)
		if config.admins.count(message.chat.id) > 0:
			#bot.forward_message(439615805,message.chat.id,message.message_id, True)
			bot.send_message(config.chat_id, message.text)
		#if message.chat.id == 439615805:
			#bot.forward_message(52268620,439615805,message.message_id, True)
		# s=''
		# while i < 50:
			# bot.edit_message_text(s+'|',msg.chat.id,msg.message_id)
			# bot.edit_message_text(s+'/',msg.chat.id,msg.message_id)
			# bot.edit_message_text(s+'-',msg.chat.id,msg.message_id)
			# bot.edit_message_text(s+'\\',msg.chat.id,msg.message_id)
			# s=s+'|'
			# i += 1
		# bot.edit_message_text(s, msg.chat.id, msg.message_id)
		# s='.\n.???\n( ????)????*?\n?. ? ...??+.\n???...°?+ *??)\n..........· ??.·*??) ?.·*?)\n..........(?.·? (?.·''* ? ВЖУХ ?'
		# bot.send_message(message.chat.id, s)
		# bot.send_message(message.chat.id, '.\n\n?( ?° ?? ?° )?──?*:?? ты пидор @' + message.from_user.username)

if __name__ == '__main__':
	#bot.polling(100)
	try:
		bot.polling(none_stop=True)
	except:
		print("косяк")
		bot.polling(none_stop=True)
		
	