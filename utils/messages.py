import time
import math
import datetime
from data.config import *
from utils.sqlite import get_user, get_num_vouch, get_sum_dep, get_sum_pay, get_sum_vouch, clear_firstname

updatemsg = 'Главное меню'
voucher_nan = '😞 Чек не найден.'
voucher_bad = 'Походу вы не успели и чек превратился в 🎃 🎃 🎃'
banmsg = f'🖕 Вы не можете использовать бот.\nПишите админу @{admin}'
send_slot = f'Вы дёрнули рычаг.\nСтавка: {game_slot_price} Super Coin.\nВыигрыш: {game_slot_win} Super Coin.\nДжекпот: {game_slot_jack} Super Coin.'
walletmsg = '💰 Введите номер кошелька:'
no_history_dep = 'Вы еще не пополняли баланс.'
nocoins = '"Не достаточно Super Coin или сумма вывода меньше минимальной."'
buycoin = f'1 Super Coin = {kurs} руб. укажиите сколько Super Coin вы хотите купить:'
refmessage = f'✉️ <b>Приветственное сообщение</b> - уникальная функция нашего бота. Это сообщение получают все Ваши рефералы при входе в бот. Вы можете мотивировать их активность или разместить любую рекламу.'
sethello = '📝 Введите текст приветствия реферала:'
chhello = 'Текст приветсвия изменён.'
hellomsgbad = '❗️ Недостаточно средств на рекламном балансе!'
info = '🌪 Полезная информация о боте.'
depositmenu = 'Выберите способ поплнения:'
depositbad = '<b>❌Платёж не найден</b>\nПопоробуйте позже.'
payout_menu = f'Минимальная сумма вывода {minpayou} Super Coin.'
exchangemsgbad = 'Не достаточно средст на основном балансе, мимнимальная сумма обмена 1 SuperCoin'
exchangemsgbadmin = 'Не достаточно средст на основном балансе или сумма меньше 1 SuperCoin\nВведите корректную сумму:'
pleaseentered = 'Для работы с ботом подпишитесь на ⤵️'
subscribe_channel = 'Подпишитесь на этот канал:\n1️⃣ Перейдите на канал 👇, подпишитесь ✔️ и пролистайте ленту вверх 🔝👁 (5-10 постов).\n2️⃣ Возвращайтесь⚡️сюда, чтобы получить вознаграждение.\n⚠️ Запрещено отписываться от каналов, иначе Вы можете быть оштрафованы!'
entered_group = '📝 <b>Вступите</b> в группу, затем вернитесь в бот и получите <b>вознаграждение</b>!\n\n⚠️ Запрещено выходить из групп, иначе Вы можете быть оштрафованы!'
no_channels = f'😔 Пока нет каналов для подписки. Но скоро будут!!\n\n{no_msg}'
no_groups = f'😔 Пока нет групп для вступления. Но скоро будут!!\n\n{no_msg}'
no_bots = f'😔 Пока нет ботов для переходов. Но скоро будут!!\n\n{no_msg}'
you_did_this = 'Вы уже выполняли это задание.'
not_allowed = '🖕 Выкуси приятель, меня не наебешь !'
bots_msg = '📝 <b>Перейдите в бота</b>, затем <b>перешлите</b> любое сообщение от него и получите <b>вознаграждение</b>!\n\n⚠️ Запрещено блокировать ботов, иначе Вы можете быть оштрафованы!\n\n<b>Перешлите любое сообщения от бота:</b>'
bots_good = f'💰 Вам начислено <b>{bots_pay}</b> Super Coin за переход в бота!'
go_views = 'Заработок на просмотре постов.'
you_dont_noch = '😡 Вы ещё не подписались на этот канал !'
you_dont_nogr = '😡 Вы ещё не вступили в данную группу !'
ch_add_msg = '📝 Введите количество подписчиков:'
bot_add_msg = '📝 Введите количество переходов:'
views_msg = '📝 Введите количество просмотров:'
subs_bad = '😳 Недостаточно Super Coin!'
views_bad1 = f'Минимальный заказ {minviews} 📢\nВведите правильную цифру:'
views_bt_txt = 'Для получения Super Coin дави кнопку ⤵️'
views_nopay = 'Вы уже просматривали этот пост!'
views_pay = f'Вам начислено {views_pay} Super Coin за просмотр сообщения!'
views_del = 'Задание недоступно !'
subs_stoped = 'Заказ отменен.'
channel_bad = f'Минимальный заказ подписчиков {minmembs} 👁\nВведите правильную цифру:'
channel_notbot = 'Бот не добавлен в канал.'
channel_errortype = 'Это не канал.'
channel_bot_not_adm = 'Бот не добавлен в админы канала.'
group_notbot = 'Бот не добавлен в группу.'
group_errortype = 'Это не публичная группа.'
group_bot_not_adm = 'Бот не добавлен в админы группы.'
group_bad = f'Минимальный заказ участников {minmembs} 👁\nВведите правильную цифру:'
bot_bad = f'Минимальный заказ переходов {minmembs} 👁\nВведите правильную цифру:'
channel_bad1 = '❌ Такой канал уже на продвижении! Дождитесь пока оно окончится, а потом попробуйте ещё раз.\nДобавьте другой канал или отмените действие:'
group_bad1 = '❌ Такой чат уже на продвижении! Дождитесь пока оно окончится, а потом попробуйте ещё раз.\nДобавьте другой чат или отмените действие:'
game_menu = 'Во что будем играть ?'
cubeentersum = 'Введите сумму ставки:'
no_views_tsk = '😎 Я не стану платить за задание которое вы сами создали.'
bonus_bad = 'Вы уже получали ежедневный бонус, ждём вас завтра.'
ref_ver = f'Ваш реферал первого уровня получил бонус вы получили {ref_pays} Super Coin'
ref_ver2 = f'Ваш реферал второго уровня получил бонус вы получили {ref_pays2} Super Coin'
vouch_new_msg = 'Введите сумму чека или вернитесь назад:'
masmailing_msg = '🖋 Отправьте текст или фото для рассылки:'
info_main_msg = 'Введите ID или @username пользователя:'
info_main_msg1 = 'Пользователь не найден\nВведите ID или @username:'
select_balmsg = 'Выберите баланс зачисления:'
select_chbalmsg = 'Выберите баланс для изменения:'
entered_sum = 'Введите сумму:'
taskmgrmainmsg = '🎯 Выберите тип заданий:'
taskchannelmain = 'Список заданий'

