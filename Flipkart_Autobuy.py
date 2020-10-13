import os
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from configparser import RawConfigParser
from colorama import Fore, init, deinit
from emai import Gmail_Otp
init()



#from os heroku
CONFIG = RawConfigParser()
CONFIG.read('config.ini')
driver_path = CONFIG.get('MAIN', 'DRIVER_LOCATION')
email_inp = CONFIG.get('CREDENTIALS', 'USERNAME')
pass_inp = CONFIG.get('CREDENTIALS', 'PASSWORD')
email = CONFIG.get('Email', 'Emailid')
Pass = CONFIG.get('Email', 'Password')
order_link = CONFIG.get('ORDER', 'LINK')
cvv_inp = CONFIG.get('ORDER', 'CVV')
addr_input = CONFIG.get('ORDER', 'ADDRESS')
pay_opt_input = CONFIG.get('ORDER', 'PAYMENT')
bankname_input = CONFIG.get('EMIOPTIONS', 'BANK')
tenure_input = CONFIG.get('EMIOPTIONS', 'TENURE')
frequency = 2500
duration = 2000



def prCyan(skk):
    print(Fore.CYAN + skk)


def prRed(skk):
    print(Fore.RED + skk)


def prGreen(skk):
    print(Fore.GREEN + skk)


def prYellow(skk):
    print(Fore.YELLOW + skk)



prRed('Opening Link in chrome..........')
prCyan('\n')
print('\nLogging in with username:', email_inp)
prYellow('\n')

driver = webdriver.Chrome(driver_path)

driver.maximize_window()
driver.get(order_link)
prCyan('\n')

def login():
    try:
        prYellow('Logging In..\n')
        try:
            login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._3Ep39l')))
            prYellow('Login Button Clickable\n')
        except:
            prYellow('Login Button Not Clickable\n')
        login.click()
        prYellow('Login Button Clicked Successfully\n')
    except:
        prRed('login Failed. Retrying.')
        time.sleep(0.5)
        login()


def login_submit():
    try:
        if 'Enter Password' in driver.page_source:
            print('Trying Usual method of Login.')
            email = driver.find_element_by_css_selector('.Km0IJL ._2zrpKA')
            passd = driver.find_element_by_css_selector('.Km0IJL ._3v41xv')
            email.clear()
            passd.clear()
            email.send_keys(email_inp)
            passd.send_keys(pass_inp)
            try:
                form = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.Km0IJL ._7UHT_c')))
                prCyan('Submit Button Clickable')
            except:
                prRed('Submit Button Not Clickable')
            else:
                form.click()
                prYellow('\nPress any key when login is done and your name appeares in menu bar.')
                time.sleep(4)
                prGreen('\nLogged in successully.')
    except:
        if 'Login &amp; Signup' not in driver.page_source and 'Login & Signup' not in driver.page_source:
            print('Logged in Manually.')
        else:
            prRed('login_submit Failed. Please login manually.')
            time.sleep(1)
            login_submit()

def buy_check():
    try:
        nobuyoption = True
        while nobuyoption:
            try:
                driver.refresh()
                time.sleep(0.2)
                buyprod = driver.find_element_by_css_selector('._1k1QCg ._7UHT_c')
                prYellow('Buy Button Clickable')
                nobuyoption = False
            except:
                nobuyoption = True
                prRed('Buy Button Not Clickable')

        buyprod.click()
        prYellow('Buy Button Clicked Successfully')
        buy_recheck()
    except:
        prRed('buy_check Failed. Retrying.')
        time.sleep(0.5)
        buy_check()


def buy_recheck():
    try:
        WebDriverWait(driver, 4).until(EC.title_contains('Secure Payment'))
        prYellow('Redirected to Payment')
    except:
        prRed('Error in Redirecting to Payment')
        time.sleep(0.5)
        buy_recheck()


def deliver_option():
    try:
        addr_input_final = "//label[@for='" + addr_input + "']"
        try:
            sel_addr = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, addr_input_final)))
            prYellow('Address Selection Button Clickable')
        except:
            prRed('Address Selection Button Not Clickable')
        else:
            sel_addr.click()
            prYellow('Address Selection Button Clicked Successfully')
    except:
        prRed('deliver_option Failed. Retrying.')


def deliver_continue():
    try:
        addr_sal_avl = True
        while addr_sal_avl:
            try:
                address_sel = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._3K1hJZ ._7UHT_c')))
                address_sel.click()
                addr_sal_avl = False
                print('Address Delivery Button Clickable')
            except:
                addr_sal_avl = True
                print('Address Delivery Button Not Clickable')

        print('Address Delivery Button Clicked Successfully')
    except:
        print('deliver_continue Failed. Retrying.')

def order_summary_continue():
    try:
        press_continue = driver.find_element_by_css_selector('._2Q4i61')
        press_continue.click()
        prYellow('Continue Button Clicked Successfully')
    except:
        prRed('order_summary_continue Failed. Retrying.')


def choose_payment():
    try:
        pay_opt_input_final = "//label[@for='" + pay_opt_input + "']"
        pay_method_sel = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, pay_opt_input_final)))
        pay_method_sel.click()
        if pay_opt_input == 'WALLET':
            WALLET_captcha()
        else:
            print("Payment Method not set")
        prGreen('Payment Method Selected Successfully')
    except:
        WALLET_captcha()


def WALLET_captcha():
    try:
        payment_sel = None
        payment_sel = driver.find_element_by_xpath("//*[@class='_1p7h2j _35T3ar']")
        payment_sel.click()
    except:
        prRed('\nCaptcha could not be entered. Plese type manually on webpage.')


def OTP_send():
    time.sleep(6)
    n = Gmail_Otp(email,Pass)
    digits = [int(x) for x in str(n)]

    one = digits[0]
    two = digits[1]
    tree = digits[2]
    four = digits[3]
    five = digits[4]
    six = digits[5]

    num1 = driver.find_element_by_xpath("//*[@id='container']/div/div[1]/div/div/div[2]/div[1]/div/div[1]/input")
    num2 = driver.find_element_by_xpath("//*[@id='container']/div/div[1]/div/div/div[2]/div[1]/div/div[2]/input")
    num3 = driver.find_element_by_xpath("//*[@id='container']/div/div[1]/div/div/div[2]/div[1]/div/div[3]/input")
    num4 = driver.find_element_by_xpath("//*[@id='container']/div/div[1]/div/div/div[2]/div[1]/div/div[4]/input")
    num5 = driver.find_element_by_xpath("//*[@id='container']/div/div[1]/div/div/div[2]/div[1]/div/div[5]/input")
    num6 = driver.find_element_by_xpath("//*[@id='container']/div/div[1]/div/div/div[2]/div[1]/div/div[6]/input")

    num1.send_keys(one)
    num2.send_keys(two)
    num3.send_keys(tree)
    num4.send_keys(four)
    num5.send_keys(five)
    num6.send_keys(six)
    driver.find_element_by_xpath("//*[@class='_2AkmmA _1Dq39F _1eFTEo']").click()
    time.sleep(5)
    driver.find_element_by_xpath("//*[@class='_2AkmmA _3jZEfz _7UHT_c']").click()
    prGreen('\nOrder confirmed successfully')
    driver.quit()
   

def try_till_otp():
    login()
    login_submit()
    buy_check()
    order_summary_continue()
    choose_payment()
    OTP_send()


if __name__ == '__main__':
    try_till_otp()
