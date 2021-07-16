from telegram.client import Telegram
from pprint import pprint


tg = Telegram(
    api_id='lala',
    api_hash='lala',
    phone='+12345678901',
    database_encryption_key='lala',
)

tg.login()



params = {'query_': 'Forsage'}
#params = {'user_id_': 482686717}
result = tg.call_method('searchPublicChats', params)
#result = tg.call_method('searchContacts', params)
#result = tg.call_method('getContacts', params)
#result = tg.call_method('getUser',params)
result.wait()
print(result.update)


# result = tg.get_me()
# result.wait()
# pprint(result.update)


# result = tg.get_chats(940932814)
# result.wait()
# update = result.update
# print(update)
# chats  = update['chat_ids']
#
# for chat_id in chats:
#     r = tg.get_chat(chat_id)
#     r.wait()
#     update = r.update
#     print(update)
#     print(update['title'])



tg.stop()
