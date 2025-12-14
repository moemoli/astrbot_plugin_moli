from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
from astrbot.core.provider.entities import ProviderRequest
from .tools import (
    napcat,
)

@register("moli", "moemoli", "Moli Bot", "1.0.0")
class MoliBot(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        self.napcat = napcat.NapCat()

    @filter.on_llm_request()
    async def message_id_hook(self, event: AiocqhttpMessageEvent, req: ProviderRequest): # 请注意有三个参数
        req.system_prompt += "\n本次发送者的消息的id为: " + str(event.message_obj.message_id) + "\n"

    @filter.llm_tool()  # type: ignore
    async def llm_poke(
        self, event: AiocqhttpMessageEvent, user_id: str, group_id: str
    ):
        """
        戳一戳某用户。被戳一戳的用户将收到戳一戳的提示。
        Args:
            user_id(string): 要戳一戳的用户的QQ账号，必定为一串数字，如(12345678)
            group_id(string): 群号，必定为一串数字，如(12345678)，若为私聊场景，该选项为空字符串
        """
        try:
            await self.napcat.send_poke(event, user_id, group_id)
            event.stop_event()
            yield
        except Exception as e:
            yield
    
    @filter.llm_tool()  # type: ignore
    async def llm_del_msg(
        self, event: AiocqhttpMessageEvent, message_id: int
    ):
        """
        撤回某一条用户的消息，被删除的消息将为群聊中所有成员不可见。
        在私聊场景中，只可以撤回自己的消息，且只能撤回两分钟内的消息。
        在群聊场景中，若你为管理员，则可以撤回所有人的消息。
        Args:
            message_id(number): 要删除的消息id，必定为一串数字，如(12345678)
            
        """
        try:
            await event.bot.delete_msg(message_id = message_id)
            event.stop_event()
            yield
        except Exception as e:
            yield
    
    @filter.llm_tool()  # type: ignore
    async def llm_get_member_info(
        self, event: AiocqhttpMessageEvent, user_id: int, group_id: int
    ):
        """
        获取你所在群的某个成员的信息。
        Args:
            user_id(number): 要获取信息的用户的QQ账号，必定为一串数字，如(12345678)
            group_id(number): 群号，必定为一串数字，如(12345678)
        """
        try:
            await event.bot.get_group_member_info(user_id=user_id, group_id=group_id)
            event.stop_event()
            yield
        except Exception as e:
            yield

    @filter.llm_tool()  # type: ignore
    async def llm_set_msg_emoji_like(
        self, event: AiocqhttpMessageEvent, message_id: int, emoji_id: str
    ):
        """
        为某个消息做出emoji回复。

        Args:
            message_id(number): 要回复的消息id，必定为一串数字，如(12345678)
            emoji_id(string): emoji的id。此为emoji的对应表: 4:得意,5:流泪,8:睡,9:大哭,10:尴尬,12:调皮,14:微笑,16:酷,21:可爱,23:傲慢,24:饥饿,25:困,26:惊恐,27:流汗,28:憨笑,29:悠闲,30:奋斗,32:疑问,33:嘘,34:晕,38:敲打,39:再见,41:发抖,42:爱情,43:跳跳,49:拥抱,53:蛋糕,60:咖啡,63:玫瑰,66:爱心,74:太阳,75:月亮,76:赞,78:握手,79:胜利,85:飞吻,89:西瓜,96:冷汗,97:擦汗,98:抠鼻,99:鼓掌,100:糗大了,101:坏笑,102:左哼哼,103:右哼哼,104:哈欠,106:委屈,109:左亲亲,111:可怜,116:示爱,118:抱拳,120:拳头,122:爱你,123:NO,124:OK,125:转圈,129:挥手,144:喝彩,147:棒棒糖,171:茶,173:泪奔,174:无奈,175:卖萌,176:小纠结,179:doge,180:惊喜,181:骚扰,182:笑哭,183:我最美,201:点赞,203:托脸,212:托腮,214:啵啵,219:蹭一蹭,222:抱抱,227:拍手,232:佛系,240:喷脸,243:甩头,246:加油抱抱,262:脑阔疼,264:捂脸,265:辣眼睛,266:哦哟,267:头秃,268:问号脸,269:暗中观察,270:emm,271:吃瓜,272:呵呵哒,273:我酸了,277:汪汪,278:汗,281:无眼笑,282:敬礼,284:面无表情,285:摸鱼,287:哦,289:睁眼,290:敲开心,293:摸锦鲤,294:期待,297:拜谢,298:元宝,299:牛啊,305:右亲亲,306:牛气冲天,307:喵喵,314:仔细分析,315:加油,318:崇拜,319:比心,320:庆祝,322:拒绝,324:吃糖,326:生气,9728:☀ 晴天,9749:☕ 咖啡,9786:☺ 可爱,10024:✨ 闪光,10060:❌ 错误,10068:❔ 问号,127801:🌹 玫瑰,127817:🍉 西瓜,127822:🍎 苹果,127827:🍓 草莓,127836:🍜 拉面,127838:🍞 面包,127847:🍧 刨冰,127866:🍺 啤酒,127867:🍻 干杯,127881:🎉 庆祝,128027:🐛 虫,128046:🐮 牛,128051:🐳 鲸鱼,128053:🐵 猴,128074:👊 拳头,128076:👌 好的,128077:👍 厉害,128079:👏 鼓掌,128089:👙 内衣,128102:👦 男孩,128104:👨 爸爸,128147:💓 爱心,128157:💝 礼物,128164:💤 睡觉,128166:💦 水,128168:💨 吹气,128170:💪 肌肉,128235:📫 邮箱,128293:🔥 火,128513:😁 呲牙,128514:😂 激动,128516:😄 高兴,128522:😊 嘿嘿,128524:😌 羞涩,128527:😏 哼哼,128530:😒 不屑,128531:😓 汗,128532:😔 失落,128536:😘 飞吻,128538:😚 亲亲,128540:😜 淘气,128541:😝 吐舌,128557:😭 大哭,128560:😰 紧张,128563:😳 瞪眼
        """
        try:
            await self.napcat.set_msg_emoji_like(event, message_id, emoji_id)
            event.stop_event()
            yield
        except Exception as e:
            yield
    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
