import time
import utilities.api.item_ids as ids
import utilities.color as clr
import utilities.random_util as rd
import pyautogui as pag
import utilities.imagesearch as imsearch

from utilities.api.morg_http_client import MorgHTTPSocket
from utilities.geometry import RuneLiteObject
from utilities.api.status_socket import StatusSocket
from model.osrs.osrs_bot import OSRSBot


class OSRSPickpocket(OSRSBot):

    
    def __init__(self):
        bot_title = "Ardy Knight Pickpocket"
        description = "This bot pickpockets from the ardy knight"
        super().__init__(bot_title=bot_title, description=description)
        self.running_time = 1
        self.take_breaks = False
        self.api_m = MorgHTTPSocket() 
        self.food_list = ['Trout', 'Swordfish', 'Shark',]


    def create_options(self):
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 360)
        self.options_builder.add_dropdown_option("food_to_use", "Select food", self.food_list)
        self.options_builder.add_checkbox_option("take_breaks", "Take breaks?", [" "])

        
    def save_options(self, options: dict):
        for option in options:
            if option == "running_time":
                self.running_time = options[option]  
            elif option == "take_breaks":
                self.take_breaks = options[option] != []     
            elif option == "food_to_use":
                self.food_to_use = options[option]     
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg("Options set successfully.")
        self.options_set = True


    def main_loop(self):      
        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:  
            self.update_progress((time.time() - start_time) / end_time)
            self.bot_loop_main()
        self.update_progress(1)
        self.log_msg("Finished.")
        self.end_run()
 
                      
    def bot_loop_main(self):
        self.check_hitpoints()
        self.check_coin_pouches()
        self.pickpocket_target()
            

    def check_hitpoints(self):
        current_hp = self.api_m.get_hitpoints()
        if current_hp[0] < 50:
            self.log_msg("Health low")

            food_id = self.get_food_id()
            
            food_location = self.api_m.get_first_occurrence(food_id)
            
            if food_location != -1:
                self.eat_food(food_location)
            else:
                self.log_msg("Out of food")
                self.find_nearest_bank()
                self.withdraw_food()
    

    def get_food_id(self):
        if self.food_to_use == 'Swordfish':
            food_id = ids.SWORDFISH
        elif self.food_to_use == 'Shark':
            food_id = ids.SHARK

        return food_id

    
    def eat_food(self, food_location):
        self.mouse.move_to(self.win.inventory_slots[food_location].random_point())
        self.mouse.click()
        self.log_msg("Ate food")


    def find_nearest_bank(self):
        self.log_msg('Looking for bank')

        while True:
            if banks := self.get_all_tagged_in_rect(self.win.game_view, clr.YELLOW):
                banks = sorted(banks, key=RuneLiteObject.distance_from_rect_center)
                self.log_msg(f"Bank found")               
                self.mouse.move_to(banks[0].random_point(), mouseSpeed='fastest')
                time.sleep(4)
                self.mouse.click()     
                time.sleep(4)
                break
            else:
                self.log_msg('Could not find bank') 


    def withdraw_food(self):
        desposit_inventory_img = imsearch.BOT_IMAGES.joinpath("bank", "deposit_inventory.png")

        while True:
            desposit_inventory = imsearch.search_img_in_rect(desposit_inventory_img, self.win.game_view)
            if desposit_inventory:
                break
            time.sleep(0.1)
   
        food_img = self.get_food_img()
       
        self.log_msg('Looking for food')
        if food := imsearch.search_img_in_rect(food_img, self.win.game_view, 0.5):
            self.mouse.move_to(food.random_point(), mouseSpeed='fastest')
            self.mouse.click()
            self.log_msg('Food found')
            pag.press('esc')
        else:
            self.log_msg(f"Out of food")
            self.end_run()


    def get_food_img(self):
        if self.food_to_use == 'Swordfish':
            food_img = imsearch.BOT_IMAGES.joinpath("items", "Swordfish_bank.png")
        elif self.food_to_use == 'Shark':
            food_img = imsearch.BOT_IMAGES.joinpath("items", "Shark_bank.png")

        return food_img


    def check_coin_pouches(self):
        coin_pouch_count = self.api_m.get_inv_item_stack_amount(ids.coin_pouches)
        if coin_pouch_count == 28:
            self.click_coin_pouches()
            self.log_msg("Cashed in a full stack")
        else:
            if rd.random_chance(probability=0.02) and coin_pouch_count > 0:
                self.click_coin_pouches()
                self.log_msg("Cashed in early")


    def click_coin_pouches(self):
        coin_pouch_location = self.api_m.get_first_occurrence(ids.coin_pouches)
        self.mouse.move_to(self.win.inventory_slots[coin_pouch_location[0]].random_point())
        self.mouse.click()


    def pickpocket_target(self):
        target = self.get_nearest_tag(clr.CYAN)
        if target:
            self.mouse.move_to(target.center(), mouseSpeed='fastest')
            self.mouse.click()
        time.sleep(0.5)
        if rd.random_chance(probability=0.005) and self.take_breaks:
                self.log_msg("Taking break")
                self.take_break(max_seconds=30, fancy=True)
      

    def end_run(self):
        ending_exp = self.api_m.get_skill_xp('Thieving')
        total_exp_gained_run = ending_exp - self.starting_exp
        self.log_msg(f'Total Exp Gained (Run): {total_exp_gained_run}')

        total_exp_gained_session = self.api_m.get_skill_xp_gained('Thieving')
        self.log_msg(f'Total Exp Gained (Session): {total_exp_gained_session}')

        self.stop()