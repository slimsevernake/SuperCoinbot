import datetime
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from data.config import logch, vtype, botname, kurs, pays, viewsch
from filters import IsPrivate, IsAdmin, IsUsr
from keyboards.default import main_default, main_menu
from keyboards.inline import AdminMenu
from loader import dp, bot
from states.states import StorageAdmin
from utils.messages import admin_main_msg, vouch_new_msg, masmailing_msg, dep_stat, payout_stat, payoutadm_menu, payouacceptmsg, payoutusrmsg, payoutmsg_ch, skippayout, retpay, myprofile, info_main_msg, info_main_msg1, ban_on, ban_off, select_balmsg, add_bal_adm_msg, add_advbal_adm_msg, add_bal_usr_msg, add_advbal_usr_msg, entered_sum, select_chbalmsg, ch_advbal_adm_msg, ch_bal_adm_msg, taskmgrmainmsg, taskchannelmain, select_ch, subs_stoped
from utils.sqlite import statistika, get_user, add_advbal, add_bal, new_voucher, all_deposits, all_payouts, get_allpays, get_pay, set_payout, set_ban, change_bal, for_subscribe, get_subs_info, stop_adm, get_bots_info, get_allviews, clear_firstname
from utils.other import sendadmins, history_pay, history_dep, is_digit
from utils.qiwi import balance_qiwi

@dp.message_handler(IsUsr(), IsPrivate(), IsAdmin(), is_forwarded=False, text="🔑 Админ-панель", state="*")
async def admin_menu(m: types.Message):
    s = await statistika()
    b = balance_qiwi()
    await m.reply(admin_main_msg(s, b), reply=False, parse_mode='html', reply_markup = AdminMenu().admin_main())

@dp.callback_query_handler(IsUsr(), IsAdmin(), text='task_mgr')
async def task_mgr_main(c: CallbackQuery):
    await c.message.edit_text(taskmgrmainmsg, reply_markup = AdminMenu().task_mgr_menu())
	
@dp.callback_query_handler(IsUsr(), IsAdmin(), text='views_adm')
async def views_mgr_main(c: CallbackQuery):
    h = await get_allviews()
    keyboard = InlineKeyboardMarkup()
    t = ""
    k = "keyboard.add("
    if h:
      for x in h:
        t += f'№{x[0]} https://t.me/{viewsch}/{str(x[1])} - Выполнено: <b>{str(len(eval(x[2])))}</b> из <b>{str(x[3])}</b> раз\n'
        k += f"InlineKeyboardButton(text = f'🚫 {x[0]}', callback_data = f'del_views{x[0]}'), "
      k += ")"
      eval(k)
      keyboard.add(InlineKeyboardButton(text = "❌ Отмена", callback_data = 'cancel'))
      await c.message.edit_text(t, disable_web_page_preview=True, reply_markup = keyboard)
    else:
      await c.message.edit_text('Нет заданий на просмотры')

