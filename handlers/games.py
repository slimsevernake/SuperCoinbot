import asyncio
import random
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from filters import IsPrivate, IsBan, IsUsr
from keyboards.inline import GameMenu
from keyboards.default import main_menu, main_default
from states.states import StorageGame
from loader import dp, bot
from utils.messages import game_menu, send_cube, cube_lost, cube_win, cube_non, game_nomoney, slot_lost, slot_jack, slot_win, send_slot, bonus_good, bonus_bad, ref_ver, ref_ver2, cubeentersum
from utils.sqlite import add_bal, get_user, get_bonus, clear_firstname
from data.config import game_cube_price, game_slot_price, game_slot_win, game_slot_jack, bonus_day

@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, text="🎁 Бонус", state="*")
async def games_menu(m: types.Message):
    await m.reply(game_menu, reply=False, parse_mode='html', reply_markup = GameMenu().game_menu())
	
@dp.callback_query_handler(IsBan(), IsUsr(), text='game_cube')
async def cude_msg(c: CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    await bot.send_message(c.from_user.id, cubeentersum)
    await StorageGame.cube.set()
	  
@dp.callback_query_handler(IsBan(), IsUsr(), text='game_slot')
async def slot_msg(c: CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    u = await get_user(c.from_user.id)
    if u['bal'] >= game_slot_price:
      await bot.send_message(c.from_user.id, send_slot)
      data = await bot.send_dice(chat_id = c.from_user.id, emoji = '🎰')
      await asyncio.sleep(3)
      data = data['dice']['value']
      win = [64, 43, 22, 1]
      win1 = [2, 3, 4, 21, 23, 24, 41, 42, 44, 61, 62, 63]
      if data in win1:
        await add_bal(c.from_user.id, game_slot_win)
        await bot.send_message(c.from_user.id, slot_win(clear_firstname(c.from_user.first_name)))
      elif data in win:
        await add_bal(c.from_user.id, game_slot_jack)
        await bot.send_message(c.from_user.id, slot_jack(clear_firstname(c.from_user.first_name)))
      else:
        await add_bal(c.from_user.id, -game_slot_price)
        await bot.send_message(c.from_user.id, slot_lost(clear_firstname(c.from_user.first_name)))
    else:
      await bot.send_message(c.from_user.id, game_nomoney(u, game_slot_price), parse_mode='html', reply_markup = main_menu(c.from_user.id))
	  
@dp.callback_query_handler(IsBan(), IsUsr(), text='bonus')
async def bonus_msg(c: CallbackQuery):
    try:
      await bot.delete_message(c.from_user.id, c.message.message_id)
    except:
      pass
    st = bonus_day.split('-')[0]
    en = bonus_day.split('-')[1]
    bonus = random.uniform(float(st),float(en))
    log = await get_bonus(c.from_user.id, round(bonus, 2))
    if log[0]:
      await bot.send_message(c.from_user.id, bonus_good(round(bonus, 2)), parse_mode='html')
      if log[1]:
        try:
          await bot.send_message(log[1], ref_ver, parse_mode='html')
        except:
          pass
      if log[2]:
        try:
          await bot.send_message(log[2], ref_ver2, parse_mode='html')
        except:
          pass
    else:
      await bot.send_message(c.from_user.id, bonus_bad)
	  
@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, state=StorageGame.cube)
async def games_cube_final(m: types.Message, state: FSMContext):
    try:
      stavka = round(int(m.text), 2)
      u = await get_user(m.from_user.id)
      await state.finish()
      if u['bal'] >= stavka:
        await bot.send_message(m.from_user.id, send_cube(stavka))
        user_data = await bot.send_dice(m.from_user.id)
        user_data = user_data['dice']['value']
        await bot.send_chat_action(m.from_user.id, action = 'typing')
        await asyncio.sleep(5)
        await bot.send_message(m.from_user.id, f'Бросает бот.', reply_markup = main_menu(m.from_user.id))
        bot_data = await bot.send_dice(m.from_user.id)
        bot_data = bot_data['dice']['value']
        await asyncio.sleep(5)
        if bot_data > user_data:
          await add_bal(m.from_user.id, -stavka)
          await bot.send_message(m.from_user.id, cube_lost(clear_firstname(m.from_user.first_name), stavka))
        elif bot_data < user_data:
          await add_bal(m.from_user.id, stavka)
          await bot.send_message(m.from_user.id, cube_win(clear_firstname(m.from_user.first_name), stavka))
        else:
          await bot.send_message(m.from_user.id, cube_non(clear_firstname(m.from_user.first_name)))
      else:
        await bot.send_message(m.from_user.id, game_nomoney(u, stavka), parse_mode='html', reply_markup = main_menu(m.from_user.id))
    except ValueError:
      await m.reply('❌ Введите цифру:', reply=False, reply_markup = main_default)
	