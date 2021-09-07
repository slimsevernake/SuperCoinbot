from aiogram.types import ReplyKeyboardMarkup
from data.config import admins, channels_pay, groups_pay, views_pay, bots_pay, channelsprice, groupsprice, viewsprice, botsprice

def main_menu(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if user_id in admins:
      keyboard.add('💰 Заработать Super Coin', '📢 Продвинуть')
      keyboard.add('👤 Профиль', '👥  Рефералы')
      keyboard.add('🎁 Бонус', '💬 Информация')
      keyboard.add('🔑 Админ-панель')
    else:
      keyboard.add('💰 Заработать Super Coin', '📢 Продвинуть')
      keyboard.add('👤 Профиль', '👥  Рефералы')
      keyboard.add('🎁 Бонус', '💬 Информация')
    return keyboard
	
def earn_menu():
      keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
      keyboard.add(f'📢 Каналы {round(channels_pay, 2)} SC', f'👤 Группы {round(groups_pay, 2)} SC')
      keyboard.add(f'🤖 Боты {round(bots_pay, 2)} SC', f'👁 Просмотры {round(views_pay, 2)} SC')
      keyboard.add('⬅ На главную')
      return keyboard
	
def promo_menu():
      keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
      keyboard.add(f'👁 Просмотры', f'📢 Каналы')
      keyboard.add(f'👥 Группы', f'🤖 Задания на ботов')
      keyboard.add('⬅ На главную')
      return keyboard

def bot_skip():
      keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
      keyboard.add('▶️ Пропустить')
      keyboard.add('⬅ На главную')
      return keyboard
	  
main_default = ReplyKeyboardMarkup(resize_keyboard=True)
main_default.row("⬅ На главную")