def ch_bal_adm_msg(id, sum):
    message = f'💰 Основной баланс пользователя <a href="tg://user?id={id}">{id}</a> изменён на <b>{round(sum, 2)}</b> Super Coin'
    return message
	
def ch_advbal_adm_msg(id, sum):
    message = f'💳 Рекламный баланс пользователя <a href="tg://user?id={id}">{id}</a> изменён на <b>{round(sum, 2)}</b> Super Coin'
    return message

def add_bal_usr_msg(sum):
    message = f'💰 Ваш основной баланс пополнен вручную на сумму <b>{round(sum, 2)}</b> Super Coin'
    return message

def add_advbal_usr_msg(sum):
    message = f'💳 Ваш рекламный баланс пополнен вручную на сумму <b>{round(sum, 2)}</b> Super Coin'
    return message
	
def add_bal_adm_msg(id, sum):
    message = f'💰 Основной баланс пользователя <a href="tg://user?id={id}">{id}</a> пополнен вручную на сумму <b>{round(sum, 2)}</b> Super Coin'
    return message
	
def add_advbal_adm_msg(id, sum):
    message = f'💳 Рекламный баланс пользователя <a href="tg://user?id={id}">{id}</a> пополнен вручную на сумму <b>{round(sum, 2)}</b> Super Coin'
    return message

def admin_main_msg(u, b):
    message = f'<b>Юзеров всего:</b> {u["u"]}\n<b>Юзеров сегодня:</b> {u["td"]}\n<b>Баланс QIWI:</b> {b}₽'
    return message

def bonus_good(s):
    message = f'Вы получили свой ежедневный бонус в размере <b>{s} Super Coin</b>'
    return message

def game_nomoney(u, stavka):
    message = f'Не достаточно Super Coin\nСтавка: {stavka} Super Coin\nБаланс: {round(u["bal"], 2)} Super Coin'
    return message

def cube_non(name):
    message = f'{name}, произошла ничья.)'
    return message

def cube_win(name, stavka):
    message = f'{name} выиграл(а) {stavka} Super Coin!'
    return message
	
def cube_lost(name, stavka):
    message = f'{name} проиграл(а) {stavka} Super Coin!'
    return message

def send_cube(stavka):
    message = f'Вы бросили кости.\nСтавка: {stavka} Super Coin.'
    return message
	
def slot_win(name):
    message = f'{name} выиграл(а) {game_slot_win} Super Coin!'
    return message
	
def slot_jack(name):
    message = f'{name} сорвал(а) джекпот {game_slot_jack} Super Coin'
    return message
	
