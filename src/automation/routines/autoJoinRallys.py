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
            "map",
            error_msg="Already on map screen",
            success_msg="Opened map screen"
        ):
            time.sleep(1)

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
                    time.sleep(1)
                    find_and_tap_template(
                        self.device_id,
                        "rally_back_home",
                        error_msg="Already on home screen",
                        success_msg="Navigated back to home"
                    )
                    return True
                else:
                    press_back(self.device_id)
            else:
                press_back(self.device_id)

        return True 