import re
import time
import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from data.config import admins, botname, vproc
from loader import dp, bot
from filters import IsAdmin, IsChat
from keyboards.inline import AdminMenu
from utils.sqlite import clear_firstname, new_voucher
from utils.messages import myprofile
from utils.other import cTime
 
premis = { 'can_send_messages' : True, 
         'can_send_media_messages' : True,
		 'can_send_polls' : True,
		 'can_send_other_messages' : True,
		 'can_add_web_page_previews' : True,
		 }
 
@dp.message_handler(IsChat(), chat_type='supergroup', content_types=["new_chat_members", "new_chat_title", "left_chat_member", "pinned_message"])
async def deleter1(m: types.Message):
    try:
      await bot.delete_message(m.chat.id, m.message_id)
    except:
      pass
 
@dp.message_handler(IsChat(), IsAdmin(), chat_type='supergroup', commands = ['help'], state="*")
async def chat_help(m: types.Message):
    await bot.delete_message(m.chat.id, m.message_id)
    await m.reply('<b>Выдать партию чеков в чате:</b>\n5 чеков по 2 рубля <i>vou 5 2</i>\n<b>Для соверешния действия над пользователем надо отметить пользователя именно так:</b>\nМут на 30 секунду <i>/mut 30s</i>\nМут на 1 минуту <i>/mut 1m</i>\nМут на 1 час <i>/mut 1h</i>\nМут на 1 день <i>/mut 1d</i>\nСнять мут <i>/mut 0</i>\nИнформация о юзере <i>/inf</i>', reply=False, parse_mode='html')
 
@dp.message_handler(IsChat(), IsAdmin(), is_reply=True, chat_type='supergroup', commands = ['inf'], state="*")
async def chat_info(m: types.Message):
    try:
      await bot.delete_message(m.chat.id, m.message_id)
    except:
      pass
    txt = await myprofile(m.reply_to_message.from_user.id)
    await m.reply(txt[0], reply=False, parse_mode='html', reply_markup = AdminMenu().chat_ban_kb(str(txt[2]), txt[1]))
	
