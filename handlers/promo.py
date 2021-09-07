import math
import re
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import Unauthorized, BotBlocked, ChatNotFound
from data.config import viewsch, viewsprice, minviews, logch, channelsprice, news, minmembs, bot_token, groupsprice, botsprice, botname
from filters import IsPrivate, IsBan, IsUsr
from keyboards.default import promo_menu, main_menu, main_default
from keyboards.inline import PromoMenu
from loader import dp, bot
from states.states import StoragePromo
from utils.messages import promo, views_main_msg, views_msg, views_bad1, subs_bad, add_view_msg, views_bt_txt, views_add_good, channels_main_msg, select_ch, not_allowed, subs_stoped, stop_subs_usr, new_views_task, new_views_task_adm, ch_add_msg, channel_bad, channel_notbot, channel_errortype, channel_bot_not_adm, channel_add_good, channel_bad1, channel_add_msg, groups_main_msg, group_bad, group_add_msg, group_add_good, group_bad1, group_notbot, group_errortype, group_bot_not_adm, bots_main_msg, select_bt, bot_add_msg, bot_bad, bt_add_msg, new_groups_task, new_channels_task, new_groups_task_adm, new_channels_task_adm, new_bots_task, new_bots_task_adm, bot_good_msg
from utils.sqlite import get_user, my_promo_count, new_views, my_subs_db, get_subs_info, stop_subs, add_advbal, new_channel, get_bots_info, new_bots
from utils.other import sendadmins, my_views_list

@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, text="📢 Продвинуть", state="*")
async def promo_main(m: types.Message):
    u = await get_user(m.from_user.id)
    await m.reply(promo(u['advbal']), reply=False, parse_mode='html', reply_markup = promo_menu())
	
@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, text="👁 Просмотры", state="*")
async def views_menu(m: types.Message):
    u = await get_user(m.from_user.id)
    task = await my_promo_count("views", m.from_user.id)
    await m.reply(views_main_msg(u, task), reply=False, parse_mode='html', reply_markup = PromoMenu().views_main())

@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, text="📢 Каналы", state="*")
async def channels_menu(m: types.Message):
    u = await get_user(m.from_user.id)
    task = await my_promo_count("channels", m.from_user.id)
    await m.reply(channels_main_msg(u, task), reply=False, parse_mode='html', reply_markup = PromoMenu().channels_main())
	
@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, text="👥 Группы", state="*")
async def groups_menu(m: types.Message):
    u = await get_user(m.from_user.id)
    task = await my_promo_count("groups", m.from_user.id)
    await m.reply(groups_main_msg(u, task), reply=False, parse_mode='html', reply_markup = PromoMenu().groups_main())
	
@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, text="🤖 Задания на ботов", state="*")
async def bots_menu(m: types.Message):
    u = await get_user(m.from_user.id)
    task = await my_promo_count("bots", m.from_user.id)
    await m.reply(bots_main_msg(u, task), reply=False, parse_mode='html', reply_markup = PromoMenu().bots_main())
	
@dp.callback_query_handler(IsBan(), IsUsr(), text='cancel')
async def canceler(c: types.CallbackQuery, state: FSMContext):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    await bot.send_message(c.from_user.id, 'Главное меню', reply_markup = main_menu(c.from_user.id))
    await state.finish()