def slot_lost(name):
    message = f'{name} проиграл(а) {game_slot_price} Super Coin!'
    return message
	
def channel_add_good(num):
    message = f'✅ <b>Канал добавлен на продвижение !</b>\n\n💸 С Вашего рекламного баланса списано <b>{round(num * channelsprice, 2)}</b>'
    return message
	
def group_add_good(num):
    message = f'✅ <b>Группа добавлена на продвижение !</b>\n\n💸 С Вашего рекламного баланса списано <b>{round(num * channelsprice, 2)}</b>'
    return message

def channel_add_msg(num):
    message = f'<b>{num}</b> подписчиков по <b>{channelsprice}</b> Super Coin =<b> {math.floor(num) * channelsprice}</b> Super Coin\n💬 Для запуска задания <b>добавьте</b> нашего бота @{botname} <b>в администраторы</b> Вашего канала, а затем <b>перешлите любое сообщение</b> из этого канала или напишите @username/ссылку на канал\n<i>Не удаляйте бота из админов до завершения заказа иначе заказ будет удалён</i>'
    return message
	
def group_add_msg(num):
    message = f'<b>{num}</b> участников по <b>{groupsprice}</b> Super Coin =<b> {math.floor(num) * groupsprice}</b> Super Coin\n💬 Для запуска задания <b>добавьте</b> нашего бота @{botname} <b>в администраторы</b> Вашего канала, а затем отправьте @username или ссылку на группу\n<i>Не удаляйте бота из админов до завершения заказа иначе заказ будет удалён</i>'
    return message
	
def bt_add_msg(num):
    message = f'<b>{num}</b> переходов по <b>{botsprice}</b> Super Coin =<b> {math.floor(num) * botsprice}</b> Super Coin\n💬 Для запуска задания отправьте ссылку на бот (реферальная разрешена), который нуждается в продвижении:'
    return message

def bot_good_msg(num):
    message = f'✅ <b>Бот добавлен!</b>\n💸 С Вашего баланса списано <b>{round(num * botsprice, 2)}</b> Super Coin'
    return message
	
def new_views_task(num):
    message = f'✅ <b>Новое задание.</b>\n👁 {num} просмотров.'
    return message
	
def new_groups_task(ch, num):
    message = f'✅ <b>Новое задание. {num} вступлений в</b><i> <a href="https://t.me/{ch.username}">{ch.title}</a></i>'
    return message
	
def new_channels_task(ch, num):
    message = f'✅ <b>Новое задание. {num} подписок на</b><i> <a href="https://t.me/{ch.username}">{ch.title}</a></i>'
    return message
	
def new_bots_task(num):
    message = f'✅ <b>Новое задание.</b> {num} переходов в бот.'
    return message

def new_bots_task_adm(c, vi):
    message = f'<a href="tg://user?id={c.from_user.id}">{clear_firstname(c.from_user.first_name)}</a> ID: <code>{c.from_user.id}</code>\nСоздал(а) заказ на <b>{vi}</b> переходов в бот\n<i>{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</i>'
    return message
	
def new_views_task_adm(c, num, vi):
    message = f'<a href="tg://user?id={c.from_user.id}">{clear_firstname(c.from_user.first_name)}</a> ID: <code>{c.from_user.id}</code>\nСоздал(а) заказ <b>№{num}</b> на {vi} просмотров\n<i>{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</i>'
    return message

def ban_on(id):
    message = f'Пользователь <a href="tg://user?id={id}">{id}</a> получил бан внутри бота'
    return message
	
def ban_off(id):
    message = f'Пользователь <a href="tg://user?id={id}">{id}</a> разбанен в боте'
    return message

def new_groups_task_adm(c, vi, name):
    message = f'<a href="tg://user?id={c.from_user.id}">{clear_firstname(c.from_user.first_name)}</a> ID: <code>{c.from_user.id}</code>\nСоздал(а) заказ {vi} вступлений в @{name}\n<i>{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</i>'
    return message
	
def new_channels_task_adm(c, vi, name):
    message = f'<a href="tg://user?id={c.from_user.id}">{clear_firstname(c.from_user.first_name)}</a> ID: <code>{c.from_user.id}</code>\nСоздал(а) заказ {vi} подписок на @{name}\n<i>{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</i>'
    return message
	
def stop_subs_usr(c, type, num, sum):
    message = f'<a href="tg://user?id={c.from_user.id}">{clear_firstname(c.from_user.first_name)}</a> ID: <code>{c.from_user.id}</code>\nОтменил(а) заказ <b>№{num}</b>\n{type}\nБыло возвращено: <b>{sum}</b> Super Coin\n<i>{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</i>'
    return message

