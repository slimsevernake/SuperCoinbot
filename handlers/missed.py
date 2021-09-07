from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageCantBeDeleted
from loader import dp, bot
from filters import IsPrivate
from utils.messages import banmsg
from utils.sqlite import isBan

@dp.callback_query_handler(text="...", state="*")
async def processing_missed_callback(call: CallbackQuery, state: FSMContext):
      await call.answer(cache_time=60)

@dp.callback_query_handler(state="*")
async def processing_missed_callback(call: CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except MessageCantBeDeleted:
        pass
    if await isBan(call.from_user.id):
        await bot.send_message(call.from_user.id, "❌ <b>Нет ответа.\n</b> Введите /start")
    else:
        await bot.send_message(call.from_user.id, banmsg, parse_mode='html')

@dp.message_handler(IsPrivate())
async def processing_missed_messages(message: types.Message):
    if await isBan(message.from_user.id):
      await message.answer("❌ <b>Комманда не найдена.</b>\nВведите /start")
    else:
      await message.reply(banmsg, reply = False, parse_mode='html')
