from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from data.config import ref_pays, ref_pays2, refmsgprice, logch
from filters import IsPrivate, IsBan, IsUsr
from keyboards.default import main_default, main_menu
from keyboards.inline import ReferalMenu
from loader import dp, bot
from states.states import StorageReferal
from utils.messages import referals, refmessage, sethello, hellomsgbad, chhello, sethello_admmsg
from utils.sqlite import reftop, get_user, add_advbal, set_hello, clear_firstname
from utils.other import sendadmins

@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, text="👥  Рефералы", state="*")
async def refrals_menu(m: types.Message, state: FSMContext):
    u = await get_user(m.from_user.id)
    await m.reply(referals(u), reply=False, parse_mode='html', disable_web_page_preview=True, reply_markup = ReferalMenu().referal_main())
	
@dp.callback_query_handler(IsBan(), text='reftop')
async def referals_top(c: CallbackQuery):
    txt = 'Топ рефоводов:\n\n'
    i = 0
    v = await reftop(c.from_user.id)
    for x in v:
      i = i + 1
      txt += f'{i}) <a href="tg://user?id={x[1]}">{x[3]}</a> - <b>{x[22]}</b> реф.\n'
    await c.message.edit_text(txt)
	
@dp.callback_query_handler(IsBan(), IsUsr(), text='hellomsg')
async def ref_message(c: CallbackQuery):
    u = await get_user(c.from_user.id)
    if u['refmsg']  == '0':
      await c.message.edit_text(f'{refmessage}\n💳 Стоимость: <b>{refmsgprice} SuperCoin</b>\n<i>📝 После покупки этой функции Вы сможете изменять приветсвенное сообщение в любое время</i>', parse_mode='html', reply_markup = ReferalMenu().ref_msg_bt(0))
    else:
      await c.message.edit_text(f'{refmessage}\n✅ <b>Функция оплачена!</b>\n🗒 <b>Текущий текст:</b>\n{u["refmsg"]}', parse_mode='html', reply_markup = ReferalMenu().ref_msg_bt(1))
	  
@dp.callback_query_handler(IsBan(), IsUsr(), text='buy_hello_msg')
async def buy_hello_msg(c: CallbackQuery):
    u = await get_user(c.from_user.id)
    if u['advbal'] >= refmsgprice:
      try:
        await bot.delete_message(c.from_user.id, c.message.message_id)
      except:
        pass
      await bot.send_message(c.from_user.id, sethello, parse_mode='html', reply_markup = main_default)
      await add_advbal(c.from_user.id, -refmsgprice)
      await set_hello("1", c.from_user.id)
      await StorageReferal.hello_msg_txt.set()
      if logch:
        await bot.send_message(logch, sethello_admmsg(c.from_user.id, clear_firstname(c.from_user.first_name)), parse_mode='html')
      else:
        await sendadmins(sethello_admmsg(c.from_user.id, c.from_user.first_name))
    else:
      await c.message.edit_text(hellomsgbad, parse_mode='html')
	  
@dp.callback_query_handler(IsBan(), IsUsr(), text='edit_hello_msg')
async def edit_hello_msg(c: CallbackQuery):
    u = await get_user(c.from_user.id)
    if u['refmsg']  != '0':
      try:
        await bot.delete_message(c.from_user.id, c.message.message_id)
      except:
        pass
      await bot.send_message(c.from_user.id, sethello, parse_mode='html', reply_markup = main_default)
      await StorageReferal.hello_msg_txt.set()
    else:
      await c.message.edit_text("Функция отключена.", parse_mode='html')
	  
@dp.message_handler(IsBan(), IsUsr(), state=StorageReferal.hello_msg_txt)
async def set_msg_txt(m: types.Message, state: FSMContext):
    if m.text != '0':
      await set_hello(m.text, m.from_user.id)
      await m.reply(chhello, parse_mode='html', reply=False, reply_markup = main_menu(m.from_user.id))
      await state.finish()
    else:
      await m.reply("Введите любой текст кроме 0:", reply=False, reply_markup = main_default)