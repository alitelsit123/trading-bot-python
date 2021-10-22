from selenium.webdriver import Opera
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import math

def countdown(timeout):
    pause = timeout
    while(pause >= 0):
        pause_countdown = str(pause)
        if(pause<10):
            pause_countdown = '0'+str(pause)
            
        print('Refresh in ' + str(pause_countdown), end='\r', flush=True)
        time.sleep(1)
        pause=pause-1

def auth(driver):
    email = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'email')))
    password = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'password')))
    submit = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.MuiButtonBase-root.MuiButton-root.MuiButton-text.css-f9d9mt.e11y3lm80')))
    email.send_keys('hikmalkoko3@gmail.com');
    password.send_keys('1234Abcde@#$_');
    submit.click();
    return driver

def getCurrentPrice(driver):
    BID = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.instrument-table__value.instrument-table__value--hideable.instrument-table__value--bid')))
    ASK = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.instrument-table__value.instrument-table__value--hideable.instrument-table__value--ask')))
    CLOSE_PRICE = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.instrument-table__value.instrument-table__value--hideable.instrument-table__value--ask')))
    return {
        'bid': BID.text,
        'ask': ASK.text,
        'recent_trade': '0'
    }

def getMyOrders(driver, type='open'):
    if type == 'open':
        tab_selector = 'div.ap-tab__menu-item.ap-tab__menu-item--active.order-history__menu-item.order-history__menu-item--active.ap-tab__menu-item.order-history__menu-item'
        tab = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, tab_selector)
            )
        )
        tab.click()

        tab_content_selector = '.ap-tab__tab-content.order-history__tab-content'
        tab_content = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, tab_content_selector)
            )
        )

        header_selector = '.flex-table__header-cell.flex-table__header-cell--absolute.order-history-table__fixed'
        header_contents = tab_content.find_elements(By.CSS_SELECTOR, header_selector)
        header_content_results = []
        for el in header_contents:
            header_content_results.append(el.text)

        value_selector = '.flex-table__column.order-history-table__column'
        value_contents = tab_content.find_elements(By.CSS_SELECTOR, value_selector)
        value_content_results = []
        for el in value_contents:
            value_content_results.append(el.text)

        result = dict(zip(header_content_results, value_content_results))
        if len(result) > 0:
            result['type'] = result['Posisi']
            return result
        else:
            return {}
    return {}

def getCurrentTradeStatus(driver):
    my_orders = getMyOrders(driver=driver, type='open')
    if len(my_orders) > 0:
        return 'pending'

def sell(driver, limit_up, limit_bottom, last_price):
    limit_price_selector = '#root > div.App.fluid.container > div.trading-layout__container > div.trading-layout__right-column > div.trading-layout__order-entry > div > div > div.order-entry__buy-sell-container > form:nth-child(2) > div:nth-child(1) > div.form-group.ap-input__input-wrapper.order-entry__limit-price.order-entry__input-wrapper.false > div > div > div.ant-input-number-input-wrap > input'
    limit_price = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, limit_price_selector)))

    amount_selector = '#root > div.App.fluid.container > div.trading-layout__container > div.trading-layout__right-column > div.trading-layout__order-entry > div > div > div.order-entry__buy-sell-container > form:nth-child(2) > div:nth-child(1) > div.ap-segmented-button__sb-container.order-entry__balance-share__sb-container > div'
    amounts = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, amount_selector)))
    amount_buttons = amounts.find_elements(By.CSS_SELECTOR, 'label')
    # for el in amount_buttons:

    # INPUT LIMIT
    limit_price.send_keys(Keys.CONTROL + 'a')
    limit_price.send_keys(Keys.DELETE)
    mean = (int(limit_up) + int(limit_bottom)) / 2
    final_limit = math.ceil((int(limit_up) + mean) / 2)
    if final_limit > last_price:
        limit_price.send_keys(str(final_limit))
    else:
        limit_price.send_keys(str(last_price+40))
    amount_buttons[-1].click()

    if len(limit_price.get_attribute('value')) == 5:
        submit_selector = '#root > div.App.fluid.container > div.trading-layout__container > div.trading-layout__right-column > div.trading-layout__order-entry > div > div > div.order-entry__buy-sell-container > form:nth-child(2) > div:nth-child(2) > button'
        submit = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_selector)))
        submit.click()