@dp.message_handler(IsAdmin(), is_reply=True, chat_type='supergroup', commands = ['mut'], state="*")
async def chat_mut(m: types.Message):
    try:
      await bot.delete_message(m.chat.id, m.message_id)
    except:
      pass
    txt = m.text.lower()
    if len(txt.split('/mut ')) == 2:
      tm = txt.split('/mut ')[1]
      if tm != '0':
        if re.search(r'^\d*s$', tm):
          tm = int(tm.split('s')[0])
          s = cTime(tm)
          await m.reply(f'<a href="tg://user?id={m.reply_to_message.from_user.id}">{clear_firstname(m.reply_to_message.from_user.first_name)}</a> будет молчать <b>0 Д. {s["h"]} Ч. {s["m"]} Мин. {s["s"]} Сек.</b>', reply=False, parse_mode='html')
          await bot.restrict_chat_member(chat_id = m.chat.id, user_id = m.reply_to_message.from_user.id, until_date = int(time.time()) + tm)
        elif re.search(r'^\d*m$', tm):
          tm = int(tm.split('m')[0]) * 60
          s = cTime(tm)
          await m.reply(f'<a href="tg://user?id={m.reply_to_message.from_user.id}">{clear_firstname(m.reply_to_message.from_user.first_name)}</a> будет молчать <b>0 Д. {s["h"]} Ч. {s["m"]} Мин. {s["s"]} Сек.</b>', reply=False, parse_mode='html')
          await bot.restrict_chat_member(chat_id = m.chat.id, user_id = m.reply_to_message.from_user.id, until_date = int(time.time()) + tm)
        elif re.search(r'^\d*h$', tm):
          tm = int(tm.split('h')[0]) * 3600
          s = cTime(tm)
          await m.reply(f'<a href="tg://user?id={m.reply_to_message.from_user.id}">{clear_firstname(m.reply_to_message.from_user.first_name)}</a> будет молчать <b>0 Д. {s["h"]} Ч. {s["m"]} Мин. {s["s"]} Сек.</b>', reply=False, parse_mode='html')
          await bot.restrict_chat_member(chat_id = m.chat.id, user_id = m.reply_to_message.from_user.id, until_date = int(time.time()) + tm)
        elif re.search(r'^\d*d$', tm):
          tm = int(tm.split('d')[0]) * 86400
          s = cTime(tm)
          await m.reply(f'<a href="tg://user?id={m.reply_to_message.from_user.id}">{clear_firstname(m.reply_to_message.from_user.first_name)}</a> будет молчать <b>1 Д.</b>', reply=False, parse_mode='html')
          await bot.restrict_chat_member(chat_id = m.chat.id, user_id = m.reply_to_message.from_user.id, until_date = int(time.time()) + tm)
        else:
          await m.reply('<b>Данные введены не коректно.</b> Надо писать так:\nМут на 30 секунду <i>/mut 30s</i>\nМут на 1 минуту <i>/mut 1m</i>\nМут на 1 час <i>/mut 1h</i>\nМут на 1 день <i>/mut 1d</i>\nСнять мут <i>/mut 0</i>', reply=False, parse_mode='html')
      else:
        await m.reply(f'<a href="tg://user?id={m.reply_to_message.from_user.id}">{clear_firstname(m.reply_to_message.from_user.first_name)}</a> был помилован и пока-что может писть в чате.', reply=False, parse_mode='html')
        await bot.restrict_chat_member(chat_id = m.chat.id, user_id = m.reply_to_message.from_user.id, until_date = 0, permissions = premis)
    else:
      await m.reply('<b>Данные введены не коректно.</b> Надо писать так:\nМут на 30 секунду <i>/mut 30s</i>\nМут на 1 минуту <i>/mut 1m</i>\nМут на 1 час <i>/mut 1h</i>\nМут на 1 день <i>/mut 1d</i>\nСнять мут <i>/mut 0</i>', reply=False, parse_mode='html')
		  
@dp.message_handler(IsChat(), IsAdmin(), chat_type='supergroup', regexp="^vou\s+\d*\s+\d*$")
async def chat_voucher(m: types.Message):
    try:
      await bot.delete_message(m.chat.id, m.message_id)
    except:
      pass
    if len(m.text.split(' ')) == 3:
      num = int(m.text.split(' ')[1])
      sum = int(m.text.split(' ')[2])
      keyboard = InlineKeyboardMarkup()
      k = "keyboard.add("
      for x in range(num):
        id = await new_voucher(sum, m.from_user.id, clear_firstname(m.from_user.first_name))
        z = random.randint(1, 100)
        if z > vproc:
          sum = -sum
        k += f"InlineKeyboardButton(text = '🧾', url = 'https://t.me/{botname}?start={id}'), "
      k += ')'
      eval(k)
      await m.reply(f'Партия случайных чеков на сумму <b>± {int(abs(sum))}</b> Super Coin', reply=False, parse_mode='html', reply_markup = keyboard)
    else:
      await m.reply('<b>Данные введены не коректно</b>.\nНадо писать так:\n5 чеков по 2 рубля <i>vou 5 2</i>', reply=False, parse_mode='html')
		  
@dp.callback_query_handler(IsAdmin(), chat_type='supergroup', text='cancel_chat')
async def cancelerchat(c: types.CallbackQuery):
    try:
      await bot.delete_message(c.message.chat.id, c.message.message_id)
    except:
      pass

@dp.message_handler(IsChat(), chat_type='supergroup', regexp='^/', state="*")
async def deleter(m: types.Message):
    try:
      await bot.delete_message(m.chat.id, m.message_id)
    except:
      pass
	
@dp.callback_query_handler(chat_type='supergroup')
async def noaccess(c: types.CallbackQuery):
    try:
      await c.answer('Это не для тебя умник!', show_alert=True)
    except:
      pass