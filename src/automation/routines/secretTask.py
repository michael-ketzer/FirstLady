from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_and_tap_template, find_all_templates, find_template
import time
from src.core.adb import press_back
from src.core.logging import app_logger
from src.game.controls import humanized_tap

class SecretTaskRoutine(TimeCheckRoutine):
    def _execute(self) -> bool:
        """Check and click secret task button if available"""
        return self.execute_with_error_handling(self._execute_internal)
        
    def _execute_internal(self) -> bool:

        if find_and_tap_template(
            self.device_id,
            "secret_icon",
            error_msg="No secret task icon",
            success_msg="Starting secret task routine"
        ):
            time.sleep(1)

            # claim current tasks
            claim_loc = find_all_templates(self.device_id, "secret_claim")

            # claim current tasks
            if len(claim_loc) > 0:
                for x, y in claim_loc:
                    app_logger.info(f"Claiming secret task")
                    humanized_tap(self.device_id, x, y)
                    time.sleep(0.5)
                    press_back(self.device_id)
                    time.sleep(0.5)
                press_back(self.device_id)
                find_and_tap_template(
                    self.device_id,
                    "secret_icon",
                    error_msg="No secret task icon",
                    success_msg="Starting secret task routine"
                )

            # start new secret tasks
            all_go_loc = find_all_templates(self.device_id, "secret_go")
            if len(all_go_loc) == 0:
                app_logger.info('No available secret tasks found')
                return True
            
            while not self._has_secret_task_on_top():
                app_logger.info('Finding secret task')
                refresh_loc = find_template(self.device_id, "secret_refresh")
                if refresh_loc:
                    app_logger.info("Found refresh button")
                    humanized_tap(self.device_id, refresh_loc[0], refresh_loc[1])
                else:
                    refresh_dia_loc = find_template(self.device_id, "secret_refresh_dias")
                    if refresh_dia_loc:
                        app_logger.info("Found refresh diamonds button")
                        humanized_tap(self.device_id, refresh_dia_loc[0], refresh_dia_loc[1])
                time.sleep(1)

            self._deploy_first_task(all_go_loc)
            return True
            
    
    def _get_top_secret_task(self) -> tuple[int, int]:
        task_loc = find_all_templates(self.device_id, "secret_task_1") + find_all_templates(self.device_id, "secret_task_2") + find_all_templates(self.device_id, "secret_task_3") + find_all_templates(self.device_id, "secret_task_4")

        for x, y in task_loc:
            app_logger.info(f"Found task at {x}, {y}")
            if y == 989:
                return (x, y)
    
    def _has_secret_task_on_top(self) -> bool:
        top_task_loc = self._get_top_secret_task()
        if top_task_loc:
            return True
        else:
            return False
        
                        
    def _deploy_first_task(self, go_loc: tuple[int, int]) -> bool:
        # find the respected go button
        for locX, locY in go_loc:
            if locY > 969 and locY < 1123:
                app_logger.info("Found go button")
                humanized_tap(self.device_id, locX, locY)
                time.sleep(2)
                return self._execute_quick_deploy()
        return True
    
    def _execute_quick_deploy(self) -> bool:
        app_logger.info("Quick deploying secret task")
        if find_and_tap_template(
            self.device_id,
            "secret_qd",
            error_msg="Could not find quick deploy button",
            success_msg="Pressed quick deploy!"
        ):
            time.sleep(1)
            no_deploy_loc = find_template(self.device_id, "secret_no_deploy")
            if no_deploy_loc:
                app_logger.info("All teams are deployed already, skipping this turn")
                press_back(self.device_id)
                return True
            
            if find_and_tap_template(
                self.device_id,
                "secret_deploy",
                error_msg="Could not find deploy button",
                success_msg="Deployed secret task"
            ): 
                return True