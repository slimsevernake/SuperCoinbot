from aiogram.types import Update
from aiogram.utils.exceptions import *
from loader import dp
from utils.logging import get_info, get_error

@dp.errors_handler()
async def errors_handler(update, exception):
    if isinstance(exception, CantDemoteChatCreator):
        get_info(f'{exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageNotModified):
        get_info(f'{exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageCantBeDeleted):
        get_info(f'{exception} \nUpdate: {update}')
        return True
		
    if isinstance(exception, ChatNotFound):
        get_info(f'{exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        get_info(f'{exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        get_info(f'{exception} \nUpdate: {update}')
        return True

    if isinstance(exception, UserDeactivated):
        get_info(f'{exception} \nUpdate: {update}')
        return True

    if isinstance(exception, Unauthorized):
        get_info(f'Unauthorized: {exception}\nUpdate: {update}')
        return True

    if isinstance(exception, InvalidQueryID):
        get_info(f'{exception} \nUpdate: {update}')
        return True

    if isinstance(exception, RetryAfter):
        get_info(f'RetryAfter: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TerminatedByOtherGetUpdates):
        print("You already have an active bot. Turn it off.")
        get_info(f'TerminatedByOtherGetUpdates: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, CantParseEntities):
        get_info(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        get_info(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
		
    if isinstance(exception, MessageIdentifierNotSpecified):
        get_info(f'{exception} \nUpdate: {update}')
        return True
		
    if isinstance(exception, MessageToReplyNotFound):
        get_info(f'{exception} \nUpdate: {update}')
        return True
		
    if isinstance(exception, MessageToEditNotFound):
        get_info(f'{exception} \nUpdate: {update}')
        return True
		
    if isinstance(exception, ObjectExpectedAsReplyMarkup):
        get_info(f'{exception} \nUpdate: {update}')
        return True
		
    if isinstance(exception, InlineKeyboardExpected):
        get_info(f'{exception} \nUpdate: {update}')
        return True
		
    if isinstance(exception, UnavailableMembers):
        get_info(f'{exception} \nUpdate: {update}')
        return True
		
    if isinstance(exception, ResultIdDuplicate):
        get_info(f'{exception} \nUpdate: {update}')
        return True
		
    if isinstance(exception, MethodIsNotAvailable):
        get_info(f'{exception} \nUpdate: {update}')
        return True
		
    if isinstance(exception, CantGetUpdates):
        get_info(f'{exception} \nUpdate: {update}')
        return True
		
    if isinstance(exception, BotKicked):
        get_info(f'{exception} \nUpdate: {update}')
        return True
		
    if isinstance(exception, NetworkError):
        get_info(f'{exception} \nUpdate: {update}')
        return True
		
    if isinstance(exception, RestartingTelegram):
        get_info(f'{exception} \nUpdate: {update}')
        return True
		
    if isinstance(exception, TimeoutWarning):
        get_info(f'{exception} \nUpdate: {update}')
        return True

    get_error(f'Update: {update} \n{exception}')
