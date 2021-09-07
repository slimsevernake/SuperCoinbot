import random
import re
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import Unauthorized, BotBlocked, ChatNotFound
from data.config import chan1, chan2, bot_token, logch1, viewsch
from filters import IsPrivate, IsBan, IsUsr
from keyboards.default import main_default, main_menu, earn_menu, bot_skip
from keyboards.inline import EarnMenu
from loader import dp, bot
from states.states import StorageEarn
from utils.messages import earnavlidmsg, subscribe_channel, all_is_successfully, channel_delete_bot, no_channels, entered_group, group_delete_bot, no_groups, pleaseentered, channel_sub_good, channel_sub_admmsg, you_are_later_ch, you_did_this, all_is_successfully_gr, group_sub_admmsg, group_sub_good, you_are_later_gr, group_delete_bot, bots_msg, no_bots, bots_good, bots_ne, go_views, bots_admmsg, views_pay, views_complete, views_del, views_completeadm, views_nopay, you_dont_nogr, you_dont_noch, no_views_tsk
from utils.sqlite import earn_valid, edit_ch_status, for_subscribe, promoch_info, add_user_to_subsch, add_promotion_to_uncheck, get_url_bot, udata, for_views, views_good_pay, edit_vi_status
from utils.other import sendadmins

black_listbt = {}
black_listgr = {}
black_listch = {}

@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, text="💰 Заработать Super Coin", state="*")
async def earns_menu(m: types.Message):
    black_listbt[m.from_user.id] = []
    black_listgr[m.from_user.id] = []
    black_listch[m.from_user.id] = []
    await m.reply(earnavlidmsg(await earn_valid(m.from_user.id)), reply=False, parse_mode='html', reply_markup = earn_menu())

@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, regexp="^📢 Каналы\s.+$", state="*")
@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, text='▶️ Пропустить', state=StorageEarn.channels_skip)
async def earn_channels(m: types.Message, state: FSMContext):
    await state.finish()
    ch1, ch2 = await bot.get_chat_member(chan1, m.from_user.id), await bot.get_chat_member(chan2, m.from_user.id)
    try:
      if black_listch[m.from_user.id] == None:
        black_listch[m.from_user.id] = []
    except:
      black_listch[m.from_user.id] = []
    if ch1.status != "left" and ch2.status != "left":
      while True:
       chlist = await for_subscribe("channels")
       if len(chlist) >= 1:
           good_channels = {}
           for x in chlist:
            if len(eval(x[3])) < x[4]:
              if m.from_user.id not in eval(x[3]) and m.from_user.id != x[5]:
                good_channels[x[1]] = x[0]
              else:
                chlist = 0
            else:
               creator = await edit_ch_status(x[0], 0, "channels")
               try:
                 await bot.send_message(creator['id'], all_is_successfully(x[2], x[4]), parse_mode='html')
               except:
                 pass
               chlist = 0
           if len(good_channels) >= 1:
             chlist = good_channels
           else:
             chlist = 0
       else:
         chlist = 0
       if chlist != 0 and len(chlist) > len(black_listch[m.from_user.id]):
         ch_to_sub = random.choice(list(chlist))
         if ch_to_sub not in black_listch[m.from_user.id]:
           try:
             bstatus = await bot.get_chat_member(ch_to_sub, bot_token.split(':')[0])
             bstatus = bstatus.status
           except (Unauthorized, BotBlocked, ChatNotFound):
             bstatus = 'left'
           if bstatus == "administrator":
             try:
               user = await bot.get_chat_member(ch_to_sub, m.from_user.id)
               username = await bot.get_chat(ch_to_sub)
               if m.text == '▶️ Пропустить':
                 black_listch[m.from_user.id].append(ch_to_sub)
               if user.status == 'left':
                 await bot.send_message(m.from_user.id, "Задание получено.", reply_markup = bot_skip())
                 await m.reply(subscribe_channel, reply=False, parse_mode='html', reply_markup = EarnMenu().chanel_chk(username.username, str(chlist[ch_to_sub])))
                 await StorageEarn.channels_skip.set()
                 break
               else:
                 black_listch[m.from_user.id].append(ch_to_sub)
             except:
               black_listch[m.from_user.id].append(ch_to_sub)
           else:
             creater = await edit_ch_status(chlist[ch_to_sub], 0, "channels")
             try:
               await bot.send_message(creater['id'], channel_delete_bot(f'@{creater["name"]}', creater["sum"]), disable_web_page_preview=True)
             except:
               pass
       else:
         await m.reply(no_channels, reply=False, parse_mode='html', reply_markup = earn_menu())
         break
    else:
      await m.reply(pleaseentered, reply=False, parse_mode='html', reply_markup = EarnMenu().chanel_main())
	
