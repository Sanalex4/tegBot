#coding=utf-8
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.types import ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

from os import remove

token 	= "1728026706:AAG4og-OlpZjL9AGKAWgDJZqOHVNBD_5fBE"
bot 	= Bot(token = token)
dp 		= Dispatcher(bot)

##	СИСТЕМНЫЕ ФУНКЦИИ
#Получение стадии
def getStage(uid):
	try:
		profile = open("PROFILES\\" + uid + ".txt", 'r', encoding = "UTF-8")
		stage = int(profile.readlines()[0])
		profile.close()
		return stage
	except FileNotFoundError:
		return 0

#Регистрация пользователя
def register(uid):
	profile = open("PROFILES\\" + uid + ".txt", 'w')
	profile.write("1\n")
	profile.close()

#Изменение стадии
def setstage(uid, stg):
	profile = open("PROFILES\\" + uid + ".txt", 'r', encoding = "UTF-8")
	content = profile.readlines()
	profile.close()

	profile = open("PROFILES\\" + uid + ".txt", 'w', encoding = "UTF-8")
	content[0] = str(stg) + "\n"
	for line in content:
		profile.write(line)
	profile.close()

#Изменение значения в профиле
def value(uid, parameter, val):
	val = str(val)
	profile = open("PROFILES\\" + uid + ".txt", 'r', encoding = "UTF-8")
	content = profile.readlines()
	profile.close()

	try:
		#Если есть значения в профиле, изменить его
		index = content.index(parameter + "\n")
		content[index + 1] = val + "\n"
	except ValueError:
		#Если нет значения в профиле, создать его
		content.append(parameter + "\n")
		content.append(val + "\n")

	#Записать результат
	profile = open("PROFILES\\" + uid + ".txt", 'w', encoding = "UTF-8")
	for line in content:
		profile.write(line)
	profile.close()

#Получение значения из профиля
#если значения нет, вернёт None
def getValue(uid, parameter):
	profile = open("PROFILES\\" + uid + ".txt", 'r', encoding = "UTF-8")
	content = profile.readlines()
	try:
		return content[content.index(parameter + "\n") + 1][:-1]
	except ValueError:
		return None

