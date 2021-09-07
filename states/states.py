from aiogram.dispatcher.filters.state import State, StatesGroup

class StorageProfile(StatesGroup):
    manual_deposit = State()
    exchange = State()
    qiwi_payout_sum = State()
    qiwi_payout_num = State()

class StorageReferal(StatesGroup):
    hello_msg_txt = State()
	
class StorageEarn(StatesGroup):
    bots_skip = State()
    groups_skip = State()
    channels_skip = State()
	
class StoragePromo(StatesGroup):
    views_add = State()
    views_fwd = State()
    channel_add = State()
    channel_add1 = State()
    group_add = State()
    group_add1 = State()
    bot_add = State()
    bot_add1 = State()
	
class StorageGame(StatesGroup):
    cube = State()
	
class StorageAdmin(StatesGroup):
    voucher_new = State()
    masmailing = State()
    dep_histroy = State()
    payout_history = State()
    info = State()
    addbal = State()
    addadv = State()
    chbal = State()
    chadv = State()