from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_and_tap_template
from src.game.controls import navigate_home
import time

class CheckValentineGiftRoutine(TimeCheckRoutine):
    def _execute(self) -> bool:
        """Check and click valentine button if available"""
        return self.execute_with_error_handling(self._execute_internal)
        
    def _execute_internal(self) -> bool:
        if find_and_tap_template(
            self.device_id,
            "valentine_icon",
            error_msg="No valentine icon at this time",
            success_msg="Started valentine gift routine!"
        ):
            time.sleep(5)

            if find_and_tap_template(
                self.device_id,
                "valentine_new",
                error_msg="No new gifts available",
                success_msg="Found new gifts!"
            ):
                time.sleep(1)

            find_and_tap_template(
                self.device_id,
                "valentine_open",
            )
            navigate_home(self.device_id, True)
            
        return True 