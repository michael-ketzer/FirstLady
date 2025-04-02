from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_and_tap_template, find_template, find_all_templates
import time
from src.core.adb import press_back, tap_screen
from src.game.controls import navigate_home,humanized_tap
import random
from src.core.logging import app_logger

class AutoJoinRallysRoutine(TimeCheckRoutine):
    def _execute(self) -> bool:
        """Check and click help button if available"""
        return self.execute_with_error_handling(self._execute_internal)
        
    def _execute_internal(self) -> bool:
        if find_and_tap_template(
            self.device_id,
            "map",
            error_msg="Already on map screen",
            success_msg="Opened map screen"
        ):
            time.sleep(0.5)

        home_loc = find_template(self.device_id, 'home')
        if not home_loc:
            press_back(self.device_id)

        if find_and_tap_template(
            self.device_id,
            "rally_icon",
            error_msg="No rally open at this time",
            success_msg="Starting rally join sequence!"
        ):
            
            time.sleep(0.1)
            if find_and_tap_template(
                self.device_id,
                "rally_available",
                error_msg="Could not find any rallys",
                success_msg="Starting joining rally!"
            ):
                time.sleep(0.4)
                zzz_loc = find_all_templates(self.device_id, 'rally_zzz', [104, 1645, 978, 1710])
                if len(zzz_loc) > 0:
                    loc = random.choice(zzz_loc)
                    tap_screen(self.device_id, loc[0], loc[1])
                    time.sleep(0.1)
                    
                    if find_and_tap_template(
                        self.device_id,
                        "rally_join",
                        error_msg="Could not rally, all squads are out",
                        success_msg="Joined rally!"
                    ):
                        return True
                else:
                    app_logger.info('Got no team at home, not joining rally')
                    time.sleep(0.2)
                    navigate_home(self.device_id)
            else: 
                find_and_tap_template(self.device_id, 'ranglist_back')

        return True 