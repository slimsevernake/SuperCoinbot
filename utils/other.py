import asyncio
import time
import random
import datetime
from aiogram import Dispatcher
from aiogram.utils.exceptions import Unauthorized, BotBlocked, ChatNotFound
from data.config import admins,  kurs, logch, viewsch, bot_token
from loader import bot, data
from utils.sqlite import dep_history, pay_history, get_channels_for_check, set_last_check, increase_fine, user_uncheck, get_last_check, user_warn, edit_ch_status, my_subs_db, add_promotion_to_uncheck
from utils.messages import fine, warnfine, admin_finemsg

def is_digit(string):
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False

def cTime(second):
    ts = time.gmtime(second)
    hour = time.strftime("%H", ts)
    min = time.strftime("%M", ts)
    sec = time.strftime("%S", ts)
    return ({'h': hour, 'm' : min, 's' : sec})

async def history_dep(id, type):
    if type == "user_id":
      h = await dep_history(id, "user_id")
      t = "<b>Дата | Номер кошелька\nСумма | Квитанция | Статус</b>\n"
      if h:
       for x in h:
         dt = datetime.datetime.fromtimestamp(x[2])
         t += f'<i>{str(dt)}</i>|<i>{x[5]}</i>\n<b>{str(round(x[3], 1))}₽</b>|<code>+{str(x[1])}</code>|{x[4]}\n➖➖➖➖➖➖➖➖➖➖\n'
       return t
      else:
       return 0
    else:
      h = await dep_history(id, "comment")
      t = "<b>Дата | Номер кошелька\nСумма | ID | Статус</b>\n"
      if h:
       for x in h:
         dt = datetime.datetime.fromtimestamp(x[2])
         t += f'<i>{str(dt)}</i>|<i>{x[5]}</i>\n<b>{str(round(x[3], 1))}₽</b>|<a href="tg://user?id={x[0]}">{x[0]}</a>|{x[4]}\n➖➖➖➖➖➖➖➖➖➖\n'
       return t
      else:
       return 0

async def my_views_list(id):
    h = await my_subs_db(id, 'views')
    t = ""
    if h:
     for x in h:
       t += f'https://t.me/{viewsch}/{str(x[1])} - Выполнено: <b>{str(len(eval(x[2])))}</b> из <b>{str(x[3])}</b> раз\n'
     return t
    else:
     return 0
	 
async def history_pay(id):
    h = await pay_history(id)
    t = "<b>Дата | Номер кошелька\nСумма | Статус</b>\n"
    if h:
     for x in h:
       dt = datetime.datetime.fromtimestamp(x[4])
       t += f'<i>{str(dt)}</i>|<i>{x[5]}</i>\n<b>{str(round((x[3] * kurs), 2))}₽</b>|<code>{str(x[6])}</code>\n➖➖➖➖➖➖➖➖➖➖\n'
     return t
    else:
     return 0
	
async def starter(dp: Dispatcher):
     for x in admins:
      try:
       await bot.send_message(x, data['about'], parse_mode="html")
      except:
       pass

async def sendadmins(message, markup=None):
    if markup is None:
        for admin in admins:
            try:
                await bot.send_message(admin, message, parse_mode="html", disable_web_page_preview=True)
            except:
                pass
    else:
        for admin in admins:
            try:
                await bot.send_message(admin, message, reply_markup = markup, parse_mode="html", disable_web_page_preview=True)
            except:
                pass

async def user_checker():
    while True:
      await asyncio.sleep(180)
      last = await get_last_check()
      if int(time.time()) > last:
        await set_last_check()
        channels = await get_channels_for_check()
        for x in channels:
         try:
           bstatus = await bot.get_chat_member(x[2], bot_token.split(':')[0])
           bstatus = bstatus.status
         except (Unauthorized, BotBlocked, ChatNotFound):
           bstatus = 'left'
         if bstatus == 'administrator':
           try:
             get_user = await bot.get_chat_member(x[2], x[1])
             if get_user.status == 'left' and x[4] > int(time.time()) and x[6]:
               await increase_fine(x[1])
               await user_uncheck(x[0], x[1])
               if logch:
                 await bot.send_message(logch, admin_finemsg(x[1], x[7]), parse_mode='html',  disable_web_page_preview=True)
               else:
                 await sendadmins(admin_finemsg(x[1], x[7]))
               try:
                 await bot.send_message(x[1], fine(x[7]))
               except:
                 pass
             elif get_user.status == 'left' and x[4] > int(time.time()):
               try:
                 await bot.send_message(x[1], warnfine(x[7]))
                 await user_warn(x[0], x[1])
               except:
                 await increase_fine(x[1])
                 await user_uncheck(x[0], x[1])
             elif get_user.status != 'left' and x[4] < int(time.time()):
                 await user_uncheck(x[0], x[1])
           except:
             pass
         else:
           creater = await edit_ch_status(x[0], 0, x[0])
           await add_promotion_to_uncheck(x[0])
           try:
             await bot.send_message(creater['id'], group_delete_bot(f'@{creater["name"]}', creater["sum"]), disable_web_page_preview=True)
           except:
             pass
      else:
        pass