@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^del_views')
async def group_mgr_select(c: CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    num = c.data.split('del_views')[1]
    log = await stop_adm(num, 'views')
    await bot.send_message(c.from_user.id, subs_stoped, reply_markup = main_menu(c.from_user.id))
    try:
      await bot.delete_message(f'@{viewsch}', log)
      await bot.delete_message(f'@{viewsch}', log + 1)
    except:
      await sendadmins(f'Бот не смог удалить пост https://t.me/{viewsch}/{log}\nУдалить придётся вручную.')
	 
@dp.callback_query_handler(IsUsr(), IsAdmin(), text='cahnnels_adm')
async def channel_mgr_main(c: CallbackQuery):
    log = await for_subscribe('channels')
    keyboard = InlineKeyboardMarkup()
    if log:
      for x in log:
        keyboard.add(InlineKeyboardButton(text = f'{x[2]}', callback_data = f'selectch_adm_{x[0]}'))
      keyboard.add(InlineKeyboardButton(text = "❌ Отмена", callback_data = 'cancel'))
      await c.message.edit_text(taskchannelmain, reply_markup = keyboard)
    else:
      await bot.send_message(c.from_user.id, "Нет активных заданий на подписки")
	
@dp.callback_query_handler(IsUsr(), IsAdmin(), text='bots_adm')
async def bots_mgr_main(c: CallbackQuery):
    log = await for_subscribe('bots')
    keyboard = InlineKeyboardMarkup()
    if log:
      for x in log:
        keyboard.add(InlineKeyboardButton(text = f'{x[2]}', callback_data = f'selectbot_adm_{x[0]}'))
      keyboard.add(InlineKeyboardButton(text = "❌ Отмена", callback_data = 'cancel'))
      await c.message.edit_text(taskchannelmain, reply_markup = keyboard)
    else:
      await bot.send_message(c.from_user.id, "Нет активных заданий на боты")

@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^selectbot_adm_')
async def group_mgr_select(c: CallbackQuery):
    num = c.data.split('selectbot_adm_')[1]
    inf = await get_bots_info(num, 'bots')
    if inf['id']:
      await c.message.edit_text(select_ch(inf, num), reply_markup = AdminMenu().bot_del_adm(num))
    else:
      await c.message.edit_text('Задание не найдено', reply_markup = AdminMenu().admin_main())

@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^botdel_adm_')
async def group_mgr_select(c: CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    num = c.data.split('botdel_adm_')[1]
    await stop_adm(num, 'bots')
    await bot.send_message(c.from_user.id, subs_stoped, reply_markup = main_menu(c.from_user.id))
	  
@dp.callback_query_handler(IsUsr(), IsAdmin(), text='groups_adm')
async def group_mgr_main(c: CallbackQuery):
    log = await for_subscribe('groups')
    keyboard = InlineKeyboardMarkup()
    if log:
      for x in log:
        keyboard.add(InlineKeyboardButton(text = f'{x[2]}', callback_data = f'selectgr_adm_{x[0]}'))
      keyboard.add(InlineKeyboardButton(text = "❌ Отмена", callback_data = 'cancel'))
      await c.message.edit_text(taskchannelmain, reply_markup = keyboard)
    else:
      await bot.send_message(c.from_user.id, "Нет активных заданий на втупление в группы")
	
@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^selectgr_adm_')
async def group_mgr_select(c: CallbackQuery):
    num = c.data.split('selectgr_adm_')[1]
    inf = await get_subs_info(num, 'groups')
    if inf['id']:
      await c.message.edit_text(select_ch(inf, num), reply_markup = AdminMenu().group_del_adm(num))
    else:
      await c.message.edit_text('Задание не найдено', reply_markup = AdminMenu().admin_main())
	  
@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^grdel_adm_')
async def group_mgr_select(c: CallbackQuery):
    await bot.delete_message(c.from_user.id, c.message.message_id)
    num = c.data.split('grdel_adm_')[1]
    await stop_adm(num, 'groups')
    await bot.send_message(c.from_user.id, subs_stoped, reply_markup = main_menu(c.from_user.id))
	
@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^selectch_adm_')
async def channel_mgr_select(c: CallbackQuery):
    num = c.data.split('selectch_adm_')[1]
    inf = await get_subs_info(num, 'channels')
    if inf['id']:
      await c.message.edit_text(select_ch(inf, num), reply_markup = AdminMenu().channel_del_adm(num))
    else:
      await c.message.edit_text('Задание не найдено', reply_markup = AdminMenu().admin_main())
	  
@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^chdel_adm_')
async def channel_mgr_select(c: CallbackQuery):
    await bot.delete_message(c.from_user.id, c.message.message_id)
    num = c.data.split('chdel_adm_')[1]
    await stop_adm(num, 'channels')
    await bot.send_message(c.from_user.id, subs_stoped, reply_markup = main_menu(c.from_user.id))
	
@dp.callback_query_handler(IsUsr(), IsAdmin(), text='payouts')
async def payouts_list_main(c: CallbackQuery):
    kb = InlineKeyboardMarkup()
    list = await get_allpays("В обработке")
    if len(list) >= 1:
      for x in list:
        kb.add(InlineKeyboardButton(text = f'{(x[3]) * kurs}₽ {x[2]}', callback_data = f'selectpay_{x[0]}'))
      kb.add(InlineKeyboardButton(text = '❌ Отмена', callback_data = 'cancel'))
      await c.message.edit_text(f'📬 Заявки на вывод средст\nВсего заявок: {len(list)}', reply_markup = kb)
    else:
      await c.message.edit_text('Нет заявок на вывод средст.', reply_markup = kb)
	  
@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='selectpay_')
async def payouts_select(c: CallbackQuery):
    pa = await get_pay(c.data.split('selectpay_')[1])
    if pa[0]:
      await c.message.edit_text(payoutadm_menu(pa[1][0], pa[1][1], pa[1][2], pa[1][3], pa[1][4], pa[1][5]), parse_mode='html', reply_markup = AdminMenu().selectpay_kb(str(pa[1][0])))
    else:
      await c.message.edit_text('Заявка не найдена')
	  
@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='accpay_')
async def payouts_accept(c: CallbackQuery):
    pa = await get_pay(c.data.split('accpay_')[1])
    if pa[0]:
      await set_payout(pa[1][0], "Подтверждён")
      await c.message.edit_text(payouacceptmsg(pa[1][3], pa[1][5], pa[1][0]), parse_mode='html')
      await bot.send_message(pa[1][1], payoutusrmsg(pa[1][3], pa[1][0]), parse_mode='html')
      await bot.send_message(f'@{pays}', payoutmsg_ch(pa[1]), parse_mode='html')
    else:
      await c.message.edit_text('Заявка не найдена')
	  
