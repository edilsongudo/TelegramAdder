from adder import adder
from scrapper import scrapper

while True:
    resposta = input('Which program do you want to execute?\n[1] - Scrape members of a group to add later\n[2] - Add scraped members to a group\nAnswer: ')
    if resposta == '1':
        break
    elif resposta == '2':
        break
    else:
        print('')
        print('============== PLEASE TYPE 1 OR 2 ===========')
        print('')

if resposta == '1':
    scrapper()

if resposta == '2':
    adder()