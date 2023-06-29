import time

import utilities.color as clr
import utilities.random_util as rd
import utilities.imagesearch as imsearch
import utilities.game_launcher as launcher
import pyautogui as pag
from model.bot import BotStatus
from model.osrs.osrs_bot import OSRSBot
from utilities.api.morg_http_client import MorgHTTPSocket
from utilities.api.status_socket import StatusSocket



import random


class OSRSMolch(OSRSBot, launcher.Launchable):
    def __init__(self):
        bot_title = "Molch Bot"
        description = "Bots Molch Island aerial fishing."
        super().__init__(bot_title=bot_title, description=description)
        # Set option variables below (initial value is only used during UI-less testing)
        self.running_time = 1
        self.take_breaks = True

    def create_options(self):
        """
        Use the OptionsBuilder to define the options for the bot. For each function call below,
        we define the type of option we want to create, its key, a label for the option that the user will
        see, and the possible values the user can select. The key is used in the save_options function to
        unpack the dictionary of options after the user has selected them.
        """
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 360)
        self.options_builder.add_checkbox_option("take_breaks", "Take breaks?", [" "])


    def save_options(self, options: dict):
        """
        For each option in the dictionary, if it is an expected option, save the value as a property of the bot.
        If any unexpected options are found, log a warning. If an option is missing, set the options_set flag to
        False.
        """
        for option in options:
            if option == "running_time":
                self.running_time = options[option]
            elif option == "take_breaks":
                self.take_breaks = options[option] != []
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg(f"Bot will{' ' if self.take_breaks else ' not '}take breaks.")
        self.log_msg("Options set successfully.")
        self.options_set = True

    def main_loop(self):
        """
        When implementing this function, you have the following responsibilities:
        1. If you need to halt the bot from within this function, call `self.stop()`. You'll want to do this
           when the bot has made a mistake, gets stuck, or a condition is met that requires the bot to stop.
        2. Frequently call self.update_progress() and self.log_msg() to send information to the UI.
        3. At the end of the main loop, make sure to set the status to STOPPED.

        Additional notes:
        Make use of Bot/RuneLiteBot member functions. There are many functions to simplify various actions.
        Visit the Wiki for more.
        """
        # Setup APIs
        api_m = MorgHTTPSocket()
        api_s = StatusSocket()

        # Main loop
        self.log_msg("Selecting inventory...")
        self.mouse.move_to(self.win.cp_tabs[3].random_point())
        self.mouse.click()



    # These aren't necessary unless you need the script to read a specific chat.
    #    self.log_msg("Selecting game chat...")
    #    self.mouse.move_to(self.win.chat_tabs[0].random_point())
    #    self.mouse.click()
    #    self.mouse.move_to(self.win.chat_tabs[1].random_point())
    #    self.mouse.click()

        # Defines image search for knife and fish.

        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:
            # -- Perform bot actions here --
            # 5% chance to take a break between clicks
            if rd.random_chance(probability=0.05) and self.take_breaks:
                self.take_break(max_seconds=130, fancy=True)

            # 8% chance to convert fish to chunks early.
            if rd.random_chance(probability=.08):
                self.__fish_chunks()

            x, y = self.win.inventory_slots[-1].get_center()  # get pixel position of last slot
            self.empty_slot_clr = pag.pixel(x, y)

# TODO: Optimize the fishing pool search so you don't run all over the fucking island.
            #This debugs the issue of having the knife selected and not being able to fish.
            #if self.mouseover_text(contains="Knife"):
            #    self.mouse.move_to(self.win.cp_tabs[3].random_point())
            #    self.mouse.click()



            pools = self.get_all_tagged_in_rect(self.win.game_view, clr.PINK)
            self.log_msg("Fishing...")
            for fish in pools:
                if fish := self.get_nearest_tag(clr.PINK):
                    n = 0

                    self.mouse.move_to(fish.random_point())
                    if not self.mouseover_text(contains="Catch"):
                        continue
                    self.mouse.click()
                    #Helps synchronize your movements to cormorant travel time.
                    while self.mouseover_text(contains="Catch"):
                        time.sleep(0.2)
                        n += 1
                        if n >= 12:
                            self.mouse.click()
                            n = 0
                if self.__inv_full():
                    self.__fish_chunks()
                time.sleep(random.uniform(1.2,1.8))



            self.update_progress((time.time() - start_time) / end_time)

        self.update_progress(1)
        self.__logout("Finished.")


    def __logout(self, msg):
        self.log_msg(msg)
        self.logout()
        self.set_status(BotStatus.STOPPED)

    def __inv_full(self):
        x, y = self.win.inventory_slots[-1].get_center()
        return pag.pixel(x, y) != self.empty_slot_clr
        #    None of these solutions for finding full inventory worked for me and are left for debugging purposes.
        #bluegill_img = imsearch.BOT_IMAGES.joinpath("items", "Bluegill.png")
        #commontench_img = imsearch.BOT_IMAGES.joinpath("items", "Commontench.png")
        #mottledeel_img = imsearch.BOT_IMAGES.joinpath("items", "Mottledeel.png")
        #greatersiren_img = imsearch.BOT_IMAGES.joinpath("items", "Greatersiren.png")
        #notfullinv = self.win.inventory_slots[-1]
        #fullinv =    imsearch.search_img_in_rect(bluegill_img, notfullinv) or \
        #          imsearch.search_img_in_rect(commontench_img, self.win.inventory_slots[-1]) or \
        #          imsearch.search_img_in_rect(mottledeel_img, self.win.inventory_slots[-1]) or \
        #          imsearch.search_img_in_rect(greatersiren_img, self.win.inventory_slots[-1])
        #return fullinv
        #fullinv = self.get_all_tagged_in_rect(self.win.inventory_slots[-1], clr.CYAN)

    def __fish_chunks(self):
        self.log_msg("Cutting fish into chunks...")
