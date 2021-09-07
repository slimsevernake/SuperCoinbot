import datetime
import random
import time
import aiosqlite
from data.config import ref_pays, ref_pays2, views_pay, channels_pay, groups_pay, bots_pay, viewsprice, botsprice, channelsprice, groupsprice, ref_workbonus, unsub, intervall, startmoney, maxtask, voucherlen, sub_term
genids = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
path_to_db = "data/data.db"

def get_mondey():
    today = datetime.date.today()
    monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)
    return int(datetime.datetime.strptime(str(monday), "%Y-%m-%d").timestamp())

def get_oneday():
    today = datetime.date.today()
    first = today.replace(day=1)
    Month = first - datetime.timedelta(days=0)
    return int(datetime.datetime.strptime(str(Month), "%Y-%m-%d").timestamp())
	
def clear_firstname(firstname):
    if "<" in firstname: firstname = firstname.replace("<", "*")
    if ">" in firstname: firstname = firstname.replace(">", "*")
    if "/" in firstname: firstname = firstname.replace("/", "*")
    return firstname
	
def idgenerator():
    result = ""
    for i in range(voucherlen):
      result += random.choice(genids)
    return str(result)
	
async def isUser(id):
  async with aiosqlite.connect(path_to_db) as conn:
    countdb = await conn.execute(f'''SELECT COUNT(uid) FROM users WHERE uid = {id}''')
    return (await countdb.fetchone())[0]
	
async def isBan(id):
    if (await get_user(id))['ban']:
      return False
    else:
      return True
	
