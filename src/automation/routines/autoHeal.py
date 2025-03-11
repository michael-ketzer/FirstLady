from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_and_tap_template, find_all_templates, find_template
import time
from src.game.controls import navigate_home, humanized_tap

class AutoHealRoutine(TimeCheckRoutine):
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
            time.sleep(1)


        collect_loc = find_template(self.device_id, 'heal_collect')
        if collect_loc:
            humanized_tap(self.device_id, collect_loc[0], collect_loc[1])


        if find_and_tap_template(
            self.device_id,
            "heal_icon",
            error_msg="No heal required at this time",
            success_msg="Starting heal sequence!"
        ):
            
            if find_and_tap_template(
                self.device_id,
                "heal_start",
                error_msg="Started healing wounded soldiers",
                success_msg="Could not start healing!"
            ):
                time.sleep(0.2)

                help_loc = find_all_templates(self.device_id, 'heal_ask_for_help')

                for x, y in help_loc:
                    humanized_tap(self.device_id, x, y)

            else:
                navigate_home(self.device_id)            

        return True 