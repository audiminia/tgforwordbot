from pyrogram import Client, filters

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from pyrogram.errors import UserNotParticipant

import logging, traceback

# vars

chat_id = -1001509450387

main_channel =  '@Movie_Backup_Channel'

sudo_users = [1693064520, 998194558, 1714843499, 979499093]# add your allowed user's IDs

bot = Client(':memory:', api_id={}, api_hash={}, bot_token={})

@bot.on_message(filters.media & filters.user(sudo_users))

async def handle_insersion(b, m: Message):

    k = await m.copy(chat_id)

    url = f"https://t.me/{(await b.get_me()).username}?start={k.message_id}"

    await m.reply(f'`{url}`',

        disable_web_page_preview=True,

        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Open', url=url)]])

    )

@bot.on_message(filters.command('start'))

async def handle_req(b: Client, m: Message):

    if not len(m.text.split()) >= 2:

        await m.reply('Hi {}, Join {}'.format(m.from_user.mention(style='md'), main_channel))

        return

    if not m.text.split()[1].isdigit():

        await m.reply('Hi {}, Join {}'.format(m.from_user.mention(style='md'), main_channel))

        return

    try:

        await b.get_chat_member(main_channel, m.from_user.id)# force sub shits

        k = await b.get_messages(chat_id, int(m.text.split()[1]))#       if user is present

        await k.copy(m.from_user.id, reply_to_message_id=m.message_id)#  sends the file

    except UserNotParticipant:#                                          or if the user isn't there

        await m.reply('Join {} and press the button below :)'.format(main_channel),# asks to join

            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Press me owo', callback_data=m.text.split()[1])]]))

    # except AttributeError:

    #     await m.reply('Opps! The media that you\'re looking for doesn\'t exists.')

        

    # else:#                                             if the user did something nasty like modifying the link to a different value that doesn't exists

    #     await m.reply('Opps! Something went wrong..')# reports the user

    #     logging.error(traceback.format_exc())#         logs the error to console

@bot.on_callback_query(filters.regex(pattern=r'.*')) # the press me stuffs

async def join_channel_else_suffer(b, cb: CallbackQuery):

    try:#                                                                         tries

        await b.get_chat_member(main_channel, cb.from_user.id)#                        to check if user is in channel

        k = await b.get_messages(chat_id, int(cb.data))

        await k.copy(cb.from_user.id, reply_to_message_id=cb.message.message_id)#  sends the media to user and remove 'reply_to_message_id' param is it's causing any trouble

        await cb.answer('yeeeeeeeee!')# to remove spinning circles 

        await cb.edit_message_text('Arigato!') # edits the message so that the user doesn't press the button multiple times

    except UserNotParticipant:# as mentioned above...

        await cb.answer('You still haven\'t joined the channel.', cache_time=0, show_alert=True)

    except AttributeError:

        await cb.answer('Error!', show_alert=True)

        await cb.edit_message_text('Please report this issue to {}'.format(main_channel))

    else:

        await cb.answer('Error!', show_alert=True)

    #     logging.error(traceback.format_exc())

if __name__ == "__main__" :

    bot.run()
