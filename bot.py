#Copyright @ItsAttitudeking
#sys
import os, logging, asyncio

#telethon bhaiya
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("API_ID", "9774346"))
api_hash = os.environ.get("API_HASH", "a92aed7d74654a563af4b07efbcd88e9")
bot_token = os.environ.get("TOKEN", "6132329564:AAEJBoyXwP9eipKIQAxT7yQHf39HzyhV_5A")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

#worker
moment_worker = []

#cancel
@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global moment_worker
  moment_worker.remove(event.chat_id)

#start
#tag
@client.on(events.NewMessage(pattern="^/tag ?(.*)"))
async def mentionall(event):
  global moment_worker
  if event.is_private:
    return await event.reply("Use This In Channel or Group!")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.reply("Only Admin can use it [😌](https://telegra.ph/file/97da0b711a6ba2f4f4482.jpg).")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.reply("I can't Mention Members for Old Post!")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.reply("Give me can an Argument. Ex: `/tag Hey, Where are you`")
  else:
    return await event.reply("Reply to Message or Give Some Text To Mention!")
    
  if mode == "text_on_cmd":
    moment_worker.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"🫦 [{usr.first_name}](tg://user?id={usr.id})\n"
      if event.chat_id not in moment_worker:
        await event.respond("Ok tagger stopped [🔇](https://telegra.ph/file/97da0b711a6ba2f4f4482.jpg)")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{msg}\n\n{usrtxt}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    moment_worker.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"🫦 [{usr.first_name}](tg://user?id={usr.id})\n"
      if event.chat_id not in moment_worker:
        await event.reply("Ok tagger stopped [🔇](https://telegra.ph/file/97da0b711a6ba2f4f4482.jpg)")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

print("~~~~Started~~~~~")
print("🔥🥂Need Help Dm @ItsAttitudeking")
client.run_until_disconnected()
