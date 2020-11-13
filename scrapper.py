from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

def scrapper():
    api_id = input('Type your api id: ')
    api_hash = input('Type your api hash: ')
    phone = input('Type your phone number starting with +: ')
    client = TelegramClient(phone, api_id, api_hash)
    async def main():
        # Now you can use all client methods listed below, like for example...
        await client.send_message('me', 'Hello !!!!')
    with client:
        client.loop.run_until_complete(main())
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter verification code: '))


    chats = []
    last_date = None
    chunk_size = 200
    groups=[]

    result = client(GetDialogsRequest(
                 offset_date=last_date,
                 offset_id=0,
                 offset_peer=InputPeerEmpty(),
                 limit=chunk_size,
                 hash = 0
             ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup== True:
                groups.append(chat)
        except:
            continue

    print('From Which Group Yow Want To Scrap A Members:')
    i=0
    for g in groups:
        g.title = g.title.encode('utf-8')
        g.title = g.title.decode('ascii', 'ignore')
        print(str(i) + '- ' + g.title)
        i+=1
        
    g_index = input("Please! Enter a Number: ")
    target_group=groups[int(g_index)]

    print('Fetching Members...')
    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=True)

    print('Saving In file...')
    with open("Scrapped.csv","w",encoding='UTF-8') as f:#Enter your file name.
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
        for user in all_participants:
            if user.username:
                username= user.username
            else:
                username= ""
            if user.first_name:
                first_name= user.first_name
            else:
                first_name= ""
            if user.last_name:
                last_name= user.last_name
            else:
                last_name= ""
            name= (first_name + ' ' + last_name).strip()
            writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
    print('Members scraped successfully.......')
