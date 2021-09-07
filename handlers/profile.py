import time
import datetime
import re
import random
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from data.config import admins, kurs, depflood, minpayou, logch, ref_depbonus
from filters import IsPrivate, IsBan, IsUsr
from keyboards.default import main_default, main_menu
from keyboards.inline import ProfileMenu
from loader import dp, bot
from states.states import StorageProfile
from utils.messages import myprofile, depositmenu, qiwi_text, no_history_dep, depositbad, amdmsg, depositflood, buycoin, manualadd, walletmsg, payoutmsg, nocoins, payout_msg, payout_admmsg, payout_menu, exchangemsg, exchangemsgbadmin, exchangegood_admmsg, exchangegood, exchangemsgbad, depgood, depgoodadm, dep_ref_good
from utils.sqlite import get_comment, new_deposit, set_deposit, add_bal, isUser, delete_deposit, setdepflood, get_depflood, new_payout, get_user, add_advbal, add_refearn, clear_firstname
from utils.other import sendadmins, history_pay, history_dep
from utils.qiwi import chk_qiwi

@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, text="👤 Профиль", state="*")
async def show_profile(m: types.Message, state: FSMContext):
    log = await myprofile(m.from_user.id)
    if log[0]:
      await m.reply(log[0], reply=False, parse_mode='html', reply_markup = ProfileMenu().profile_main())
    else:
      await m.reply('Что то пошло не так.', reply=False)
	
@dp.callback_query_handler(IsBan(), IsUsr(), text='dep')
async def handle_dep(c: CallbackQuery):
    await c.message.edit_text(depositmenu, reply_markup = ProfileMenu().profile_deposit())

@dp.callback_query_handler(IsBan(), IsUsr(), text='exchange')
async def exchange(c: CallbackQuery):
    await bot.delete_message(c.from_user.id, c.message.message_id)
    bal = await get_user(c.from_user.id)
    if bal['bal'] >= 1:
      await bot.send_message(c.from_user.id, exchangemsg(bal['bal']), reply_markup = main_default)
      await StorageProfile.exchange.set()
    else:
      await bot.send_message(c.from_user.id, exchangemsgbad, reply_markup = main_menu(c.from_user.id))
	
@dp.callback_query_handler(IsBan(), IsUsr(), text='qiwi_method')
async def qiwi(c: types.CallbackQuery):
    comment = await get_comment(c.from_user.id)
    if comment == None:
      comment = random.randint(1000000000, 9999999999)
      await new_deposit(c.from_user.id, comment)
    await c.message.edit_text(qiwi_text(comment), reply_markup = ProfileMenu().deposit_qiwi(comment), parse_mode="html")
	
@dp.callback_query_handler(IsBan(), IsUsr(), text='history_dep')
async def deposit_history(c: types.CallbackQuery): 
    h = await history_dep(c.from_user.id, "user_id")
    if h:
     await c.message.edit_text(h, parse_mode="html")
    else:
     await c.message.edit_text("Вы еще не пополняли баланс.")
	 
@dp.callback_query_handler(IsBan(), IsUsr(), text='check_qiwi')
async def check_qiwi_deposit(c: types.CallbackQuery):
    if await isUser(c.from_user.id):
      answer, amount, comment, num = await chk_qiwi(c.from_user.id, 20)
      if answer:
        await set_deposit(c.from_user.id, amount, num)
        await add_advbal(c.from_user.id, amount / kurs)
        ref = await get_user(c.from_user.id)
        if ref['ref']:
          await add_bal(ref['ref'], (amount / kurs) * (ref_depbonus / 100))
          await add_refearn(ref['ref'], (amount / kurs) * (ref_depbonus / 100))
          try:
            await bot.send_message(ref['ref'], dep_ref_good(round(((amount / kurs) * (ref_depbonus / 100)), 2)), parse_mode="html")
          except:
            pass
        await c.message.edit_text(depgood(amount, comment), parse_mode="html")
        if logch:
          await bot.send_message(logch, depgoodadm(c, amount, comment), parse_mode="html")
        else:
          await sendadmins(depgoodadm(c, amount, comment))
      else:
        await c.message.edit_text(depositbad, parse_mode="html")

@dp.callback_query_handler(IsBan(), IsUsr(), text='del_deposit')
async def cancel_qiwi_deposit(c: types.CallbackQuery): 
    val = await delete_deposit(c.from_user.id)
    if val:
      text = "Платеж успешно отменён"
    else:
      text = "Платеж не найден"
    await c.message.edit_text(text, parse_mode="html")
		
@dp.callback_query_handler(IsBan(), IsUsr(), text='delete_message')
async def del_button(c: types.CallbackQuery): 
    await bot.delete_message(c.from_user.id, c.message.message_id)
	