## Make sure you have the .png's listed downloaded into the ./src/images/bot/items folder.
        knife_img = imsearch.BOT_IMAGES.joinpath("items", "Knife.png")
        bluegill_img = imsearch.BOT_IMAGES.joinpath("items", "Bluegill.png")
        commontench_img = imsearch.BOT_IMAGES.joinpath("items", "Commontench.png")
        mottledeel_img = imsearch.BOT_IMAGES.joinpath("items", "Mottledeel.png")
        greatersiren_img = imsearch.BOT_IMAGES.joinpath("items", "Greatersiren.png")
        if knife := imsearch.search_img_in_rect(knife_img, self.win.control_panel):
            self.mouse.move_to(knife.random_point())
            self.mouse.click()
            self.mouse.move_to(self.win.inventory_slots[-1].random_point())
            while self.mouseover_text(contains="Bluegill")\
                or self.mouseover_text(contains="Common")\
                or self.mouseover_text(contains="Greater")\
                or self.mouseover_text(contains="Mottled"):
                    self.mouse.click()
                    self.mouse.move_to(knife.random_point())
                    self.mouse.click()
                    self.mouse.move_to(self.win.inventory_slots[-1].random_point())
                    time.sleep(random.uniform(0.3,0.35))
            self.mouse.move_to(self.win.inventory_slots[-2].random_point())
            while self.mouseover_text(contains="Bluegill") \
                or self.mouseover_text(contains="Common") \
                or self.mouseover_text(contains="Greater") \
                or self.mouseover_text(contains="Mottled"):
                    self.mouse.click()
                    self.mouse.move_to(knife.random_point())
                    self.mouse.click()
                    self.mouse.move_to(self.win.inventory_slots[-2].random_point())
                    time.sleep(random.uniform(0.3,0.35))
            # Optional code to try and chunk the third to last inventory slot.
#            self.mouse.move_to(self.win.inventory_slots[-3].random_point())
#            while self.mouseover_text(contains="Bluegill") \
#                or self.mouseover_text(contains="Common") \
#                or self.mouseover_text(contains="Greater") \
#                or self.mouseover_text(contains="Mottled"):
#                    self.mouse.click()
#                    self.mouse.move_to(knife.random_point())
#                    self.mouse.click()
#                    self.mouse.move_to(self.win.inventory_slots[-3].random_point())
#                    time.sleep(random.uniform(0.3,0.35))
            while bluegill_inv := imsearch.search_img_in_rect(bluegill_img, self.win.control_panel):
                    self.mouse.move_to(bluegill_inv.random_point())
                    if not self.mouseover_text(contains="Knife"):
                        self.mouse.move_to(knife.random_point())
                        self.mouse.click()
                    self.mouse.click()
                    self.mouse.move_to(knife.random_point())
                    self.mouse.click()
                    time.sleep(random.uniform(0.3,0.35))
            while mottledeel_inv := imsearch.search_img_in_rect(mottledeel_img, self.win.control_panel):
                    self.mouse.move_to(mottledeel_inv.random_point())
                    if not self.mouseover_text(contains="Knife"):
                        self.mouse.move_to(knife.random_point())
                        self.mouse.click()
                    self.mouse.click()
                    self.mouse.move_to(knife.random_point())
                    self.mouse.click()
                    time.sleep(random.uniform(0.3,0.35))
            while commontench_inv := imsearch.search_img_in_rect(commontench_img, self.win.control_panel):
                    self.mouse.move_to(commontench_inv.random_point())
                    if not self.mouseover_text(contains="Knife"):
                        self.mouse.move_to(knife.random_point())
                        self.mouse.click()
                    self.mouse.click()
                    self.mouse.move_to(knife.random_point())
                    self.mouse.click()
                    time.sleep(random.uniform(0.3,0.35))
            while greatersiren_inv := imsearch.search_img_in_rect(greatersiren_img, self.win.control_panel):
                    self.mouse.move_to(greatersiren_inv.random_point())
                    if not self.mouseover_text(contains="Knife"):
                        self.mouse.move_to(knife.random_point())
                        self.mouse.click()
                    self.mouse.click()
                    self.mouse.move_to(knife.random_point())
                    self.mouse.click()
                    time.sleep(random.uniform(0.3,0.35))
            if self.mouseover_text(contains="Knife"):
                self.mouse.click()



