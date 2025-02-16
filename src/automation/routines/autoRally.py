from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_and_tap_template, find_template
import time
from src.core.adb import press_back
from src.core.config import CONFIG
from src.core.logging import app_logger

class AutoRallyRoutine(TimeCheckRoutine):
    def _execute(self) -> bool:
        """Start Routine"""
        return self.execute_with_error_handling(self._execute_internal)
        
    def _execute_internal(self) -> bool:

        energy_loc = find_template(
            self.device_id,
            "got_energy"
        )

        if energy_loc:
            app_logger.info("Got enough energy to start a rally")
            for _ in range(CONFIG['autoRallySquads']):
                if not self._start_rally():
                    return False
        else:
            app_logger.info("Not enough energy to start a rally")

        return True 
    
    def _start_rally(self) -> bool:
        """Start a rally"""
        if find_and_tap_template(
            self.device_id,
            "map",
            error_msg="Already on map screen",
            success_msg="Opened map screen"
        ):
            time.sleep(1)

        if find_and_tap_template(
            self.device_id,
            "rally_search",
            error_msg="No rally search icon at this time",
            success_msg="Starting rally creation sequence!"
        ):
            time.sleep(1)

            find_and_tap_template(
                self.device_id,
                "rally_doom_elite",
                error_msg="Already on doom elite search",
                success_msg="Switched to doom elite search"
            )

            if find_and_tap_template(
                self.device_id,
                "rally_search_doom_elite",
                error_msg="Could not search for doom elite rally",
                success_msg="Searching doom elite rally"
            ):
                time.sleep(1)
                if find_and_tap_template(
                    self.device_id,
                    "rally_start",
                    error_msg="Could not find doom elite",
                    success_msg="Starting squad selection!"
                ):
                    time.sleep(1)
                    find_and_tap_template(
                        self.device_id,
                        "rally_fight",
                        error_msg="Could not create rally, all squads are out",
                        success_msg="Created new doom elite rally"
                    )
                    return True
                else:
                    press_back(self.device_id)
            else:
                press_back(self.device_id)

        return True 