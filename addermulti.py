from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserNotMutualContactError, UserChannelsTooMuchError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random
import os
import json

def addermulti():
    g_scrape_id = ''
    g_id = ''
    def add_credentials():
        if os.path.isfile(os.path.join(os.getcwd(), 'multiconfig.json')) == True:
            with open(os.path.join(os.getcwd(), 'multiconfig.json'), 'r') as config_file:
                data = json.load(config_file)

                print(f'Credentials found, for {len(data)} Telegram accounts')
                for cred in data:
                    print(f'Checking if two factor authentication is already done with {cred["phone"]}')
                    client = TelegramClient(cred['phone'], cred['api_id'], cred['api_hash'])
                    async def main():
                        # Now you can use all client methods listed below, like for example...
                        await client.send_message('me', 'Hello !!!!!')

                    with client:
                        client.loop.run_until_complete(main())
                    client.connect()
                    if not client.is_user_authorized():
                        print(f'Sending request code to {cred["phone"]}, please authenticate')
                        client.send_code_request(phone)
                        client.sign_in(cred["phone"], input('40779'))
                    else:
                        print(f'Good! Client {cred["phone"]} is authenticated, I can use it.')
                    client.disconnect()

            print(f'Credentials found, for {len(data)} Telegram accounts')
            while True:
                question = input('Do you want to use these credentials?[y/n] ').lower()
                if question == 'y':
                    break
                elif question == 'n':
                    print('Good, lets define new credentials...')
                    ammount_of_credentials = int(input('How many accounts do you want to add?'))
                    credentials = []
                    for i in range(ammount_of_credentials):
                        phone = input('Type the phone number: ')
                        api_id = input(f'Type {phone} api id: ')
                        api_hash = input(f'Type {phone} api hash: ')

                        config = {}
                        config['api_id'] = api_id
                        config['api_hash'] = api_hash
                        config['phone'] = phone
                        credentials.append(config.copy())

                        with open(os.path.join(os.getcwd(), 'multiconfig.json'), 'w') as config_file:
                            json.dump(credentials, config_file, indent=2)

                        client = TelegramClient(phone, api_id, api_hash)
                        async def main():
                            # Now you can use all client methods listed below, like for example...
                            await client.send_message('me', 'Hello !!!!!')

                        with client:
                            client.loop.run_until_complete(main())
                        client.connect()
                        if not client.is_user_authorized():
                            print(f'Sending request code to {phone}, please authenticate')
                            client.send_code_request(phone)
                            client.sign_in(phone, input('40779'))
                        else:
                            print(f'Good! Client {phone} is authenticated, I can use it.')
                        client.disconnect()
                    break
        else:
            print('No credentials found. Lets define new ones')
            ammount_of_credentials = int(input('How many accounts do you want to add?'))
            credentials = []
            for i in range(ammount_of_credentials):
                phone = input('Type the phone number: ')
                api_id = input(f'Type {phone} api id: ')
                api_hash = input(f'Type {phone} api hash: ')

                config = {}
                config['api_id'] = api_id
                config['api_hash'] = api_hash
                config['phone'] = phone
                credentials.append(config.copy())

                with open(os.path.join(os.getcwd(), 'multiconfig.json'), 'w') as config_file:
                    json.dump(credentials, config_file, indent=2)

                client = TelegramClient(phone, api_id, api_hash)
                async def main():
                    # Now you can use all client methods listed below, like for example...
                    await client.send_message('me', 'Hello !!!!!')

                with client:
                    client.loop.run_until_complete(main())
                client.connect()
                if not client.is_user_authorized():
                    print(f'Sending request code to {phone}, please authenticate')
                    client.send_code_request(phone)
                    client.sign_in(phone, input('40779'))
                else:
                    print(f'Good! Client {phone} is authenticated, I can use it.')
                client.disconnect()

    add_credentials()

    with open(os.path.join(os.getcwd(), 'multiconfig.json'), 'r') as config_file:
        credentials = json.load(config_file)

    for config in credentials:
        api_id = config['api_id']
        api_hash = config['api_hash']
        phone = config['phone']

        AMMOUNT_OF_FLOOD_ERROS = 0
        AMMOUNT_OF_USERS_ADDED = 0
        print(f'Now trying use account {phone}')

        try:
            client = TelegramClient(phone, api_id, api_hash)
            async def main():
                # Now you can use all client methods listed below, like for example...
                await client.send_message('me', 'Hello !!!!!')


            SLEEP_TIME_1 = 100
            SLEEP_TIME_2 = 100
            with client:
                client.loop.run_until_complete(main())
            client.connect()
            if not client.is_user_authorized():
                client.send_code_request(phone)
                client.sign_in(phone, input('40779'))

            chats = []
            last_date = None
            chunk_size = 200
            groups = []

            result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash=0
            ))
            chats.extend(result.chats)

            for chat in chats:
                try:
                    if chat.megagroup == True:
                        groups.append(chat)
                except:
                    continue


            try:
                print('Which Group Do You Want To Scrape Members From: ')
                i=0

                for g in groups:
                    g.title = g.title.encode('utf-8')
                    g.title = g.title.decode('ascii', 'ignore')
                    print(f'[Group]: {str(g.title)} [Id]: {str(g.id)}')
                    i+=1

                if g_scrape_id == '':        
                    g_scrape_id = input("Please! Enter the group to scrape id: ").strip()

                for group in groups:
                    if str(group.id) == g_scrape_id:      
                        target_group_scrape = group

                print('Fetching Members...')
                all_participants_to_scrape = []
                all_participants_to_scrape = client.get_participants(target_group_scrape, aggressive=True)

                print('Saving In file...')

                with open(os.path.join(os.getcwd(), 'Scraped.json'), 'w+') as f:
                    users = []
                    jsonuser = {}
                    for user in all_participants_to_scrape:
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

                users = []
                with open(os.path.join(os.getcwd(), 'Scraped.json'), "r", encoding='utf-8', errors='ignore') as f:
                    list = json.load(f, strict=False)
                    for dict in list:
                        user = {}
                        user['username'] = dict['username']
                        user['id'] = dict['id']
                        user['access_hash'] = dict['access_hash']
                        user['name'] = dict['name']
                        users.append(user)

            except Exception as e:
                print(e)

            print('Choose a group to add members:')
            i = 0
            for group in groups:
                group.title = group.title.encode('utf-8')
                group.title = group.title.decode('ascii', 'ignore')
                print(f'[Group]: {str(group.title)} [Id]: {str(group.id)}')
                i += 1

            if g_id == '':
                g_id = input("Enter the group Id: ")

            for group in groups:
                if g_id == str(group.id):
                    target_group = group

            #Start of scrappe members from that group to avoid repetition

            try:
                all_participants = []
                all_participants = client.get_participants(target_group, aggressive=True)

                scrapedusers = []
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
                    scrapedusers.append(jsonuser.copy())

                print('Members scraped successfully.......')
            except:
                print('Error scrapping members of this group. Danger of false positives.')

            #End of scrappe members of that group to avoid repetition

            target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

            # mode = int(input("Enter 1 to add by username or 2 to add by ID: "))
            mode = 2

            n = 0

            try:
                with open(os.path.join(os.getcwd(), 'tried.json'), 'r') as file:
                    tried = json.load(file)
            except:
                tried = []

            for user in users:
                if AMMOUNT_OF_FLOOD_ERROS > 10:
                    print('UPS, GOT 10 FLOOD ERRORS, SWITCHING TO THE NEXT ACCOUNT')
                    break
                if AMMOUNT_OF_USERS_ADDED >= 45:
                    print('GREAT! ADDED 45 USERS WITH THIS NUMBER TODAY. SWITCHING TO THE NEXT ACCOUNT')
                    break
                if user not in scrapedusers:
                    if user not in tried:
                        tried.append(user.copy())
                        with open(os.path.join(os.getcwd(), 'tried.json'), 'w+') as file:
                            json.dump(tried, file, indent=2)
                        try:
                            n += 1
                            if n % 80 == 0:
                                sleep(60)
                            try:
                                print("Trying to add user {}".format(user['id']))
                                if mode == 1:
                                    if user['username'] == "":
                                        continue
                                    user_to_add = client.get_input_entity(user['username'])
                                elif mode == 2:
                                    user_to_add = InputPeerUser(user['id'], user['access_hash'])
                                else:
                                    sys.exit("Invalid Mode Selected. Please Try Again.")
                                client(InviteToChannelRequest(target_group_entity, [user_to_add]))
                                print("Waiting for 60-180 Seconds...")
                                time.sleep(random.randrange(60, 90))
                            except PeerFloodError:
                                AMMOUNT_OF_FLOOD_ERROS += 1
                                print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
                                print("Waiting {} seconds".format(SLEEP_TIME_2))
                                time.sleep(SLEEP_TIME_2)
                                continue #continues adicionado por mim
                            except UserPrivacyRestrictedError:
                                print("The user's privacy settings do not allow you to do this. Skipping.")
                                print("Waiting for 5 Seconds...")
                                time.sleep(random.randint(0, 5)) #Alterei, antes era randrange(5,0)
                                continue # adicionado por mim
                            except UserNotMutualContactError:
                                continue
                            except UserChannelsTooMuchError:
                                print('This user is already in too many channels/supergroups.')
                                continue
                            except Exception as e:
                                # traceback.print_exc()
                                print(f"Unexpected Error: {e}")
                                continue
                            AMMOUNT_OF_USERS_ADDED += 1

                            try:
                                with open(os.path.join(os.getcwd(), 'added.json'), 'r') as file:
                                    added = json.load(file)
                                    added.append(user.copy())
                            except:
                                added = []

                            with open(os.path.join(os.getcwd(), 'added.json'), 'w+') as file:
                                json.dump(added, file, indent=2)
                                try:
                                    print(f'User {user["name"]} with id: {user["id"]} has been sucessfully added to your group.')
                                except UnicodeEncodeError:
                                    print(f'User with id: {user["id"]} has been sucessfully added your group.')

                        except Exception as e:
                            print(f'An unnespected error ocureed: {e}')

                    else:
                        print(f'This user has been checked by me before. Skipping. If you want o erase data, delete "tried.json".')
                else:
                    print('This user already is in this group. Skipping.')
        except Exception as e:
            e = str(e)
            print(e)
            try:
                client.disconnect()
            except:
                print('Unable to disconnect client')
                time.sleep(30000)
            if 'database' in e:
                print('The last time program was executed it was not closed properly. Please delete the .session files and restart the program.')
                time.sleep(30000)
                try:
                    client.disconnect()
                except:
                    print('Unable to disconnect client')

        try:
            client.disconnect()
        except:
            print('Unable to disconnect client')

