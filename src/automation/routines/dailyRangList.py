
from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_and_tap_template, find_all_templates, get_server
import time
from src.game.controls import human_delay, humanized_tap, handle_swipes,navigate_home, exact_handle_swipes
from src.core.logging import app_logger
from src.core.adb import get_screen_size
from src.core.config import CONFIG
from src.core.device import save_screenshot
import aiohttp
import asyncio
from src.core.audio import play_beep


class DailyRangListRoutine(TimeCheckRoutine):
    def _execute(self) -> bool:
        return self.execute_with_error_handling(self._execute_internal)
        
    def _execute_internal(self) -> bool:
        # open map screen
        if find_and_tap_template(
            self.device_id,
            "map",
            error_msg="Already on map screen",
            success_msg="Opened map screen"
        ):
            time.sleep(1)

        self._start_routine()

        return True

    def _start_routine(self) -> bool:
        for cateogry in ['ranglist_search_special', 'ranglist_search_friend']:
            for i in range(8):
                app_logger.info(f"Recording toplist on server {cateogry} #{i}")
                if find_and_tap_template(
                    self.device_id,
                    "ranglist_search",
                    error_msg="Could not find search button",
                ):
                    time.sleep(0.1)

                    if find_and_tap_template(
                        self.device_id,
                        cateogry,
                        error_msg="Could not find category",
                    ):
                        time.sleep(0.1)

                        if(i >= 4):
                            custom_swipe_cfg = {
                                'start_x': '20%',
                                'start_y': '20%',
                                'end_x': '10%',
                                'end_y': '40%'
                            }
                            handle_swipes(self.device_id, direction="down", num_swipes=1, custom_swipe_cfg=custom_swipe_cfg)
                            time.sleep(0.5)
            
                        go_buttons = find_all_templates(self.device_id, 'ranglist_search_go')

                        if go_buttons:
                            go_buttons.sort(key=lambda b: b[1])
                            visible_index = i % 4
                            if visible_index < len(go_buttons):
                                button = go_buttons[visible_index]
                                humanized_tap(self.device_id, button[0], button[1])
                                time.sleep(0.5)
                                self._take_ranglist_screenshot()
                            else:
                                print("Could not find enough 'go' buttons on screen.")

        return True
                    
    
    def open_profile_menu(self, device_id: str) -> bool:
        """Open the profile menu"""
        try:
            width, height = get_screen_size(device_id)
            profile = CONFIG['ui_elements']['profile']
            profile_x = int(width * float(profile['x'].strip('%')) / 100)
            profile_y = int(height * float(profile['y'].strip('%')) / 100)
            humanized_tap(device_id, profile_x, profile_y)

            # Look for notification indicators

            time.sleep(2)

            if find_and_tap_template(device_id, "awesome", "No likes", "Found likes and clicked it"):
                human_delay(CONFIG['timings']['menu_animation'])                

            return True
        except Exception as e:
            app_logger.error(f"Error opening profile menu: {e}")
            return False

    def _take_ranglist_screenshot(self) -> bool:
        self.open_profile_menu(self.device_id)

        if find_and_tap_template(
            self.device_id,
            'ranglist_rankings',
            error_msg="Could not find rankings button",
        ):
            time.sleep(0.2)

            server = ""

            if find_and_tap_template(
                self.device_id,
                'ranglist_alliance_power',
                error_msg="Could not find alliance rankings button",
            ):
                server = get_server(self.device_id)
                if not server:
                    play_beep()
                    app_logger.error("Could not find server")
                    server = input('Please enter server id:')
                app_logger.info(f"Recording alliance power on server {server}")
                self._record_ranglist(location=f"{server}_alliance_power", server=server, type="ALLIANCE_RANGLIST")

            if find_and_tap_template(
                self.device_id,
                'ranglist_alliance_kills',
                error_msg="Could not find alliance kills button",
            ):
                if server == "":
                    server = get_server(self.device_id)
                    app_logger.info(f"Recording alliance kills on server {server}")
                    
                self._record_ranglist(location=f"{server}_alliance_kills", server=server, type="ALLIANCE_KILLS")

            if find_and_tap_template(
                self.device_id,
                'ranglist_individual_power',
                error_msg="Could not find individual rankings button",
            ):
                if server == "":
                    server = get_server(self.device_id)
                    app_logger.info(f"Recording individual power on server {server}")
                    
                self._record_ranglist(location=f"{server}_individual_power", server=server, type="INDIVIDUAL_RANGLIST")
            
            custom_swipe_cfg = {
                'start_x': '20%',
                'start_y': '20%',
                'end_x': '10%',
                'end_y': '40%'
            }
            handle_swipes(self.device_id, direction="down", num_swipes=1, custom_swipe_cfg=custom_swipe_cfg)
            time.sleep(0.5)


            if find_and_tap_template(
                self.device_id,
                'ranglist_hero_power',
                error_msg="Could not find hero rankings button",
            ):
                if server == "":
                    server = get_server(self.device_id)
                    app_logger.info(f"Recording individual power on server {server}")
                
                self._record_ranglist(location=f"{server}_hero_power", server=server, type="HERO_POWER_RANGLIST")
                    

            if find_and_tap_template(
                self.device_id,
                'ranglist_strongest_hero',
                error_msg="Could not find strongest hero button",
            ):
                if server == "":
                    server = get_server(self.device_id)
                    app_logger.info(f"Recording strongest hero on server {server}")
                
                self._record_ranglist(location=f"{server}_strongest_hero", server=server, type="SINGLE_HERO_POWER_RANGLIST")

            time.sleep(0.2)
            navigate_home(self.device_id)

    def _record_ranglist(self, location: str, server: str, type: str):

        custom_swipe_cfg = {
            'start_x': '20%',
            'start_y': '20%',
            'end_x': '23%',
            'end_y': '47%'
        }

        for i in range(8):
            curr_location = f"{location}_{i}"
            save_screenshot(self.device_id, location=curr_location)
            time.sleep(0.5)
            image_path=f"tmp/{curr_location}.png"
            asyncio.run(self._upload_image(image_path=image_path, server=server, type=type, sort=str(i)))
            exact_handle_swipes(self.device_id, direction="down", num_swipes=1, custom_swipe_cfg=custom_swipe_cfg)

        find_and_tap_template(self.device_id, 'ranglist_back')
        time.sleep(0.2)
                
    async def _upload_image(self, image_path: str, server: str, type: str, sort: str):
        print(f"Uploading image to Ranglist: {image_path}")

        headers = {
            "Authorization": CONFIG['ranglist']['api_key']
        }

        async with aiohttp.ClientSession() as session:
            with open(image_path, "rb") as file:
                form_data = aiohttp.FormData()
                form_data.add_field("file", file, filename=image_path, content_type="image/png")
                form_data.add_field("server", server)
                form_data.add_field("type", type)
                form_data.add_field("sort", sort)

                try:
                    async with session.post(CONFIG['ranglist']['api_url'], data=form_data, headers=headers) as response:
                        response_text = await response.text()  # Get response as text or use `.json()`
                        print(f"Upload Response: {response_text}")
                        return response_text
                except aiohttp.ClientError as e:
                    print(f"Error uploading image: {e}")
                    return None