@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, regexp="^👤 Группы\s.+$", state="*")
@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, text='▶️ Пропустить', state=StorageEarn.groups_skip)
async def earn_groups(m: types.Message, state: FSMContext):
    await state.finish()
    ch1, ch2 = await bot.get_chat_member(chan1, m.from_user.id), await bot.get_chat_member(chan2, m.from_user.id)
    try:
      if black_listgr[m.from_user.id] == None:
        black_listgr[m.from_user.id] = []
    except:
      black_listgr[m.from_user.id] = []
    if ch1.status != "left" and ch2.status != "left":
      while True:
       grlist = await for_subscribe("groups")
       if len(grlist) >= 1:
           good_groups = {}
           for x in grlist:
            if len(eval(x[3])) < x[4]:
              if m.from_user.id not in eval(x[3]) and m.from_user.id != x[5]:
                good_groups[x[1]] = x[0]
              else:
                grlist = 0
            else:
               creator = await edit_ch_status(x[0], 0, "groups")
               try:
                 await bot.send_message(creator['id'], all_is_successfully_gr(x[2], x[4]), parse_mode='html')
               except:
                 pass
               grlist = 0
           if len(good_groups) >= 1:
             grlist = good_groups
           else:
             grlist = 0
       else:
         grlist = 0
       if grlist != 0 and len(grlist) > len(black_listgr[m.from_user.id]):
         gr_to_sub = random.choice(list(grlist))
         if gr_to_sub not in black_listgr[m.from_user.id]:
           try:
             bstatus = await bot.get_chat_member(gr_to_sub, bot_token.split(':')[0])
             bstatus = bstatus.status
           except (Unauthorized, BotBlocked, ChatNotFound):
             bstatus = 'left'
           if bstatus == "administrator":
             try:
               user = await bot.get_chat_member(gr_to_sub, m.from_user.id)
               username = await bot.get_chat(gr_to_sub)
               if m.text == '▶️ Пропустить':
                 black_listgr[m.from_user.id].append(gr_to_sub)
               if user.status == 'left':
                 await bot.send_message(m.from_user.id, "Задание получено.", reply_markup = bot_skip())
                 await m.reply(entered_group, reply=False, parse_mode='html', reply_markup = EarnMenu().group_chk(username.username, str(grlist[gr_to_sub])))
                 await StorageEarn.groups_skip.set()
                 break
               else:
                 black_listgr[m.from_user.id].append(gr_to_sub)
             except:
               black_listgr[m.from_user.id].append(gr_to_sub)
           else:
             creater = await edit_ch_status(grlist[gr_to_sub], 0, "groups")
             try:
               await bot.send_message(creater['id'], group_delete_bot(f'@{creater["name"]}', creater["sum"]), disable_web_page_preview=True)
             except:
               pass
       else:
         await m.reply(no_groups, reply=False, parse_mode='html', reply_markup = earn_menu())
         break
    else:
      await m.reply(pleaseentered, reply=False, parse_mode='html', reply_markup = EarnMenu().chanel_main())

