import requests
from data.config import qnum, qtoken
from utils.sqlite import get_comment

def get_qiwi_url(code):
 	s = requests.Session()
 	parameters = {"extra['comment']": code, "extra['account']": qnum, "blocked[0]": 'comment', "blocked[1]": 'account'}
 	url = 'https://qiwi.com/payment/form/99'
 	h = s.get(url,params = parameters)
 	return h.url
	
def deposit_check(rows_num):
	s = requests.Session()
	s.headers['authorization'] = 'Bearer ' + qtoken
	parameters = {'rows': rows_num, 'operation': 'IN'}
	h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + qnum + '/payments', params = parameters)
	return h.json()

def balance_qiwi():
    try:
      s = requests.Session()
      s.headers['authorization'] = 'Bearer ' + qtoken
      b = s.get(f'https://edge.qiwi.com/funding-sources/v2/persons/{str(qnum)}/accounts')
      for b in b.json().get("accounts", []):
        if b.get("balance", {}).get("currency") == 643:
          return b.get("balance", {}).get("amount")
    except Exception as e:
      print(f'Ошибка QIWI: {e}')
	
async def chk_qiwi(id, rows_num):
  try:
    comment = await get_comment(id)
    if comment != None:
      payments = deposit_check(rows_num)
      pay_len = len(payments['data'])
      if rows_num >= pay_len:
        pay_len = rows_num
        for i in range(rows_num):
          if payments['data'][i]['comment'] == str(comment) and payments['data'][i]['status'] == 'SUCCESS':
            amount = payments['data'][i]['sum']['amount']
            number = payments['data'][i]['account']
            return True, amount, str(comment), number
          else:
            return False, 0, 0, 0
    else:
      return False, 0, 0
  except Exception as e:
    print(e)
    return False, 0, 0