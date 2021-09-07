from aiogram.dispatcher.filters import BoundFilter
from data.config import admins, chatbot
from aiogram import types
from utils.sqlite import get_user, isUser


class IsPrivate(BoundFilter):
    async def check(self, m: types.Message):
        return m.chat.type == types.ChatType.PRIVATE


class IsAdmin(BoundFilter):
    async def check(self, m: types.Message):
        if m.from_user.id in admins:
            return True
        else:
            return False

class IsBan(BoundFilter):
    async def check(self, m: types.Message):
        if (await get_user(m.from_user.id))['ban']:
            return False
        else:
            return True
			
class IsUsr(BoundFilter):
    async def check(self, m: types.Message):
        if await isUser(m.from_user.id):
            return True
        else:
            return False
			
class IsChat(BoundFilter):
    async def check(self, m: types.Message):
        if m.chat.type == 'supergroup':
          if m.chat.username == chatbot:
            return True
          else:
            return False
        return False