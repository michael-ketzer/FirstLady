
from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_and_tap_template, _take_and_load_screenshot
import time
from src.core.adb import press_back
from src.core.logging import app_logger
from src.game.controls import handle_swipes
import cv2

class VsWeeklyTopListRoutine(TimeCheckRoutine):
    def _execute(self) -> bool:
        """Check and click secret task button if available"""
        return self.execute_with_error_handling(self._execute_internal)
        
    def _execute_internal(self) -> bool:
        if find_and_tap_template(
            self.device_id,
            "vs_icon",
            error_msg="No vs icon",
            success_msg="Starting vs weekly top list routine"
        ):
            time.sleep(1)

            if find_and_tap_template(
                self.device_id,
                "vs_ranking",
                error_msg="Could not find vs ranking button",
                success_msg="Found vs ranking button"
            ):
                time.sleep(1)
                if find_and_tap_template(
                    self.device_id,
                    "vs_weekly",
                    error_msg="Could not find vs weekly button",
                    success_msg="Found vs weekly button"
                ):
                    for i in range(10):
                        img = _take_and_load_screenshot(self.device_id)
                        cv2.imwrite(f'tmp/vs_duell_toplist_{i}.png', img)
                        handle_swipes(self.device_id, direction="down", num_swipes=1)
                        time.sleep(3)
                    return True
                else:
                    press_back(self.device_id)
            else:
                press_back(self.device_id)

        return True