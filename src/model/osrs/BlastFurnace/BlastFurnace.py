import time
import utilities.api.item_ids as ids
import utilities.color as clr
import utilities.random_util as rd
from model.osrs.osrs_bot import OSRSBot
from model.runelite_bot import BotStatus
from utilities.api.morg_http_client import MorgHTTPSocket
from utilities.api.status_socket import StatusSocket
from utilities.geometry import RuneLiteObject,Point,Rectangle
import pyautogui as pag
import model.osrs.BlastFurnace.BotSpecImageSearch as imsearch
import utilities.game_launcher as launcher
import pathlib



    
class OSRSBlastFurnace(OSRSBot):
    api_m = MorgHTTPSocket()
    def __init__(self):
        bot_title = "ThatOneGuys BlastFurnace"
        description = "Blast Furnace"
        super().__init__(bot_title=bot_title, description=description)
        self.potion_to_make = None
        self.running_time = 1
        self.take_breaks = False
        self.break_length_min = 1
        self.break_length_max = 500
        self.time_between_actions_min =0.8
        self.time_between_actions_max =5
        self.potion_to_make = None
        self.mouse_speed = "medium"
        self.break_probabilty = 0.13
        self.Client_Info = None
        self.win_name = None
        self.pid_number = None
        self.Input = "failed to set mouse input"
        self.setupran = False
        self.stamina_active = True
        self.barsmade = 0
        self.collection_attempts = 0

    def create_options(self):
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 500)
        self.options_builder.add_checkbox_option("take_breaks", "Take breaks?", [" "])
        self.options_builder.add_slider_option("break_probabilty", "Chance to take breaks (percent)",1,100)
        self.options_builder.add_slider_option("break_length_min", "How long to take breaks (min) (Seconds)?", 1, 300)
        self.options_builder.add_slider_option("break_length_max", "How long to take breaks (max) (Seconds)?", 2, 300)    
        self.options_builder.add_checkbox_option("mouse_speed", "Mouse Speed (must choose & only select one)",[ "slowest", "slow","medium","fast","fastest"])
        self.options_builder.add_slider_option("time_between_actions_min", "How long to take between actions (min) (MiliSeconds)?", 600,3000)
        self.options_builder.add_slider_option("time_between_actions_max", "How long to take between actions (max) (MiliSeconds)?", 600,3000)
        
                                               
    def save_options(self, options: dict):
        for option in options:        
            if option == "running_time":
                self.running_time = options[option]
            elif option == "take_breaks":
                self.take_breaks = options[option] != []
            elif option == "break_length_min":
                self.break_length_min = options[option]
            elif option == "break_length_max":
                self.break_length_max = (options[option])
            elif option == "mouse_speed":
                self.mouse_speed = options[option]
            elif option == "time_between_actions_min":
                self.time_between_actions_min = options[option]/1000
            elif option == "time_between_actions_max":
                self.time_between_actions_max = options[option]/1000
            elif option == "break_probabilty":
                self.break_probabilty = options[option]/100
                
                
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg(f"Bot will{' ' if self.take_breaks else ' not '}take breaks.")
        self.log_msg(f"We are making {self.potion_to_make}s")
        self.log_msg("Options set successfully.")
        self.options_set = True
        
        

    def main_loop(self):
        print(self.mouse_speed)
        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:
            if rd.random_chance(probability=self.break_probabilty) and self.take_breaks:
                self.take_break(min_seconds =self.break_length_min, max_seconds=self.break_length_max, fancy=True)   
        
            self.update_progress((time.time() - start_time) / end_time)
            self.bot_loop_main()
            function_end_time = time.time()
            elapsed_time = function_end_time - start_time
            hours_elapsed = elapsed_time / 3600
            bars_per_hour = self.barsmade / hours_elapsed
            print(f"bars made {self.barsmade}")
            print(f"bars per hour {bars_per_hour}")
        self.update_progress(1)
        self.log_msg("Finished.")
        self.logout()
        self.stop()
         
    
            

            
    '''def bot_loop_main(self):
        self.find_Bank()
        self.deposit_all()
        #self.depsoit_bars()
        self.CheckActiveStamina()
        self.check_run_engery()
        self.get_coal()
        self.fill_coalBag()
        #self.get_gold()
        self.close_bank()
        self.deposit_Ores()
        self.wait_for_ores_Deposit()
        self.empty_coalBag()
        self.deposit_Ores()
        self.wait_for_coal_Deposit()
        self.find_Bank()
        self.deposit_all2()
        self.CheckActiveStamina()
        self.check_run_engery()
        self.get_adamantite()
        self.fill_coalBag()
        self.close_bank()
        self.deposit_Ores()
        self.wait_for_ores_Deposit()
        self.empty_coalBag()
        self.deposit_Ores()
        self.wait_for_coal_Deposit()
        #self.glove_switch_tile()
        #self.switch_gloves_Ice()
        self.collectBars()
        self.wait_for_bar_collecion()
        #self.switch_gloves_Gold()
        self.barsmade = self.barsmade + 27'''
        
    def bot_loop_main(self):
        self.find_Bank()
        self.CheckActiveStamina()
        self.check_run_engery()
        
        self.get_adamantite()
        self.fill_coalBag()
        self.close_bank()
        self.deposit_Ores()
        self.wait_for_ores_Deposit()
        self.empty_coalBag()
        self.deposit_Ores()
        self.wait_for_coal_Deposit()
        self.find_Bank()
        self.deposit_all2()
        self.CheckActiveStamina()
        self.check_run_engery()
        
        self.coal_run()
        self.coal_run()
        self.coal_run_no_bank()
        
        self.collectBars()
        self.wait_for_bar_collecion()
        
        self.find_Bank()
        self.deposit_all()
        self.get_adamantite()
        self.fill_coalBag()
        self.close_bank()
        self.deposit_Ores()
        self.wait_for_ores_Deposit()
        self.empty_coalBag()
        self.deposit_Ores()
        self.wait_for_coal_Deposit()
        self.collectBars()
        self.wait_for_bar_collecion()
        
        self.barsmade = self.barsmade + 54
        
        
    def coal_run(self):
        self.get_coal()
        self.fill_coalBag()
        self.close_bank()
        self.deposit_Ores()
        self.wait_for_ores_Deposit()
        self.empty_coalBag()
        self.deposit_Ores()
        self.wait_for_coal_Deposit()
        self.find_Bank()
        self.deposit_all2()
    
    def coal_run_no_bank(self):
        self.get_coal()
        self.fill_coalBag()
        self.close_bank()
        self.deposit_Ores()
        self.wait_for_ores_Deposit()
        self.empty_coalBag()
        self.deposit_Ores()
        self.wait_for_coal_Deposit()
        
        
    def depsoit_bars(self):
        self.mouse.move_to(self.win.inventory_slots[0].random_point())
        self.mouse.click()
        EmptySlot27_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "emptySlot27.png")  
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        counter = 0

        while True:
            EmptySlot27 = imsearch.search_img_in_rect(EmptySlot27_img, self.win.inventory_slots[27])
            if EmptySlot27:  
                break
            time.sleep(0.1)
        print("inventory emptied")
       
        
        
    def find_Bank(self):
        print("Find Bank")
        count = 0
        self.collection_attempts = 0
        if bank := self.get_all_tagged_in_rect(self.win.game_view, clr.CYAN):
            bank = sorted(bank, key=RuneLiteObject.distance_from_rect_center)
            while True:
                bank = self.get_all_tagged_in_rect(self.win.game_view, clr.CYAN)
                bank = sorted(bank, key=RuneLiteObject.distance_from_rect_center)   
                if bank:         
                    self.mouse.move_to(bank[0].random_point(),mouseSpeed=self.mouse_speed[0])
                    time.sleep(rd.fancy_normal_sample(0.1,0.3))
                    break
            self.mouse.click(check_red_click=True)


            
    def deposit_all(self):
        Desposit_all_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "deposit.png")  
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        counter = 0

        while True:
            Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.game_view)
            if Desposit_all:  
                break
            time.sleep(0.1)
            counter = counter + 1
            if counter ==90:
                self.find_Bank()
            if counter == 120:
                self.logout()
                self.stop()
        Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.game_view)
        self.mouse.move_to(Desposit_all.random_point(),mouseSpeed=self.mouse_speed[0])
        self.mouse.click()
        
    def deposit_all2(self):
        Desposit_all_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "deposit.png")  
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        counter = 0

        while True:
            Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.game_view)
            if Desposit_all:  
                break
            time.sleep(0.1)
            counter = counter + 1
            if counter ==90:
                self.find_Bank()
            if counter == 120:
                self.logout()
                self.stop()

 
          
        
        
    def close_bank(self):
        print("close bank")
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        Close_Bank_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "x.png")
        counter = 0
        if Close_bank := imsearch.search_img_in_rect(Close_Bank_img, self.win.game_view):
            self.mouse.move_to(Close_bank.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            while True:
                if Close_bank := imsearch.search_img_in_rect(Close_Bank_img, self.win.game_view):
                    counter = counter + 1
                    time.sleep(0.1)
                    if counter > 10:
                        print("retrying close bank")
                        self.close_bank()
                        time.sleep(0.8)
                else:
                    time.sleep(.1)
                    break
                
                
        else:
            self.log_msg(f"Could not close bank")
            self.stop()                      
                      
                      
    def get_coal(self):
        Desposit_all_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "Coal_bank.png")  
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        counter = 0

        while True:
            Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.game_view)
            if Desposit_all:
                break
            time.sleep(0.1)
            counter = counter + 1
            if counter ==10:
                self.find_Bank()
            if counter == 20:
                self.logout()
                self.stop()
        Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.game_view)
        if Desposit_all:  
            self.mouse.move_to(Desposit_all.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
            self.mouse.click()
            time.sleep(0.1)
        
        
        
    def get_adamantite(self):
        Desposit_all_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "Runite_ore_bank.png")  
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        counter = 0

        while True:
            Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.game_view)
            if Desposit_all:  
                break
            time.sleep(0.1)
            counter = counter + 1
            if counter ==10:
                self.find_Bank()
            if counter == 20:
                self.logout()
                self.stop()
        Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.game_view)  
        self.mouse.move_to(Desposit_all.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
        self.mouse.click()
        
    def get_gold(self):
        Desposit_all_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "Gold_ore_bank.png")  
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        counter = 0

        while True:
            Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.game_view)
            if Desposit_all:  
                break
            time.sleep(0.1)
            counter = counter + 1
            if counter ==10:
                self.find_Bank()
            if counter == 20:
                self.logout()
                self.stop()
        Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.game_view)  
        self.mouse.move_to(Desposit_all.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
        self.mouse.click()
        
        
    def fill_coalBag(self):
        Desposit_all_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "Coal_bag.png")
        fill_bag_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "FillCoalBag.png")
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        counter = 0

        while True:
            Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.control_panel)
            if Desposit_all:  
                break
            time.sleep(0.1)
            counter = counter + 1
            if counter ==10:
                self.find_Bank()
            if counter == 20:
                self.logout()
                self.stop()
        Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.control_panel)  
        self.mouse.move_to(Desposit_all.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
        self.mouse.click()
      
        
        
    def empty_coalBag(self):
        Desposit_all_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "Coal_bag.png")
        fill_bag_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "empty_coal_bag.png")
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        counter = 0

        while True:
            Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.control_panel)
            if Desposit_all:  
                break
            time.sleep(0.1)
            counter = counter + 1
            if counter ==10:
                self.find_Bank()
            if counter == 20:
                self.logout()
                self.stop()
        Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.control_panel)  
        self.mouse.move_to(Desposit_all.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
        self.mouse.click()
        time.sleep(Sleep_time)
        

    def switch_gloves_Ice(self):
            Desposit_all_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "Ice_gloves.png")
            Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
            counter = 0

            while True:
                Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.control_panel)
                if Desposit_all:  
                    break
                time.sleep(0.1)
                if counter == 20:
                    self.logout()
                    self.stop()
            Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.control_panel)  
            self.mouse.move_to(Desposit_all.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
            self.mouse.click()
            time.sleep(Sleep_time)
            
    def switch_gloves_Gold(self):
            Desposit_all_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "Goldsmith_gauntlets.png")
            Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
            counter = 0

            while True:
                Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.control_panel)
                if Desposit_all:  
                    break
                time.sleep(0.1)
                if counter == 20:
                    self.logout()
                    self.stop()
            Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.control_panel)  
            self.mouse.move_to(Desposit_all.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
            self.mouse.click()
            time.sleep(Sleep_time)
        
            
                                                       
    def deposit_Ores(self):
        print("deposit ores")
        count = 0
        if hopper := self.get_all_tagged_in_rect(self.win.game_view, clr.PURPLE):
            hopper = sorted(hopper, key=RuneLiteObject.distance_from_rect_center)
            while True:
                hopper = self.get_all_tagged_in_rect(self.win.game_view, clr.PURPLE)
                hopper = sorted(hopper, key=RuneLiteObject.distance_from_rect_center)   
                if hopper:         
                    self.mouse.move_to(hopper[0].random_point(),mouseSpeed=self.mouse_speed[0])
                    time.sleep(rd.fancy_normal_sample(0.1,0.3))
                    break  
            self.mouse.click(check_red_click=True)
                
        
    def wait_for_ores_Deposit(self):
        EmptySlot27_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "emptySlot27.png")  
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        counter = 0

        while True:
            EmptySlot27 = imsearch.search_img_in_rect(EmptySlot27_img, self.win.inventory_slots[27])
            if EmptySlot27:  
                break
            time.sleep(0.1)
            counter = counter + 1
            if counter ==70:
                self.deposit_Ores()
                time.sleep(Sleep_time)
        EmptySlot27 = imsearch.search_img_in_rect(EmptySlot27_img, self.win.inventory_slots[27])  
        print("inventory emptied")
    
    def wait_for_coal_Deposit(self):
        EmptySlot27_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "emptySlot27.png")  
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        counter = 0

        while True:
            EmptySlot27 = imsearch.search_img_in_rect(EmptySlot27_img, self.win.inventory_slots[27])
            if EmptySlot27:  
                break
            time.sleep(0.5)
            counter = counter + 1
            if counter ==8:
                self.deposit_Ores()
                time.sleep(Sleep_time)
        EmptySlot27 = imsearch.search_img_in_rect(EmptySlot27_img, self.win.inventory_slots[27])  
        print("inventory emptied")
        
        
    def collectBars(self):
        self.collection_attempts = self.collection_attempts + 1
        if self.collection_attempts <10:
            if broken_wheel := self.get_all_tagged_in_rect(self.win.game_view, clr.GREEN):
                broken_wheel = sorted(broken_wheel, key=RuneLiteObject.distance_from_rect_center)
                while True:            
                    broken_wheel = self.get_all_tagged_in_rect(self.win.game_view, clr.GREEN)
                    broken_wheel = sorted(broken_wheel, key=RuneLiteObject.distance_from_rect_center)
                    if broken_wheel:
                        self.mouse.move_to(broken_wheel[0].random_point(),mouseSpeed=self.mouse_speed[0])
                        time.sleep(rd.fancy_normal_sample(0.2,0.35))
                        break   
                self.mouse.click()
        else:
            self.logout()
            self.stop()
    
    def wait_for_bar_collecion(self):
        Desposit_all_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "adamant_bar_chat.png")  
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        counter = 0

        while True:
            Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.chat)
            if Desposit_all:  
                break
            time.sleep(rd.fancy_normal_sample(0.1,0.4))
            counter = counter + 1
            if counter > 13:
                counter = 0
                self.collectBars()
           
        #Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.chat)  
        self.mouse.move_to(Desposit_all.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
        self.mouse.click()
        time.sleep(0.3)
        self.check_for_full_collect()
        
    def check_for_full_collect(self):
        EmptySlot27_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "emptySlot27.png")  
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        counter = 0
        trys = 0

        while True:
            EmptySlot27 = imsearch.search_img_in_rect(EmptySlot27_img, self.win.inventory_slots[27])
            if EmptySlot27:  
                counter = counter +1
                time.sleep(0.1)
            else:
                self.collection_attempts = 0
                break
            if counter ==20:
                    counter = 0
                    self.collectBars()
                    self.wait_for_bar_collecion()
                    time.sleep(Sleep_time)
        EmptySlot27 = imsearch.search_img_in_rect(EmptySlot27_img, self.win.inventory_slots[27])  

    
    def check_run_engery(self):
        if self.stamina_active == False:
            Stamina_Potion_1_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "Stamina_potion(1)_bank.png")
            Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
            Stamina_Potion_1 = imsearch.search_img_in_rect(Stamina_Potion_1_img, self.win.game_view)
          
            if Stamina_Potion_1:  
                Stamina_Potion_1 = imsearch.search_img_in_rect(Stamina_Potion_1_img, self.win.game_view)  
                self.mouse.move_to(Stamina_Potion_1.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
                self.mouse.click()
                time.sleep(1)
                self.drink_stamina_pot()
                self.deposit_all()
            else: 
                self.log_msg("out of Stamina Potions")
                self.logout()
                self.stop()
            
    
    def drink_stamina_pot(self):
            Stamina_Potion_1_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "Stamina_potion(1).png")
            drink_stamina_Potion_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "drink_stamina.png")
            Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
            Stamina_Potion_1 = imsearch.search_img_in_rect(Stamina_Potion_1_img, self.win.inventory_slots[1])
            
            if Stamina_Potion_1:  

                self.mouse.move_to(Stamina_Potion_1.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
                self.mouse.right_click()
                drink_stamina_Potion = imsearch.search_img_in_rect(drink_stamina_Potion_img, self.win.control_panel)
                if drink_stamina_Potion:
                    self.mouse.move_to(drink_stamina_Potion.random_point(),mouseSpeed="fast")
                    self.mouse.click()
                
            else: 
                self.log_msg("out of Stamina Potions")
                self.logout()
                self.stop()
           
    def deposit_stamina_pot(self):
            Stamina_Potion_4_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "Stamina_potion(4)_bank.png")
            Stamina_Potion_3_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "Stamina_potion(3)_bank.png")
            Stamina_Potion_2_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "Stamina_potion(2)_bank.png")
            Stamina_Potion_1_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "Stamina_potion(1)_bank.png")
            Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
            Stamina_Potion_4 = imsearch.search_img_in_rect(Stamina_Potion_4_img, self.win.control_panel)
            Stamina_Potion_3 = imsearch.search_img_in_rect(Stamina_Potion_3_img, self.win.control_panel)
            Stamina_Potion_2 = imsearch.search_img_in_rect(Stamina_Potion_2_img, self.win.control_panel)
            Stamina_Potion_1 = imsearch.search_img_in_rect(Stamina_Potion_1_img, self.win.control_panel)
            
            if Stamina_Potion_4:  
                Stamina_Potion_4 = imsearch.search_img_in_rect(Stamina_Potion_4_img, self.win.control_panel)  
                self.mouse.move_to(Stamina_Potion_4.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
                self.mouse.click()
            if Stamina_Potion_3:  
                Stamina_Potion_3 = imsearch.search_img_in_rect(Stamina_Potion_3_img, self.win.control_panel)  
                self.mouse.move_to(Stamina_Potion_3.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
                self.mouse.click()
            if Stamina_Potion_2:  
                Stamina_Potion_2 = imsearch.search_img_in_rect(Stamina_Potion_2_img, self.win.control_panel)  
                self.mouse.move_to(Stamina_Potion_2.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
                self.mouse.click()
            if Stamina_Potion_1:  
                Stamina_Potion_1 = imsearch.search_img_in_rect(Stamina_Potion_1_img, self.win.control_panel)  
                self.mouse.move_to(Stamina_Potion_1.random_point(),mouseSpeed=self.mouse_speed[0])#change this line to click on item in inventory
                self.mouse.click()
                
          
            
    def CheckActiveStamina(self):
        Desposit_all_img = imsearch.BOT_IMAGES.joinpath("BlastFurnace_IMG", "stamina_active.png")  
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.run_orb)
        if Desposit_all: 
            self.stamina_active = True
        else:
            self.stamina_active = False

    def glove_switch_tile(self):
        print("Find Bank")
        count = 0
        if bank := self.get_all_tagged_in_rect(self.win.game_view, clr.PINK):
            bank = sorted(bank, key=RuneLiteObject.distance_from_rect_center)
            while True:
                bank = self.get_all_tagged_in_rect(self.win.game_view, clr.PINK)
                bank = sorted(bank, key=RuneLiteObject.distance_from_rect_center)   
                if bank:         
                    self.mouse.move_to(bank[0].random_point(),mouseSpeed=self.mouse_speed[0])
                    time.sleep(rd.fancy_normal_sample(0.1,0.3))
                    break
            self.mouse.click()
            time.sleep(rd.fancy_normal_sample(2.8,3.1))
            
