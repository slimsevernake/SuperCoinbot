from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from filters import IsPrivate, IsBan, IsUsr
from keyboards.inline import InfoMenu
from loader import dp, bot
from utils.messages import info, statistikamsg
from utils.sqlite import statistika

@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, text="💬 Информация", state="*")
async def information_menu(m: types.Message, state: FSMContext):
    await m.reply(info, reply=False, parse_mode='html', reply_markup = InfoMenu().info_main())
	
@dp.callback_query_handler(IsBan(), IsUsr(), text='statistika')
async def statistika_msg(c: CallbackQuery):
    val = await statistika()
    await c.message.edit_text(statistikamsg(val), parse_mode='html')
	