async def newuser(id, name, username, ref_father, ref_father2):
  async with aiosqlite.connect(path_to_db) as conn:
    name = clear_firstname(name)
    if ref_father and ref_father2:
        await conn.execute('''INSERT INTO users(uid, username, name, balance, adv_balance, referals, referals2, ref_father, ref_father2, reg_time, addbal, subscount, viewscount, botscount, groupscount, ban, refearn, refearn2, advspend, fine, depflood, refcount, refmsg, data, refcount2, last_bonus) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (id, username, name, 0, startmoney, str([]), str([]), ref_father, ref_father2, int(time.time()), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        referals = await conn.execute('''SELECT referals FROM users WHERE uid = ?''', (ref_father,))
        referals = eval((await referals.fetchall())[0][0])
        referals.append(id)
        referals = str(referals)
        await conn.execute('''UPDATE users SET referals = ?, refcount = (refcount + 1) WHERE uid = ?''', (referals, ref_father,))
        referals2 = await conn.execute(f'''SELECT referals2 FROM users WHERE uid = ?''', (ref_father2,))
        referals2 = eval((await referals2.fetchall())[0][0])
        referals2.append(id)
        referals2 = str(referals2)
        await conn.execute('''UPDATE users SET referals2 = ?, refcount2 = (refcount2 + 1) WHERE uid = ?''', (referals2, ref_father2,))
        await conn.commit()
    elif ref_father and ref_father2 == 0:
        await conn.execute('''INSERT INTO users(uid, username, name, balance, adv_balance, referals, referals2, ref_father, ref_father2, reg_time, addbal, subscount, viewscount, botscount, groupscount, ban, refearn, refearn2, advspend, fine, depflood, refcount, refmsg, data, refcount2, last_bonus) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (id, username, name, 0, startmoney, str([]), str([]), ref_father, 0, int(time.time()), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        referals = await conn.execute(f'''SELECT referals FROM users WHERE uid = ?''', (ref_father,))
        referals = eval((await referals.fetchall())[0][0])
        referals.append(id)
        referals = str(referals)
        await conn.execute('''UPDATE users SET referals = ?, refcount = (refcount + 1) WHERE uid = ?''', (referals, ref_father,))
        await conn.commit()
    else:
        await conn.execute('''INSERT INTO users(uid, username, name, balance, adv_balance, referals, referals2, ref_father, ref_father2, reg_time, addbal, subscount, viewscount, botscount, groupscount, ban, refearn, refearn2, advspend, fine, depflood, refcount, refmsg, data, refcount2, last_bonus) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (id, username, name, 0, startmoney, str([]), str([]), 0, 0, int(time.time()), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        await conn.commit()
		
async def get_user(id):
  async with aiosqlite.connect(path_to_db) as conn:
     try:
      id = int(id)
      cursor = await conn.cursor()
      await cursor.execute('''SELECT * FROM users WHERE uid = ?''', (id,))
      u = await cursor.fetchone()
      if u:
       return ({'id' : u[1], 'uname' : u[2], 'name' : u[3], 'bal' : u[4], 'advbal' : u[5], 'ref' : u[8], 'ref2' : u[9], 'date' : u[10], 'addbal' : u[11], 'subs' : u[12], 'views' : u[13], 'bots' : u[14], 'groups' : u[15], 'ban' : u[16], 'refearn' : u[17], 'refearn2' : u[18], 'advspend' : u[19], 'fine' : u[20], 'refcount' : u[22], 'refmsg' : u[23],'refcount2' : u[25]})
      else:
       return ({'id' : 0, 'uname' : 0, 'name' : 0, 'bal' : 0, 'advbal' : 0, 'ref' : 0, 'ref2' : 0, 'date' : 0, 'addbal' : 0, 'subs' : 0, 'views' : 0, 'bots' : 0, 'groups' : 0, 'ban' : 0, 'refearn' : 0, 'refearn2' : 0, 'advspend' : 0, 'fine' : 0, 'refcount' : 0, 'refmsg' : 0,'refcount2' : 0})
     except ValueError:
      try:
        id = str(id.split('@')[1])
        cursor = await conn.cursor()
        await cursor.execute('''SELECT * FROM users WHERE username = ?''', (id,))
        u = await cursor.fetchone()
        if u:
         return ({'id' : u[1], 'uname' : u[2], 'name' : u[3], 'bal' : u[4], 'advbal' : u[5], 'ref' : u[8], 'ref2' : u[9], 'date' : u[10], 'addbal' : u[11], 'subs' : u[12], 'views' : u[13], 'bots' : u[14], 'groups' : u[15], 'ban' : u[16], 'refearn' : u[17], 'refearn2' : u[18], 'advspend' : u[19], 'fine' : u[20], 'refcount' : u[22], 'refmsg' : u[23],'refcount2' : u[25]})
        else:
         return ({'id' : 0, 'uname' : 0, 'name' : 0, 'bal' : 0, 'advbal' : 0, 'ref' : 0, 'ref2' : 0, 'date' : 0, 'addbal' : 0, 'subs' : 0, 'views' : 0, 'bots' : 0, 'groups' : 0, 'ban' : 0, 'refearn' : 0, 'refearn2' : 0, 'advspend' : 0, 'fine' : 0, 'refcount' : 0, 'refmsg' : 0,'refcount2' : 0})
      except IndexError:
        return ({'id' : 0, 'uname' : 0, 'name' : 0, 'bal' : 0, 'advbal' : 0, 'ref' : 0, 'ref2' : 0, 'date' : 0, 'addbal' : 0, 'subs' : 0, 'views' : 0, 'bots' : 0, 'groups' : 0, 'ban' : 0, 'refearn' : 0, 'refearn2' : 0, 'advspend' : 0, 'fine' : 0, 'refcount' : 0, 'refmsg' : 0,'refcount2' : 0})

async def earn_valid(id):
  async with aiosqlite.connect(path_to_db) as conn:
    chn = []
    grn = []
    btn = []
    vin = []
    ch = await conn.execute('''SELECT * FROM channels WHERE status = 1''')
    ch = await ch.fetchall()
    for x in ch:
      if id not in eval(x[3]) and id != x[5]:
        chn.append(x[0])
    gr = await conn.execute('''SELECT * FROM groups WHERE status = 1''')
    gr = await gr.fetchall()
    for x in gr:
      if id not in eval(x[3]) and id != x[5]:
        grn.append(x[0])
    vi = await conn.execute('''SELECT * FROM views WHERE status = 1''')
    vi = await vi.fetchall()
    for x in vi:
      if id not in eval(x[2]) and id != x[4]:
        vin.append(x[0])
    bot = await conn.execute('''SELECT * FROM bots WHERE status = 1''')
    bot = await bot.fetchall()
    for x in bot:
      if id not in eval(x[4]) and id != x[6]:
        btn.append(x[0])
    return ({'ch' : len(chn), 'gr' : len(grn), 'vi' : len(vin), 'bot' : len(btn)})
	
async def statistika():
  async with aiosqlite.connect(path_to_db) as conn:
    usr = await conn.execute('''SELECT COUNT(id) FROM users''')
    usr = await usr.fetchone()
    usrd = await conn.execute(f'''SELECT COUNT(id) FROM users WHERE reg_time > ({int(time.time())} - 86400)''')
    usrd = await usrd.fetchone()
    che = await conn.execute('''SELECT SUM(subscount) FROM users''')
    che = await che.fetchone()
    gre = await conn.execute('''SELECT SUM(groupscount) FROM users''')
    gre = await gre.fetchone()
    be = await conn.execute('''SELECT SUM(botscount) FROM users''')
    be = await be.fetchone()
    ve = await conn.execute('''SELECT SUM(viewscount) FROM users''')
    ve = await ve.fetchone()
    ch = await conn.execute('''SELECT COUNT(number) FROM channels WHERE status = 1''')
    ch = await ch.fetchone()
    gr = await conn.execute('''SELECT COUNT(number) FROM groups WHERE status = 1''')
    gr = await gr.fetchone()
    vi = await conn.execute('''SELECT COUNT(number) FROM views WHERE status = 1''')
    vi = await vi.fetchone()
    bot = await conn.execute('''SELECT COUNT(number) FROM bots WHERE status = 1''')
    bot = await bot.fetchone()
    return ({'ch' : ch[0], 'gr' : gr[0], 'vi' : vi[0], 'bot' : bot[0], 'u' : usr[0], 'td' : usrd[0], 'c' : che[0], 'g' : gre[0], 'b' : be[0], 'v' : ve[0]})

async def my_promo_count(type, id):
  async with aiosqlite.connect(path_to_db) as conn:
    sql = await conn.execute(f'''SELECT COUNT(number) FROM {type} WHERE status = 1 AND creator = {id}''')
    sql = await sql.fetchone()
    return sql[0]

async def get_subs_info(num, type):
  async with aiosqlite.connect(path_to_db) as conn:
     row = await conn.execute(f'''SELECT * FROM {type} WHERE status = 1 AND number = ?''', (num,))
     row = await row.fetchone()
     if row:
       cr = await conn.execute('''SELECT name FROM users WHERE uid = ?''', (row[5],))
       cr = await cr.fetchone()
       num = len(eval(row[3]))
       return ({'id' : row[1], 'name' : row[2], 'count' : num, 'memb' : row[4], 'cid' : row[5], 'cn' : cr[0]})
     else:
       return ({'id' : 0, 'name' : 0, 'count' : 0, 'memb' : 0, 'cid' : 0, 'cn' : 0})
	   
async def get_bots_info(num, type):
  async with aiosqlite.connect(path_to_db) as conn:
     row = await conn.execute(f'''SELECT * FROM {type} WHERE status = 1 AND number = ?''', (num,))
     row = await row.fetchone()
     if row:
       cr = await conn.execute('''SELECT name FROM users WHERE uid = ?''', (row[6],))
       cr = await cr.fetchone()
       num = len(eval(row[4]))
       return ({'id' : row[1], 'name' : row[2], 'count' : num, 'memb' : row[5], 'cid' : row[6], 'cn' : cr[0]})
     else:
       return ({'id' : 0, 'name' : 0, 'count' : 0, 'memb' : 0, 'cid' : 0, 'cn' : 0})

async def stop_adm(num, type):
  async with aiosqlite.connect(path_to_db) as conn:
     await conn.execute(f'''UPDATE {type} SET status = 0 WHERE number = ?''', (num,))
     await conn.commit()
     if type == 'views':
       vi = await conn.execute('''SELECT mid FROM views WHERE number = ?''', (num,))
       vi = await vi.fetchone()
       return vi[0]
	   
async def stop_subs(num, id, type):
  async with aiosqlite.connect(path_to_db) as conn:
     row = await conn.execute(f'''SELECT creator, members, users, name FROM {type} WHERE status = 1 AND number = ?''', (num,))
     row = await row.fetchone()
     if row[0] == id:
       co = len(eval(row[2]))
       await conn.execute(f'''UPDATE {type} SET status = 0 WHERE number = ?''', (num,))
       await conn.commit()
       return ({'name' : row[3], 'count' : co, 'memb' : row[1]})
     else:
       return False
	
async def my_subs_db(id, type):
  async with aiosqlite.connect(path_to_db) as conn:
    try:
     row = await conn.execute(f'''SELECT * FROM {type} WHERE status = 1 AND creator = ? ORDER BY number''', (id,))
     row = await row.fetchall()
     return row
    except:
     return 0
	
async def for_subscribe(type):
  async with aiosqlite.connect(path_to_db) as conn:
    cursor = await conn.cursor()
    await cursor.execute(f'''SELECT * FROM {type} WHERE status = 1''')
    channels = await cursor.fetchall()
    return channels
	
async def for_views(num):
  async with aiosqlite.connect(path_to_db) as conn:
    channels = await conn.execute(f'''SELECT * FROM views WHERE status = 1 AND number = ?''', (num,))
    channels = await channels.fetchone()
    if channels:
      return channels
    else:
      return 0

async def get_allviews():
  async with aiosqlite.connect(path_to_db) as conn:
    channels = await conn.execute(f'''SELECT * FROM views WHERE status = 1 ORDER BY number DESC LIMIT 35''')
    channels = await channels.fetchall()
    if channels:
      return channels
    else:
      return 0
	  
async def views_good_pay(id, number):
  async with aiosqlite.connect(path_to_db) as conn:
    sql = await conn.execute(f'''SELECT users FROM views WHERE number = ?''', (number,))
    sql = await sql.fetchall()
    listusr = eval(sql[0][0])
    listusr.append(id)
    await conn.execute('''UPDATE views SET users = ? WHERE number = ?''', (str(listusr), number,))
    await conn.execute('''UPDATE users SET balance = (balance + ?), viewscount = (viewscount + 1) WHERE uid = ?''', (views_pay, id,))
    referal = await conn.execute('''SELECT ref_father FROM users WHERE uid = ?''', (id,))
    referal = await referal.fetchone()
    if referal[0]:
      ref_pays = views_pay * (ref_workbonus / 100)
      await conn.execute('''UPDATE users SET balance = balance + ?, refearn = refearn + ? WHERE uid = ?''', (ref_pays, ref_pays, referal[0],))
    await conn.commit()
	
async def reftop(id):
  async with aiosqlite.connect(path_to_db) as conn:
    try:
     count = await conn.execute('''SELECT * FROM users ORDER BY refcount DESC LIMIT 15''')
     count = await count.fetchall()
     return count
    except:
     return 0

async def set_hello(txt, id):
  async with aiosqlite.connect(path_to_db) as conn:
    await conn.execute('''UPDATE users SET refmsg = ? WHERE uid = ?''', (txt, id,))
    await conn.commit()

async def set_ban(id, s):
  async with aiosqlite.connect(path_to_db) as conn:
    await conn.execute('''UPDATE users SET ban = ? WHERE uid = ?''', (s, id,))
    await conn.commit()

async def change_bal(id, sum, type):
  async with aiosqlite.connect(path_to_db) as conn:
    await conn.execute(f'''UPDATE users SET {type} = ? WHERE uid = ?''', (sum, id,))
    await conn.commit()
	
async def add_advbal(id, sum):
  async with aiosqlite.connect(path_to_db) as conn:
    await conn.execute('''UPDATE users SET adv_balance = (adv_balance + ?) WHERE uid = ?''', (sum, id,))
    await conn.commit()
	 
async def add_bal(id, sum):
  async with aiosqlite.connect(path_to_db) as conn:
    await conn.execute('''UPDATE users SET balance = (balance + ?) WHERE uid = ?''', (sum, id,))
    await conn.commit()

async def add_refearn(id, sum):
  async with aiosqlite.connect(path_to_db) as conn:
    await conn.execute('''UPDATE users SET referals = (referals + ?) WHERE uid = ?''', (sum, id,))
    await conn.commit()
	
async def edit_vi_status(id):
  async with aiosqlite.connect(path_to_db) as conn:
    await conn.execute('''UPDATE views SET status = 0 WHERE number = ?''', (id,))
    await conn.commit()
	
async def edit_ch_status(num, status, type):
  async with aiosqlite.connect(path_to_db) as conn:
    try:
      sql = await conn.execute(f'''SELECT COUNT(number), creator, name, users, members FROM {type} WHERE number = ?''', (num,))
      sql = await sql.fetchall()
      if sql[0][0] == 1 and status == 0:
        await conn.execute(f'''UPDATE {type} SET status = ? WHERE number = ?''', (status, num,))
        cursor = await conn.cursor()
        if type != "bots":
          await cursor.execute('''DELETE FROM subscriptions WHERE num = ?''', (num,))
        delta = sql[0][4] - len(eval(sql[0][3]))
        delta = abs(delta) * 0.5
        delta = round(delta, 0) * eval(f'{type}price')
        await conn.execute('''UPDATE users SET adv_balance = adv_balance + ? WHERE uid = ?''', (delta, sql[0][1],))
        await conn.commit()
      return ({'id' : sql[0][1], 'name' : sql[0][2], 'sum' : delta})
    except:
      return ({'id' : 0, 'name' : 0, 'sum' : 0})

async def add_user_to_subsch(number, user_id, type):
  async with aiosqlite.connect(path_to_db) as conn:
    tm = int(time.time()) + (sub_term * 86400)
    number = int(number)
    get_count_of_num_i_status = await conn.execute(f'''SELECT COUNT(number), status FROM {type} WHERE number = ?''', (number,))
    get_count_of_num_i_status = await get_count_of_num_i_status.fetchall()
    count_of_number = get_count_of_num_i_status[0][0]
    if count_of_number == 1 and get_count_of_num_i_status[0][1]:
        sql = await conn.execute(f'''SELECT users, members, creator, id, name FROM {type} WHERE number = ?''', (number,))
        sql_fetchall = await sql.fetchall()
        subscriptions = eval(sql_fetchall[0][0])
        if len(subscriptions) < sql_fetchall[0][1]:
            subscriptions.append(user_id)
            await conn.execute(f'''UPDATE {type} SET users = ? WHERE number = ?''', (str(subscriptions), number))
            if type != "bots":
              await conn.execute('''INSERT INTO subscriptions(num, id, creator, cid, time, type, warn, name) VALUES(?,?,?,?,?,?,?,?)''', (number, user_id,sql_fetchall[0][2], sql_fetchall[0][3], tm, str(type), 0,sql_fetchall[0][4]))
            referal = await conn.execute('''SELECT ref_father FROM users WHERE uid = ?''', (user_id,))
            referal = await referal.fetchone()
            if type == "channels":
              count = "subscount"
            else:
              count = f"{type}count"
            if referal[0]:
              ref_pays = eval(f'{type}_pay') * (ref_workbonus / 100)
              await conn.execute('''UPDATE users SET balance = balance + ?, refearn = refearn + ? WHERE uid = ?''', (ref_pays, ref_pays, referal[0],))
            await conn.execute(f'''UPDATE users SET balance = balance + ?, {count} = {count} + 1 WHERE uid = ?''', (eval(f'{type}_pay'), user_id,))
            await conn.commit()
            return 1, sql_fetchall[0][2], sql_fetchall[0][4]
        else:
            return 0, sql_fetchall[0][2], sql_fetchall[0][4]
    else:
        return 0, sql_fetchall[0][2], sql_fetchall[0][4]

async def new_bots(id, name, url, vi, cr):
  async with aiosqlite.connect(path_to_db) as conn:
    cursor = await conn.cursor()
    await cursor.execute('''INSERT INTO bots(id, name, url, users, members, creator, status) VALUES(?,?,?,?,?,?,?)''', (id, name, url, str([]), vi, cr, 1,))
    await conn.execute('''UPDATE users SET adv_balance = adv_balance - ?, advspend = advspend + ? WHERE uid = ?''', ((vi * botsprice), (vi * botsprice), cr,))
    await conn.commit()
		
async def new_views(mid, vi, cr):
  async with aiosqlite.connect(path_to_db) as conn:
    cursor = await conn.cursor()
    await cursor.execute('''INSERT INTO views(mid, users, views, creator, status) VALUES(?,?,?,?,?)''', (mid, str([]), vi, cr, 1,))
    num = await conn.execute('''SELECT MAX(number) FROM views''')
    num = await num.fetchone()
    await conn.execute('''UPDATE users SET adv_balance = adv_balance - ?, advspend = advspend + ? WHERE uid = ?''', ((vi * viewsprice), (vi * viewsprice), cr,))
    await conn.commit()
    return num[0]
		
async def new_channel(id, name, memb, cr, type):
  async with aiosqlite.connect(path_to_db) as conn:
    info = await conn.execute(f'''SELECT COUNT(number) FROM {type} WHERE id = ? AND status = 1''', (id,))
    info = await info.fetchone()
    if info[0] >= maxtask:
      return False
    else:
      cursor = await conn.cursor()
      await cursor.execute(f'''INSERT INTO {type}(id, name, users, members, creator, status) VALUES(?,?,?,?,?,?)''', (id, name, str([]), memb, cr, 1,))
      await conn.execute('''UPDATE users SET adv_balance = adv_balance - ?, advspend = advspend + ? WHERE uid = ?''', ((memb * eval(f'{type}price')), (memb * eval(f'{type}price')), cr,))
      await conn.commit()
      return True
		
async def get_url_bot(number, id):
  async with aiosqlite.connect(path_to_db) as conn:
    await conn.execute('''UPDATE users SET data = ? WHERE uid = ?''', (f'fwdbot{number}', id,))
    await conn.commit()
    info = await conn.execute('''SELECT url FROM bots WHERE number = ?''', (number,))
    info = await info.fetchone()
    return info[0]
	
async def promoch_info(number_of_promotion, type):
  async with aiosqlite.connect(path_to_db) as conn:
    number = int(number_of_promotion)
    check_promotion = await conn.execute(f'''SELECT COUNT(number) FROM {type} WHERE number = ?''', (number,))
    if (await check_promotion.fetchall())[0][0] == 1:
        info = await conn.execute(f'''SELECT users, members, id, name FROM {type} WHERE number = ?''', (number,))
        info = await info.fetchall()
        subscriptions = info[0][0]
        subscriptions = eval(subscriptions)
        subs_count = info[0][1]
        if len(subscriptions) < subs_count:
            return 1, info[0][2], info[0][3], info[0][0]
        else:
            return 0, info[0][2], info[0][3], info[0][0]
    else:
        return 0, info[0][2], info[0][3], info[0][0]
        
async def get_sum_dep(id):
  async with aiosqlite.connect(path_to_db) as conn:
    try:
     sum = await conn.execute('''SELECT SUM(sum) FROM deposits WHERE user_id = ? AND status = 0''', (id,))
     sum = await sum.fetchall()
     if sum:
       return round(sum[0][0], 2)
     return 0
    except:
     return 0

async def get_sum_vouch(id):
  async with aiosqlite.connect(path_to_db) as conn:
    try:
     sum = await conn.execute('''SELECT SUM(sum) FROM vaucher WHERE actid = ? AND status = 0''', (id,))
     sum = await sum.fetchall()
     if sum:
       return round(sum[0][0], 2)
     return 0
    except:
     return 0
	 
async def get_num_vouch(id):
  async with aiosqlite.connect(path_to_db) as conn:
    try:
     count = await conn.execute('''SELECT COUNT(num) FROM vaucher WHERE actid = ? AND status = 0''', (id,))
     sum = await sum.fetchall()
     if count:
       return count[0]
     return 0
    except:
     return 0
	 
async def get_sum_pay(id):
  async with aiosqlite.connect(path_to_db) as conn:
    try:
     sum = await conn.execute('''SELECT SUM(sum) FROM payouts WHERE uid = ? AND status = "Подтверждён"''', (id,))
     sum = await sum.fetchall()
     if sum:
       return round(sum[0][0], 2)
     return 0
    except:
     return 0
		
async def get_channels_for_check():
  async with aiosqlite.connect(path_to_db) as conn:
    channels = await conn.execute('''SELECT * FROM subscriptions''')
    channels = await channels.fetchall()
    return channels
    
async def get_last_check():
  async with aiosqlite.connect(path_to_db) as conn:
    sql = await conn.execute('''SELECT * FROM other''')
    last_check = await sql.fetchone()
    if last_check == None:
        return last_check
    else:
        return eval(last_check[0])

async def about():
  async with aiosqlite.connect(path_to_db) as conn:
    a = await conn.execute('''SELECT * FROM other''').fetchall()
    if a == None:
        return False
    else:
        return a[0][1]
        
async def set_last_check():
  async with aiosqlite.connect(path_to_db) as conn:
    ltime = int(time.time()) + (intervall * 60)
    await conn.execute('''UPDATE other SET last_check = ?''', (ltime,))
    await conn.commit()
        
async def add_promotion_to_uncheck(number):
  async with aiosqlite.connect(path_to_db) as conn:
    cursor = await conn.cursor()
    await cursor.execute('''DELETE FROM subscriptions WHERE num = ?''', (number,))
    await conn.commit()
	
async def user_uncheck(number, id):
  async with aiosqlite.connect(path_to_db) as conn:
    cursor = await conn.cursor()
    await cursor.execute('''DELETE FROM subscriptions WHERE num = ? AND id = ?''', (number, id,))
    await conn.commit()

async def user_warn(number, id):
  async with aiosqlite.connect(path_to_db) as conn:	
    await conn.execute('''UPDATE subscriptions SET warn = ? WHERE num = ? AND id = ?''', (1, number, id,))
    await conn.commit()

async def setdepflood(id, dat):
  async with aiosqlite.connect(path_to_db) as conn:
    await conn.execute('''UPDATE users SET depflood = ? WHERE uid = ?''', (dat, id,))
    await conn.commit()

async def get_depflood(id):
  async with aiosqlite.connect(path_to_db) as conn:
    cursor = await conn.cursor()
    await cursor.execute('''SELECT depflood FROM users WHERE uid = ?''', (id,))
    row = await cursor.fetchone()
    return row[0] or 0
	
async def get_bonus(id, bonus):
  async with aiosqlite.connect(path_to_db) as conn:
    cursor = await conn.cursor()
    await cursor.execute('''SELECT last_bonus, ref_father, ref_father2 FROM users WHERE uid = ?''', (id,))
    row = await cursor.fetchone()
    if row[0] < int(time.time()):
      await conn.execute('''UPDATE users SET last_bonus = ?, addbal = addbal + ?, balance = balance + ? WHERE uid = ?''', (int(time.time()) + 86400, bonus, bonus, id,))
      await conn.commit()
      if row[0] == 0:
        if row[1] and row[2] == 0:
          await conn.execute('''UPDATE users SET balance = (balance + ?), refearn = (refearn + ?) WHERE uid = ?''', (ref_pays, ref_pays, row[1],))
          await conn.commit()
        elif row[1] and row[2] != 0:
          await conn.execute('''UPDATE users SET balance = (balance + ?), refearn = (refearn + ?) WHERE uid = ?''', (ref_pays, ref_pays, row[1],))
          await conn.execute('''UPDATE users SET balance = (balance + ?), refearn2 = (refearn2 + ?) WHERE uid = ?''', (ref_pays2, ref_pays2, row[2],))
          await conn.commit()
        return 1, row[1], row[2]
      else:
        return 1, 0, 0
    else:
      return 0, 0, 0
	
async def setdata(id, dat):
  async with aiosqlite.connect(path_to_db) as conn:
    await conn.execute('''UPDATE users SET data = ? WHERE uid = ?''', (dat, id,))
    await conn.commit()
	
async def udata(id):
  async with aiosqlite.connect(path_to_db) as conn:
    cursor = await conn.cursor()
    await cursor.execute('''SELECT data FROM users WHERE uid = ?''', (id,))
    row = await cursor.fetchone()
    return row[0] or 0
	
async def new_voucher(sum, uid, name):
  async with aiosqlite.connect(path_to_db) as conn:
    sum = round(sum, 2)
    id = idgenerator()
    cursor = await conn.cursor()
    await cursor.execute(f'''INSERT INTO vouchers(id, sum, status, date, creator, creator_name) VALUES(?,?,?,?,?,?)''', (id, sum, 1, int(time.time()), uid, clear_firstname(name),))
    await conn.commit()
    return str(id)

async def act_voucher(vid, uid, sum):
  async with aiosqlite.connect(path_to_db) as conn:
    await conn.execute('''UPDATE vouchers SET status = 0, actid = ? WHERE id = ?''', (uid, vid,))
    await conn.execute('''UPDATE users SET balance = balance + ? WHERE uid = ?''', (sum, uid,))
    await conn.commit()
    cursor = await conn.cursor()
    await cursor.execute('''SELECT balance FROM users WHERE uid = ?''', (uid,))
    row = await cursor.fetchone()
    return row[0]
	
async def get_voucher(id):
  async with aiosqlite.connect(path_to_db) as conn:
    cursor = await conn.cursor()
    await cursor.execute('''SELECT * FROM vouchers WHERE id = ?''', (id,))
    row = await cursor.fetchone()
    return row
	
async def get_user_mm():
  async with aiosqlite.connect(path_to_db) as conn:
    cursor = await conn.cursor()
    await cursor.execute('''SELECT uid, name FROM users''')
    row = await cursor.fetchall()
    return row
	
async def increase_fine(id):
  async with aiosqlite.connect(path_to_db) as conn:
    await conn.execute('''UPDATE users SET fine = fine - ?, balance = balance - ? WHERE uid = ?''', (unsub, unsub, id,))
    await conn.commit()
    
async def new_deposit(user_id, comment):
  async with aiosqlite.connect(path_to_db) as conn:
    cursor = await conn.cursor()
    await cursor.execute('''INSERT INTO deposits(user_id, comment, time, sum, status, number) VALUES(?,?,?,?,?,?)''', (user_id, comment, int(time.time()), 0, '⌛️', 0,))
    await conn.commit()

async def delete_deposit(user_id):
  async with aiosqlite.connect(path_to_db) as conn:
    try:
      cursor = await conn.cursor()
      await cursor.execute('''DELETE FROM deposits WHERE user_id = ? AND status = ?''', (user_id, '⌛️',))
      await conn.commit()
      return True
    except:
      return False

async def set_deposit(user_id, sum, num):
  async with aiosqlite.connect(path_to_db) as conn:
    cursor = await conn.cursor()
    await cursor.execute('''UPDATE deposits SET status = ?, sum = ?, number = ? WHERE user_id = ?''', ('✅', sum, num, user_id,))
    await conn.commit()

async def get_comment(user_id):
  async with aiosqlite.connect(path_to_db) as conn:
    cursor = await conn.cursor()
    await cursor.execute(f'''SELECT comment FROM deposits WHERE user_id = ? AND status = ?''', (user_id, '⌛️',))
    row = await cursor.fetchone()
    if row != None:
     return row[0]
    else:
     return row

async def dep_history(id, type):
  async with aiosqlite.connect(path_to_db) as conn:
    row = await conn.execute(f'''SELECT * FROM deposits WHERE {type} = '{id}' LIMIT 30''')
    row = await row.fetchall()
    return row
	
async def pay_history(id):
  async with aiosqlite.connect(path_to_db) as conn:
    row = await conn.execute('''SELECT * FROM payouts WHERE uid = ? LIMIT 30''',(id,))
    row = await row.fetchall()
    return row
	 
async def get_pay(num):
  async with aiosqlite.connect(path_to_db) as conn:
    row = await conn.execute('''SELECT * FROM payouts WHERE num = ? AND status = ?''',(num, 'В обработке',))
    row = await row.fetchone()
    if row:
      return True, row
    else:
      return False, 0
	 
async def get_allpays(st):
  async with aiosqlite.connect(path_to_db) as conn:
    row = await conn.execute('''SELECT * FROM payouts WHERE status = ?''', (st,))
    row = await row.fetchall()
    return row
	 
async def new_payout(user_id, name, sum, w):
  async with aiosqlite.connect(path_to_db) as conn:
    await conn.execute('''INSERT INTO payouts(uid, name, sum, time, wallet, status) VALUES(?,?,?,?,?,?)''',(user_id, name, sum, int(time.time()), w, 'В обработке',))
    await conn.commit()
	
async def set_payout(num, status):
  async with aiosqlite.connect(path_to_db) as conn:
    cursor = await conn.cursor()
    await cursor.execute('''UPDATE payouts SET status = ? WHERE num = ?''', (status, num,))
    await conn.commit()

async def all_deposits():
  async with aiosqlite.connect(path_to_db) as conn:
    all = await conn.execute('''SELECT * FROM deposits WHERE status = ? LIMIT 30''', ('✅',))
    all = await all.fetchall()
    sum = await conn.execute('''SELECT SUM(sum), COUNT(user_id) FROM deposits WHERE status = ?''', ('✅',))
    sum = await sum.fetchone()
    sumd = await conn.execute('''SELECT SUM(sum), COUNT(user_id) FROM deposits WHERE status = ? AND time > ?''', ('✅', (int(time.time()) - 86400),))
    sumd = await sumd.fetchone()
    sumw = await conn.execute('''SELECT SUM(sum), COUNT(user_id) FROM deposits WHERE status = ? AND time > ?''', ('✅', get_mondey()))
    sumw = await sumw.fetchone()
    summ = await conn.execute('''SELECT SUM(sum), COUNT(user_id) FROM deposits WHERE status = ? AND time > ?''', ('✅', get_oneday()))
    summ = await summ.fetchone()
    return all, sum[0], sumd[0], sumw[0], summ[0], sum[1], sumd[1], sumw[1], summ[1]
	
async def all_payouts():
  async with aiosqlite.connect(path_to_db) as conn:
    all = await conn.execute('''SELECT * FROM payouts WHERE status = ?  ORDER BY num DESC LIMIT 30''', ('Выполнено',))
    all = await all.fetchall()
    sum = await conn.execute('''SELECT SUM(sum), COUNT(uid) FROM payouts WHERE status = ?''', ('Выполнено',))
    sum = await sum.fetchone()
    sumd = await conn.execute('''SELECT SUM(sum), COUNT(uid) FROM payouts WHERE status = ? AND time > ?''', ('Выполнено', (int(time.time()) - 86400),))
    sumd = await sumd.fetchone()
    sumw = await conn.execute('''SELECT SUM(sum), COUNT(uid) FROM payouts WHERE status = ? AND time > ?''', ('Выполнено', get_mondey()))
    sumw = await sumw.fetchone()
    summ = await conn.execute('''SELECT SUM(sum), COUNT(uid) FROM payouts WHERE status = ? AND time > ?''', ('Выполнено', get_oneday()))
    summ = await summ.fetchone()
    return all, sum[0], sumd[0], sumw[0], summ[0], sum[1], sumd[1], sumw[1], summ[1]