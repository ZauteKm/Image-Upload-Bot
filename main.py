import os
import uuid
import shutil
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from creds import Credentials
from telegraph import upload_file

logging.basicConfig(level=logging.INFO)


TGraph = Client(
    "Image upload bot",
    bot_token=Credentials.BOT_TOKEN,
    api_id=Credentials.API_ID,
    api_hash=Credentials.API_HASH,
)


@TGraph.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        text=f"Hello {message.from_user.first_name}!\n<b>I am Telegram to telegra.ph Image Uploader Bot</b>\n\n▷ Just give me a media under 5MB.\n▷ Then I will download it.\n▷ I will then upload it to the telegra.ph link.",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="👥 Group", url=f"https://t.me/iZaute/5"), InlineKeyboardButton(text="Channel 📢", url=f"https://t.me/iZaute/6"), ],
                                           [InlineKeyboardButton(text="🤫 Source", url=f"https://t.me/iZaute/7"), InlineKeyboardButton(text="GitHup 🤪", url=f"https://githup.com/ZauteKm"), InlineKeyboardButton(text="Bot Lists 🤖", url=f"https://t.me/iZaute/8"),],
                                           [InlineKeyboardButton(text="⚜️ Subscribe Now YouTube ⚜️", url=f"https://youtube.com/playlist?list=PLzkiTywVmsSfmhaDdWNZ5PRmmMKGTIxPJ")]])
        )


@TGraph.on_message(filters.photo)
async def getimage(client, message):
    tmp = os.path.join("downloads", str(message.chat.id))
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    img_path = os.path.join(tmp, str(uuid.uuid4()) + ".jpg")
    dwn = await message.reply_text("<b>Downloading to my server...</b>", True)
    img_path = await client.download_media(message=message, file_name=img_path)
    await dwn.edit_text("<code>Uploading as telegra.ph link...</code>")
    try:
        response = upload_file(img_path)
    except Exception as error:
        await dwn.edit_text(f"<b>Oops something went wrong\n Please ▷Contact @ZauteBot.</b>")
        return
    await dwn.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{response[0]}</code>,\n\n<b>▷ Please Subscribe</b> ❤️ [@ZauteKm](https://t.me/iZaute/6)",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="🔗 Open Link", url=f"https://telegra.ph{response[0]}"), InlineKeyboardButton(text="Share Link 👥", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}"), ],
                                           [InlineKeyboardButton(text="❤️ Share & Support Me ❤️", url="https://t.me/share/url?url=Hi%20Friend%2C%0D%0AAm%20Introducing%20a%20Powerful%20%2A%2ATelegraph%20Image%20Upload%20Bot%2A%2A%20for%20Free.%0D%0A%2A%2ABot%20Link%2A%2A%20%3A%20%40TGraphZKbot")]])
        )
    shutil.rmtree(tmp, ignore_errors=True)


TGraph.run()
