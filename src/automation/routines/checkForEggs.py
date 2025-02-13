from src.automation.routines import TimeCheckRoutine
from src.core.logging import app_logger
from src.core.config import CONFIG
from src.core.image_processing import find_and_tap_template
from src.core.discord_bot import DiscordNotifier
from discord import Embed
import asyncio
import os

class CheckForEggsRoutine(TimeCheckRoutine):
    
    def __init__(self, device_id: str, interval: int, last_run: float = None, automation=None):
        super().__init__(device_id, interval, last_run, automation)
        self.discord = DiscordNotifier()
        self.is_enabled = bool(os.getenv('DISCORD_WEBHOOK_URL'))
        if not self.is_enabled:
            app_logger.warning("Egg notification routine disabled: DISCORD_WEBHOOK_URL not found in environment variables")
        
    def _execute(self) -> bool:
        """Execute egg notification check sequence"""
        if not self.is_enabled:
            return True
        return self.execute_with_error_handling(self._execute_internal)
        
    def _execute_internal(self) -> bool:
        """Check for egg icon and handle if found"""
        try:
            # Open chat by clicking the dig icon
            if not find_and_tap_template(
                self.device_id,
                "egg",
                error_msg="Could not find egg icon",
                success_msg="Found egg icon"
            ):
                return True
            
            self.automation.game_state["is_home"] = False;
                
            # Send Discord notification
            asyncio.run(self.send_notification())
            return True
            
        except Exception as e:
            app_logger.error(f"Error in egg check routine: {e}")
            return False
            
    async def send_notification(self) -> bool:
        """Send bilingual notification"""
        return True
        if not self.is_enabled:
            return True
            
        egg_config = CONFIG['discord']['egg_notification']
        embed = Embed(color=int(egg_config['embed_color'], 16))
        embed.add_field(
            name=egg_config['embed_title'],
            value=egg_config['embed_value']
        )
        
        return await self.discord.send_notification(
            egg_config['content'],
            embed,
            username=CONFIG['discord'].get('bot_name', 'Last War Bot')
        )
