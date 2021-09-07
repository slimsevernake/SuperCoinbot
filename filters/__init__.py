from aiogram import Dispatcher
from .myfilters import IsPrivate
from .myfilters import IsAdmin
from .myfilters import IsUsr
from .myfilters import IsBan
from .myfilters import IsChat

def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
