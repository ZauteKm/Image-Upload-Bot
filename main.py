#!/usr/bin/env python3
# Copyright (C) @ZauteKm
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import time
import math
import json
import string
import random
import traceback
import asyncio
import datetime
import aiofiles
from random import choice

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid, UserNotParticipant, UserBannedInChannel
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
from telegraph import upload_file
from database import Database


UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "")
BOT_OWNER = int(os.environ["BOT_OWNER"])
DATABASE_URL = os.environ["DATABASE_URL"]
db = Database(DATABASE_URL, "TGraphRoBot")

Bot = Client(
    "Telegraph Uploader Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START_TEXT = """**Hello {}

I am small media or file to telegra.ph link uploader bot.**

>> I can convert under 5MB photo or video to telegraph link.

**Tap help button or hits /help for more Info.**"""

HELP_TEXT = """**Hey, Follow these steps:**

▷ Just give me a media under 5MB.
▷ Then I will download it.
▷ I will then upload it to the telegra.ph link.
"""

ABOUT_TEXT = """--**About Me**-- 😎

🤖 **Name :** [TGraphRoBot](https://telegram.me/TGraphRoBot)

👨‍💻 **Developer :** [Zaute](https://t.me/zautekm)

📢 **Channel :** [Jos Projects](https://telegram.me/josprojects)

👥 **Feedback :** [Tap here](https://telegram.me/jospsupportbot)

🌐 **Source :** [👉 Press me](https://github.com/ZauteKm/Image-Upload-Bot)

📝 **Language :** [Python3](https://python.org)

🧰 **Framework :** [Pyrogram](https://pyrogram.org)"""

FORCE_SUBSCRIBE_TEXT = "<b>Sorry Dear You Must Join My Updates Channel for using me 😌😉....</b>"

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('❗ Help', callback_data='help'),
        InlineKeyboardButton('About 🤖', callback_data='about'),
        ],
        [
        InlineKeyboardButton('Close ❌', callback_data='close')
        ]]
    )

HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏘 Home', callback_data='home'),
        InlineKeyboardButton('About 🤖', callback_data='about'),
        ],
        [
        InlineKeyboardButton('Close ❌', callback_data='close')
        ]]
    )

ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏘 Home', callback_data='home'),
        InlineKeyboardButton('Help 🖲️', callback_data='help'),
        ],
        [
        InlineKeyboardButton('Close ❌', callback_data='close')
        ]]
    )


async def send_msg(user_id, message):
	try:
		await message.copy(chat_id=user_id)
		return 200, None
	except FloodWait as e:
		await asyncio.sleep(e.x)
		return send_msg(user_id, message)
	except InputUserDeactivated:
		return 400, f"{user_id} : deactivated\n"
	except UserIsBlocked:
		return 400, f"{user_id} : user is blocked\n"
	except PeerIdInvalid:
		return 400, f"{user_id} : user id invalid\n"
	except Exception as e:
		return 500, f"{user_id} : {traceback.format_exc()}\n"


@Bot.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT.format((await bot.get_me()).username),
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
    FSub = await ForceSub(bot, update)
    if FSub == 400:
        return
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
	reply_markup=START_BUTTONS
    )


@Bot.on_message(filters.private & filters.command(["help"]))
async def help(bot, update):
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
    FSub = await ForceSub(bot, update)
    if FSub == 400:
        return
    await update.reply_text(
        text=HELP_TEXT,
      	disable_web_page_preview=True,
	reply_markup=HELP_BUTTONS
    )


@Bot.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
    FSub = await ForceSub(bot, update)
    if FSub == 400:
        return
    await update.reply_text(
        text=ABOUT_TEXT.format((await bot.get_me()).username),
        disable_web_page_preview=True,
	reply_markup=ABOUT_BUTTONS
    )


