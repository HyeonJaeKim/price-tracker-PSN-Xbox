import time
import requests
from bs4 import BeautifulSoup
import traceback
import random
import re

#tracks prices on PSN's store
def PSN_price_tracker(game, url):
    #header
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    store_link = url

    #game is on sale
    try:
        price = soup.find('h3','price-display__price').text
        discount = '−' + soup.find('span','discount-badge__message').text.replace('SAVE ','')

        #if there is only a PS+ discount present, ignore it
        if soup.find('div','discount-badge-plus discount-badge-plus__large'):
            discount = '0%'
            print(game + ': not on sale')

        elif soup.find('div','discount-badge-normal discount-badge-normal__large'):
            print(game + ': on sale')
            print(price + '(' + discount + ')')

        else:
            raise AttributeError

    #game is not on sale
    except AttributeError:
        price = ''
        discount = '0%'
        print(game + ': not on sale')

    #parts of the title and chart, the minus in discount must be replaced with a hyphen
    title_part = game + " for " + price + " (" + discount + ")"
    chart_row = "\n[" + game + "](" + store_link + ") | " + price + " | " + discount

    game_info_list = [title_part, chart_row]
    no_discount_game_info_list = ['', '']

    if discount != '0%':
        return game_info_list

    else:
        return no_discount_game_info_list

#tracks prices on Xbox's store
def Xbox_price_tracker(game, url):
    #header
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    store_link = url

    #game is on sale
    try:
        price = soup.find('span','price-disclaimer').span.text.replace('+','')
        discount = '−' + soup.find('span','sub').text.replace(' off','')
        print(game + ': on sale')
        print(price + '(' + discount + ')')

    #game is not on sale
    except AttributeError:
        price = ''
        discount = '0%'
        print(game + ': not on sale')

    #parts of the title and chart, the minus in discount must be replaced with a hyphen
    title_part = game + " for " + price + " (" + discount + ")"
    chart_row = "\n[" + game + "](" + store_link + ") | " + price + " | " + discount

    game_info_list = [title_part, chart_row]
    no_discount_game_info_list = ['', '']

    if discount != '0%':
        return game_info_list

    else:
        return no_discount_game_info_list

#compiles the resuls of the price trackers
def sale_compiler(store, delay_factor, url1, url2, url3, url4, url5, url6, url7):
    if store == 'PSN':
        DMC5_list = PSN_price_tracker('DMC5', url1)
        time.sleep(60*delay_factor)
        DMC5_Deluxe_list = PSN_price_tracker('DMC5:DE', url2)
        time.sleep(60*delay_factor)
        DMC4_list = PSN_price_tracker('DMC4:SE', url3)
        time.sleep(60*delay_factor)
        DHB_list = PSN_price_tracker('DMC4:SE DH Bundle', url4)
        time.sleep(60*delay_factor)
        HD_list = PSN_price_tracker('DMC HD Collect.', url5)
        time.sleep(60*delay_factor)
        DMCHD_DMC4_list = PSN_price_tracker('DMC HD Collect. & DMC4:SE Bundle', url6)
        time.sleep(60*delay_factor)
        DmC_list = PSN_price_tracker('DmC:DE', url7)


    elif store == 'Xbox':
        DMC5_list = Xbox_price_tracker('DMC5', url1)
        time.sleep(60*delay_factor)
        DMC5_Deluxe_list = Xbox_price_tracker('DMC5:DE', url2)
        time.sleep(60*delay_factor)
        DMC4_list = Xbox_price_tracker('DMC4:SE', url3)
        time.sleep(60*delay_factor)
        DHB_list = Xbox_price_tracker('DMC4:SE DH Bundle', url4)
        time.sleep(60*delay_factor)
        HD_list = Xbox_price_tracker('DMC HD Collect.', url5)
        time.sleep(60*delay_factor)
        DMCHD_DMC4_list = Xbox_price_tracker('DMC HD Collect. & DMC4:SE Bundle', url6)
        time.sleep(60*delay_factor)
        DmC_list = Xbox_price_tracker('DmC:DE', url7)

    super_list = [DMC5_list, DMC5_Deluxe_list, DMC4_list, DHB_list, HD_list, DMCHD_DMC4_list, DmC_list]

    return super_list

#sets the title and time limit
def time_limit_setter(title_and_date, log):
    new_time_limit = open('logs/'+log+'_limit.txt', 'w', encoding='utf-8')
    new_time_limit.write(title_and_date)
    new_time_limit.close()

