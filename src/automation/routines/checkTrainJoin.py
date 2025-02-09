from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_and_tap_template
from src.game.controls import navigate_home
import time

class CheckTrainJoinRoutine(TimeCheckRoutine):
    def _execute(self) -> bool:
        """Check and click help button if available"""
        return self.execute_with_error_handling(self._execute_internal)
        
    def _execute_internal(self) -> bool:
        if find_and_tap_template(
            self.device_id,
            "train_icon",
            error_msg="No join train icon at this time",
            success_msg="Started train onboarding!"
        ):
            if find_and_tap_template(
                self.device_id,
                "train_outer_seat",
                error_msg="Could not join train",
                success_msg="Successfully opened train onboarding!"
            ):
                time.sleep(10)

                if find_and_tap_template(
                    self.device_id,
                    "train_join",
                    error_msg="Could not take seat in train",
                    success_msg="Successfully took seat in the train!"
                ):
                    navigate_home(self.device_id, True)
                    return True
            
        return True 