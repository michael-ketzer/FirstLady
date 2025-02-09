from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_and_tap_template
from src.game.controls import navigate_home

class CollectTruckRoutine(TimeCheckRoutine):
    def _execute(self) -> bool:
        """Check and click help button if available"""
        return self.execute_with_error_handling(self._execute_internal)
        
    def _execute_internal(self) -> bool:
        if find_and_tap_template(
            self.device_id,
            "collect_icon",
            error_msg="No collect truck icon at this time",
            success_msg="Clicked collect truck!"
        ):
            if find_and_tap_template(
                self.device_id,
                "collect_accept",
                error_msg="Could not collect truck",
                success_msg="Collected truck!"
            ):
                navigate_home(self.device_id, True)
                return True
            
        return True 