def views_complete(vi, mid):
    message = f'✅ Ваш заказ на {vi} просмотров поста https://t.me/{viewsch}/{mid} выполнен!\nПост будет удален с канала просмотров.'
    return message
	
def views_completeadm(vi, mid, cr):
    message = f'✅ Заказ пользлователя <a href="tg://user?id={cr}">{cr}</a> на {vi} просмотров поста https://t.me/{viewsch}/{mid} выполнен!\nНеобходимо удалить пост вручную.'
    return message

def views_add_good(num):
    message = f'✅ <b>Пост добавлен!</b>\nС Вашего рекламного баланса списано <b>{round(num * viewsprice, 2)}</b> Super Coin'
    return message

def add_view_msg(num):
    message = f'<b>{math.floor(num)}</b> просмотров по <b>{viewsprice}</b> Super Coin <b>= {math.floor(num) * viewsprice}</b> Super Coin\n💬 Для запуска задания <b>перешлите пост</b>, который нуждается в продвижении:'
    return message

def startmsg():
    if startmoney:
      message = f'🙋‍♂ Добро пожаловать. Перед началом использования бота, обязательно прочитай небольшую инструкцию по использованию бота, а также правила {rules}\n<b>Вы получили бонус за регистрацию в размере {startmoney} Super Coin</b>'
    else:
      message = f'🙋‍♂ Добро пожаловать. Перед началом использования бота, обязательно прочитай небольшую инструкцию по использованию бота, а также правила {rules}'
    return message

def views_main_msg(u, task):
    message = \
 f'<b>Накрутка просмотров на пост</b>\n' \
 f'👁 1 просмотр = <b>{viewsprice}</b> Super Coin\n' \
 f'💳 Рекламный баланс: <b>{math.floor(u["advbal"])}</b> Super Coin\n' \
 f'📊 Его хватит на <b>{math.floor(u["advbal"] / viewsprice)} </b>просмотров\n' \
 f'⏱ Активных заказов: <b>{task}</b>\n'
    return message

def bots_main_msg(u, task):
    message = \
 f'<b>Накрутка переходов в бот</b>\n' \
 f'👁 1 переход = <b>{botsprice}</b> Super Coin\n' \
 f'💳 Рекламный баланс: <b>{math.floor(u["advbal"])}</b> Super Coin\n' \
 f'📊 Его хватит на <b>{math.floor(u["advbal"] / botsprice)} </b>переходов\n' \
 f'⏱ Активных заказов: <b>{task}</b>\n'
    return message
	
def channels_main_msg(u, task):
    message = \
 f'<b>Накрутка подписчиков на канал</b>\n' \
 f'👤 1 подписчик = <b>{channelsprice}</b> Super Coin\n' \
 f'💳 Рекламный баланс: <b>{math.floor(u["advbal"])}</b> Super Coin\n' \
 f'📊 Его хватит на <b>{math.floor(u["advbal"] / channelsprice)} </b>подписчиков\n' \
 f'⏱ Активных заказов: <b>{task}</b>\n' \
 f'❗️ <i>Наш бот</i> @{botname} <i>должен быть администратором продвигаемого канала</i>'
    return message
	
def groups_main_msg(u, task):
    message = \
 f'<b>Накрутка участников чата</b>\n' \
 f'👤 1 участник = <b>{groupsprice}</b> Super Coin\n' \
 f'💳 Рекламный баланс: <b>{math.floor(u["advbal"])}</b> Super Coin\n' \
 f'📊 Его хватит на <b>{math.floor(u["advbal"] / groupsprice)} </b>подписчиков\n' \
 f'⏱ Активных заказов: <b>{task}</b>\n' \
 f'❗️ <i>Наш бот</i> @{botname} <i>должен быть администратором продвигаемой группы</i>'
    return message

def select_ch(inf, num):
    message = f'Номер задания: <b>№{num}</b>\nID: {inf["id"]}\nЮзернейм: @{inf["name"]}\nВсего: <b>{inf["memb"]}</b>\nВыполненно: <b>{inf["count"]}</b>\nID создателя: <code>{inf["cid"]}</code>\nСоздатель: <a href="tg://user?id={inf["cid"]}">{inf["cn"]}</a>'
    return message
	