####=======================####
####======ОБРАБОТЧИК=======####
####=======================####
@dp.message_handler()
async def poll(message: types.Message):
	text 	= message.text
	uid 	= str(message.from_user.id)
	stage 	= getStage(uid)

	if stage == 0:
		register(uid)
		await bot.send_message(uid, "Приветствую вас. Меня зовут Екатерина Яковлева. Я специалист области психологии, психологии питания, здорового питания. В современном ритме жизни, очень важно уметь сохранять свое здоровье, наша голова и тело - это единая система.  Как же понять и оценить свое здоровье? Предлагаю пройти 2 теста, чтобы оценить состояние тревожности и пищевого поведения:")
		await bot.send_message(uid, "Тест на уровень тревожности – подскажет как ты справляешься со сложными ситуациями")
		await bot.send_message(uid, "Тест ЕАТ-26 – первично подскажет если у тебя проблемы с пищевым поведением.")
		await bot.send_message(uid, "Начнем?! Выберите тест который хотите пройти...")
		await bot.send_message(uid, "В каждом тесте можно отвечать только с помощью кнопок", reply_markup = kb_choose)

		setstage(uid, 100)

	elif stage == 100:
		if text == "EAT-26":
			await bot.send_message(uid, "Пожалуйста, прочитайте утверждения, приведённые ниже, и отметьте в каждой строчке ответ, наиболее соответствующий Вашему мнению. Помните, что данный тест является инструментом предварительной оценки и не может служить для постановки диагноза.", reply_markup = kb_exit)
			setstage(uid, 101)
		elif text == "Тест тревожности":
			await bot.send_message(uid, 'Здравствуйте! Предлагаем Вам пройти тест на выявление уровня "тревожности". Тест состоит из 40 высказываний, используйте клавиатуру, чтобы показать ваше состояние, относительно утверждений. Над вопросами долго не задумывайтесь. Обычно первый ответ, который приходит в голову, является наиболее правильным, адекватным Вашему состоянию.', reply_markup = kb_exit)
			setstage(uid, 102)

	elif stage == 101:
		if text == "Начать тест!":
			value(uid, "testid", "1")
			await bot.send_message(uid, questions[0], reply_markup = kb)
			value(uid, "points", "0")
			setstage(uid, 1)
		else:
			await bot.send_message(uid, "Возвращаемся...", reply_markup = kb_choose)
			setstage(uid, 100)

	elif stage == 102:
		if text == "Начать тест!":
			value(uid, "testid", "0")
			value(uid, "1_s", "0")
			value(uid, "1_r", "0")
			value(uid, "2_s", "0")
			value(uid, "2_r", "0")
			setstage(uid, 1)
			await bot.send_message(uid, "===КАК ВЫ СЕБЯ ЧУВСТВУЕТЕ В ДАННЫЙ МОМЕНТ===")
			await bot.send_message(uid, questions2[0], reply_markup = kb2)
		else:
			await bot.send_message(uid, "Возвращаемся...", reply_markup = kb_choose)
			setstage(uid, 100)

	else:
		testid = int(getValue(uid, "testid"))

		if testid == 1:
			if stage <= 24:
				if text == "Всегда":
					increase = 3
				elif text == "Как правило":
					increase = 2
				elif text == "Довольно часто":
					increase = 1
				elif text == "Иногда":
					increase = 0
				elif text == "Редко":
					increase = 0
				elif text == "Никогда":
					increase = 0
				else:
					increase = -1

				if increase == -1:
					await bot.send_message(uid, "Пожалуйста, используйте клавиатуру")
				else:
					value(uid, "points", int(getValue(uid, "points")) + increase)
					await bot.send_message(uid, questions[stage])
					setstage(uid, stage + 1)

			elif stage == 25:
				if text == "Всегда":
					increase = 0
				elif text == "Как правило":
					increase = 0
				elif text == "Довольно часто":
					increase = 0
				elif text == "Иногда":
					increase = 1
				elif text == "Редко":
					increase = 2
				elif text == "Никогда":
					increase = 3
				else:
					increase = -1

				if increase == -1:
					await bot.send_message(uid, "Пожалуйста, используйте клавиатуру")
				else:
					await bot.send_message(uid, "Тест завершён!", reply_markup = kb_result)
					value(uid, "points", int(getValue(uid, "points")) + increase)
					setstage(uid, stage + 1)

			elif stage == 26:
				if int(getValue(uid, "points")) <= 20:
					await bot.send_message(uid, "У вас все хорошо. Проблем связанных с булимией или анорексией не обнаружено. Но если у вас остались вопросы вы можете обратится https://www.instagram.com/yakovleva.katrin/", reply_markup = kb_return)
				else:
					await bot.send_message(uid, "У вас есть очень высокая вероятность отклонений, расстройств. Вашего отношения к приему пищи. То есть можно говорить, что у Вас имеются какие-либо нарушения пищевого поведения, предположительно, анорексия или булимия. Тем не менее, помните, что тест ЕАТ-26 самостоятельным диагностическим инструментом не является, а используется для предварительной оценки отношения к приему пищи. Только лишь по показателям этого теста ставить диагноз неправильно. Обратитесь к специалисту  https://www.instagram.com/yakovleva.katrin/", reply_markup = kb_return)
				setstage(uid, 27)
			elif stage == 27:
				await bot.send_message(uid, "Возвращаемся...", reply_markup = kb_choose)
				setstage(uid, 100)
		else:
			if stage <= 19:
				need_reverse = False
				for item in reverse:
					if item == stage:
						need_reverse = True
						break

				if text == "Нет, это не так":
					increase = 1
				elif text == "Пожалуй, так":
					increase = 2
				elif text == "Верно":
					increase = 3
				elif text == "Совершенно верно":
					increase = 4
				else:
					increase = 0

				if increase == 0:
					await bot.send_message(uid, "Пожалуйста, используйте клавиатуру")
				else:
					if need_reverse:
						value(uid, "1_r", int(getValue(uid, "1_r")) + increase)
					else:
						value(uid, "1_s", int(getValue(uid, "1_s")) + increase)

					if stage != 19:
						await bot.send_message(uid, questions2[stage])
					else:
						await bot.send_message(uid, "===КАК ВЫ СЕБЯ ЧУВСТВУЕТЕ ОБЫЧНО===")
						await bot.send_message(uid, questions3[0], reply_markup = kb3)
					setstage(uid, stage + 1) 

			elif stage <= 39:
				need_reverse = False
				for item in reverse2:
					if item == stage:
						need_reverse = True
						break

				if text == "Почти никогда":
					increase = 1
				elif text == "Иногда":
					increase = 2
				elif text == "Часто":
					increase = 3
				elif text == "Почти всегда":
					increase = 4
				else:
					increase = 0

				if increase == 0:
					await bot.send_message(uid, "Пожалуйста, используйте клавиатуру")
				else:
					if need_reverse:
						value(uid, "2_s", int(getValue(uid, "2_s")) + increase)
					else:
						value(uid, "2_r", int(getValue(uid, "2_r")) + increase)
					if stage != 39:
						await bot.send_message(uid, questions3[stage - 19])
					else:
						await bot.send_message(uid, "Мы готовы предоставить вам результат!", reply_markup = kb_result)
					setstage(uid, stage + 1)

			elif stage == 40:

				await bot.send_message(uid, "Ситуационная, или ситуативная тревога характеризуется состоянием личности в определенный момент времени и связана с внешними факторами, обусловливающими «витальную» или социальную угрозу. Такая тревожность является ответом на изменения обстоятельств, которые расцениваются субъектом как стрессовые. Когда раздражающий фактор иссякает, состояние индивида нормализуется. Реактивную тревогу могут провоцировать самые разные причины: сложная политическая и экономическая ситуация, природные катаклизмы, негативные новости, проблемы в семье и на работе, собственный багаж неудачного опыта, страхи. На физиологическом уровне реакция тревоги проявляется усилением сердцебиения, учащением дыхания, повышением артериального давления, снижением порога чувствительности и возрастанием общей возбудимости как стремления изменить трудную жизненную ситуацию.")
				await bot.send_message(uid, "У вас...")

				points = int(getValue(uid, "1_s")) - int(getValue(uid, "1_r")) + 50

				if points < 30:
					await bot.send_message(uid, "Низкий уровень ситуативной тревожности. У вас хорошие адаптивные возможности личности, способность самостоятельно принимать решения в сложных ситуациях и осознать причину своей тревоги.")
				elif points < 45:
					await bot.send_message(uid, "Cредний уровень ситуативной тревожности. У вас достаточно хороших адаптивных возможностях личности, вы способны самостоятельно принимать решения в сложных ситуациях. Обратите внимание всегда ли вы можете отслеживать причину своего психоэмоционального состояния и управлять им. Рекомендуем пройти онлайн курс 'Перезагрузка' https://taplink.cc/yakovleva.katrin")
				else:
					await bot.send_message(uid, "Высокий уровень ситуативной тревожности. Адаптивные возможности личности снижены, вам трудно принимать решения в сложных ситуациях и осознавать причину тревоги. Рекомендуется обратится к специалисту на индивидуальную консультацию https://taplink.cc/yakovleva.katrin")

				await bot.send_message(uid, "Личностная тревожность формируется с раннего детства, базируясь на индивидуальных особенностях личности и под влиянием внешних факторов, а также типов воспитания. Причиной тревоги может выступать внутриличностный конфликт, формирующийся в процессе воспитания и жизнедеятельности")
				points = int(getValue(uid, "2_s")) - int(getValue(uid, "2_r")) + 35

				if points < 30:
					await bot.send_message(uid, "У вас низкий уровень личностной тревожности. Все хорошо")
				elif points < 45:
					await bot.send_message(uid, "У вас адекватный уровень личностной тревожности. Вы хотите больше узнать о том, как восстанавливать и поддерживать внутренние ресурсы? Контролировать и управлять своим психоэмоциональным состоянием? Ждем Вас на онлайн-курсе «Перезагрузка» https://www.instagram.com/yakovleva.katrin/")
				else:
					await bot.send_message(uid, "Повышенный уровень личностной тревожности, как правило, связано с формированием внутриличностного конфликта и проявляется ощущением постоянной опасности, чувством неопределенности, озабоченности, напряжения и надвигающейся неудачи, тревожного ожидания, неопределенного беспокойства или как ощущение неопределенной угрозы, характер и время которой не поддается предсказанию. Рекомендуется консультация специалиста.")
				await bot.send_message(uid, "...", reply_markup = kb_return)
				setstage(uid, 41)
			elif stage == 41:
				await bot.send_message(uid, "Возвращаемся...", reply_markup = kb_choose)
				setstage(uid, 100)

