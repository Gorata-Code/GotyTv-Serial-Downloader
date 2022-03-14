#!/usr/bin/python
# -*- coding: latin-1 -*-

import os
import sys
import time
from selenium import webdriver
import serial_bot.constants as const
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Scrubber(webdriver.Chrome):

    def __init__(self, driver_path=resource_path(r"./SeleniumDrivers"), teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.page_load_strategy = 'normal'
        super(Scrubber, self).__init__(options=options)
        self.implicitly_wait(20)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def launch_goty_tv(self) -> None:
        self.get(const.BASE_URL)

    def login(self, user_name: str, password: str) -> int:
        login_btn = self.find_element(By.CLASS_NAME, 'login')
        login_btn.click()

        # USERNAME

        name_box = self.find_element(By.ID, 'login_email')
        name_box.click()
        name_box.clear()
        name_box.send_keys(user_name)

        # PASSWORD

        password_box = self.find_element(By.ID, 'login_password')
        password_box.click()
        password_box.clear()
        password_box.send_keys(password)

        # SLEEP SO THE USER HAS TIME TO HANDLE CAPTCHA
        # BTW - THIS IS THE ONLY APPLICATION OF TIME DOT SLEEP ON THIS CODE ;)

        time.sleep(15)
        try:
            login_btn_two = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_btn_two.click()

            try:
                log_stat = self.find_element(By.CLASS_NAME, 'dropdownMenu').find_element(By.TAG_NAME, 'ul'). \
                    find_element(By.CSS_SELECTOR, 'form[action="https://gotytv.com/logout"]').find_element(
                    By.CSS_SELECTOR, 'button[type="submit"]').get_attribute('innerHTML')
                if log_stat == 'Logout':
                    print('\n\tYou have successfully logged in!')
            except NoSuchElementException:
                print('\n\tThere seems to be an issue logging you in.')
        except WebDriverException and AttributeError:
            return 0

    # REFRESH THE WINDOW IN CASE OF POP-UPS

    def the_loop(self) -> None:
        while self.title.__contains__('New Message!'):
            print('TITLE WHILE: ' + self.title)
            self.refresh()

    def handle_search_box(self, search_query: str) -> None:
        self.the_loop()
        search_box = self.find_element(By.ID, 'search_FM')
        self.the_loop()
        search_box.click()
        self.the_loop()
        search_box.clear()
        self.the_loop()
        search_box.send_keys(search_query.title().strip())
        self.the_loop()
        search_box.send_keys(Keys.ENTER)

    def get_the_list(self, search_query: str):
        similar_serials = []
        query_matching_titles = []

        # CHECKING TO SEE IF THE SEARCH HAS RETURNED ANY ITEM(S)

        try:
            the_series_search_grid = self.find_element(By.CLASS_NAME, 'itemGridsMovie').find_element(By.CLASS_NAME,
                                                                                                     f'row'). \
                find_elements(By.CLASS_NAME, 'col-4')

            for series in the_series_search_grid:
                self.the_loop()
                title = series.find_element(By.TAG_NAME, 'h3').text
                self.the_loop()

                # IN-CASE ONE OF THE RESULTANT TITLES IS A MATCH TO THE SEARCH QUERY

                if title.casefold() == search_query.casefold().strip():
                    if len(query_matching_titles) < 1:
                        print(f'\nWe have found your series "{title}". Please wait for a moment.')
                    query_matching_titles.append(series)
                else:
                    similar_serials.append(title)

                # IN-CASE SEARCH RESULTS IN ZERO

        except NoSuchElementException:
            print(f'\nYour series "{search_query.title().strip()}" is NOT AVAILABLE. Please try a different series.')

        finally:

            # IN-CASE ONE OF THE RESULTANT TITLES IS A MATCH TO THE SEARCH QUERY

            if len(query_matching_titles) > 0:
                return query_matching_titles

            # IN-CASE SEARCH RESULTS SHOW AT LEAST 1 TITLE BUT NO MATCHES

            if len(similar_serials) > 0:
                print(
                    f'\nWe have not found your series "{search_query.title().strip()}".\nInstead, we have found '
                    f'the similar series below. Please refer to them in-case you have misspelled the title.')
                print('\n\tSIMILAR TITLES:\n' + str(similar_serials))

    def choose_series_title(self, search_query: str) -> None:
        self.the_loop()
        if len(search_query) > 1:
            search_matching_titles = self.get_the_list(search_query)

            try:

                # IN-CASE SEARCH RESULTS SHOW TWO OR MORE TITLES THAT MATCH

                if len(search_matching_titles) > 1:

                    print(f'Okay, so we have {len(search_matching_titles)} entries for {search_query.title().strip()}')

                    choose_date = input(f'Please choose the {search_query.title().strip()} you want by typing the date '
                                        f'e.g. Aug 22 & Press Enter: ').title()
                    choose_year = input('And now type the year e.g.(2021) & Press Enter: ')

                    # REFINING THE SEARCH TO LET THE USER PICK THEIR PREFERRED ENTRY

                    for title in search_matching_titles:
                        date = title.find_element(By.CLASS_NAME, 'dtBox').find_element(By.TAG_NAME, 'time').text
                        year = title.find_element(By.CLASS_NAME, 'titleBoxHolder').find_element(By.TAG_NAME,
                                                                                                'span').get_attribute(
                            'innerHTML')
                        if choose_year == year and choose_date == date:
                            print(
                                f'Alright, you have chosen {search_query.title().strip()} from the year {choose_year} '
                                f'and date {choose_date}')
                            title.find_element(By.TAG_NAME, 'a').click()
                            break

                # CHECKING THE LENGTH OF THE LIST IN-CASE NO IDENTICAL TITLES HAVE BEEN FOUND BUT A MATCH FOR THE QUERY

                elif len(search_matching_titles) == 1:
                    the_series_search_grid = self.find_element(By.CLASS_NAME, 'itemGridsMovie').find_element(
                        By.CLASS_NAME,
                        f'row').find_elements(
                        By.CLASS_NAME, 'col-4')
                    for _ in the_series_search_grid:
                        print(str(_.find_element(By.TAG_NAME, 'h3').text).casefold())
                        if str(_.find_element(By.TAG_NAME, 'h3').text).casefold() == search_query.casefold().strip():
                            _.find_element(By.TAG_NAME, 'a').click()
            except TypeError:
                print(search_matching_titles)

        elif len(search_query) == 0:
            print('\nPlease type something.')

    def handle_download_choices(self) -> None:

        # MAKING SURE THE USER IS ACTUALLY LOGGED IN BEFORE PRESENTING OPTIONS

        try:
            log_stat = self.find_element(By.CLASS_NAME, 'dropdownMenu').find_element(By.TAG_NAME, 'ul').find_element(
                By.CSS_SELECTOR, 'form[action="https://gotytv.com/logout"]').find_element(By.CSS_SELECTOR,
                                                                                          'button[type="submit"]'). \
                get_attribute(
                'innerHTML')
            if log_stat == 'Logout':
                download_criteria = input(
                    '\nPlease type:\n\t"A" to download an Episode\n\t"B" to download a Season\n\t"C" to '
                    'download the entire series\n\t"D" to download a list of serials/series\n\t"E" to '
                    'download a trailer\n\t"F" to download a list of trailers\n\t"X" to quit\nType Here '
                    '& Press Enter: ').title()

                if download_criteria == "A":
                    self.download_an_episode()

                elif download_criteria == "B":
                    self.download_a_season()

                elif download_criteria == "C":
                    self.download_a_full_series()

                elif download_criteria == "D":
                    self.download_a_list_of_series()

                elif download_criteria == "E":
                    self.download_a_trailer()

                elif download_criteria == "F":
                    self.download_a_list_of_trailers()

                elif download_criteria == "X":
                    pass

                input('\n\tIf your download has completed, Press Enter To Quit:')

        # TOO MANY EXCEPTIONS & POTENTIAL ERRORS TO SINGLE OUT -
        # NoSuchElementException StaleElementReferenceException WebDriverException
        # NewConnectionError MaxRetryError ResponseError

        except Exception as tooMany:
            if tooMany:
                print('\nPlease follow all instructions correctly and try again.')

    def download_a_trailer(self, trailer_title=None) -> None:

        # ESSENTIALLY ATTEMPTING TO ASCERTAIN WHETHER THE USER IS DOWNLOADING A TRAILER OR A LIST OF TRAILERS

        if trailer_title is None:
            trailer_series_name = input('\nPlease type the name of the series & Press Enter: ').title().strip()
        else:
            trailer_series_name = trailer_title.title().strip()
        self.handle_search_box(trailer_series_name)
        self.choose_series_title(trailer_series_name)
        self.the_loop()
        try:
            trailer_button = self.find_element(By.CLASS_NAME, 'trailerBtn')
            self.the_loop()
            trailer_button.click()
            trailer_button_click = self.find_element(By.TAG_NAME, 'iframe')
            source = trailer_button_click.get_attribute('src')
            print('TRAILER LINK: ' + source)

            # NAVIGATING TO Y2MATE TO DOWNLOAD SINCE IT IS A YOUTUBE LINK

            self.get(const.Y2M8_URL)
            self.the_loop()
            search_box = self.find_element(By.ID, 'txt-url')
            self.the_loop()
            search_box.click()
            self.the_loop()
            search_box.send_keys(source)
            self.the_loop()
            search_box.send_keys(Keys.ENTER)
            self.the_loop()
            try:
                download_button = self.find_element(By.XPATH, '//*[@id="mp4"]/table/tbody/tr[1]/td[3]/a')
                self.the_loop()
                download_button.click()
                self.the_loop()
                final_download_button = self.find_element(By.XPATH, '//*[@id="process-result"]/div/a')
                self.the_loop()
                final_download_button.click()
            except NoSuchElementException:
                print(
                    f'The Trailer for "{trailer_series_name.title().strip()}" is NOT AVAILABLE. '
                    f'Please try another trailer.')

            # Y2MATE IS NOTORIOUS FOR ITS POP-UPS AND NEW TABS
            # CLOSING ALL THE EXTRAS TABS AND SWITCHING FOCUS BACK TO OUR MAIN WINDOW

            while len(self.window_handles) > 1:
                self.switch_to.window(self.window_handles[1])
                self.close()
                self.switch_to.window(self.window_handles[0])
            self.back()

        except NoSuchElementException:
            self.get('view-source:' + self.current_url)
            if not str(self.find_element(By.TAG_NAME, 'html').text).__contains__('<trailerBtn'):
                print(f'The trailer for "{trailer_series_name}" is not available.')
                self.back()

    def download_a_list_of_trailers(self) -> None:
        trailer_list = input('\nList the series names whose trailers you would like to download.\nPlease use a comma '
                             'to separate the series names &\nPress Enter: ').casefold().split(',')
        if len(trailer_list) > 1:
            print('\nTrailers:\n\t' + str(trailer_list).title().strip())
            for trailer in trailer_list:
                print('\n' + trailer.title().strip())
                self.the_loop()
                self.download_a_trailer(trailer)
                print(f'Trailer download for "{trailer.title().strip()}" successful.')

            print(f'-------------------------------YOUR LIST OF TRAILERS ENDS HERE------------------------------------')
        elif len(trailer_list) == 1:
            print('\nA list must have two or more names on it. Otherwise, please search by "Trailer".')

        elif len(trailer_list) <= 0:
            print('\nPlease type two or more names.')

    def download_an_episode(self, series_name=None, season_no=None, episode_no=None) -> None:

        # WHEN YOU ARE ONLY DOWNLOADING AN EPISODE

        if series_name is None and season_no is None and episode_no is None:
            series_title = input(
                'Please type the name of the series you want to download & Press Enter: ').title().strip()
            season_number = int(input(f'Please type the Season Number & Press Enter: '))
            episode_number = int(
                input(f'\nSeason {season_number} of "{series_title.title().strip()}" Episode number?: '))
            self.handle_search_box(series_title)
            self.choose_series_title(series_title)
            episode_download = self.current_url + f'/{season_number}/{episode_number}'
            self.get(episode_download)

        # WHEN YOU ARE DOWNLOADING A SEASON OR A FULL SERIES OR A LIST OF SERIALS

        else:
            series_title = series_name.title().strip()
            season_number = season_no
            episode_number = episode_no
        try:
            source = self.find_element(By.TAG_NAME, 'source')
            link = source.get_attribute('src')
            print('LINK:' + link)
            self.get(link)

        except NoSuchElementException:
            try:

                # IN-CASE WE GET A 404
                # SOMETIMES THIS HAPPENS BECAUSE THE SERIES HAS NOT BEEN NAMED / NUMBERED CORRECTLY

                page_not_found = self.find_element(By.CLASS_NAME, 'page404')

                if str(page_not_found.text[:3]) == '404':
                    # DECREMENT EPISODE NUMBER SINCE WE ARE HENCEFORTH DEALING WITH INDICES

                    episode_number -= 1
                    self.back()

                    # GET THE EPISODE LIST FOR THE CURRENT SERIES

                    episode_list = self.find_element(By.CSS_SELECTOR,
                                                     f'.contentTab[data-content-tab="Season {season_number}"]'). \
                        find_elements(By.TAG_NAME, 'li')

                    # RETRIEVE THE INNER-HTML TO GET THE LABEL OF THE EPISODE IN QUESTION

                    misnomer_episode = episode_list[episode_number].find_element(By.TAG_NAME, 'a').get_attribute(
                        'innerHTML')
                    print(
                        f'It seems "{series_title.title()}" Season {season_number} Episode {episode_number + 1} is '
                        f'NOT AVAILABLE. Instead, {misnomer_episode} is where Episode {episode_number + 1} would be. '
                        f'We will download this episode regardless, but please be aware you may wind up with'
                        f' duplicates.')

                    self.get(self.current_url + f'/{season_number}/{misnomer_episode[8:]}')
                    source_two = self.find_element(By.TAG_NAME, 'source')
                    link_two = source_two.get_attribute('src')
                    self.get(link_two)
                    self.back()

            except NoSuchElementException:

                # GOING TO THE SOURCE CODE JUST TO MAKE SURE THE EPISODE LINK IS TRULY UNAVAILABLE

                self.get('view-source:' + self.current_url)
                if not str(self.find_element(By.TAG_NAME, 'html').text).__contains__('<source'):
                    print(f'"{series_title}" Season {season_number} Episode {episode_number} is not available.')
                    self.back()
                print('\n\tPlease try another episode.')

    def download_a_season(self, series_name=None, season_no=None) -> None:

        # IN-CASE YOU ARE DOWNLOADING A SEASON

        if series_name is None and season_no is None:
            series_title = input('Please type the series name & Press Enter: ').title().strip()
            season_number = int(input(f'Download "{series_title.title().strip()}" Season number?: '))
            self.handle_search_box(series_title)
            self.choose_series_title(series_title)

        # IN-CASE YOU ARE DOWNLOADING A FULL SERIES OR A LIST OF SERIALS

        else:
            series_title = series_name.title().strip()
            season_number = season_no

        # IN-CASE A USER INPUTS ZERO OR A NUMBER EXCEEDING THE AVAILABLE NUMBER OF SEASONS

        if season_number > len(self.find_element(By.CSS_SELECTOR, f'.contentTab[data-content-tab="Season '
                                                                  f'{season_number}"]').find_elements(By.TAG_NAME,
                                                                                                      'li')) or \
                season_number <= 0:

            print(f'Season "{season_number}" is NOT AVAILABLE. :(')
        else:

            # NOT SURE ABOUT THIS VARIABLE AND ITS SUPPOSED UTILITY

            season_download = self.current_url + f'/{season_number}/1'

            try:
                target_season_episodes = self.find_element(By.CSS_SELECTOR, f'.contentTab[data-content-tab="Season '
                                                                            f'{season_number}"]').find_elements(
                    By.TAG_NAME, 'li')
                print(f'\n"{series_title}" Season {season_number} contains {len(target_season_episodes)} Episodes.')
                print(' We will now download all the episodes for you.\n')
                for episode in range(len(target_season_episodes)):
                    episode += 1
                    print('\tDOWNLOADING EPISODE: ' + str(episode))
                    self.get(str(season_download)[:-2] + f'/{episode}')
                    self.download_an_episode(series_title, season_number, episode)

            except NoSuchElementException:
                print(f'There seems to be some issue with "{series_title}" Season {season_number}.\nPlease try again '
                      f'later, or try other seasons or downloading per episode for this season.')

        print(
            f'-----------------------------------END of SEASON {season_number}----------------------------------------')

    def download_a_full_series(self, series_name=None) -> None:

        # DOWNLOADING A SERIES

        if series_name is None:
            series_title = input('Please type the name of the series you want to download & Press Enter: ')

        # DOWNLOADING TWO OR MORE SERIALS

        else:
            series_title = series_name
        self.handle_search_box(series_title)
        self.choose_series_title(series_title)
        series_seasons = self.find_element(By.CLASS_NAME, 'menuListItemsBox').text
        print(f'\n"{series_title.title().strip()}" goes up to ' + series_seasons + '!')
        print(f' We will now download all of the seasons for you.')
        total_sum_of_seasons = self.find_element(By.CLASS_NAME, 'itemTabList').find_elements(By.TAG_NAME, 'li')

        # WE USE THIS URL LATER TO RETURN TO THIS POINT
        # EVERY SERIES TITLE WILL START FROM HERE IN THE NEXT METHOD

        url_capture = self.current_url

        for season in range(len(total_sum_of_seasons)):
            season += 1
            print('\n\tSeason Number: ' + str(season))
            self.download_a_season(series_title, season)
            self.get(str(self.current_url)[:-5])

        # RETURNING TO SERIES-TITLE-STARTING-POINT AS REFERENCED IN THE PRECEDING COMMENT

        self.get(url_capture)

        print(f'\n--------------------------"{series_title.title().strip()}" ENDS HERE--------------------------------')

    def download_a_list_of_series(self) -> None:
        serial_titles_list = input('List all the serials you want to download, using a comma to separate series names '
                                   '& Press Enter: ').casefold().split(',')

        if len(serial_titles_list) > 1:
            print('Serial List:\n\t' + str(serial_titles_list))
            for serial_title in serial_titles_list:
                print(serial_title.title())
                self.the_loop()
                self.download_a_full_series(serial_title)
                print(f'Series "{serial_title.title()}" has been fully downloaded.')
            print(f'--------------------------------YOUR LIST OF SERIES ENDS HERE-------------------------------------')

        elif len(serial_titles_list) == 1:
            print('\nA list must have two or more names on it. Otherwise, please search by "Entire Series".')

        elif len(serial_titles_list) <= 0:
            print('\nPlease type two or more names.')