def select_bt(inf, num):
    message = f'Номер задания: <b>№{num}</b>\nРЕФ ID: {inf["id"]}\nЮзернейм: @{inf["name"]}\nВсего: <b>{inf["memb"]}</b>\nВыполненно: <b>{inf["count"]}</b>\nID создателя: <code>{inf["cid"]}</code>\nСоздатель: <a href="tg://user?id={inf["cid"]}">{inf["cn"]}</a>'
    return message
	
def promo(bal):
    message = f'📨 <b>Давай выберим тип продвижения:</b>\n💳 Рекламный баланс: <b>{round(bal, 2)}</b> Super Coin'
    return message

def bots_ne(name):
    message = f'Необходимо переслать сообщение именно из бота @{name}'
    return message

def fine(username):
    message = f'😡 Вы отписались от @{username} раньше чем через {sub_term} дней!\nВ качестве штрафа с вашего баланса снято {unsub} Super Coin 💠.'
    return message
	
def warnfine(username):
    message = f'⚠️ Вы отписались от @{username} раньше чем через {sub_term} дней!\nНемедленно подпишитесь иначе будете оштрафованы.'
    return message

def sethello_admmsg(id, name):
    message = f'✉️ Выполнена покупка функции приветственное сообщение.\nПользователь <a href="tg://user?id={id}">{name}</a>\nID: <code>{id}</code>'
    return message
	
def exchangemsg(bal):
    message = f'Обмен основного баланса на рекламный.\nОсновной баланс: <b>{round(bal, 2)}</b> SuperCoin\nВведите сумму для обмена:'
    return message
	
def exchangegood(sum):
    message = f'Вы успешно обменяли {sum} SuperCoin'
    return message
	
def exchangegood_admmsg(id, name, sum):
    message = f'♻️ Произведен обмен <b>{round(sum, 2)} Super Coin</b>\nПользователь <a href="tg://user?id={id}">{name}</a>\nID: <code>{id}</code>'
    return message
	
def new_ref(argument, id, name):
    message = f'🥳 Поздравляем, у вас новый реферал первого уровня!\nВы получите {round(ref_pays, 2)} Super Coin после того как он получит бонус <a href="tg://user?id={id}">{name}</a>'
    return message
    
def new_ref2(argument, id, name):
    message = f'🥳 Поздравляем, у вас новый реферал второго уровня!\nВы получите {round(ref_pays2, 2)} Super Coin после того как он получит бонус <a href="tg://user?id={id}">{name}</a>'
    return message
	
def ref_admmsg(id, name, ref):
    message = f'👥 Новый реферал <a href="tg://user?id={id}">{name}</a>\nID: <code>{id}</code>\nУ пользователя <a href="tg://user?id={ref}">{ref}</a>'
    return message

def ref_admmsg2(id, name, ref):
    message = f'👥 Новый реферал второго уровня <a href="tg://user?id={id}">{name}</a>\nID: <code>{id}</code>\nУ пользователя <a href="tg://user?id={ref}">{ref}</a>'
    return message
	
def depgood(amount, comment):
    message = f"<b>✅Баланс успешно пополнен на {round((amount / kurs), 2)} Super Coin</b>\n📃 Квитанция: <code>+{comment}</code>"
    return message
	
def dep_ref_good(amount):
    message = f"<b>✅Баланс успешно пополнен на {round(amount, 2)} Super Coin за пополнение реферала.</b>"
    return message
	
def depgoodadm(c, amount, com):
    message = f'💰 Пользователь <a href="tg://user?id={c.from_user.id}">{clear_firstname(c.from_user.first_name)}</a>\nID: <code>{c.from_user.id}</code>\n✅ Успешно провел платёж на сумму <b>{round(amount, 2)}₽</b>, баланс пополнен на <b>{round(amount / kurs, 2)} Super Coin</b>\n📃 Квитанция: +{com}'
    return message

def depositflood(dt):
    message = f'Заявку на ручное пополнение можно подавать только после\n{dt}'
    return message

def voucher_good(id, name, sum, date):
    message = f'<b><a href="tg://user?id={id}">{name}</a></b>, чек на <b>{sum} Super Coin</b> активирован\n🕜 <i>{date}</i>'
    return message
	
def voucher_admmsg(id, name, sum, date, cdate, cr, crn, bal):
    message = f'✅ <a href="tg://user?id={id}">{name}</a> <code>{id}</code>\n🧾 Сумма: <b>{sum} SC</b>\n💰 Баланс: {round(bal, 2)} SC\nСоздал: <a href="tg://user?id={cr}">{crn}</a>\n<b>Создан:</b>\n<i>{cdate}</i>\n<b>Активрован:</b>\n<i>{date}</i>'
    return message

