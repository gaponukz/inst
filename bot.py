''' Bot for sending top posts from instagram '''

from aiogram import Bot, Dispatcher, executor, types # all for bot
from instaparser import User # main parser
from config import * # texts (help...)

# 1201136195:AAGr1ioNsrOHqTfJAg_JeOV6FzuxU-RatDI - @sometestbotforparsingbot
API_TOKEN = '1201136195:AAGr1ioNsrOHqTfJAg_JeOV6FzuxU-RatDI'
bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)

@dp.callback_query_handler(lambda c: True)
async def process_callback_button(callback_query: types.CallbackQuery):
	data = callback_query.data.split()
	await bot.send_message(callback_query.from_user.id, "Processing...")

	user = User(data[0])
	if data[1] == 'likes':
		if len(data) > 3:
			posts = user.filter_by_date(user.sort_by_like(), \
				 _from = arguments[3], _to = arguments[4])
		else:
			posts = user.sort_by_like()

	elif data[1] == 'comments':
		if len(data) > 3:
			posts = user.filter_by_date(user.sort_by_comment(), \
				 _from = arguments[3], _to = arguments[4])
		else:
			posts = user.sort_by_comment()

	elif data[1] == 'posts':
		posts = user.filter_by_date(user.get_posts(), \
				_from = arguments[3], _to = arguments[4])

	if posts[int(data[2]):int(data[2])+10]:
		for post in posts[int(data[2]):int(data[2])+10]:
			try:
				media = list(map(lambda x: types.InputMediaPhoto(x), post['img_url']))

				media[-1] = types.InputMediaPhoto(post['img_url'][-1], caption = \
					message_text.format(post['description'],
					post['like_count'], post['comment_count'], post['post_url']))

				await bot.send_media_group(callback_query.from_user.id, media)

			except:
				pass

		if len(data) > 3:
			inline_btn = types.InlineKeyboardButton('Show more', callback_data = f"{user.username} {data[1]} {int(data[2])+10} {data[3]} {data[4]}")
		else:
			inline_btn = types.InlineKeyboardButton('Show more', callback_data = f"{user.username} {data[1]} {int(data[2])+10}")

		inline = types.InlineKeyboardMarkup(row_width = 2).add(inline_btn)

		await callback_query.message.answer("Press the button to show more", reply_markup = inline)

	else:
		await bot.send_message(callback_query.from_user.id, "No more posts")


@dp.message_handler(commands = ['likes'])
async def likes(message: types.Message):
	arguments = message.get_args().split()
	if arguments:
		await bot.send_message(message.from_user.id, "Processing...")

		user = User(arguments[0])

		if not user.is_private():
			if len(arguments) == 1:
				posts = user.sort_by_like()
			else:
				posts = user.filter_by_date(user.sort_by_like(), \
				 _from = arguments[1], _to = arguments[3])

			for post in posts[:10]:
				try:
					media = list(map(lambda x: types.InputMediaPhoto(x), post['img_url']))

					media[-1] = types.InputMediaPhoto(post['img_url'][-1], caption = \
						message_text.format(post['description'],
						post['like_count'], post['comment_count'], post['post_url']))

					await bot.send_media_group(message.from_user.id, media)

				except:
					pass

			if len(arguments) == 1:
				inline_btn = types.InlineKeyboardButton('Show more', callback_data = f"{user.username} likes 10")
			else:
				inline_btn = types.InlineKeyboardButton('Show more', callback_data = f"{user.username} likes 10 {arguments[1]} {arguments[3]}")

			inline = types.InlineKeyboardMarkup(row_width = 2).add(inline_btn)
			await message.answer("Press the button to show more", reply_markup = inline)

		else:
			lang = 1 if message.from_user.language_code == 'ru' else 0

			await message.answer(text['private'][lang])

@dp.message_handler(commands = ['comments'])
async def comments(message: types.Message):
	arguments = message.get_args().split()
	if arguments:
		await bot.send_message(message.from_user.id, "Processing...")

		user = User(arguments[0])

		if not user.is_private():
			if len(arguments) == 1:
				posts = user.sort_by_comment()

			else:
				posts = user.filter_by_date(user.sort_by_comment(), \
				 _from = arguments[1], _to = arguments[3])

			for post in posts[:10]:
				try:
					media = list(map(lambda x: types.InputMediaPhoto(x), post['img_url']))

					media[-1] = types.InputMediaPhoto(post['img_url'][-1], caption = \
						message_text.format(post['description'],
						post['like_count'], post['comment_count'], post['post_url']))

					await bot.send_media_group(message.from_user.id, media)

				except:
					pass

			if len(arguments) == 1:
				inline_btn = types.InlineKeyboardButton('Show more', callback_data = f"{user.username} likes 10")
			else:
				inline_btn = types.InlineKeyboardButton('Show more', callback_data = f"{user.username} likes 10 {arguments[1]} {arguments[3]}")

			inline = types.InlineKeyboardMarkup(row_width = 2).add(inline_btn)
			await message.answer("Press the button to show more", reply_markup = inline)

		else:
			lang = 1 if message.from_user.language_code == 'ru' else 0

			await message.answer(text['private'][arguments[0]])

@dp.message_handler(commands = ['posts'])
async def posts(message: types.Message):
	arguments = message.get_args().split()
	if arguments:
		await bot.send_message(message.from_user.id, "Processing...")

		user = User(arguments[0])

		if not user.is_private():
			posts = user.filter_by_date(user.get_posts(), \
				_from = arguments[1], _to = arguments[3])

			for post in posts[:10]:
				try:
					media = list(map(lambda x: types.InputMediaPhoto(x), post['img_url']))

					media[-1] = types.InputMediaPhoto(post['img_url'][-1], caption = \
						message_text.format(post['description'],
						post['like_count'], post['comment_count'], post['post_url']))

					await bot.send_media_group(message.from_user.id, media)

				except:
					pass

			if len(arguments) == 1:
				inline_btn = types.InlineKeyboardButton('Show more', callback_data = f"{user.username} likes 10")
			else:
				posts = user.filter_by_date(user.sort_by_like(), \
				 _from = arguments[1], _to = arguments[3])
				inline_btn = types.InlineKeyboardButton('Show more', callback_data = f"{user.username} likes 10 {arguments[1]} {arguments[3]}")

			inline = types.InlineKeyboardMarkup(row_width = 2).add(inline_btn)
			await message.answer("Press the button to show more", reply_markup = inline)

		else:
			lang = 1 if message.from_user.language_code == 'ru' else 0

			await message.answer(text['private'][lang])

@dp.message_handler(commands = ['language'])
async def language(message: types.Message):
	arguments = message.get_args().split()
	if arguments: message.from_user.language_code = arguments[0]

@dp.message_handler(commands = ['help'])
async def help(message: types.Message):
	lang = 1 if message.from_user.language_code == 'ru' else 0
	await message.answer(text['help_text'][lang])

@dp.message_handler(commands = ['start'])
async def help(message: types.Message):
	await message.answer('Hello! I am Instagram Sorting Bot. Write /help to see the list of commands.')

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates = True)