@dp.callback_query_handler(IsBan(), IsUsr(), text='mych')
async def my_channels(c: types.CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    keyboard = InlineKeyboardMarkup()
    log = await my_subs_db(c.from_user.id, 'channels')
    if log:
      for x in log:
        keyboard.add(InlineKeyboardButton(text = x[2], callback_data = f'select_ch:{x[0]}'))
      keyboard.add(InlineKeyboardButton(text = "❌ Отмена", callback_data = 'cancel'))
      await bot.send_message(c.from_user.id, "Задания на подписки", parse_mode='html', reply_markup = keyboard)
    else:
      await bot.send_message(c.from_user.id, "Нет активных заданий на подписки", reply_markup = promo_menu())
	  
@dp.callback_query_handler(IsBan(), IsUsr(), text='mygr')
async def my_groups(c: types.CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    keyboard = InlineKeyboardMarkup()
    log = await my_subs_db(c.from_user.id, 'groups')
    if log:
      for x in log:
        keyboard.add(InlineKeyboardButton(text = x[2], callback_data = f'select_gr:{x[0]}'))
      keyboard.add(InlineKeyboardButton(text = "❌ Отмена", callback_data = 'cancel'))
      await bot.send_message(c.from_user.id, "Задания на вступления в группы", parse_mode='html', reply_markup = keyboard)
    else:
      await bot.send_message(c.from_user.id, "Нет активных заданий на вступления в группы", reply_markup = promo_menu())
	  
@dp.callback_query_handler(IsBan(), IsUsr(), text='mybot')
async def my_bots(c: types.CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    keyboard = InlineKeyboardMarkup()
    log = await my_subs_db(c.from_user.id, 'bots')
    if log:
      for x in log:
        keyboard.add(InlineKeyboardButton(text = x[2], callback_data = f'select_bt:{x[0]}'))
      keyboard.add(InlineKeyboardButton(text = "❌ Отмена", callback_data = 'cancel'))
      await bot.send_message(c.from_user.id, "Задания на переходы в бот", parse_mode='html', reply_markup = keyboard)
    else:
      await bot.send_message(c.from_user.id, "Нет активных заданий на переходы в бот", reply_markup = promo_menu())

@dp.callback_query_handler(IsBan(), IsUsr(), regexp='select_bt:')
async def select_bots(c: types.CallbackQuery):
    num = c.data.split('select_bt:')[1]
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    inf = await get_bots_info(num, "bots")
    if inf['cid'] == c.from_user.id:
      await bot.send_message(c.from_user.id, select_bt(inf, num), parse_mode='html', disable_web_page_preview=True, reply_markup = PromoMenu().bot_del(num))
    else:
      await bot.send_message(c.from_user.id, not_allowed, reply_markup = main_menu(c.from_user.id))
	  
@dp.callback_query_handler(IsBan(), IsUsr(), regexp='select_ch:')
async def select_channels(c: types.CallbackQuery):
    num = c.data.split('select_ch:')[1]
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    inf = await get_subs_info(num, "channels")
    if inf['cid'] == c.from_user.id:
      await bot.send_message(c.from_user.id, select_ch(inf, num), parse_mode='html', disable_web_page_preview=True, reply_markup = PromoMenu().channel_del(num))
    else:
      await bot.send_message(c.from_user.id, not_allowed, reply_markup = main_menu(c.from_user.id))
	  
@dp.callback_query_handler(IsBan(), IsUsr(), regexp='select_gr:')
async def select_groups(c: types.CallbackQuery):
    num = c.data.split('select_gr:')[1]
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    inf = await get_subs_info(num, "groups")
    if inf['cid'] == c.from_user.id:
      await bot.send_message(c.from_user.id, select_ch(inf, num), parse_mode='html', disable_web_page_preview=True, reply_markup = PromoMenu().group_del(num))
    else:
      await bot.send_message(c.from_user.id, not_allowed, reply_markup = main_menu(c.from_user.id))

@dp.callback_query_handler(IsBan(), IsUsr(), regexp='grdel:')
async def del_groups(c: types.CallbackQuery):
    num = c.data.split('grdel:')[1]
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    inf = await stop_subs(num, c.from_user.id, "groups")
    if inf:
      await bot.send_message(c.from_user.id, subs_stoped, parse_mode='html', disable_web_page_preview=True, reply_markup = promo_menu())
      await add_advbal(c.from_user.id, (inf["memb"] - inf["count"]) * groupsprice)
      if logch:
          await bot.send_message(logch,stop_subs_usr(c, "Вступление в группы", num, (inf["memb"] - inf["count"]) * groupsprice), parse_mode='html',  disable_web_page_preview=True)
      else:
          await sendadmins(stop_subs_usr(c, "Вступление в группы", num, (inf["memb"] - inf["count"]) * groupsprice))
    else:
      await bot.send_message(c.from_user.id, not_allowed, reply_markup = main_menu(c.from_user.id))
	  
@dp.callback_query_handler(IsBan(), IsUsr(), regexp='botdel:')
async def del_bots(c: types.CallbackQuery):
    num = c.data.split('botdel:')[1]
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    inf = await stop_subs(num, c.from_user.id, "bots")
    if inf:
      await bot.send_message(c.from_user.id, subs_stoped, parse_mode='html', disable_web_page_preview=True, reply_markup = promo_menu())
      await add_advbal(c.from_user.id, (inf["memb"] - inf["count"]) * botsprice)
      if logch:
          await bot.send_message(logch,stop_subs_usr(c, "Переходы в бот", num, (inf["memb"] - inf["count"]) * botsprice), parse_mode='html',  disable_web_page_preview=True)
      else:
          await sendadmins(stop_subs_usr(c, "Переходы в бот", num, (inf["memb"] - inf["count"]) * botsprice))
    else:
      await bot.send_message(c.from_user.id, not_allowed, reply_markup = main_menu(c.from_user.id))
	  
@dp.callback_query_handler(IsBan(), IsUsr(), regexp='chdel:')
async def del_channels(c: types.CallbackQuery):
    num = c.data.split('chdel:')[1]
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    inf = await stop_subs(num, c.from_user.id, "channels")
    if inf:
      await bot.send_message(c.from_user.id, subs_stoped, parse_mode='html', disable_web_page_preview=True, reply_markup = promo_menu())
      await add_advbal(c.from_user.id, (inf["memb"] - inf["count"]) * channelsprice)
      if logch:
          await bot.send_message(logch,stop_subs_usr(c, "Подписки на канал", num, (inf["memb"] - inf["count"]) * channelsprice), parse_mode = 'html',  disable_web_page_preview=True)
      else:
          await sendadmins(stop_subs_usr(c, "Подписки на канал", num, (inf["memb"] - inf["count"]) * channelsprice))
    else:
      await bot.send_message(c.from_user.id, not_allowed, reply_markup = main_menu(c.from_user.id))
	  
@dp.callback_query_handler(IsBan(), IsUsr(), text='myviews')
async def my_views(c: types.CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    text = await my_views_list(c.from_user.id)
    if text:
      await bot.send_message(c.from_user.id, text, disable_web_page_preview=True, parse_mode='html', reply_markup = promo_menu())
    else:
      await bot.send_message(c.from_user.id, "Нет активных заданий на просмотры", reply_markup = promo_menu())
	  
@dp.callback_query_handler(IsBan(), IsUsr(), text='addview')
async def views_add(c: types.CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    await bot.send_message(c.from_user.id, views_msg, parse_mode='html', reply_markup = main_default)
    await StoragePromo.views_add.set()
	
@dp.callback_query_handler(IsBan(), IsUsr(), text='addch')
async def channel_add_menu(c: types.CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    await bot.send_message(c.from_user.id, ch_add_msg, parse_mode='html', reply_markup = main_default)
    await StoragePromo.channel_add.set()
	
@dp.callback_query_handler(IsBan(), IsUsr(), text='addgr')
async def group_add_menu(c: types.CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    await bot.send_message(c.from_user.id, ch_add_msg, parse_mode='html', reply_markup = main_default)
    await StoragePromo.group_add.set()

@dp.callback_query_handler(IsBan(), IsUsr(), text='addbot')
async def bot_add_menu(c: types.CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    await bot.send_message(c.from_user.id, bot_add_msg, parse_mode='html', reply_markup = main_default)
    await StoragePromo.bot_add.set()

@dp.message_handler(IsBan(), IsUsr(), is_forwarded=False, state=StoragePromo.bot_add)
async def bot_add_handler(m: types.Message, state: FSMContext):
    try:
      if math.floor(int(m.text)) >= minmembs:
        u = await get_user(m.from_user.id)
        if u["advbal"] >= (math.floor(int(m.text)) * botsprice):
          await m.reply(bt_add_msg(int(m.text)), reply_markup = main_default)
          async with state.proxy() as data:
            data["bot_amount"] = math.floor(int(m.text))
          await StoragePromo.bot_add1.set()
        else:
          await m.reply(subs_bad, reply=False, reply_markup = PromoMenu().get_money())
          await state.finish()
      else:
        await m.reply(bot_bad, reply=False, reply_markup = main_default)
    except ValueError:
      await m.reply('Введите число:', reply=False, reply_markup = main_default)
	  
@dp.message_handler(IsBan(), IsUsr(), is_forwarded=False, state=StoragePromo.bot_add1)
async def bot_final_handler(m: types.Message, state: FSMContext):
    async with state.proxy() as data:
      num = data["bot_amount"]
    text = m.text.replace("http://", "https://").replace("telegram.me", "t.me")
    if re.search(r'^https://t.me/', text):
      try:
        uname = text.split("https://t.me/")[1].split("?start=")[0]
        ref = text.split("?start=")[1]
      except (ValueError, IndexError):
        ref = 0
        uname = text.split("https://t.me/")[1].replace('@', '')
      await new_bots(ref, uname, text, num, m.from_user.id)
      await m.reply(bot_good_msg(num), reply=False, parse_mode='html', reply_markup = promo_menu())
      await state.finish()
      await bot.send_message(f'@{news}', new_bots_task(num), parse_mode='html', disable_web_page_preview=True)
      if logch:
        await bot.send_message(logch, new_bots_task_adm(m, num), parse_mode='html', disable_web_page_preview=True)
      else:
        await sendadmins(new_bots_task_adm(m, num))
    else:
     await m.reply(f'Введите ссылку в виде https://t.me/{botname}?start={m.from_user.id}', reply=False, disable_web_page_preview=True, reply_markup = main_default)
	
@dp.message_handler(IsBan(), IsUsr(), is_forwarded=False, state=StoragePromo.group_add)
async def group_add_handler(m: types.Message, state: FSMContext):
    try:
      if math.floor(int(m.text)) >= minmembs:
        u = await get_user(m.from_user.id)
        if u["advbal"] >= (math.floor(int(m.text)) * groupsprice):
          await m.reply(group_add_msg(int(m.text)), reply_markup = main_default)
          async with state.proxy() as data:
            data["gr_amount"] = math.floor(int(m.text))
          await StoragePromo.group_add1.set()
        else:
          await m.reply(subs_bad, reply=False, reply_markup = PromoMenu().get_money())
          await state.finish()
      else:
        await m.reply(group_bad, reply=False, reply_markup = main_default)
    except ValueError:
      await m.reply('Введите число:', reply=False, reply_markup = main_default)
	
@dp.message_handler(IsBan(), IsUsr(), is_forwarded=False, state=StoragePromo.channel_add)
async def channel_add_handler(m: types.Message, state: FSMContext):
    try:
      if math.floor(int(m.text)) >= minmembs:
        u = await get_user(m.from_user.id)
        if u["advbal"] >= (math.floor(int(m.text)) * channelsprice):
          await m.reply(channel_add_msg(int(m.text)), reply_markup = main_default)
          async with state.proxy() as data:
            data["ch_amount"] = math.floor(int(m.text))
          await StoragePromo.channel_add1.set()
        else:
          await m.reply(subs_bad, reply=False, reply_markup = PromoMenu().get_money())
          await state.finish()
      else:
        await m.reply(channel_bad, reply=False, reply_markup = main_default)
    except ValueError:
      await m.reply('Введите число:', reply=False, reply_markup = main_default)
	  
@dp.message_handler(IsBan(), IsUsr(), content_types=["photo", "text", "video"], state=StoragePromo.channel_add1)
async def channel_final_handler(m: types.Message, state: FSMContext):
    async with state.proxy() as data:
      num = data["ch_amount"]
    try:
      txt = m.forward_from_chat.id
    except:
      txt = f'@{m.text.replace("https://t.me", "").replace("/", "").replace("@", "")}'
    try:
      channelinf = await bot.get_chat(txt)
      if channelinf.type == 'channel':
        status_bot_in_channel = await bot.get_chat_member(txt, bot_token.split(':')[0])
        if status_bot_in_channel.status == 'administrator':
          log = await new_channel(channelinf.id, channelinf.username, num, m.from_user.id, "channels")
          if log:
            await m.reply(channel_add_good(num), reply=False, parse_mode='html', reply_markup = promo_menu())
            await state.finish()
            await bot.send_message(f'@{news}', new_channels_task(channelinf, num), parse_mode='html',  disable_web_page_preview=True)
            if logch:
              await bot.send_message(logch, new_channels_task_adm(m, num, channelinf.username), parse_mode='html', disable_web_page_preview=True)
            else:
              await sendadmins(new_channels_task_adm(m, num, channelinf.username))
          else:
            await m.reply(channel_bad1, reply=False, parse_mode='html', reply_markup = main_default)
        else:
          await m.reply(channel_bot_not_adm, reply=False, parse_mode='html', reply_markup = promo_menu())
          await state.finish()
      else:
        await m.reply(channel_errortype, reply=False, parse_mode='html', reply_markup = promo_menu())
        await state.finish()
    except (Unauthorized, BotBlocked, ChatNotFound):
      await m.reply(channel_notbot, reply=False, parse_mode='html', reply_markup = promo_menu())
      await state.finish()
   
@dp.message_handler(IsBan(), IsUsr(), is_forwarded=False, state=StoragePromo.group_add1)
async def group_final_handler(m: types.Message, state: FSMContext):
    async with state.proxy() as data:
      num = data["gr_amount"]
    txt = f'@{m.text.replace("https://t.me", "").replace("/", "").replace("@", "")}'
    try:
      channelinf = await bot.get_chat(txt)
      if channelinf.type == 'supergroup':
        status_bot_in_channel = await bot.get_chat_member(channelinf.id, bot_token.split(':')[0])
        if status_bot_in_channel.status == 'administrator':
          log = await new_channel(channelinf.id, channelinf.username, num, m.from_user.id, "groups")
          if log:
            await m.reply(group_add_good(num), reply=False, parse_mode='html', reply_markup = promo_menu())
            await state.finish()
            await bot.send_message(f'@{news}', new_groups_task(channelinf, num), parse_mode='html',  disable_web_page_preview=True)
            if logch:
              await bot.send_message(logch, new_groups_task_adm(m, num, channelinf.username), parse_mode='html', disable_web_page_preview=True)
            else:
              await sendadmins(new_groups_task_adm(m, num, channelinf.username))
          else:
            await m.reply(group_bad1, reply=False, parse_mode='html', reply_markup = main_default)
        else:
          await m.reply(group_bot_not_adm, reply=False, parse_mode='html', reply_markup = promo_menu())
          await state.finish()
      else:
        await m.reply(group_errortype, reply=False, parse_mode='html', reply_markup = promo_menu())
        await state.finish()
    except (Unauthorized, BotBlocked, ChatNotFound):
      await m.reply(group_notbot, reply=False, parse_mode='html', reply_markup = promo_menu())
      await state.finish()
   
@dp.message_handler(IsBan(), IsUsr(), is_forwarded=False, state=StoragePromo.views_add)
async def views_add_handler(m: types.Message, state: FSMContext):
    try:
      if math.floor(int(m.text)) >= minviews:
        u = await get_user(m.from_user.id)
        if u["advbal"] >= (math.floor(int(m.text)) * viewsprice):
          await m.reply(add_view_msg(int(m.text)), parse_mode='html', reply_markup = main_default)
          async with state.proxy() as data:
            data["views_amount"] = math.floor(int(m.text))
          await StoragePromo.views_fwd.set()
        else:
          await m.reply(subs_bad, reply=False, parse_mode='html', reply_markup = PromoMenu().get_money())
          await state.finish()
      else:
        await m.reply(views_bad1, reply=False, parse_mode='html', reply_markup = main_default)
    except ValueError:
      await m.reply('Введите число:', reply=False, parse_mode='html', reply_markup = main_default)
	  
@dp.message_handler(IsBan(), IsUsr(), content_types=['text', 'video', 'photo', 'document', 'animation'], is_forwarded=True, state=StoragePromo.views_fwd)
async def views_fwd_handler(m: types.Message, state: FSMContext):
    async with state.proxy() as data:
      num = data["views_amount"]
    await state.finish()
    log = await bot.forward_message(f'@{viewsch}', m.chat.id, m.message_id)
    id = await new_views(log.message_id, num, m.from_user.id)
    await bot.send_message(f'@{viewsch}', views_bt_txt, reply_markup = PromoMenu().views_bt(str(id)))
    await m.reply(views_add_good(num), reply=False, reply_markup = promo_menu())
    await bot.send_message(f'@{news}', new_views_task(num), parse_mode='html',  disable_web_page_preview=True)
    if logch:
      await bot.send_message(logch, new_views_task_adm(m, id, num), parse_mode='html', disable_web_page_preview=True)
    else:
      await sendadmins(new_views_task_adm(m, id, num))