def payout_msg(sum):
    message = f'📤 Заявка на вывод {sum} Super Coin успешно создана, ожидайте обработки.'
    return message

def payout_admmsg(id, name, sum):
    message = f'📤 Новая заявка на вывод средст <b>{sum} Super Coin</b> (<b>{sum * kurs} руб.</b>)\nПользователь <a href="tg://user?id={id}">{name}</a>\nID: <code>{id}</code>'
    return message
	
def payoutadm_menu(num, id, name, sum, time, w):
    dt = datetime.datetime.fromtimestamp(time)
    message = f'📤 Заявка №{num}\nID: <code>{id}</code>\nИмя: <a href="tg://user?id={id}">{name}</a>\nСумма: <b>{round(sum * kurs, 2)}₽ </b>\nКошелёк: <code>{w}</code>'
    return message

def payouacceptmsg(sum, w, n):
    message = f'✅ Заявка <b>№{n}</b> подтверждена, необходимо выполнить перевод в размере <b>{round(sum * kurs, 2)}₽</b> на кошелёк <code>{w}</code>'
    return message
	
def payoutusrmsg(sum, n):
    message = f'✅ Заявка <b>№{n}</b> на <b>{round(sum * kurs, 2)}₽</b> была одобрена администрацией проекта.'
    return message
	
def skippayout(sum, n):
    message = f'🛑 Заявка <b>№{n}</b> на вывод <b>{round(sum, 2)} Sub Coin</b> была отклонена.'
    return message

def retpay(sum, n):
    message = f'⚠️ Заявка <b>№{n}</b>. <b>{round(sum, 2)} Sub Coin</b> возвращено на баланс.'
    return message
	
def payoutmsg_ch(pa):
    message = f'<a href="tg://user?id={pa[1]}">{pa[2]}</a> вывел <b>{round(pa[3], 2)} Super Coin</b> (<b>{round(pa[3] * kurs, 2)}₽</b>)'
    return message
	
def payoutmsg(bal):
    message = f'💰 Баланс: <b>{round(bal, 2)}</b> Super Coin <b>{round(bal * kurs, 2)}₽</b>\n1 Super Coin = {kurs} руб. укажиите сколько Super Coin вы хотите вывести:'
    return message
	
def amdmsg(m):
    message = f'Сообщение от <a href="tg://user?id={m.from_user.id}">{clear_firstname(m.from_user.first_name)}</a> ID: <code>{m.from_user.id}</code>\n'
    return message

def manualadd(sum):
    message = f'📥 Заявка отправлена, скоро с вами саяжется администратор.\nСумма оплаты составит <b>{sum * kurs} руб.</b>'
    return message

def referals(u):
    message = f'<b>1 уровень:</b>\n<b>{ref_pays} SuperCoin</b> за регистрацию\n<b>{ref_workbonus}%</b> от заработка\n<b>{ref_depbonus}%</b> от пополнений рекламного баланса\n<b>2 уровень:</b>\n<b>{ref_pays2} SuperCoin</b> за регистрацию\n🔗 <b>Ваша партнёрская ссылка:</b>\nhttps://t.me/{botname}?start={u["id"]}\n1️⃣ Уровень: <b>{u["refcount"]} - {round(u["refearn"], 2)} SuperCoin</b>\n2️⃣ Уровень: <b>{u["refcount2"]} - {round(u["refearn2"], 2)} SuperCoin</b>'
    return message

def dep_stat(s):
    message = \
 f'<b>Статистика депозитов:</b>\n' \
 f'<b>Всего пополнений:</b> {s[5]} на {s[1]}₽\n' \
 f'<b>Пополнений за сегодня:</b> {s[6]} на {s[2]}₽\n' \
 f'<b>Пополнений за эту неделю:</b> {s[7]} на {s[3]}₽\n' \
 f'<b>Пополнений за этот месяц:</b> {s[8]} на {s[4]}₽\n' \
 f'<b>Последние 30 пополнений:</b>\n' \
 f'<b>ID|Дата|Сумма</b>\n'
    return message
	
def payout_stat(s):
    message = \
 f'<b>Статистика выплат:</b>\n' \
 f'<b>Всего выплачено:</b> {s[5]} на {s[1] or 0}SC\n' \
 f'<b>Выплат за сегодня:</b> {s[6]} на {s[2] or 0}SC\n' \
 f'<b>Выплат за эту неделю:</b> {s[7]} на {s[3] or 0}SC\n' \
 f'<b>Выплат за этот месяц:</b> {s[8]} на {s[4] or 0}SC\n' \
 f'<b>Последние 30 выплат:</b>\n' \
 f'<b>ID|Дата|Сумма</b>\n'
    return message
	
