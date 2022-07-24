import sys
from win32com.client import Dispatch
from serial_bot.goty_downloader import Scrubber
from selenium.common.exceptions import WebDriverException


def script_summary() -> None:
    print('''
    
               ***----------------------------------------------------------------------------------------***
         \t***------------------------ DUMELANG means GREETINGS! ~ G-CODE -----------------------***
                   \t***------------------------------------------------------------------------***\n
              
        \t"GOTY-DOWNLOADER" Version 1.1.0\n
        
        This Program will help you download serial and their trailers from gotytv.com.\n
        No need for installation.\n
        Firstly, you have to visit https://www.gotytv.com and create an account; it's free.\n
        Then you can run this "goty_downloader.exe" file and follow these instructions.\n
        Please make sure you keep this window (the command prompt) open and you don't disturb\n
        the browser window that opens after you have typed your password. After typing your\n
        password and pressing enter, you will have to handle the "Captcha" thing also known as\n
        'I am not a robot'. You click on 'I am not a robot' and then you select all the necessary\n
        images and click 'verify' or 'skip' depending on what it shows. Then you will be asked to\n
        type YES to continue. Then you wait for the program to automatically log you in and show\n
        you download options from which to choose your preferred method e.g 'Trailer' or 'Episode'\n
        or 'Season' etc.
        
        ''')


def goty_droid(user_name: str, password: str) -> None:

    try:

        with Scrubber() as machine:
            machine.launch_goty_tv()
            machine.login(user_name, password)
            machine.handle_download_choices()

    except Exception as e:
        if 'executable needs to be in PATH' in str(e):
            print('''
                       Please make sure you have not deleted or moved or renamed the "chromedriver.exe"

                       file that is next to the "Goty Downloader.exe". The programme needs it

                       to work.

                       ''')
            input('\nPress Enter To Exit.')
            sys.exit(1)

        elif 'version of ChromeDriver only supports Chrome version' in str(e):
            message: str = str(e).split('\n')[0].split(':')[-1]
            print(f'''
                      {message}.

                       You need to download the ChromeDriver for your version of Chrome.

                       Please refer to the information about GOOGLE CHROME & CHROME_DRIVER above. 

                       Once you are done downloading the ChromeDriver, you unzip it and then 

                       replace the current one by placing the new one in the same folder as

                       this "Goty Downloader.exe".

                   ''')
            input('\nPress Enter To Exit.')
            sys.exit(1)

        elif 'INTERNET' in str(e):
            print(''''
                Please make sure you are connected to the internet and Try again.
                Cheers!
                ''')
            input('\nPress Enter to Exit & Try Again.')
            sys.exit(1)

        elif WebDriverException:
            if 'version' in str(e):
                print('\nPlease make sure your version of Google Chrome is at least version 103.\n'

                      'Open your Chrome browser and go to "Menu -> Help -> About Google Chrome"\n'

                      'to update your web browser.\n')

            else:
                print('\nSomething went wrong, please make sure you do not disturb the Google Chrome window\n'
                      'while it works when you try again.')

            input('\nPress Enter to Exit & Try Again.')
            sys.exit(1)

        elif 'Timed out receiving message from renderer' or 'cannot determine loading status' in str(e):
            print('\nGoogle Chrome is taking too long to respond :( .')

        elif 'ERR_NAME_NOT_RESOLVED' or 'ERR_CONNECTION_CLOSED' or 'unexpected command response' in str(e):
            print('\nYour internet connection may have been interrupted.')
            print('\nPlease make sure you\'re still connected to the internet and try again.')

        else:
            print('\nSomething went wrong, please make sure you do not disturb the Google Chrome window\n'
                  'while it works when you try again.')

        input('\nPress Enter to Exit & Try Again.')
        sys.exit(1)


def detect_browser_version(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version


if __name__ == "__main__":
    script_summary()
    absolute_paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                      r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    users_browser_version = list(filter(None, [detect_browser_version(p) for p in absolute_paths]))[0]
    print('YOUR GOOGLE CHROME VERSION: ' + users_browser_version)
    print(f'IF YOU NEED TO DOWNLOAD THE CHROME_DRIVER: https://chromedriver.chromium.org/downloads\n')


def main() -> None:
    user_name = input('Enter your Username: ')
    password = input('Enter your Password: ')
    goty_droid(user_name, password)


if __name__ == '__main__':
    main()
