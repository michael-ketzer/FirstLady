from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_and_tap_template
from src.game.controls import navigate_home
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
            if find_and_tap_template(
                self.device_id,
                "survivor_accept",
                error_msg="Could not accept survivor",
                success_msg="Successfully accepted new survivor!"
            ):
                return True
            
        return True 