def statistikamsg(val):
    message = \
 f'📊 <b>Статистика нашего бота:</b>\n' \
 f'📟 <b>Дата старта:</b> {startdata}\n' \
 f'⚡️ <b>Всего пользователей:</b> {val["u"]}\n' \
 f'🐾 <b>Новых за сегодня:</b> {val["td"]}\n' \
 f'👁 <b>Всего просмотров:</b> {val["v"]}\n' \
 f'👤 <b>Подписались (Канал):</b> {val["c"]}\n' \
 f'👥 <b>Подписались (Группа):</b> {val["g"]}\n' \
 f'🤖 <b>Всего переходов:</b> {val["b"]}\n' \
 f'🎯 <b>Каналов на продвижении:</b> {val["ch"]}\n' \
 f'👤 <b>Групп на продвижении</b>: {val["gr"]}\n' \
 f'🎬 <b>Постов на продвижении:</b> {val["vi"]}\n' \
 f'🤖 <b>Ботов на продвижении</b>: {val["bot"]}\n'
    return message
	
def earnavlidmsg(earn):
    message = \
 f'<b>Для вас доступно: </b>\n'\
 f'📢 <b>Подписок на канал:</b> {earn["ch"]}\n'\
 f'👁 <b>Просмотров постов:</b> {earn["vi"]}\n'\
 f'🤖 <b>Переходов в бот:</b> {earn["bot"]}\n'\
 f'👤 <b>Вступлений в группу:</b> {earn["gr"]}'
    return message
  
def all_is_successfully(name, num):
    message = f'✅ Ваш заказ на: {num} подписчиков на {name} полностью выполнен!'
    return message

def all_is_successfully_gr(name, num):
    message = f'✅ Ваш заказ на: {num} вступлений в группу {name} полностью выполнен!'
    return message
	
def all_is_successfully_bot(name, num):
    message = f'✅ Ваш заказ на: {num} переходов в бот {name} полностью выполнен!'
    return message
	
def channel_delete_bot(id, sum):
    message =f'❗️Вам экстренное сообщение.\n\nБыло обнаружено, что бот был удален из канала: {id}\n😡 В качестве штрафа за нарушение правил {rules}, продвижение канала остановлено и только половина из неиспользованных для продвижения этого канала Super Coin, возвращены вам на баланс.\nПроверка юзеров на отписку также остановлена.\n<b>{round(sum, 2)}</b> SuperCoin было возвращено вам на рекламный баланс.'
    return message	
	
def group_delete_bot(id, sum):
    message =f'❗️Вам экстренное сообщение.\n\nБыло обнаружено, что бот был удален из группы: {id}\n😡 В качестве штрафа за нарушение правил {rules}, продвижение группы остановлено и только половина из неиспользованных для продвижения этой группы Super Coin, возвращены вам на баланс.\nПроверка юзеров на отписку также остановлена.\n<b>{round(sum, 2)}</b> SuperCoin было возвращено вам на рекламный баланс.'
    return message	

def group_delete_bot(id, sum):
    message =f'❗️Вам экстренное сообщение.\n\nБыло обнаружено, что бот был удален из группы: {id}\n😡 В качестве штрафа за нарушение правил {rules}, продвижение группы остановлено и только половина из неиспользованных для продвижения этого канала Super Coin, возвращены вам на баланс.\nПроверка юзеров на отписку также остановлена.\n<b>{round(sum, 2)}</b> SuperCoin было возвращено вам на рекламный баланс.'
    return message	

def admin_finemsg(id, ch):
    message = f'Пользователь <a href="tg://user?id={id}">{id}</a>\nПолучил штраф за отписку от @{ch}\n<i>{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</i>'
    return message
	
def channel_sub_good(username):
    message = f'👍 Вы успешно подписались на канал: @{username}\nВам на баланс начислено {round(channels_pay, 2)} Super Coin 💠.'
    return message
	
def group_sub_good(username):
    message = f'👍 Вы успешно вступили в группы: @{username}\nВам на баланс начислено {round(channels_pay)} Super Coin 💠.'
    return message

def channel_sub_admmsg(c, username):
    message = f'<a href="tg://user?id={c.from_user.id}">{clear_firstname(c.from_user.first_name)}</a> ID: <code>{c.from_user.id}</code>\nСовершил(а) подписку на канал <a href="https://t.me/{username}">{username}</a>\n<i>{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</i>'
    return message
	
