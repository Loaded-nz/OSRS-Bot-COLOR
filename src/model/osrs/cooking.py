import time
import time
import random
import cv2

import utilities.api.item_ids as ids
import utilities.color as clr
import utilities.random_util as rd
import utilities.imagesearch as imsearch

from utilities.api.morg_http_client import MorgHTTPSocket
from utilities.api.status_socket import StatusSocket
from model.osrs.osrs_bot import OSRSBot

import pyautogui as pag


class OSRSCook(OSRSBot):

    def __init__(self):
        bot_title = "🐟  Pranko's Fish Cooking  🐟"  # Bot name
        description = "Cooks various fish at a range. Banks = Yellow, Range = Green"  # Bot description
        super().__init__(bot_title=bot_title, description=description)
        self.running_time = 1
        self.max_delay = 0.7 # Had trouble setting these with sliders
        self.min_delay = 0.5 # ^

    def create_options(self):
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 500)
        self.options_builder.add_dropdown_option("food_type", "Food type", ["Raw shrimps", "Raw anchovies", "Raw herring", "Raw trout", "Raw salmon", "Raw tuna", "Raw lobster", "Raw swordfish", "Raw monkfish", "Raw shark", "Raw manta ray", "Raw sea turtle"])

    def save_options(self, options: dict):
        for option in options:
            if option == "running_time":
                self.running_time = options[option]
            elif option == "food_type":
                self.food_type = options[option]
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return

        # Convert delay values to strings before logging
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg(f"Minimum delay: {self.min_delay} seconds.")
        self.log_msg(f"Maximum delay: {self.max_delay} seconds.")
        self.log_msg(f"Food type: {self.food_type}")
        self.log_msg("Options set successfully.")
        self.options_set = True


    def main_loop(self):
        api_m = MorgHTTPSocket()

        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:
            if api_m.get_if_item_in_inv(get_fish_id(self.food_type)):
                self.cook(api_m)
                self.sleep_until_idle(api_m)
            else:
                self.open_bank(api_m)
                self.deposit_items()
                self.withdraw_items()

        self.update_progress(1)
        self.log_msg("Finished.")
        self.stop()

    def cook(self, api_m: MorgHTTPSocket):
        cooking_range = self.get_nearest_tag(clr.GREEN)
        try:
            self.mouse.move_to(cooking_range.random_point())
            self.mouse.click()
            self.sleep_until_idle(api_m)
            pag.press('space')
        except:
            self.sleep(self.min_delay, self.max_delay)

    def sleep(self, min_delay, max_delay):
        sleep_time = rd.fancy_normal_sample(min_delay, max_delay)
        #self.log_msg(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)

    def open_bank(self, api_m: MorgHTTPSocket):
        bank_object = self.get_nearest_tag(clr.YELLOW)
        try:
            self.mouse.move_to(bank_object.random_point())
            self.mouse.click()
            self.sleep_until_idle(api_m)
        except:
            self.log_msg('Did not find a bank')
            self.sleep(self.min_delay, self.max_delay)

    def deposit_items(self):
        deposit_button = imsearch.BOT_IMAGES.joinpath("items", "bank_all.png")
        try:
            if deposit := imsearch.search_img_in_rect(deposit_button, self.win.game_view):
                self.mouse.move_to(deposit.random_point())
                self.mouse.click()
        except:
            self.log_msg('No items left to deposit, exiting')
            self.stop()

    def withdraw_items(self):
        fish_bank = imsearch.BOT_IMAGES.joinpath("items", f"{self.food_type.lower().replace(' ', '_')}_bank.png")
        try:
            if fish := imsearch.search_img_in_rect(fish_bank, self.win.game_view):
                self.mouse.move_to(fish.random_point())
                self.mouse.click()
                self.sleep(self.min_delay, self.max_delay)
                pag.press('escape')
        except:
            self.log_msg('No fish left, exiting')
            self.stop()

    def sleep_until_idle(self, api_m: MorgHTTPSocket):
        while not api_m.get_is_player_idle(2):
            self.sleep(self.min_delay, self.max_delay)

def get_fish_id(fish_type):
    if fish_type == "Raw shrimps":
        return ids.RAW_SHRIMPS
    elif fish_type == "Raw anchovies":
        return ids.RAW_ANCHOVIES
    elif fish_type == "Raw herring":
        return ids.RAW_HERRING
    elif fish_type == "Raw trout":
        return ids.RAW_TROUT
    elif fish_type == "Raw salmon":
        return ids.RAW_SALMON
    elif fish_type == "Raw tuna":
        return ids.RAW_TUNA
    elif fish_type == "Raw lobster":
        return ids.RAW_LOBSTER
    elif fish_type == "Raw swordfish":
        return ids.RAW_SWORDFISH
    elif fish_type == "Raw monkfish":
        return ids.RAW_MONKFISH
    elif fish_type == "Raw shark":
        return ids.RAW_SHARK
    elif fish_type == "Raw manta ray":
        return ids.RAW_MANTA_RAY
    elif fish_type == "Raw sea turtle":
        return ids.RAW_SEA_TURTLE
    else:
        return None
