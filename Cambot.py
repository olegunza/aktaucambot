import live555
import sys
import threading
import multiprocessing
import time
from datetime import datetime
from telegram.ext import Updater, CommandHandler


def catch_video(duration):

    def one_frame(codecName, bytes, sec, usec, durUSec):
        print('frame for %s: %d bytes' % (codecName, len(bytes)))
        f_video.write(b'\0\0\0\1' + bytes)

    seconds = float(duration)
    file_video = '/home/relea/scripts/' + datetime.now().strftime("%Y-%m-%d %H:%M:%S\n") + '.mp4'

    url = 'rtsp://kgti.ru:7447/e8bd304e-56e9-32c6-aa70-d3fabecfcdb6_0'

    with open(file_video,'wb') as f_video:

       useTCP = True
       live555.startRTSP(url, one_frame, useTCP)
       t = multiprocessing.Process(target=live555.runEventLoop, args=())
       t.start()

       endTime = time.time() + seconds
       while time.time() < endTime:
           time.sleep(0.1)


       live555.stopEventLoop()
       t.terminate()

    return file_video


def get_video(bot, update, args):
    print(args[0])
    duration = float(args[0]) + 6
    if duration > 60: duration = 60
    file_video = catch_video(duration)
    with open(file_video,'rb') as ff_video:
        bot.sendVideo(update.message.chat_id, video=ff_video)



def main():
    token = "223725336:AAHyOTJC-bG-g433e_HFJhgSGViYI_Wo_Mo"
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add handlers for Telegram messages
    dp.add_handler(CommandHandler("getvideo", get_video,pass_args=True))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()