def group_sub_admmsg(c, username):
    message = f'<a href="tg://user?id={c.from_user.id}">{clear_firstname(c.from_user.first_name)}</a> ID: <code>{c.from_user.id}</code>\nСовершил(а) вступление в группу <a href="https://t.me/{username}">{username}</a>\n<i>{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</i>'
    return message

def bots_admmsg(c, username):
    message = f'<a href="tg://user?id={c.from_user.id}">{clear_firstname(c.from_user.first_name)}</a> ID: <code>{c.from_user.id}</code>\nСовершил(а) переход в бот <a href="https://t.me/{username}">{username}</a>\n<i>{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</i>'
    return message
	
def you_are_later_ch(username):
    message = f'☹️ Вы не успели подписаться на канал, прежде чем его продвижение окончилось.\nМожете отписаться от этого канала: @{username}'
    return message
	
def you_are_later_gr(username):
    message = f'☹️ Вы не успели вступить в группу, прежде чем ее продвижение окончилось.\nМожете покинуть группу: @{username}'
    return message

def qiwi_text(comment):
 	text = \
 f"Пополнение через Qiwi\nОтправьте любую сумму на реквизиты:\n"\
 f"➖➖➖➖➖➖➖➖\n"\
 f" Номер: {qnum}\n"\
 f" Комментарий: <code>{comment}</code>\n"\
 f"➖➖➖➖➖➖➖➖\n\n"\
 f"🏦 Курс: <b>1</b> Super Coin <b>{1 * kurs}₽</b>\n"\
 f"💳 Для пополнения через карту нажмите кнопку оплатить.\n"\
 f"⚠️ Внимательно проверяйте комментарий к платежу, в случае ошибки деньги не придут.\n"
 	return text
	
async def myprofile(m):
    u = await get_user(m)
    if u['id']:
      message = \
 f'🕜 Дней в боте: <b>{math.floor((int(time.time()) - u["date"]) / 86400)}</b>\n' \
 f'🆔 Ваш ID: <code>{u["id"]}</code>\n' \
 f'👤 Имя: <a href="tg://user?id={u["id"]}">{u["name"]}</a>\n' \
 f'😎 Юзернейм: <b>@{u["uname"] or "Не задано"}</b>\n' \
 f'👥 Ваш наставник: <a href="tg://user?id={u["ref"]}">{(await get_user(u["ref"]))["name"] or "Нету"}</a>\n' \
 f'👥 Наставник наставника: <a href="tg://user?id={u["ref2"]}">{(await get_user(u["ref2"]))["name"] or "Нету"}</a>\n' \
 f'1️⃣ Рефералов 1 уровень: <b>{u["refcount"]}</b>\n' \
 f'2️⃣ Рефералов 2 уровень: <b>{u["refcount2"]}</b>\n' \
 f'👥 Подписок на канал: <b>{u["subs"]}</b>\n' \
 f'👁 Просмотров постов: <b>{u["views"]}</b>\n' \
 f'🤖 Переходов в боты: <b>{u["bots"]}</b>\n' \
 f'👤 Вступлений в группы: <b>{u["groups"]}</b>\n' \
 f'🧾 Активировано чеков: <b>{await get_num_vouch(u["id"])}</b>\n' \
 f'📢 Потрачено на рекламу: <b>{u["advspend"]} Super Coin</b>\n' \
 f'👤 Заработано с рефералов: <b>{round((u["refearn"] + u["refearn2"]), 2)} Super Coin</b>\n' \
 f'🤥 Штрафы: <b>{round(u["fine"], 2)}</b> Super Coin\n' \
 f'➕ Дополнительные зачисления: <b>{round(u["addbal"], 2)} Super Coin</b>\n' \
 f'🧾 С чеков: <b>{await get_sum_vouch(u["id"])} Super Coin</b>\n' \
 f'📥 Пополнено всего: <b>{round(await get_sum_dep(u["id"]), 2)}₽</b>\n' \
 f'📤 Выведено всего: <b>{round(await get_sum_pay(u["id"]), 2)} Super Coin</b>\n' \
 f'🏦 Курс: <b>1</b> Super Coin <b>{kurs}₽</b>\n' \
 f'💰 Основной баланс: <b>{round(u["bal"], 2)}</b> Super Coin <b>{round((u["bal"] * kurs), 2)}₽</b>\n' \
 f'💳 Рекламный баланс: <b>{round(u["advbal"], 2)} Super Coin</b>' 
      return message, u['ban'], u['id']
    else:
      return False, False, False
