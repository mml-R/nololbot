from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random
from telegram import Update
import json
import os
from keep_alive import keep_alive

TOKEN = os.environ.get("TOKEN")

global_question = None
global_answer = None
global_asker_id = None
kill_switch = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
save_file = os.path.join(BASE_DIR, "users_data.json")

# بارگذاری کاربران از فایل
def load_users():
    if os.path.exists(save_file):
        with open(save_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# ذخیره کاربران در فایل
def save_users(updated_users):
    current_data = load_users()

    for chat_id in updated_users:
        if chat_id not in current_data:
            current_data[chat_id] = {}

        for user_id in updated_users[chat_id]:
            current_data[chat_id][user_id] = updated_users[chat_id][user_id]

    with open(save_file, "w", encoding="utf-8") as f:
        json.dump(current_data, f, ensure_ascii=False, indent=4)

# دیتای کلی کاربران در حافظه
users = load_users()

# بررسی و اضافه کردن کاربر جدید
def ensure_user(chat_id, user_id, name):
    global users
    if chat_id not in users:
        users[chat_id] = {}
    if user_id not in users[chat_id]:
        users[chat_id][user_id] = {"score": 0, "name": name}

# دستورات ربات
def start(update, context):
    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)
    name = update.message.from_user.first_name
    ensure_user(chat_id, user_id, name)
    update.message.reply_text("🗡🧮ربات لور آماده جنگ🗡🧮")
    save_users(users)

def help(update, context):
    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)
    name = update.message.from_user.first_name
    ensure_user(chat_id, user_id, name)
    update.message.reply_text(
        "این ربات برای تخصیص اجر نولولی به اعضای نولول طراحی شده\n"
        "راه فعلی: حل سوالات ریاضی یا شعارهای انقلابی نولولی مانند:\n"
        "زنده باد پرسیوال، درود بر اترنال، زنده باد نولول و ...")

def leaderboard(update, context):
    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)
    name = update.message.from_user.first_name
    ensure_user(chat_id, user_id, name)

    top = sorted(users[chat_id].items(), key=lambda x: x[1]['score'], reverse=True)
    msg = "🏆 لیدربورد نولولی:\n"
    for i, (uid, data) in enumerate(top[:10], 1):
        msg += f"{i}- {data['name']} : {data['score']} اجر نولولی\n"
    update.message.reply_text(msg)

def id(update, context):
    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)
    name = update.message.from_user.first_name
    ensure_user(chat_id, user_id, name)

    score = users[chat_id][user_id]['score']
    update.message.reply_text(f"اجر شما:\n{name}: {score}")

def play(update, context):
    global global_question, global_answer, global_asker_id

    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)
    name = update.message.from_user.first_name
    ensure_user(chat_id, user_id, name)

    num1, num2 = random.randint(1, 100), random.randint(1, 100)
    op = random.choice(["+", "-", "*", "/"])

    if op == "+":
        answer = num1 + num2
    elif op == "-":
        answer = num1 - num2
    elif op == "*":
        num2 = random.randint(1, 10)
        answer = num1 * num2
    else:
        while num2 == 0 or num1 % num2 != 0:
            num1, num2 = random.randint(1, 100), random.randint(1, 100)
        answer = num1 / num2

    global_question = f"{num1} {op} {num2} = "
    global_answer = answer
    global_asker_id = user_id
    update.message.reply_text(f"حل کن:\n{global_question}")

def killswitch(update: Update, context: CallbackContext):
    global kill_switch
    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)
    name = update.message.from_user.first_name
    ensure_user(chat_id, user_id, name)

    kill_switch = not kill_switch
    update.message.reply_text(f"killswitch: {'On' if kill_switch else 'Off'}")
    save_users(users)

def ban(chat_id, user_id, context):
    try:
        context.bot.ban_chat_member(int(chat_id), int(user_id))
    except Exception as e:
        print(f"خطا در بن کردن {user_id}: {e}")

def handle_all_messages(update, context):
    global global_question, global_answer, kill_switch
    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)
    name = update.message.from_user.first_name
    message = update.message.text.strip().lower()

    ensure_user(chat_id, user_id, name)

    slogans = ["زنده باد پرسیوال", "درود بر پرسیوال", "زنده باد نولول",
               "زنده باد اترنال", "درود بر اترنال", "پیشوا جاوید", "شیرزاد",
               "فمبوی", "صبح بخیر", "شب بخیر", "بشار", "سلام", "خداحافظ"]

    if kill_switch:
        for uid in list(users[chat_id].keys()):
            ban(chat_id, uid, context)
        update.message.reply_text("گروه با موفقیت پاکسازی شد")
        kill_switch = False
        return

    if global_question:
        try:
            if float(update.message.text) == global_answer:
                users[chat_id][user_id]['score'] += 5
                update.message.reply_text(
                    f"آفرین!\n{global_question} {global_answer}\n"
                    f"+5 اجر نولولی\n"
                    f"اجر فعلی: {users[chat_id][user_id]['score']}")
                global_question = global_answer = None
                save_users(users)
            else:
                update.message.reply_text(f"اشتباهه! جواب: {global_answer}")
                global_question = global_answer = None
        except ValueError:
            pass
        return

    for s in slogans:
        if s in message:
            if s in ["شیرزاد", "فمبوی"]:
                update.message.reply_text("نون و پنیر و کیوی\nفمبوی بیاد به پیوی")
            elif s == "سلام":
                update.message.reply_text("سلام گوگولی مگولی نولول")
            elif s == "خداحافظ":
                update.message.reply_text("خداحافظت باشه گل باغچه نولول")
            elif s == "صبح بخیر":
                update.message.reply_text("صبح تو هم بخیر گل باغچه نولول")
            elif s == "شب بخیر":
                update.message.reply_text("شبت بخیر گل باغچه نولول")
            elif s == "بشار":
                update.message.reply_text("نحن رجلک یا بشار")
            else:
                users[chat_id][user_id]['score'] += 1
                update.message.reply_text(
                    f"آفرین به شعار انقلابیت!\n"
                    f"{users[chat_id][user_id]['name']} +1 اجر گرفت\n"
                    f"امتیاز فعلی: {users[chat_id][user_id]['score']}")
                save_users(users)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("leaderboard", leaderboard))
    dp.add_handler(CommandHandler("id", id))
    dp.add_handler(CommandHandler("play", play))
    dp.add_handler(CommandHandler("killswitch", killswitch))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_all_messages))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    keep_alive()
    main()
