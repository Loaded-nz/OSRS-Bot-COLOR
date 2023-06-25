import time
import utilities.color as clr
import utilities.random_util as rd
import utilities.game_launcher as launcher
import utilities.imagesearch as imsearch
from model.osrs.osrs_bot import OSRSBot

 
class OSRSHunter(OSRSBot, launcher.Launchable):
    
    def __init__(self):
        bot_title = "Red chin bot"
        description = "This bot hunts red chins."
        super().__init__(bot_title=bot_title, description=description)
        self.running_time = 1
        self.take_breaks = False


    def create_options(self):
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 500)

        
    def save_options(self, options: dict):
        for option in options:
            if option == "running_time":
                self.running_time = options[option]            
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
        
        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:  
            self.update_progress((time.time() - start_time) / end_time)
            self.bot_loop_main()
        self.update_progress(1)
        self.log_msg("Finished.")
        self.stop()
        
               
    def bot_loop_main(self):
        self.hunt()
    
    def hunt(self):
        yellow_traps = self.get_all_tagged_in_rect(self.win.game_view, clr.YELLOW)
        
        if not yellow_traps:                   
            if caught_trap := self.get_all_tagged_in_rect(self.win.game_view, clr.PINK):
                self.mouse.move_to(caught_trap[0].center(), mouseSpeed="fastest")
                self.log_msg("Caught the chin $$$")
                if self.mouseover_text(contains= "Reset", color=clr.OFF_WHITE):
                    self.mouse.click()
                    time.sleep(7.25)
        
        if not self.get_nearest_tag(clr.PINK):
            if failed_trap := self.get_all_tagged_in_rect(self.win.game_view, clr.RED):
                self.log_msg("Slippery chinchompa got away :(")
                self.mouse.move_to(failed_trap[0].center(), mouseSpeed='fastest')
                if self.mouseover_text(contains= "Reset", color=clr.OFF_WHITE):
                    self.mouse.click()
                    time.sleep(7.25)      
        
        if reset_trap := self.get_nearest_tag(clr.OFF_YELLOW):
            self.log_msg("Resetting trap, must of had a funny smell..")
            self.mouse.move_to(reset_trap.random_point(), mouseSpeed='fastest')
            if self.mouseover_text(contains= "Lay", color=clr.OFF_WHITE):
                self.mouse.click()
                time.sleep(5)
            
        
        box_traps = self.get_all_tagged_in_rect(self.win.game_view, clr.CYAN)                                   
        probability = 0.10
        if len(box_traps) == 5:
            while True:
                self.log_msg("waiting for chins")
                if rd.random_chance(probability):
                    self.mouse.move_to(self.win.game_view.random_point(), mouseSpeed="medium", knotsCount=2)
                    probability /= 2
                break