@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='cancpay_')
async def payouts_cancel(c: CallbackQuery):
    pa = await get_pay(c.data.split('cancpay_')[1])
    if pa[0]:
      await set_payout(pa[1][0], "Отклонён")
      await c.message.edit_text(skippayout(pa[1][3], pa[1][0]), parse_mode='html')
      await bot.send_message(pa[1][1], skippayout(pa[1][3], pa[1][0]), parse_mode='html')
    else:
      await c.message.edit_text('Заявка не найдена')

@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='info_adm')
async def information(c: CallbackQuery):
    await bot.delete_message(c.from_user.id, c.message.message_id)
    await StorageAdmin.info.set()
    await bot.send_message(c.from_user.id, info_main_msg, reply_markup = main_default)

	  
@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='backpay_')
async def payouts_back(c: CallbackQuery):
    pa = await get_pay(c.data.split('backpay_')[1])
    if pa[0]:
      await set_payout(pa[1][0], "Возврат")
      await add_bal(c.from_user.id, pa[1][3])
      await c.message.edit_text(retpay(pa[1][3], pa[1][0]), parse_mode='html')
      await bot.send_message(pa[1][1], retpay(pa[1][3], pa[1][0]), parse_mode='html')
    else:
      await c.message.edit_text('Заявка не найдена')
	
