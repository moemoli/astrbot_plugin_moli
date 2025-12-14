from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import (
    AiocqhttpMessageEvent,
)


class NapCat:
    def __init__(self):
        pass

    async def send_poke(
        self, event: AiocqhttpMessageEvent, user_id: str, group_id: str
    ):
        await event.bot.call_action(
            "send_poke",
            user_id=user_id,
            group_id=group_id,
        )

    async def set_msg_emoji_like(
        self, event: AiocqhttpMessageEvent, message_id: int, emoji_id: str
    ):
        await event.bot.call_action(
            "set_msg_emoji_like",
            message_id=message_id,
            emoji_id=emoji_id,
            set=True,
        )
