from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_and_tap_template, find_template
from src.core.adb import press_back

class HelpRoutine(TimeCheckRoutine):
    def _execute(self) -> bool:
        """Check and click help button if available"""
        return self.execute_with_error_handling(self._execute_internal)
        
    def _execute_internal(self) -> bool:
        if not find_and_tap_template(
            self.device_id,
            "help",
            error_msg="No help needed at this time",
            success_msg="Helping allies!"
        ):
            if not find_template(self.device_id, "home"):
                press_back(self.device_id)
                return True
            
        return True 