@dp.callback_query_handler(IsBan(), IsUsr(), text='manual_dep')
async def manual_deposit_set(c: types.CallbackQuery):
    deptime = await get_depflood(c.from_user.id)
    if deptime < int(time.time()):
     await c.message.edit_text(buycoin)
     await StorageProfile.manual_deposit.set()
     await setdepflood(c.from_user.id, int(time.time()) + depflood)
    else:
     dt = datetime.datetime.fromtimestamp(deptime)
     await c.message.edit_text(depositflood(dt), parse_mode="html")

@dp.callback_query_handler(IsBan(), IsUsr(), text='payout')
async def payout_menu_change(c: types.CallbackQuery):
    await c.message.edit_text(payout_menu, parse_mode="html", reply_markup = ProfileMenu().payout_menu_main())
	 
@dp.callback_query_handler(IsBan(), IsUsr(), text='payoutq')
async def payout_qiwi(c: types.CallbackQuery):
    await c.message.edit_text(walletmsg, parse_mode="html")
    await StorageProfile.qiwi_payout_num.set()
	
@dp.callback_query_handler(IsBan(), IsUsr(), text='payoutshistory')
async def payout_history(c: types.CallbackQuery):
    h = await history_pay(c.from_user.id)
    if h:
     await c.message.edit_text(h, parse_mode="html")
    else:
     await c.message.edit_text("Вы еще не выводили средства.")
	 
@dp.message_handler(IsBan(), IsUsr(), state=StorageProfile.manual_deposit)
async def manual_deposit(m: types.Message, state: FSMContext):
    try:
      sum = int(m.text)
      await m.reply(manualadd(sum), parse_mode="html", reply=False)
      await sendadmins(f'{amdmsg(m)} Хочу пополнить баланс на <b>{sum} Super Coin</b> (<b>{sum * kurs} руб.</b>)')
      await state.finish()
    except ValueError:
      await m.reply('❌ Введите корректную сумму:', reply=False, reply_markup = main_default)
    except:
      await m.reply('❌ Ошибка.', reply=False, reply_markup = main_menu(m.from_user.id))
      await state.finish()
	  
@dp.message_handler(IsBan(), IsUsr(), state=StorageProfile.qiwi_payout_num)
async def qiwi_payout(m: types.Message, state: FSMContext):
    try:
      if re.search(r"(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$", m.text):
        sum = int(m.text)
        bal = await get_user(m.from_user.id)
        await m.reply(payoutmsg(bal['bal']), reply=False)
        async with state.proxy() as data:
          data["qiwi_payout_num"] = m.text
        await StorageProfile.qiwi_payout_sum.set()
      else:
        await m.reply('❌ Введите корректный номер кошелька:', reply=False, reply_markup = main_default)
    except ValueError:
      await m.reply('❌ Введите корректный номер кошелька', reply=False, reply_markup = main_default)
	  
@dp.message_handler(IsBan(), IsUsr(), state=StorageProfile.qiwi_payout_sum)
async def qiwi_payout(m: types.Message, state: FSMContext):
    try:
      sum = int(m.text)
      async with state.proxy() as data:
         num = data["qiwi_payout_num"]
      bal = await get_user(m.from_user.id)
      if bal['bal'] >= sum and sum >= minpayou:
        await new_payout(m.from_user.id, clear_firstname(m.from_user.first_name), sum, num)
        await add_bal(m.from_user.id, -sum)
        await m.reply(payout_msg(round(sum, 2)), parse_mode="html", reply=False, reply_markup = main_menu(m.from_user.id))
        await sendadmins(payout_admmsg(m.from_user.id, clear_firstname(m.from_user.first_name), round(sum, 2)))
        await state.finish()
      else:
        await m.reply(nocoins, reply=False, reply_markup = main_menu(m.from_user.id))
        await state.finish()
    except ValueError:
      await m.reply('❌ Введите коректную сумму:', reply=False, reply_markup = main_default)
	  
@dp.message_handler(IsBan(), IsUsr(), state=StorageProfile.exchange)
async def exchange(m: types.Message, state: FSMContext):
    try:
      sum = int(m.text)
      bal = await get_user(m.from_user.id)
      if bal['bal'] >= sum and sum >= 1:
        await add_bal(m.from_user.id, -sum)
        await add_advbal(m.from_user.id, sum)
        await m.reply(exchangegood(round(sum, 2)), parse_mode="html", reply=False, reply_markup = main_menu(m.from_user.id))
        if logch:
          await bot.send_message(logch, exchangegood_admmsg(m.from_user.id, clear_firstname(m.from_user.first_name), round(sum, 2)), parse_mode="html")
        else:
          await sendadmins(exchangegood_admmsg(m.from_user.id, clear_firstname(m.from_user.first_name), round(sum, 2)))
        await state.finish()
      else:
        await m.reply(exchangemsgbadmin, reply=False, reply_markup = main_menu(m.from_user.id))
        await state.finish()
    except ValueError:
      await m.reply('❌ Введите коректную сумму:', reply=False, reply_markup = main_default)