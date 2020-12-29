import os
import re
import requests
import urllib
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

from telegram import InputMediaPhoto, TelegramError
from telegram import Update
from telegram.ext import CallbackContext, run_async

from SaitamaRobot import dispatcher

from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from SaitamaRobot.modules.helper_funcs.alternate import typing_action

opener = urllib.request.build_opener()
useragent = 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'
opener.addheaders = [('User-agent', useragent)]

@run_async
def reverse(update: Update, context:CallbackContext):
    if os.path.isfile("okgoogle.png"):
            os.remove("okgoogle.png")
    msg = update.effective_message
        chat_id = update.effective_chat.id
            bot, args = context.bot, context.args
                rtmid = msg.message_id
                    imagename = "okgoogle.png"
    reply = msg.reply_to_message
        if reply:
                if reply.sticker:
                            file_id = reply.sticker.file_id
                                    elif reply.photo:
                                                file_id = reply.photo[-1].file_id
                                                        elif reply.document:
                                                                    file_id = reply.document.file_id
                                                                            else:
                                                                                        msg.reply_text("Reply to an image or sticker to lookup.")
                                                                                                    return
                                                                                                            image_file = bot.get_file(file_id)
                                                                                                                    image_file.download(imagename)
                                                                                                                            if args:
                                                                                                                                        txt = args[0]
                                                                                                                                                    try:
                                                                                                                                                                    lim = int(txt)
                                                                                                                                                                                except:
                                                                                                                                                                                                lim = 2
                                                                                                                                                                                                        else:
                                                                                                                                                                                                                    lim = 2
                                                                                                                                                                                                                        elif args and not reply:
                                                                                                                                                                                                                                splatargs = msg.text.split(" ")
                                                                                                                                                                                                                                        if len(splatargs) == 3:                
                                                                                                                                                                                                                                                    img_link = splatargs[1]
                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                lim = int(splatargs[2])
                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                            lim = 2
                                                                                                                                                                                                                                                                                                                    elif len(splatargs) == 2:
                                                                                                                                                                                                                                                                                                                                img_link = splatargs[1]
                                                                                                                                                                                                                                                                                                                                            lim = 2
                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                msg.reply_text("/reverse <link> <amount of images to return.>")
                                                                                                                                                                                                                                                                                                                                                                            return
                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                urllib.request.urlretrieve(img_link, imagename)
                                                                                                                                                                                                                                                                                                                                                                                                        except HTTPError as HE:
                                                                                                                                                                                                                                                                                                                                                                                                                    if HE.reason == 'Not Found':
                                                                                                                                                                                                                                                                                                                                                                                                                                    msg.reply_text("Image not found.")
                                                                                                                                                                                                                                                                                                                                                                                                                                                    return
                                                                                                                                                                                                                                                                                                                                                                                                                                                                elif HE.reason == 'Forbidden':
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                msg.reply_text("Couldn't access the provided link, The website might have blocked accessing to the website by bot or the website does not existed.")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                return
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        except URLError as UE:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    msg.reply_text(f"{UE.reason}")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                return
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        except ValueError as VE:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    msg.reply_text(f"{VE}\nPlease try again using http or https protocol.")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                return
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            msg.reply_markdown("Please reply to a sticker, or an image to search it!\nDo you know that you can search an image with a link too? /reverse [picturelink] <amount>.")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    return
    try:
            searchUrl = 'https://www.google.com/searchbyimage/upload'
                    multipart = {'encoded_image': (imagename, open(imagename, 'rb')), 'image_content': ''}
                            response = requests.post(searchUrl, files=multipart, allow_redirects=False)
                                    fetchUrl = response.headers['Location']
        if response != 400:
                    xx = bot.send_message(chat_id, "Image was successfully uploaded to Google."
                                                      "\nParsing it, please wait.", reply_to_message_id=rtmid)
                                                              else:
                                                                          xx = bot.send_message(chat_id, "Google told me to go away.", reply_to_message_id=rtmid)
                                                                                      return
        os.remove(imagename)
                match = ParseSauce(fetchUrl + "&hl=en")
                        guess = match['best_guess']
                                if match['override'] and not match['override'] == '':
                                            imgspage = match['override']
                                                    else:
                                                                imgspage = match['similar_images']
        if guess and imgspage:
                    xx.edit_text(f"[{guess}]({fetchUrl})\nProcessing...", parse_mode='Markdown', disable_web_page_preview=True)
                            else:
                                        xx.edit_text("Couldn't find anything.")
                                                    return
        images = scam(imgspage, lim)
                if len(images) == 0:
                            xx.edit_text(f"[{guess}]({fetchUrl})\n[Visually similar images]({use= o