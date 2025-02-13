from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_and_tap_template
import time
from src.core.adb import press_back

class AutoJoinRallysRoutine(TimeCheckRoutine):
    def _execute(self) -> bool:
        """Check and click help button if available"""
        return self.execute_with_error_handling(self._execute_internal)
        
    def _execute_internal(self) -> bool:
        if find_and_tap_template(
            self.device_id,
            "rally_icon",
            error_msg="No rally open at this time",
            success_msg="Starting rally join sequence!"
        ):
            if find_and_tap_template(
                self.device_id,
                "rally_available",
                error_msg="Could not find any doom elite rallys",
                success_msg="Starting join sequence!"
            ):
                time.sleep(1)
                if find_and_tap_template(
                    self.device_id,
                    "rally_join",
                    error_msg="Could not join rally, all squads are out",
                    success_msg="Joined doom rally!"
                ):
                  return True
            else:
              press_back(self.device_id)

        return True 