#constructs title and chart, announces sales
def announce_sales(store, region):
    log = store + '-' + region
    print(log)
    print('----------------------------------------------------------------')

    if store == 'PSN':

        if region == 'NA':
            super_list = sale_compiler(store, 2, 'https://store.playstation.com/en-us/product/UP0102-CUSA08216_00-DMC5000000000001', 'https://store.playstation.com/en-us/product/UP0102-CUSA08216_00-DMC5BUNDLE000001', 'https://store.playstation.com/en-us/product/UP0102-CUSA01671_00-MAINRDOBXXXX0000', 'https://store.playstation.com/en-us/product/UP0102-CUSA01671_00-MAINRDOBXXXX0009', 'https://store.playstation.com/en-us/product/UP0102-CUSA09407_00-DMCHDC0000000000', 'https://store.playstation.com/en-us/product/UP0102-CUSA09407_00-DMCHDC4SEBUNDLE0', 'https://store.playstation.com/en-us/product/UP0102-CUSA01013_00-DMCDEFINITIVE000')

        elif region == 'EU':
            super_list = sale_compiler(store, 2, 'https://store.playstation.com/en-gb/product/EP0102-CUSA08161_00-DMC5BUNDLE000005', 'https://store.playstation.com/en-gb/product/EP0102-CUSA08161_00-DMC5BUNDLE000006', 'https://store.playstation.com/en-gb/product/EP0102-CUSA01708_00-MAINRDOBXXXX0000', 'https://store.playstation.com/en-gb/product/EP0102-CUSA01708_00-MAINRDOBXXXX0009', 'https://store.playstation.com/en-gb/product/EP0102-CUSA09263_00-DMCHDC0000000000', 'https://store.playstation.com/en-gb/product/EP0102-CUSA09263_00-DMCHDC4SEBUNDLE0', 'https://store.playstation.com/en-gb/product/EP0102-CUSA01022_00-DMCDEFINITIVE000')

    elif store == 'Xbox':

        if region == 'NA':
            super_list = sale_compiler(store, 2, 'https://www.microsoft.com/en-us/p/devil-may-cry-5/c1ngmg14j5p2#activetab=pivot:overviewtab', 'https://www.microsoft.com/en-us/p/devil-may-cry-5-deluxe-edition/c2tq3t171b8j#activetab=pivot:overviewtab', 'https://www.microsoft.com/en-us/p/devil-may-cry-4-special-edition/BPZT3CQCCWKG?activetab=pivot%3aoverviewtab', 'https://www.microsoft.com/en-us/p/dmc4se-demon-hunter-bundle/bp1gzs0z6g58?activetab=pivot%3aoverviewtab', 'https://www.microsoft.com/en-us/p/devil-may-cry-hd-collection/bvnrff9xj6km?activetab=pivot%3aoverviewtab', 'https://www.microsoft.com/en-us/p/devil-may-cry-hd-collection-4se-bundle/bt259h6m8l07#activetab=pivot:overviewtab', 'https://www.microsoft.com/en-us/p/dmc-devil-may-cry-definitive-edition/c27lhb0dh095?activetab=pivot%3aoverviewtab')

        elif region == 'EU':
            super_list = sale_compiler(store, 2, 'https://www.microsoft.com/en-gb/p/devil-may-cry-5/bnlg5j5kdvj3#activetab=pivot:overviewtab', 'https://www.microsoft.com/en-gb/p/devil-may-cry-5-deluxe-edition/c2tq3t171b8j#activetab=pivot:overviewtab', 'https://www.microsoft.com/en-gb/p/devil-may-cry-4-special-edition/bpzt3cqccwkg?activetab=pivot%3aoverviewtab', 'https://www.microsoft.com/en-gb/p/dmc4se-demon-hunter-bundle/bp1gzs0z6g58?activetab=pivot%3aoverviewtab', 'https://www.microsoft.com/en-gb/p/devil-may-cry-hd-collection/bvnrff9xj6km?activetab=pivot:overviewtab', 'https://www.microsoft.com/en-gb/p/devil-may-cry-hd-collection-4se-bundle/bt259h6m8l07#activetab=pivot:overviewtab', 'https://www.microsoft.com/en-gb/p/dmc-devil-may-cry-definitive-edition/c27lhb0dh095?activetab=pivot%3aoverviewtab')

    title= "[" + log + "] "
    chart = """Game |Price | Discount
    ---|---|----|----"""

    #used to check if there is a discount present
    title_test_value = title[:-3]

    #creates the title and chart
    for list in super_list:
        if list[0] != '':
            title += list[0] + ' | '
            chart += list[1]

    #removes the extra ' | ' from the end
    title = title[:-3]
    chart += "\n\n___\n\n^(This bot was created by moderator SuperNeroEX. Learn how to use the bot by reading the guide linked on the sidebar. To remove, downvote.)"

    #get current UNIX time
    current_time_utc = int(time.time())

    #get time limit log of store/region
    time_limit = open('logs/' + log + '_limit.txt').read().split(' , ')

    #accounts for change from utf-8 to unicode and spacing, also has hyphen used in place of minus
    converted_title = time_limit[0].replace('Â£','£').replace("âˆ’",'−')
    converted_status = time_limit[2].strip()

    if title == title_test_value:
        unchanged_title_and_date = title + ' , ' + time_limit[1] + ' , waiting'
        print('Status: ' + converted_status)
        print('Able to post again after ' + time.strftime("%I:%M:%S %p %m-%d-%Y", time.localtime(int(time_limit[1]))))
        print('----------------------------------------------------------------')

        time_limit_setter(unchanged_title_and_date, log)

    elif title != title_test_value:

        if title != converted_title:
            print('Updated: ' + title)

        print('Current: ' + converted_title)

        #forces bot to wait for 2 hours until all games on the tracker site have been updated
        if title != converted_title and converted_status == 'waiting':
            print('started updating prices.')
            waiting_title_and_date = converted_title + ' , ' + str(current_time_utc + (60*60*2)) + ' , updating'
            print(waiting_title_and_date)

            time_limit_setter(waiting_title_and_date, log)

        #posts updated prices
        if current_time_utc > int(time_limit[1]) and converted_status == 'updating':

            #clears the old title and records a new time limit, which is current time plus 7 days minus delay time
            #while testing, 10 minutes or less
            new_title_and_date = title + ' , ' + str(current_time_utc + (60*60*24*7) - (60*60*2)) + ' , waiting'
            print(new_title_and_date)

            time_limit_setter(new_title_and_date, log)

        #reposts prices
        elif title == converted_title and current_time_utc > int(time_limit[1]):
            print('reposting prices to the subreddit.')

            #clears the old title and records a new time limit, which is current time plus 1 week
            #while testing, 10 minutes or less
            new_title_and_date = title + ' , ' + str(current_time_utc + 60*60*24*7) + ' , waiting'
            print(new_title_and_date)

            time_limit_setter(new_title_and_date, log)

        time_limit = open('logs/' + log + '_limit.txt').read().split(' , ')
        print('Status: ' + converted_status)
        print('Able to post again after ' + time.strftime("%I:%M:%S %p %m-%d-%Y", time.localtime(int(time_limit[1]))))
        print('----------------------------------------------------------------')