kb = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)
kb.add("Всегда", "Как правило", "Довольно часто")
kb.add("Иногда", "Редко", "Никогда")

kb2 = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)
kb2.add("Нет, это не так", "Пожалуй, так")
kb2.add("Верно", "Совершенно верно")

kb3 = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)
kb3.add("Почти никогда", "Иногда")
kb3.add("Часто", "Почти всегда")

kb_choose = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)
kb_choose.add("EAT-26", "Тест тревожности")

kb_exit = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)
kb_exit.add("Начать тест!")
kb_exit.add("Вернуться")

kb_return = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)
kb_return.add("Вернуться")

kb_result = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)
kb_result.add("Узнать результат")

questions = [	"Меня пугает мысль о том, что я располнею",
				"Я  воздерживаюсь от еды, будучи голодным(ой)",
				"Я нахожу, что поглощён(на) мыслями о еде",
				"У меня бывают приступы бесконтрольного поглощения пищи, во время которых я не могу себя остановить",
				"Я делю свою еду на мелкие кусочки",
				"Я знаю, сколько калорий в пище, которую я ем",
				"Я в особенности воздерживаюсь от еды, содержащей много углеводов (хлеб, рис, картофель)",
				"Я чувствую, что окружающие предпочли бы, чтобы я больше ел(а)",
				"Меня рвёт после еды",
				"Я испытываю обострённое чувство вины после еды",
				"Когда я занимаюсь спортом, то думаю, что я сжигаю калории",
				"Окружающие считают меня слишком худым(ой)",
				"Я озабочен(а) мыслями об имеющимся в моём теле жире",
				"на то, чтобы съесть еду, у меня уходит больше времени, чем у других людей",
				"Я воздерживаюсь от еды, содержащей сахар",
				"Я ем диетические продукты",
				"Я чувствую, что вопросы, связанные с едой, контролируют мою жизнь",
				"У меня есть самоконтроль в вопросах, связанных с едой",
				"Я чувствую, что окружающие оказывают на меня давление, чтобы я ел(а)",
				"Я трачу слишком много времени на вопросы, связанные с едой",
				"Я чувствую дискомфорт после того, как поем сладости",
				"Я соблюдаю диету",
				"Мне нравится ощущение пустого желудка",
				"После еды у меня бывает импульсивное желание её вырвать",
				"Я получаю удовольствие, когда пробую новые и вкусные блюда" ]


