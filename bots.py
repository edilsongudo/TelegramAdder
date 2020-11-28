from adder import adder
from scrapper import scrapper
from addermulti import addermulti
import time

while True:
	try:
		resposta = input('Which program do you want to execute?\n[1] - Scrape members of a group to add later\n[2] - Add scraped members to a group\n[3] - Add users with two or more Telegram accounts\nAnswer: ')
		if resposta == '1':
			try:
				scrapper()
			except Exception as e:
				print(e)
				# time.sleep(3600)
			# break
		elif resposta == '2':
			try:
				adder()
			except Exception as e:
				print(e)
				# time.sleep(3600)
			# break
		elif resposta == '3':
			try:
				addermulti()
			except Exception as e:
				print(e)
				# time.sleep(3600)
			# break
		else:
		    print('')
		    print('============== PLEASE TYPE 1 OR 2 ===========')
		    print('')
	except Exception as e:
		print(e)
		time.sleep(3600)

        
    
