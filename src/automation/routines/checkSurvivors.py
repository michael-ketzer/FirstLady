from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_template, find_and_tap_template, find_all_templates
from src.game.controls import navigate_home
from src.core.logging import app_logger
from src.game.controls import humanized_tap
import time

class CheckNewSurvivorsRoutine(TimeCheckRoutine):
    def _execute(self) -> bool:
        """Check and click help button if available"""
        return self.execute_with_error_handling(self._execute_internal)
        
    def _execute_internal(self) -> bool:
        if find_and_tap_template(
            self.device_id,
            "survivor_icon",
            error_msg="No survivor icon at this time",
            success_msg="Found a survivor, attempting to let him join"
        ):
            all_templates = find_all_templates(self.device_id, 'survivor_accept')
            humanized_tap(self.device_id, 544, 1075) #Game somehow does not accept the first tap, maybe due to the stupid arrow
            for _i in range(len(all_templates)):
                humanized_tap(self.device_id, 544, 1075)
                time.sleep(2)

            return True
            
        return True 