@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, regexp="^🤖 Боты\s.+$", state="*")
@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, text='▶️ Пропустить', state=StorageEarn.bots_skip)
async def earn_bots(m: types.Message, state: FSMContext):
    await state.finish()
    ch1, ch2 = await bot.get_chat_member(chan1, m.from_user.id), await bot.get_chat_member(chan2, m.from_user.id)
    try:
      if black_listbt[m.from_user.id] == None:
        black_listbt[m.from_user.id] = []
    except:
      black_listbt[m.from_user.id] = []
    if ch1.status != "left" and ch2.status != "left":
      while True:
       botlist = await for_subscribe("bots")
       if len(botlist) >= 1:
           good_bots = {}
           for x in botlist:
            if len(eval(x[4])) < x[5]:
              if m.from_user.id not in eval(x[4]) and m.from_user.id != x[6]:
                good_bots[x[1]] = x[0]
              else:
                botlist = 0
            else:
               creator = await edit_ch_status(x[0], 0, "bots") 
               try:
                 await bot.send_message(creator['id'], all_is_successfully_bot(x[2], x[4]), parse_mode='html')
               except:
                 pass
               btlist = 0
           if len(good_bots) >= 1:
             btlist = good_bots
           else:
             btlist = 0		
       else:
         btlist = 0
       if btlist != 0 and len(btlist) > len(black_listbt[m.from_user.id]):
         bt_to_sub = random.choice(list(btlist))
         if bt_to_sub not in black_listbt[m.from_user.id]:
           url = await get_url_bot(btlist[bt_to_sub], m.from_user.id)
           await bot.send_message(m.from_user.id, "Задание получено.", reply_markup = bot_skip())
           await bot.send_message(m.from_user.id, bots_msg, parse_mode='html', reply_markup = EarnMenu().bots(url))
           await StorageEarn.bots_skip.set()
         else:
           await m.reply(no_bots, reply=False, parse_mode='html', reply_markup = earn_menu())
         if m.text == '▶️ Пропустить':
           black_listbt[m.from_user.id].append(bt_to_sub)
         break
       else:
         await m.reply(no_bots, reply=False, parse_mode='html', reply_markup = earn_menu())
         break
    else:
      await m.reply(pleaseentered, reply=False, parse_mode='html', reply_markup = EarnMenu().chanel_main()) 
	
@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), regexp="^👁 Просмотры\s.+$", state="*")
async def earn_views(m: types.Message, state: FSMContext):
    await m.reply(go_views, reply=False, parse_mode='html', reply_markup = EarnMenu().views_ch())
	
@dp.callback_query_handler(IsBan(), IsUsr(), regexp='chchk_', state=StorageEarn.channels_skip)
async def check_user_in_channel(c: types.CallbackQuery):
    number = c.data.replace('chchk_', '')
    info = await promoch_info(number, "channels")
    if c.from_user.id not in eval(info[3]):
      if info[0]:
        try:
          botstatus = await bot.get_chat_member(info[1], bot_token.split(':')[0])
          botstatus = botstatus.status
        except (Unauthorized, BotBlocked, ChatNotFound):
          botstatus = 'left'
        if botstatus == "administrator":
          stusr = await bot.get_chat_member(info[1], c.from_user.id)
          if stusr.status != 'left':
            add_to_subs = await add_user_to_subsch(number, c.from_user.id, "channels")
            if add_to_subs[0]:
              try:
                await bot.delete_message(c.from_user.id, c.message.message_id)
              except:
                pass
              await bot.send_message(c.from_user.id, channel_sub_good(add_to_subs[2]), reply_markup = earn_menu())
              if logch1:
                await bot.send_message(logch1, channel_sub_admmsg(c, add_to_subs[2]), parse_mode='html',  disable_web_page_preview=True)
              else:
                await sendadmins(channel_sub_admmsg(c, add_to_subs[2]))
            else:
              await c.message.edit_text(you_are_later_ch(add_to_subs[2]))
          else:
            await c.answer(you_dont_noch, show_alert=True)
        else:
          creater = await edit_ch_status(number, 0)
          await add_promotion_to_uncheck(number)
          await bot.send_message(creater['id'], channel_delete_bot(f'@{creater["name"]}', creater["sum"]), disable_web_page_preview=True)
      else:
        await c.message.edit_text(you_are_later_ch(info[2]))
    else:
      await c.message.edit_text(you_did_this)
	  