questions2 = [	"Мне ничего не угрожает",
				"Я нахожусь в напряжении",
				"Я испытываю сожаление",
				"Я чувствую себя свободно",
				"Я расстроен",
				"Меня волнуют возможные неудачи",
				"Я чувствую себя отдохнувшим",
				"Я встревожен",
				"Я испытываю чувство внутреннего удовлетворения",
				"Я уверен в себе",
				"Я нервничаю",
				"Я не нахожу себе места",
				"Я взвинчен",
				"Я не чувствую скованности",
				"Я доволен",
				"Я озабочен",
				"Я слишком возбуждён и мне не по себе",
				"Мне радостно",
				"Мне приятно",	]


questions3 = [	"Я испытываю удовольствие",
				"Я обычно быстро устаю",
				"Я легко могу заплакать",
				"Я хотел бы быть таким же счастливым, как и другие",
				"Нередко я проигрываю из-за того, что недостаточно быстро принимаю решения",
				"Обычно я чувствую себя бодрым",
				"Я спокоен, хладнокровен и собран",
				"Ожидаемые трудности обычно очень тревожат меня",
				"Я слишком переживаю из-за пустяков",
				"Я вполне счастлив",
				"Я принимаю всё слишком близко к сердцу",
				"Мне не хватает уверенности в себе",
				"Обычно я чувствую себя в безопасности",
				"Я стараюсь избегать критических ситуаций и трудностей",
				"У меня бывает хандра",
				"Я доволен",
				"Всякие пустяки отвлекают и волнуют меня",
				"Я так сильно переживаю свои разочарования, что потом долго не могу о них забыть",
				"Я уравновешенный человек",
				"Меня охватывает беспокойство, когда я думаю о своих делах и заботах"	]

reverse = [1,2,5,8,10,11,15,16,19]
reverse2 = [20, 21,26,27,30,33,36,39]

##	ПРОСЛУШИВАТЕЛЬ
print("Бот запущен")
executor.start_polling(dp)