@Bot.on_message(filters.media & filters.private)
async def telegraph_upload(bot, update):
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
    FSub = await ForceSub(bot, update)
    if FSub == 400:
        return
        except Exception as error:
            print(error)
            await update.reply_text(text="Something wrong. Contact <a href='https://telegram.me/zautebot'>Developer</a>.", disable_web_page_preview=True)
            return
    medianame = "./DOWNLOADS/" + "ZauteKm/TGraphRoBot"
    text = await update.reply_text(
        text="<code>Downloading to My Server ...</code>",
        disable_web_page_preview=True, reply_to_message_id=update.message_id,
    )
    await bot.download_media(
        message=update,
        file_name=medianame
    )
    await text.edit_text(
        text="<code>Downloading Completed. Now I am Uploading to telegra.ph Link ...</code>",
        disable_web_page_preview=True,
    )
    try:
        response = upload_file(medianame)
    except Exception as error:
        print(error)
        await text.edit_text(
            text=f"Error :- {error}",
            disable_web_page_preview=True,
        )
        return
    try:
        os.remove(medianame)
    except Exception as error:
        print(error)
        return
    await text.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{response[0]}</code>\n\n<b>Thank You For Using Me:- \nPlease Subscribe ❤️ [@ZauteKm](https://t.me/iZaute/6)</b>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="🔗 Open Link", url=f"https://telegra.ph{response[0]}"),
                    InlineKeyboardButton(text="Share Link 👥", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}")
                ],
                [InlineKeyboardButton(text="❤️ Share & Support Me ❤️", url="https://t.me/share/url?url=Hi%20Friend%2C%0D%0AAm%20Introducing%20a%20Powerful%20%2A%2ATelegraph%20Image%20Upload%20Bot%2A%2A%20for%20Free.%0D%0A%2A%2ABot%20Link%2A%2A%20%3A%20%40TGraphRobot")]
            ]
        )
    )


@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(BOT_OWNER) & filters.reply)
async def broadcast(bot, update):
	broadcast_ids = {}
	all_users = await db.get_all_users()
	broadcast_msg = update.reply_to_message
	while True:
	    broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
	    if not broadcast_ids.get(broadcast_id):
	        break
	out = await update.reply_text(text=f"Broadcast Started! You will be notified with log file when all the users are notified.")
	start_time = time.time()
	total_users = await db.total_users_count()
	done = 0
	failed = 0
	success = 0
	broadcast_ids[broadcast_id] = dict(total = total_users, current = done, failed = failed, success = success)
	async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
	    async for user in all_users:
	        sts, msg = await send_msg(user_id = int(user['id']), message = broadcast_msg)
	        if msg is not None:
	            await broadcast_log_file.write(msg)
	        if sts == 200:
	            success += 1
	        else:
	            failed += 1
	        if sts == 400:
	            await db.delete_user(user['id'])
	        done += 1
	        if broadcast_ids.get(broadcast_id) is None:
	            break
	        else:
	            broadcast_ids[broadcast_id].update(dict(current = done, failed = failed, success = success))
	if broadcast_ids.get(broadcast_id):
	    broadcast_ids.pop(broadcast_id)
	completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
	await asyncio.sleep(3)
	await out.delete()
	if failed == 0:
	    await update.reply_text(text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.", quote=True)
	else:
	    await update.reply_document(document='broadcast.txt', caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.")
	os.remove('broadcast.txt')


@Bot.on_message(filters.private & filters.command("status"), group=5)
async def status(bot, update):
    total_users = await db.total_users_count()
    text = "**Bot Status**\n"
    text += f"\n**Total Users:** `{total_users}`"
    await update.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )


async def ForceSub(bot: Client, event: Message):
    """
    Custom Pyrogram Based Telegram Bot's Force Subscribe Function by @ZauteKm.
    If User is not Joined Force Sub Channel Bot to Send a Message & ask him to Join First.
    
    :param bot: Pass Client.
    :param event: Pass Message.
    :return: It will return 200 if Successfully Got User in Force Sub Channel and 400 if Found that User Not Participant in Force Sub Channel or User is Kicked from Force Sub Channel it will return 400. Also it returns 200 if Unable to Find Channel.
    """
    
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=(int(UPDATES_CHANNEL) if UPDATES_CHANNEL.startswith("-100") else UPDATES_CHANNEL))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event)
        return fix_
    except Exception as err:
        print(f"Unable to do Force Subscribe to {Config.UPDATES_CHANNEL}\n\nError: {err}\n\nContact Support Group: https://t.me/JOSPSupport")
        return 200
    try:
        user = await bot.get_chat_member(chat_id=(int(UPDATES_CHANNEL) if UPDATES_CHANNEL.startswith("-100") else UPDATES_CHANNEL), user_id=event.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=event.from_user.id,
                text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/Jospsupport).",
                parse_mode="markdown",
                disable_web_page_preview=True,
                reply_to_message_id=event.message_id
            )
            return 400
        else:
            return 200
    except UserNotParticipant:
        await bot.send_message(
            chat_id=event.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                    ]
                ]
            ),
            parse_mode="markdown",
            reply_to_message_id=event.message_id
        )
        return 400
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event)
        return fix_
    except Exception as err:
        print(f"Something Went Wrong! Unable to do Force Subscribe.\nError: {err}\n\nContact Support Group: https://t.me/JOSPSupport")
        return 200


Bot.run()