@dp.callback_query_handler(IsBan(), IsUsr(), regexp='grchk_', state=StorageEarn.groups_skip)
async def check_user_in_groups(c: types.CallbackQuery):
    number = c.data.replace('grchk_', '')
    info = await promoch_info(number, "groups")
    if c.from_user.id not in eval(info[3]):
      if info[0]:
        try:
          botstatus = await bot.get_chat_member(info[1], bot_token.split(':')[0])
          botstatus = botstatus.status
        except (Unauthorized, BotBlocked, ChatNotFound):
          botstatus = 'left'
        if botstatus == "administrator":
          stusr = await bot.get_chat_member(info[1], c.from_user.id)
          if stusr.status != 'left':
            add_to_subs = await add_user_to_subsch(number, c.from_user.id, "groups")
            if add_to_subs[0]:
              try:
                await bot.delete_message(c.from_user.id, c.message.message_id)
              except:
                pass
              await bot.send_message(c.from_user.id, group_sub_good(add_to_subs[2]), reply_markup = earn_menu())
              if logch1:
                await bot.send_message(logch1, group_sub_admmsg(c, add_to_subs[2]), parse_mode = 'html',  disable_web_page_preview=True)
              else:
                await sendadmins(group_sub_admmsg(c, add_to_subs[2]))
            else:
              await c.message.edit_text(you_are_later_gr(add_to_subs[2]))
          else:
            await c.answer(you_dont_nogr, show_alert=True)
        else:
          creater = await edit_ch_status(number, 0)
          await add_promotion_to_uncheck(number)
          await bot.send_message(creater['id'], group_delete_bot(f'@{creater["name"]}', creater["sum"]), disable_web_page_preview=True)
      else:
        await c.message.edit_text(you_are_later_gr(info[2]))
    else:
      await c.message.edit_text(you_did_this)

@dp.callback_query_handler(IsBan(), IsUsr(), regexp='chkview_')
async def check_views(c: types.CallbackQuery):
    number = c.data.replace('chkview_', '')
    info = await for_views(number)
    if info:
      if c.from_user.id not in eval(info[2]):
        if len(eval(info[2])) < info[3]:
          if info[4] != c.from_user.id:
            await views_good_pay(c.from_user.id, int(number))
            await c.answer(views_pay, show_alert=True)
          else:
            await c.answer(no_views_tsk, show_alert=True)
        else:
          await edit_vi_status(number)
          try:
            await bot.send_message(info[4], views_complete(info[3], info[1]), parse_mode='html', disable_web_page_preview=True)
          except:
            pass
          try:
            await bot.delete_message(f'@{viewsch}', info[1])
            await bot.delete_message(f'@{viewsch}', info[1] + 1)
          except:
            await sendadmins(views_completeadm(info[3], info[1], info[4]))
      else:
        await c.answer(views_nopay, show_alert=True)
    else:
      await c.answer(views_del, show_alert=True)
	  
@dp.message_handler(IsBan(), IsUsr(), content_types=['text', 'video', 'photo', 'document', 'animation'], is_forwarded=True, state=StorageEarn.bots_skip)
async def bots_handler(m: types.Message, state: FSMContext):
    data = await udata(m.from_user.id)
    if re.search(r'fwdbot', data):
      number = int(data.replace('fwdbot', ''))
      info = await promoch_info(number, "bots")
      if info[0]:
        if m.forward_from.is_bot:
          if m.from_user.id not in eval(info[3]):
            if m.forward_from.username.lower() == info[2].lower():
              await m.reply(bots_good, reply=False, parse_mode='html', reply_markup = earn_menu())
              await add_user_to_subsch(number, m.from_user.id, "bots")
              await state.finish()
              if logch1:
                await bot.send_message(logch1, bots_admmsg(m, info[2]), parse_mode = 'html',  disable_web_page_preview=True)
              else:
                await sendadmins(bots_admmsg(m, info[2]))
            else:
              await m.reply(bots_ne(info[2]), reply=False, parse_mode='html', reply_markup = bot_skip())
          else:
            await m.reply(you_did_this, reply=False, parse_mode='html', reply_markup = earn_menu())
            await state.finish()
        else:
          await m.reply(bots_ne(info[2]), reply=False, parse_mode='html', reply_markup = bot_skip())
          await state.finish()
      else:
        await state.finish()
    else:
      await state.finish()