def buy(driver, limit_up, limit_bottom):
    limit_price_selector = '#root > div.App.fluid.container > div.trading-layout__container > div.trading-layout__right-column > div.trading-layout__order-entry > div > div > div.order-entry__buy-sell-container > form:nth-child(1) > div:nth-child(1) > div.form-group.ap-input__input-wrapper.order-entry__limit-price.order-entry__input-wrapper.false > div > div > div.ant-input-number-input-wrap > input'
    limit_price = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, limit_price_selector)))

    amount_selector = '#root > div.App.fluid.container > div.trading-layout__container > div.trading-layout__right-column > div.trading-layout__order-entry > div > div > div.order-entry__buy-sell-container > form:nth-child(1) > div:nth-child(1) > div.ap-segmented-button__sb-container.order-entry__balance-share__sb-container > div'
    amounts = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, amount_selector)))
    amount_buttons = amounts.find_elements(By.CSS_SELECTOR, 'label')
    # for el in amount_buttons:

    # INPUT LIMIT
    limit_price.send_keys(Keys.CONTROL + 'a')
    limit_price.send_keys(Keys.DELETE)
    mean = (int(limit_up) + int(limit_bottom)) / 2
    final_limit = math.ceil((int(limit_bottom) + mean) / 2)
    limit_price.send_keys(str(final_limit-5))        
    amount_buttons[-1].click()

    submit_selector = '#root > div.App.fluid.container > div.trading-layout__container > div.trading-layout__right-column > div.trading-layout__order-entry > div > div > div.order-entry__buy-sell-container > form:nth-child(1) > div:nth-child(2) > button'
    submit = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_selector)))
    submit.click()
    return final_limit

def recentTrades(driver):
    container_selector = '.recent-trade__container'
    container = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, container_selector)
        )
    )
    body_selector = '.flex-table__body recent-trades__body'
    body = container.find_element(By.CSS_SELECTOR, '.flex-table__body.recent-trades__body')

    price_row_selector = '.flex-table__row.recent-trades__row'
    price_row = body.find_elements(By.CSS_SELECTOR, price_row_selector)
    results = []
    for row in price_row:
        price_column_selector = '.flex-table__column.recent-trades__column'
        price_column = row.find_element(By.CSS_SELECTOR, price_column_selector)
        wrapper = price_column.find_element(By.CSS_SELECTOR, 'div')
        buy_class = 'recent-trades__table-price recent-trades__table-price--buy'
        sell_class = ''
        current_price_is = wrapper.get_attribute('class')
        if current_price_is == buy_class:
            price_result_selector = 'span.ap-padded-decimal__units--buy'
            price_result = price_column.find_element(By.CSS_SELECTOR, price_result_selector)
            results.append({
                'type': 'buy',
                'price': price_result.text
            })
        else:
            price_result_selector = 'span.ap-padded-decimal__units--sell'
            price_result = price_column.find_element(By.CSS_SELECTOR, price_result_selector)
            results.append({
                'type': 'sell',
                'price': price_result.text
            })
    return results



def run():
    driver = Opera()
    currentBid = ''
    currentAsk = ''
    alive = True
    last_trade_type = 'buy'
    last_price = 0

    driver.get('https://trade.zipmex.co.id')
    authenticated = auth(driver=driver)
    
    if authenticated:
        print('Authenticated!')
        time.sleep(10)
    else:
        print('Unauthenticated!')

    driver.get('https://trade.zipmex.co.id/trade/USDTIDR')    
    
    time.sleep(10)

    last_trade_type = input('(buy) / (sell)')

    refresh_at = 30
    
    while(alive):
        if refresh_at <= 0:
            driver.execute_script('location.reload()')
            refresh_at = 30
            time.sleep(10)
            continue
        os.system('cls')
        current_price = getCurrentPrice(driver=driver)
        print('OPTION')
        print('Bid: {}\nAsk: {}\n'.format(current_price['bid'], current_price['ask']))
        
        my_orders = getMyOrders(driver=driver, type='open')
        if len(my_orders) > 0:
            print('MY ORDER')
            for order in my_orders:
                print('{}: {}'.format(order, my_orders[order]))
            print('Not time to Trade!')
        else:
            print('PLACING ORDER TYPE ({})'.format(last_trade_type))
            trade_result = 0
            final_limit_bottom = current_price['bid'].replace(',', '')
            final_limit_up = current_price['ask'].replace(',', '')
            if last_trade_type == 'buy':
                sell(driver=driver, limit_up=final_limit_up, limit_bottom=final_limit_bottom, last_price=last_price)
                last_trade_type = 'sell'
            elif last_trade_type == 'sell':
                lp = buy(driver=driver, limit_up=final_limit_up, limit_bottom=final_limit_bottom)
                last_price = lp
                last_trade_type = 'buy'
            print('Successed!')
        print('')

        recent_trades = recentTrades(driver=driver)
        filtered_recent_trades = {
            'buy': '',
            'sell': ''
        }
        for trade in recent_trades:
            if trade['type'] == 'buy':
                if filtered_recent_trades['buy'] == '':
                    filtered_recent_trades['buy'] = trade['price']
            elif trade['type'] == 'sell':
                if filtered_recent_trades['sell'] == '':
                    filtered_recent_trades['sell'] = trade['price']
            if not filtered_recent_trades['buy'] and not filtered_recent_trades['sell']:
                break;

        # print('RECENT TRADE')
        # for frt in filtered_recent_trades:
        #     print('{}: {}'.format(frt, filtered_recent_trades[frt]))
        countdown(timeout=10)
        refresh_at-=1
run()
