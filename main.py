#!/usr/bin/python
# -*- coding: latin-1 -*-

from serial_bot.goty_downloader import Scrubber
from selenium.common.exceptions import WebDriverException


def script_summary() -> None:
    print('''
        This Program will help you download serial from gotytv.com.\n
        No need for installation.\n
        First, you have to visit https://www.gotytv.com and create an account; it's free.\n
        Then you can run the goty_downloader.exe file and follow the instructions.\n
        Please make sure you keep this window (the command prompt) open and you don't disturb the browser window\n
        that opens after you have typed your password. After typing your password and pressing enter\n
        you will have 15 seconds to handle the captcha thing also known as 'I am not a robot'.\n
        You click on 'I am not a robot' and then you select all the necessary images and click\n
        'verify' or 'skip' depending on what it shows. Then you wait for the program to automatically\n
        log you in and give you your download options from which to choose your preferred download e.g\n
        'Trailer' or 'Episode' or 'Season' etc. 
    ''')


def goty_droid(user_name: str, password: str) -> None:
    try:

        with Scrubber() as machine:
            machine.launch_goty_tv()
            machine.login(user_name, password)
            machine.handle_download_choices()

    except Exception as e:
        if 'in PATH' in str(e):
            print(''''
                Please make sure you have not deleted or moved the folder named Selenium Drivers.
                The programme needs the chromedriver.exe inside of in order to function. If you
                still get this error, then you need to download the chromedriver for your version
                of Chrome. There are many videos online about how to get that set up.
                ''')
            input('Press Enter To Exit.')

        elif 'INTERNET' in str(e):
            print(''''
                Please make sure you are connected to the internet and Try again.
                Cheers!
                ''')
            input('Press Enter To Exit.')

        elif WebDriverException:
            print('\nSomething went wrong, please make sure you do not disturb the Chrome window while it works when '
                  'you try again.')

        else:
            raise


def main():
    script_summary()
    user_name = input('Enter your Username: ')
    password = input('Enter your Password: ')
    goty_droid(user_name, password)


if __name__ == '__main__':
    main()
