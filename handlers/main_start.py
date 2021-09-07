import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data.config import admins, logch, logch2
from loader import dp, bot
from filters import IsPrivate, IsBan
from keyboards.default import main_menu
from utils.sqlite import isUser, newuser, act_voucher, get_user, get_voucher, isBan, clear_firstname
from utils.other import sendadmins
from utils.messages import new_ref, new_ref2, startmsg, voucher_good, voucher_admmsg, voucher_nan, voucher_bad, updatemsg, ref_admmsg, ref_admmsg2

@dp.message_handler(IsBan(), IsPrivate(), text="⬅ На главную", state="*")
async def main_menu_handler(m: types.Message, state: FSMContext):
     await state.finish()
     await m.reply("Главное меню.", reply=False, reply_markup = main_menu(m.from_user.id))
	 
@dp.message_handler(IsBan(), IsPrivate(), commands = ['start'], state="*")
async def bot_start(m: types.Message, state: FSMContext):
     await state.finish()
     argument = m.get_args()
     if await isUser(m.from_user.id) == 0:
         if (argument is not None) and (argument.isdigit() == True) and (await isUser(argument)) == 1:
             u = await get_user(argument)
             if u['ref']:
               await newuser(m.from_user.id, m.from_user.first_name, m.from_user.username, argument, u['ref'])
               await m.reply(startmsg(), reply=False, parse_mode='html', reply_markup = main_menu(m.from_user.id), disable_web_page_preview=True)
               if u['refmsg'] != '0':
                 await bot.send_message(m.from_user.id, u['refmsg'])
               await bot.send_message(argument, new_ref(argument, m.from_user.id, clear_firstname(m.from_user.first_name)), parse_mode='html')
               await bot.send_message(u['ref'], new_ref2(argument, m.from_user.id, clear_firstname(m.from_user.first_name)), parse_mode='html')
               if logch2:
                 await bot.send_message(logch2, ref_admmsg(m.from_user.id, clear_firstname(m.from_user.first_name), argument), parse_mode='html')
                 await bot.send_message(logch2, ref_admmsg2(m.from_user.id, clear_firstname(m.from_user.first_name), u['ref']), parse_mode='html')
               else:
                 await sendadmins(ref_admmsg(m.from_user.id, clear_firstname(m.from_user.first_name), argument))
                 await sendadmins(ref_admmsg2(m.from_user.id, clear_firstname(m.from_user.first_name), u['ref']))
             else:
               await newuser(m.from_user.id, m.from_user.first_name, m.from_user.username, argument, 0)
               await m.reply(startmsg(), reply=False, parse_mode='html', disable_web_page_preview=True, reply_markup = main_menu(m.from_user.id))
               if u['refmsg'] != '0':
                 await bot.send_message(m.from_user.id, u['refmsg'])
               await bot.send_message(argument, new_ref(argument, m.from_user.id, clear_firstname(m.from_user.first_name)), parse_mode='html')
               if logch2:
                 await bot.send_message(logch2, ref_admmsg(m.from_user.id, clear_firstname(m.from_user.first_name), argument), parse_mode='html')
               else:
                 await sendadmins(ref_admmsg(m.from_user.id, clear_firstname(m.from_user.first_name), argument))
         else:
             await newuser(m.from_user.id, m.from_user.first_name, m.from_user.username, 0, 0)
             await m.reply(startmsg(), reply=False, parse_mode='html', disable_web_page_preview=True, reply_markup = main_menu(m.from_user.id))
     elif (len(argument) > 2) and (argument.isdigit() == False):
         v = await get_voucher(argument)
         if v:
          if v[3] == 1:
           bal = await act_voucher(argument, m.from_user.id, v[2])
           await m.reply(voucher_good(m.from_user.id, clear_firstname(m.from_user.first_name), v[2], datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")), reply = False, parse_mode='html', reply_markup = main_menu(m.from_user.id))
           if logch:
            await bot.send_message(logch, voucher_admmsg(m.from_user.id, clear_firstname(m.from_user.first_name), v[2], datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), datetime.datetime.fromtimestamp(v[4]), v[6], v[7], bal), parse_mode='html')
           else:
            await sendadmins(voucher_admmsg(m.from_user.id, clear_firstname(m.from_user.first_name), v[2], datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), datetime.datetime.fromtimestamp(v[4])), v[6], v[7], bal)
          elif v[3] == 0:
           await m.reply(voucher_bad, reply=False, parse_mode='html', reply_markup = main_menu(m.from_user.id))
         else:
           await m.reply(voucher_nan, reply=False, parse_mode='html', reply_markup = main_menu(m.from_user.id))
     else:
         await m.reply(updatemsg, reply=False, parse_mode='html', reply_markup = main_menu(m.from_user.id))
