from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv
import os
import json
import time


def scrapper():
    if os.path.isdir('/Program Files/Telegram') == False:
        os.mkdir('/Program Files/Telegram')
    try:
        if os.path.isfile(os.path.join(os.getcwd(), 'config.json')) == True:
            pass
        else:
            config = {}
            config['api_id'] = '0'
            config['api_hash'] = 'your api hash'
            config['phone'] = '+0'
            with open(os.path.join(os.getcwd(), 'config.json'), 'w') as config_file:
                json.dump(config, config_file, indent=2)

        session = False
        for item in os.listdir():
            if '.session' in item:
                number = item.split('.')[0]
                session = True

        if session:
            while True:
                a = input(f'Do you want to recover your login session with number {number}? [y/n] ').lower()
                if a == 'y':
                    print('Program Started...')
                    with open(os.path.join(os.getcwd(), 'config.json'), 'r') as config_file:
                        config = json.load(config_file)
                        api_id = config['api_id']
                        api_hash = config['api_hash']
                        phone = config['phone']
                    break
                elif a == 'n':
                    for item in os.listdir():
                        if '.session' in item:
                            os.remove(item)
                    print('Program Started...')
                    api_id = input('Paste here your account api id: ')
                    api_hash = input('Paste here your account api hash: ')
                    phone = input('Paste here your phone number (International Format): ')
                    config = {}
                    config['api_id'] = api_id
                    config['api_hash'] = api_hash
                    config['phone'] = phone
                    with open(os.path.join(os.getcwd(), 'config.json'), 'w') as config_file:
                        json.dump(config, config_file, indent=2)
                    break

        else:
            print('No session found. Lets define a new one...')
            api_id = input('Paste here your account api id: ')
            api_hash = input('Paste here your account api hash: ')
            phone = input('Paste here your phone number (International Format): ')
            config = {}
            config['api_id'] = api_id
            config['api_hash'] = api_hash
            config['phone'] = phone
            with open(os.path.join(os.getcwd(), 'config.json'), 'w') as config_file:
                json.dump(config, config_file, indent=2)

        # ========================== FIXING BUGS ================================
        with open(os.path.join(os.getcwd(), 'config.json'), 'r') as config_file:
            config = json.load(config_file)

            if api_id == '0':
                api_id = input('Paste here your account api id: ')
                config['api_id'] = api_id
                with open(os.path.join(os.getcwd(), 'config.json'), 'w') as config_file:
                    json.dump(config, config_file, indent=2)

            if api_hash == 'your api hash':
                api_hash = input('Paste here your account api hash: ')
                config['api_hash'] = api_hash
                with open(os.path.join(os.getcwd(), 'config.json'), 'w') as config_file:
                    json.dump(config, config_file, indent=2)
            if phone == '+0':
                phone = input('Paste here your phone number (International Format): ')
                config['phone'] = phone
                with open(os.path.join(os.getcwd(), 'config.json'), 'w') as config_file:
                    json.dump(config, config_file, indent=2)

        # ====================== END OF FIXING BUGS ===============================

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

        print('Which Group Do You Want To Scrape Members From: ')
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
        # with open('/Program Files/Telegram/Scrapped.csv',"w+",encoding='UTF-8') as f:#Enter your file name.
        #     writer = csv.writer(f,delimiter=",",lineterminator="\n")
        #     writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
        #     for user in all_participants:
        #         if user.username:
        #             username= user.username
        #         else:
        #             username= ""
        #         if user.first_name:
        #             first_name= user.first_name
        #         else:
        #             first_name= ""
        #         if user.last_name:
        #             last_name= user.last_name
        #         else:
        #             last_name= ""
        #         name= (first_name + ' ' + last_name).strip()
        #         writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])

        with open(os.path.join(os.getcwd(), 'Scraped.json'), 'w+') as f:
            users = []
            jsonuser = {}
            for user in all_participants:
                jsonuser.clear()
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
                jsonuser['username'] = username
                jsonuser['id'] = user.id
                jsonuser['access_hash'] = user.access_hash
                jsonuser['name'] = name
                users.append(jsonuser.copy())
            json.dump(users, f, indent=2)

        print('Members scraped successfully.......')
        client.disconnect()
        # print('Please, close this window...')
        # time.sleep(10000)

    except Exception as e:
        e = str(e)
        client.disconnect()
        print(e)
        time.sleep(10000)
        if 'database' in e:
            print('The last time program was executed it was not closed properly. Please delete the files ending with .session, and restart the program.')
            time.sleep(10000)

