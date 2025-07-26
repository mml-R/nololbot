from telegram.ext import Updater, CommandHandler, MessageHandler, Filters , CallbackContext
import random
from telegram import Update
import json
import os

TOKEN = "8128083225:AAE5fFfZGAbllNd0c2vcx3oURBQDLJgq5P4"

#متغیر سراری برای سوالات
global_question = None
global_answer = None
global_asker_id = None

#متغیر سراسری برای کیل سویچ
kill_switch = False

#فایل ذخیره اطلاعات کاربر
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
save_file = os.path.join(BASE_DIR, "users_data.json")

#لود کردن کاربر
def load_users():
    if os.path.exists(save_file):
        with open(save_file , "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}



#ذخیره کاربر
def save_users():
    with open(save_file , "w") as f:
        json.dump(users , f)


users = load_users()


#شروع
def start(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    save_users()
    if chat_id not in users:
        users[chat_id] = {}
    if user_id not in users[chat_id]:
        users[chat_id][user_id] = {"score": 0, "name": update.message.from_user.first_name}
    update.message.reply_text("🗡🧮ربات لور آماده جنگ🗡🧮")

#/help
def help(update , context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    save_users()
    if chat_id not in users:
        users[chat_id] =  {}
    if user_id not in users[chat_id]:
        users[chat_id][user_id] = {"score": 0, "name": update.message.from_user.first_name}
    update.message.reply_text("این ربات برای تخصیص اجر نولولی به اعضای نولول طراحی شده\nتنها راه گرفتن اجر نولولی در حال حاضر حل سوالات ریاضی و یا دادن شعار انقلابی نولولی هستش، مثل:\nزنده باد/درود بر پرسیوال/اترنال و زنده باد نولول\nراه های بیشتر برای کسب اجر نولولی در دست ساخته")

#لیدربورد
def leaderboard(update , context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    save_users()
    if chat_id not in users:
        users[chat_id] =  {}
    if user_id not in users[chat_id]:
        users[chat_id][user_id] = {"score": 0, "name": update.message.from_user.first_name}
    sorted_users = sorted(users[chat_id].items() , key= lambda x:x[1]['score'] , reverse= True)
    message = "🏆 لیدربورد نولولی:\n"
    for i , (user_id , data) in enumerate(sorted_users[:10],1):
        message += f"{i}- {data['name']} : {data['score']} اجر نولولی\n"

    update.message.reply_text(message)


#مشخصات کاربر
def id(update , context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    save_users()
    if chat_id not in users:
        users[chat_id] =  {}
    if user_id not in users[chat_id]:
        users[chat_id][user_id] = {"score": 0, "name": update.message.from_user.first_name}

    update.message.reply_text(f"اجر شخصی شما:\n{users[chat_id][user_id]['name']}: {users[chat_id][user_id]['score']}")




#بازی
def play(update, context):
    global global_question,global_answer,global_asker_id

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    save_users()

    if chat_id not in users:
        users[chat_id] =  {}
    if user_id not in users[chat_id]:
        users[chat_id][user_id] = {"score": 0, "name": update.message.from_user.first_name}

    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    op = random.choice(["+", "-", "*", "/"])

    if op == "+":
        answer = num1 + num2
    elif op == "-":
        answer = num1 - num2
    elif op == "*":
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 11)
        answer = num1 * num2
    else:
        while num2 == 0 or num1 % num2 != 0:
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
        answer = num1 / num2

    global_question = f"{num1} {op} {num2} = "
    global_answer = answer
    global_asker_id = user_id

    update.message.reply_text(f"حل کن:\n{global_question}")



#killswitch
def killswitch(update: Update , context: CallbackContext):
    global kill_switch
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    save_users()
    if chat_id not in users:
        users[chat_id] =  {}
    if user_id not in users[chat_id]:
        users[chat_id][user_id] = {"score": 0, "name": update.message.from_user.first_name}


    kill_switch = not kill_switch

    if kill_switch:
        update.message.reply_text("killswitch: On")
    else:
        update.message.reply_text("killswitch: Off")


#دستور بن کامل
def ban(chat_id , user_id , context):
    try:
        context.bot.ban_chat_member(chat_id,user_id)
    except Exception as e:
        print(f"خطا در بن کردن {user_id}: {e}")





def handle_all_messages(update, context):
    global global_question,global_answer,global_asker_id,kill_switch
    user_id = update.message.from_user.id
    chat_id = update.effective_chat.id
    message_text = update.message.text.strip().lower()
    special_text = ["زنده باد پرسیوال", 
                    "درود بر پرسیوال",
                    "زنده باد نولول"
                    ,"زنده باد اترنال",
                    "درود بر اترنال" , 
                    "پیشوا جاوید",
                    "شیرزاد",
                    "فمبوی",
                    "صبح بخیر",
                    "شب بخیر",
                    "بشار",
                    "سلام",
                    "خداحافظ"
                    ]
    if not kill_switch:
        #اگر نبود اضافه بشه به یوزر
        if chat_id not in users:
            users[chat_id] =  {}
        if user_id not in users[chat_id]:
            users[chat_id][user_id] = {"score": 0, "name": update.message.from_user.first_name}
        # اگه سوال فعال داشت
        if global_question:
            try:
                guess = float(update.message.text)

                if guess == global_answer:
                    users[chat_id][user_id]["score"] += 5
                    save_users()
                    update.message.reply_text(
                        f"آفرین!\n{global_question} {global_answer}\n"
                        f"مقدار 5 اجر نولولی به شما اضافه شد\nاجر فعلی = {users[chat_id][user_id]['score']}\n"
                        f"برای سوال بعدی /play بزن!"
                    )
                else:
                    update.message.reply_text(
                        f"اشتباه!\n{global_question} {global_answer} بود\n"
                        f"برای سوال بعدی /play بزن!"
                    )
                global_question = None
                global_answer = None
            except ValueError:
                pass

        # اگر سوالی فعال نبود، بررسی پیام خاص
        for special in special_text:
            if special in message_text:
                if special == "شیرزاد" or special == "فمبوی":
                    update.message.reply_text("نون و پنیر و کیوی\nفمبوی بیاد به پیوی")
                elif special == "سلام":
                    update.message.reply_text("سلام گوگولی مگولی نولول")
                elif special == "خداحافظ":
                    update.message.reply_text("خداحافظت باشه گل باغچه نولول")
                elif special == "صبح بخیر":
                    update.message.reply_text("صبح توهم بخیر گل باغچه نولول")
                elif special == "شب بخیر":
                    update.message.reply_text("شبت بخیر گل باغچه نولول")
                elif special == "بشار":
                    update.message.reply_text("نحن رجلک یا بشار")
                else:
                    users[chat_id][user_id]['score'] +=1
                    save_users()
                    update.message.reply_text(
                        f"آفرین به این شعار انقلابیت\n{users[chat_id][user_id]['name']}، اجر نولولی شما +1 شد:\n"
                        f"امتیاز فعلی = {users[chat_id][user_id]['score']}"
                    )
    else:
        for user_id in list(users[chat_id].keys()):
            save_users()
            ban(chat_id,user_id,context)
            update.message.reply_text(f"کاربر {users[chat_id][user_id]['name']} با موفقیت بن شد")
        update.message.reply_text("گروه با موفقیت پاکسازی شد")
        kill_switch = False






def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("help" , help))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("leaderboard" , leaderboard))
    dp.add_handler(CommandHandler("id", id))
    dp.add_handler(CommandHandler("play", play))
    dp.add_handler(CommandHandler("killswitch",killswitch))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_all_messages))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