def get_status(store, region):
    time_limit = open('logs/'+ store + '-' + region +'_limit.txt').read().split(' , ')
    converted_status = time_limit[2].strip()

    return converted_status

#Starts the entire process of looking for sales
def sales(status):
    #the last time the prices were checked
    last_run_time_NA = int(open('logs/NA_limit.txt').read())
    last_run_time_EU = int(open('logs/EU_limit.txt').read())

    #status of store prices
    status_PSN_NA = get_status('PSN', 'NA')
    status_Xbox_NA = get_status('Xbox', 'NA')
    status_PSN_EU = get_status('PSN', 'EU')
    status_Xbox_EU = get_status('Xbox', 'EU')

    checked_for_sale = False

    #if there's a sale, indicated by the status == 'updating', checks in 2.25 hours
    if status_PSN_NA == 'updating' or status_Xbox_NA == 'updating':

        if current_time_utc > (last_run_time_NA + (60*60*2.25)):

            if status == 'ON':
                announce_sales('PSN', 'NA')

            #prevents error from posting again too soon
            if status_PSN_NA == 'updating' and status_Xbox_NA == 'updating':
                time.sleep(60*15)

            if status == 'ON':
                announce_sales('Xbox', 'NA')

            time_limit_setter(str(current_time_utc), 'NA')

            checked_for_sale = True

    elif status_PSN_EU == 'updating' or status_Xbox_EU == 'updating':

        if current_time_utc > (last_run_time_EU + (60*60*2.25)):

            if status == 'ON':
                announce_sales('PSN', 'EU')

            #prevents error from posting again too soon
            if status_PSN_EU == 'updating' and status_Xbox_EU == 'updating':
                time.sleep(60*15)

            if status == 'ON':
                announce_sales('Xbox', 'EU')

            time_limit_setter(str(current_time_utc), 'EU')

            checked_for_sale = True

    #otherwise, checks every 6 hours, alternating between regions
    elif current_time_utc > (last_run_time_NA + (60*60*6)) and (current_time_utc - last_run_time_EU) > (60*60*3):

        if status == 'ON':
            announce_sales('PSN', 'NA')
            announce_sales('Xbox', 'NA')

        time_limit_setter(str(current_time_utc), 'NA')

        checked_for_sale = True

    elif current_time_utc > (last_run_time_EU + (60*60*6)) and (current_time_utc - last_run_time_NA) > (60*60*3):

        if status == 'ON':
            announce_sales('PSN', 'EU')
            announce_sales('Xbox', 'EU')

        time_limit_setter(str(current_time_utc), 'EU')

        checked_for_sale = True

    if checked_for_sale is False or status == 'OFF':
        time.sleep(60*random.randint(4,10))


#restarts program if exception occurs
while True:

    try:
        print('Currently running at ' + time.strftime("%I:%M:%S %p %m-%d-%Y", time.localtime()))
        print('----------------------------------------------------------------')

        current_time_utc = int(time.time())

        #also controls delay, so change "ON" to "OFF" instead of commenting out or uncomment delay below
        sales('ON')

    except prawcore.exceptions.RequestException as e:
        print("There was an exception: {}".format(e))
        time.sleep(60)

    except Exception as e:
        print("There was an exception: {}".format(e))
        traceback.print_exc()
        time.sleep(60*random.randint(29,40))
