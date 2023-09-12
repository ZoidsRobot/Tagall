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
@client.on(events.NewMessage(pattern="^/mstart$"))
async def start(event):
  await event.reply("Hey [🤗](https://telegra.ph/file/97da0b711a6ba2f4f4482.jpg)\nWelcome🔥🥂\n━━━━━━━━━━━━━━━━━━━━\n┏━━━━━━━━━━━━━━━━━┓\n┣★I m Highly advanced Tag Member Bot.\n┣★I can tag  members in group as well as in Channel.\n┣★Need Help hit ☛ [★𝐎𝐀𝐍★](Https://t.me/OAN_Support)\n┗━━━━━━━━━━━━━━━━━┛\n━━━━━━━━━━━━━━━━━━━━",
                   buttons=(
                      [Button.url('🔥ᴀᴅᴅ ᴛᴀɢ ᴍᴇᴍʙᴇʀ ᴛᴏ ɢʀᴏᴜᴩ🔥', 'http://t.me/Tag_member_bot?startgroup=true')],
                      [Button.url('⚜ᴏᴡɴᴇʀ⚜', 'Https://t.me/ItsAttitudeking')],
                      [Button.url('🛎ꜱᴜᴩᴩᴏʀᴛ', 'https://t.me/OAN_Support'),
                      Button.url('ᴜᴩᴅᴀᴛᴇ🔊', 'https://t.me/Attitude_Network')],
                     [Button.url('⚒ʀᴇᴩᴏ⚒', 'https://github.com/ItsAttitudeking/Tag_member')]
                     ),
                    link_preview=False
                   )

#help
@client.on(events.NewMessage(pattern="^/mhelp$"))
async def help(event):
  helptext = "**[🔥](https://te.legra.ph/file/8d6307fcac08120cb9380.jpg), ᴛᴀɢ ᴍᴇᴍʙᴇʀ ʙᴏᴛ'ꜱ ʜᴇʟᴩ ᴍᴇɴᴜ👑**\n\nCommand: /tag \n You can use this command with text you want to tell others. \n`Example: /tag Good morning!` \nYou can use this command as an answer. any message Bot will tag users to replied message"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('⚜ᴏᴡɴᴇʀ⚜', 'https://t.me/ItsAttitudeking'),
                      Button.url('🛎ꜱᴜᴩᴩᴏʀᴛ', 'https://t.me/OAN_Support')]
                      [Button.url('⚒ʀᴇᴩᴏ⚒', 'https://github.com/ItsAttitudeking/Tag_member')]
                     ),
                    link_preview=False
                   )

#Wah bhaiya full ignorebazi

#bsdk credit de dena verna maa chod dege

#tag
@client.on(events.NewMessage(pattern="^/tagall|@all|/all ?(.*)"))
async def mentionall(event):
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond("__Perintah ini hanya digunakan dalam grup dan channel.__*")

    is_admin = False
    try:
        partici_ = await client(GetParticipantRequest(
            event.chat_id,
            event.sender_id
        ))
    except UserNotParticipantError:
        is_admin = False
    else:
        if (
                isinstance(
                    partici_.participant,
                    (
                            ChannelParticipantAdmin,
                            ChannelParticipantCreator
                    )
                )
        ):
            is_admin = True
    if not is_admin:
        return await event.reply("__Hanya admin yang dapat menjalankan perintah ini...__")

    if event.pattern_match.group(1) and event.is_reply:
        return await event.reply("__Berikan beberapa teks atau balas pesan..__")
    elif event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg = event.pattern_match.group(1)
    elif event.is_reply:
        mode = "text_on_reply"
        msg = await event.get_reply_message()
        if msg == None:
            return await event.respond(
                "Saya tidak bisa menyebut anggota untuk pesan lama! (pesan yang dikirim sebelum saya ditambahkan ke grup)")
    else:
        return await event.reply("__Berikan beberapa teks atau balas pesan..__")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ''
    async for usr in client.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"🫦 [{usr.first_name}](tg://user?id={usr.id})\n"
        if usrnum == 5:
            if mode == "text_on_cmd":
                txt = f"{msg}\n\n{usrtxt}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(usrtxt)
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ''
    try:
        spam_chats.remove(chat_id)
    except:
        pass


print("~~~~Started~~~~~")
print("🔥🥂Need Help Dm @ItsAttitudeking")
client.run_until_disconnected()

