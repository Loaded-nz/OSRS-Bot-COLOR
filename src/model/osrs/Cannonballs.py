import time
import random

import utilities.api.item_ids as ids
import utilities.color as clr
import utilities.random_util as rd
import utilities.imagesearch as imsearch

from utilities.api.morg_http_client import MorgHTTPSocket
from utilities.api.status_socket import StatusSocket
from model.osrs.osrs_bot import OSRSBot

import pyautogui as pag


class Smithing(OSRSBot):

    def __init__(self):
        bot_title = "Pranko's Cannonballs"  # Bot name
        description = "Makes cannonballs in edgeville"  # Bot description
        super().__init__(bot_title=bot_title, description=description)
        self.running_time = 1
        self.delay = 1  # Default delay value

    def create_options(self):
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 500)
        self.options_builder.add_slider_option("delay", "Minimum delay before next action (seconds)", 1.0, 2.0)

    def save_options(self, options: dict):
        for option in options:
            if option == "running_time":
                self.running_time = options[option]
            elif option == "delay":
                self.delay = options[option]
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg(f"Delay: {self.delay} seconds.")
        self.log_msg("Options set successfully.")
        self.log_msg("Start this script at the edgeville bank, with both the furnace and the booths visible")
        self.log_msg("Highlight colors: Furnace - Green, Bank booth - Yellow")
        self.options_set = True

    def main_loop(self):
        api_m = MorgHTTPSocket()

        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:

            if api_m.get_if_item_in_inv(2353):
                smith(self, api_m)
            else:
                open_bank(self, api_m)
                withdraw_items(self)

        self.update_progress(1)
        self.log_msg("Finished.")
        self.stop()

def smith(self, api_m: MorgHTTPSocket):
    anvil = self.get_nearest_tag(clr.GREEN)
    try:
        self.mouse.move_to(anvil.random_point())
        self.mouse.click()
        sleep_until_idle(self, api_m)
        pag.press('space')
        sleep_until_idle(self, api_m)
    except:
        self.log_msg('Did not find a furnace, maybe there\'s an interface open. Pressing escape and trying again')
        pag.press('escape')
        time.sleep(rd.random.random() + self.delay)

def open_bank(self, api_m: MorgHTTPSocket):
    bank = self.get_nearest_tag(clr.YELLOW)
    try:
        self.mouse.move_to(bank.random_point())
        self.mouse.click()
        sleep_until_idle(self, api_m)
    except:
        self.log_msg('Did not find a bank, maybe there\'s an interface open. Pressing escape and trying again')
        pag.press('escape')
        time.sleep(rd.random.random() + self.delay)

def withdraw_items(self):
    steel_bar_bank = imsearch.BOT_IMAGES.joinpath("items", "steel_bar_bank.png")
    try:
        if steel_bar := imsearch.search_img_in_rect(steel_bar_bank, self.win.game_view):
            self.mouse.move_to(steel_bar.random_point())
            self.mouse.click()
            pag.press('escape')
            time.sleep(rd.random.random() + self.delay)
    except:
        self.log_msg('No steel bars left, exiting')
        self.stop()

def sleep_until_idle(self, api_m: MorgHTTPSocket):
    while not api_m.get_is_player_idle(2):
        time.sleep(self.delay)