@dp.callback_query_handler(IsUsr(), IsAdmin(), text='payslist_adm')
async def payouts_main(c: CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    s = await all_payouts()
    txt = payout_stat(s)
    for x in s[0]:
      dt = datetime.datetime.fromtimestamp(x[4])
      txt += f'<a href="tg://user?id={x[1]}">{x[1]}</a>|<i>{dt}</i>|<b>{x[3]}SC</b>\n'
    txt += 'Для подробной информации введите ID:'
    await bot.send_message(c.from_user.id, txt, parse_mode='html', reply_markup = main_default)
    await StorageAdmin.payout_history.set()
	
@dp.callback_query_handler(IsUsr(), IsAdmin(), text='dep_adm')
async def deposit_main(c: CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    s = await all_deposits()
    txt = dep_stat(s)
    for x in s[0]:
      dt = datetime.datetime.fromtimestamp(x[2])
      txt += f'<a href="tg://user?id={x[0]}">{x[0]}</a>|<i>{dt}</i>|<b>{x[3]}₽</b>\n'
    txt += 'Для посика платежа введите ID или квитанцию вместе с <b>+</b>:\nНапример:\n1715232225\n+0123456789'
    await bot.send_message(c.from_user.id, txt, parse_mode='html', reply_markup = main_default)
    await StorageAdmin.dep_histroy.set()
	
@dp.callback_query_handler(IsUsr(), IsAdmin(), text='vaucher_adm')
async def vaucher_new(c: CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    await bot.send_message(c.from_user.id, vouch_new_msg, reply_markup = main_default)
    await StorageAdmin.voucher_new.set()
	
@dp.callback_query_handler(IsUsr(), IsAdmin(), text='masmailing')
async def masmailing_new(c: CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    await bot.send_message(c.from_user.id, masmailing_msg, reply_markup = main_default)
    await StorageAdmin.masmailing.set()

@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^selectbalch_')
async def select_chbal(c: CallbackQuery, state: FSMContext):
    id = c.data.split('selectbalch_')[1]
    await c.message.edit_text(select_chbalmsg, reply_markup = AdminMenu().selectchbal_kb(id))

@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^chbal_')
async def chbal_user(c: CallbackQuery, state: FSMContext):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    id = c.data.split('chbal_')[1]
    async with state.proxy() as data:
      data["idchbal"] = id
    await bot.send_message(c.from_user.id, entered_sum, reply_markup = main_default)
    await StorageAdmin.chbal.set()
	
@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^chadv_')
async def chadv_user(c: CallbackQuery, state: FSMContext):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    id = c.data.split('chadv_')[1]
    async with state.proxy() as data:
      data["idchadv"] = id
    await bot.send_message(c.from_user.id, entered_sum, reply_markup = main_default)
    await StorageAdmin.chadv.set()
	
@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^selectbaladd_')
async def select_addbal(c: CallbackQuery, state: FSMContext):
    id = c.data.split('selectbaladd_')[1]
    await c.message.edit_text(select_balmsg, reply_markup = AdminMenu().selectbal_kb(id))

@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^addbal_')
async def addbal_user(c: CallbackQuery, state: FSMContext):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    id = c.data.split('addbal_')[1]
    async with state.proxy() as data:
      data["idaddbal"] = id
    await bot.send_message(c.from_user.id, entered_sum, reply_markup = main_default)
    await StorageAdmin.addbal.set()

@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^addadv_')
async def addbal_user(c: CallbackQuery, state: FSMContext):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    id = c.data.split('addadv_')[1]
    async with state.proxy() as data:
      data["idaddadv"] = id
    await bot.send_message(c.from_user.id, entered_sum, reply_markup = main_default)
    await StorageAdmin.addadv.set()
	
@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^ban_')
async def ban_user(c: CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    id = c.data.split('ban_')[1]
    await set_ban(id, 1)
    await bot.send_message(c.message.chat.id, ban_on(id))
	
@dp.callback_query_handler(IsUsr(), IsAdmin(), regexp='^unban_')
async def uban_user(c: CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    id = c.data.split('unban_')[1]
    await set_ban(id, 0)
    await bot.send_message(c.message.chat.id, ban_off(id))

@dp.message_handler(IsUsr(), IsAdmin(), is_forwarded=False, state=StorageAdmin.chbal)
async def chbal_user_finish(m: types.Message, state: FSMContext):
    try:
      async with state.proxy() as data:
        id = data["idchbal"]
      sum = int(m.text)
      await change_bal(id, sum, 'balance')
      await state.finish()
      await sendadmins(ch_bal_adm_msg(id, sum))
    except ValueError:
      await m.reply('Введите число:', reply=False, reply_markup = main_default)
	  
@dp.message_handler(IsUsr(), IsAdmin(), is_forwarded=False, state=StorageAdmin.chadv)
async def chadv_user_finish(m: types.Message, state: FSMContext):
    try:
      async with state.proxy() as data:
        id = data["idchadv"]
      sum = int(m.text)
      await change_bal(id, sum, 'adv_balance')
      await state.finish()
      await sendadmins(ch_advbal_adm_msg(id, sum))
    except ValueError:
      await m.reply('Введите число:', reply=False, reply_markup = main_default)
	
@dp.message_handler(IsUsr(), IsAdmin(), is_forwarded=False, state=StorageAdmin.addadv)
async def addbal_user_finish(m: types.Message, state: FSMContext):
    try:
      async with state.proxy() as data:
        id = data["idaddadv"]
      sum = int(m.text)
      await add_advbal(id, sum)
      await state.finish()
      await sendadmins(add_advbal_adm_msg(id, sum))
      try:
        await bot.send_message(id, add_advbal_usr_msg(sum), parse_mode='html')
      except:
        pass
    except ValueError:
      await m.reply('Введите число:', reply=False, reply_markup = main_default)
	
@dp.message_handler(IsUsr(), IsAdmin(), is_forwarded=False, state=StorageAdmin.addbal)
async def addbal_user_finish(m: types.Message, state: FSMContext):
    try:
      async with state.proxy() as data:
        id = data["idaddbal"]
      sum = int(m.text)
      await add_bal(id, sum)
      await state.finish()
      await sendadmins(add_bal_adm_msg(id, sum))
      try:
        await bot.send_message(id, add_bal_usr_msg(sum), parse_mode='html')
      except:
        pass
    except ValueError:
      await m.reply('Введите число:', reply=False, reply_markup = main_default)
	
@dp.message_handler(IsUsr(), IsAdmin(), is_forwarded=False, state=StorageAdmin.info)
async def info_main(m: types.Message, state: FSMContext):
    log = await myprofile(m.text)
    if log[0]:
      await state.finish()
      await m.reply(log[0], reply=False, parse_mode='html', reply_markup = AdminMenu().info_kb(str(log[2]), log[1]))
    else:
      await m.reply(info_main_msg1, reply=False, reply_markup = main_default)
	  
@dp.message_handler(IsUsr(), IsAdmin(), is_forwarded=False, state=StorageAdmin.payout_history)
async def payout_finish(m: types.Message, state: FSMContext):
    try:
      txt = int(m.text)
      txt = await history_pay(txt)
      await state.finish()
      await m.reply(txt, reply=False, parse_mode='html', reply_markup = main_menu(m.from_user.id))
    except ValueError:
      await m.reply('❌ Введите цифру:', reply=False, reply_markup = main_default)
	
@dp.message_handler(IsUsr(), IsAdmin(), is_forwarded=False, state=StorageAdmin.dep_histroy)
async def deposit_finish(m: types.Message, state: FSMContext):
    try:
      if m.text.startswith("+"):
        txt = int(m.text.split("+")[1])
        txt = await history_dep(txt, 'comment')
        await state.finish()
        await m.reply(txt, reply=False, parse_mode='html', reply_markup = main_menu(m.from_user.id))
      else:
        txt = int(m.text)
        txt = await history_dep(txt, 'user_id')
        await state.finish()
        await m.reply(txt, reply=False, parse_mode='html', reply_markup = main_menu(m.from_user.id))
    except ValueError:
      await m.reply('❌ Введите цифру:', reply=False, reply_markup = main_default)
	
@dp.message_handler(IsUsr(), IsAdmin(), is_forwarded=False, state=StorageAdmin.voucher_new)
async def vaucher_finish(m: types.Message):
    if is_digit(m.text):
      text = eval(m.text)
      id = await new_voucher(text, m.from_user.id, clear_firstname(m.from_user.first_name))
      if vtype:
        await m.reply(f'Чек на сумму <b>{abs(round(text, 2))} Super Coin</b>', parse_mode='html', reply=False, reply_markup = AdminMenu().voucher_kb(id))
      else:
        await m.reply(f'Чек на сумму <b>{abs(round(text, 2))} Super Coin</b>\nhttps://t.me/{botname}?start={id}', parse_mode='html', reply=False, disable_web_page_preview=True)
    else:
      await m.reply('❌ Введите цифру:', reply=False, reply_markup = main_default)