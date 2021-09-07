import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.states import StorageAdmin
from data.config import mmtime
from filters import IsUsr, IsAdmin
from loader import dp, bot
from utils.sqlite import get_user_mm

@dp.message_handler(IsUsr(), IsAdmin(), content_types=['text', 'photo'], state=StorageAdmin.masmailing)
async def send_mail(m: types.Message, state: FSMContext):
    await state.finish()
    try:
      users = await get_user_mm()
      val = await bot.send_message(m.from_user.id, 'Рассылка запущена.', parse_mode='html')
      txt = ""
      if m.content_type == 'text':
        all_users = len(users)
        good = 0
        blocked = 0
        for x in users:
          try:
            await bot.send_message(x[0], m.html_text, parse_mode='html')
            good += 1
            txt += f'✅ <a href="tg://user?id={x[0]}">{x[1]}</a> получил сообщение\n'
            await asyncio.sleep(mmtime)
          except:
            blocked += 1
            txt += f'❌ <a href="tg://user?id={x[0]}">{x[1]}</a> получил сообщение\n'
          if (good + blocked) % 10 == 0:
            await bot.edit_message_text(chat_id = m.chat.id, message_id = val.message_id, text = txt, parse_mode='html')
            txt = ""
      elif m.content_type == 'photo':
        all_users = len(users)
        good = 0
        blocked = 0
        for x in users:
          try:
            try:
              await bot.send_photo(x[0], photo = m.photo[0].file_id, caption = m.html_text, parse_mode='html')
            except:
              await bot.send_photo(x[0], photo = m.photo[0].file_id, parse_mode='html')
            txt += f'✅ <a href="tg://user?id={x[0]}">{x[1]}</a> получил сообщение\n'
            good += 1
            await asyncio.sleep(mmtime)
          except:
            blocked += 1
            txt += f'❌ <a href="tg://user?id={x[0]}">{x[1]}</a> получил сообщение\n'
          if (good + blocked) % 10 == 0:
            await bot.edit_message_text(chat_id = m.chat.id, message_id = val.message_id, text = txt, parse_mode='html')
            txt = ""
      await bot.edit_message_text(chat_id = m.chat.id, message_id = val.message_id, text = f'📊 Статистика:\n🌪 Всего: <b>{all_users}</b>\n✅ Успешно: <b>{good}</b>\n❌ Бот заблокали: <b>{blocked}</b>', parse_mode='html')
    except Exception as e:
      await bot.send_message(m.from_user.id, e)