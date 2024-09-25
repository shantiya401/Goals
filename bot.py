import telebot
import os
import json
import telebot
from datetime import datetime
import jdatetime
import re
# ایجاد ربات با توکن شما
bot_token = "ENTER YOUR TELEGRAM BOT"
bot = telebot.TeleBot(bot_token)

# بررسی و ایجاد پوشه و فایل جیسون در صورت نیاز
if not os.path.exists('json'):
    os.makedirs('json')

file_path = 'json/hadaf.json'
if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        json.dump({"short_term_goals": [], "long_term_goals": [], "passed_goals": []}, file)

# دیکشنری موقت برای ذخیره اطلاعات اهداف
temp_goal = {}


@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message)

# صفحه اصلی
def main_menu(message):
    # ساخت دکمه‌ها
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("ثبت اهداف", callback_data="register_goal"))
    markup.add(telebot.types.InlineKeyboardButton("بازدید اهداف", callback_data="view_goals"))

    # ارسال عکس با دکمه‌ها
    with open("images/start.png", 'rb') as photo:
        bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,# خوش آمدگویی
            reply_markup=markup  # دکمه‌ها
        )

# ساختار منوی اصلی (برای دکمه بازگشت)
def main_menu_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("ثبت اهداف", callback_data="register_goal"))
    markup.add(telebot.types.InlineKeyboardButton("بازدید اهداف", callback_data="view_goals"))
    return markup
    
# هندلر برای بازگشت به صفحه اصلی
@bot.callback_query_handler(func=lambda call: call.data == "back")
def go_back(call):
    bot.edit_message_text("بازگشت به صفحه اصلی", call.message.chat.id, call.message.message_id, reply_markup=main_menu_markup())
    
    
# کال‌بک هندلر برای دکمه ثبت اهداف
# کال‌بک هندلر برای دکمه ثبت اهداف
@bot.callback_query_handler(func=lambda call: call.data == "register_goal")
def register_goal(call):
    # ارسال عکس بدون کپشن
    with open("images/goals.png", 'rb') as photo:
        msg = bot.send_photo(call.message.chat.id, photo)

    # ساخت دکمه‌ها
    markup = telebot.types.InlineKeyboardMarkup()
    
    # اضافه کردن دکمه‌های اهداف کوتاه مدت و بلند مدت در یک سطر
    row = [
        telebot.types.InlineKeyboardButton("اهداف کوتاه مدت", callback_data="short_term"),
        telebot.types.InlineKeyboardButton("اهداف بلند مدت", callback_data="long_term"),
    ]
    markup.add(*row)  # اضافه کردن دکمه‌ها در یک سطر

    # اضافه کردن دکمه بازگشت
    markup.add(telebot.types.InlineKeyboardButton("بازگشت", callback_data="back"))

    # ویرایش پیام عکس برای اضافه کردن دکمه‌ها
    bot.edit_message_reply_markup(call.message.chat.id, msg.message_id, reply_markup=markup)
# هندلر برای اهداف کوتاه مدت
@bot.callback_query_handler(func=lambda call: call.data == "short_term")
def short_term_goal(call):
    temp_goal["type"] = "کوتاه مدت"
    
    # ارسال عکس بدون کپشن
    with open("images/sabt_sh.png", 'rb') as photo:
        msg = bot.send_photo(call.message.chat.id, photo)
    
    # ارسال پیام برای درخواست موضوع
    bot.send_message(call.message.chat.id, "لطفاً یک موضوع کوتاه برای هدف کوتاه مدت خود را بنویسید:")
    
    # ثبت دستورات بعدی
    bot.register_next_step_handler(call.message, get_short_term_subject)

# هندلر برای اهداف بلند مدت
@bot.callback_query_handler(func=lambda call: call.data == "long_term")
def long_term_goal(call):
    temp_goal["type"] = "بلند مدت"
    
    # ارسال عکس بدون کپشن
    with open("images/sabt_l.png", 'rb') as photo:
        msg = bot.send_photo(call.message.chat.id, photo)

    # ارسال پیام برای درخواست موضوع
    bot.send_message(call.message.chat.id, "لطفاً یک موضوع کوتاه برای هدف بلند مدت خود را بنویسید:")
    
    # ثبت دستورات بعدی
    bot.register_next_step_handler(call.message, get_long_term_subject)

def get_short_term_subject(message):
    temp_goal["subject"] = message.text
    bot.send_message(message.chat.id, "لطفاً توضیحی کوتاه در مورد هدف خود ارسال کنید:")
    bot.register_next_step_handler(message, get_short_term_description)

def get_long_term_subject(message):
    temp_goal["subject"] = message.text
    bot.send_message(message.chat.id, "لطفاً توضیحی کوتاه در مورد هدف خود ارسال کنید:")
    bot.register_next_step_handler(message, get_long_term_description)

def get_short_term_description(message):
    temp_goal["description"] = message.text
    bot.send_message(message.chat.id, "لطفاً زمانی را که برای رسیدن به این هدف در نظر دارید را ارسال کنید (فرمت: 14030606 یا 1403/06/06):")
    bot.register_next_step_handler(message, get_short_term_deadline)

def get_long_term_description(message):
    temp_goal["description"] = message.text
    bot.send_message(message.chat.id, "لطفاً زمانی را که برای رسیدن به این هدف در نظر دارید را ارسال کنید (فرمت: 14030606 یا 1403/06/06):")
    bot.register_next_step_handler(message, get_long_term_deadline)

def get_short_term_deadline(message):
    temp_goal["deadline"] = message.text
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("معمولی", callback_data="priority_normal"))
    markup.add(telebot.types.InlineKeyboardButton("مهم", callback_data="priority_important"))
    markup.add(telebot.types.InlineKeyboardButton("خیلی مهم", callback_data="priority_very_important"))
    bot.send_message(message.chat.id, "لطفاً اولویت هدف را تایین کنید:", reply_markup=markup)

def get_long_term_deadline(message):
    temp_goal["deadline"] = message.text
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("معمولی", callback_data="priority_normal"))
    markup.add(telebot.types.InlineKeyboardButton("مهم", callback_data="priority_important"))
    markup.add(telebot.types.InlineKeyboardButton("خیلی مهم", callback_data="priority_very_important"))
    bot.send_message(message.chat.id, "لطفاً اولویت هدف را تایین کنید:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("priority_"))
def get_priority(call):
    priorities = {
        "priority_normal": "معمولی",
        "priority_important": "مهم",
        "priority_very_important": "خیلی مهم"
    }
    temp_goal["priority"] = priorities[call.data]
    bot.send_message(call.message.chat.id, "بودجه ای را که برای این هدف در نظر گرفته اید حدوداً و به تومان بنویسید:")
    bot.register_next_step_handler(call.message, get_budget)

def get_budget(message):
    temp_goal["budget"] = message.text
    save_goal(temp_goal)
    bot.send_message(message.chat.id, "هدف با موفقیت ثبت شد!", reply_markup=main_menu_markup())

def save_goal(goal_data):
    with open(file_path, 'r+') as file:
        data = json.load(file)
        if goal_data["type"] == "کوتاه مدت":
            data["short_term_goals"].append(goal_data)
        elif goal_data["type"] == "بلند مدت":
            data["long_term_goals"].append(goal_data)
        file.seek(0)
        json.dump(data, file, ensure_ascii=False, indent=4)

# کال‌بک هندلر برای دکمه بازدید اهداف
@bot.callback_query_handler(func=lambda call: call.data == "view_goals")
def view_goals(call):
    # ساخت دکمه‌ها
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)  # تنظیم چینش دکمه‌ها در ۲ ستون
    markup.add(
        telebot.types.InlineKeyboardButton("اهداف کوتاه مدت", callback_data="view_short_term"),
        telebot.types.InlineKeyboardButton("اهداف بلند مدت", callback_data="view_long_term")
    )
    markup.add(
        telebot.types.InlineKeyboardButton("اهداف پاس شده", callback_data="view_passed_goals"),
        telebot.types.InlineKeyboardButton("بازگشت", callback_data="back")
    )

    # ارسال عکس و دکمه‌ها در یک پست
    with open("images/view.png", 'rb') as photo:
        bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            reply_markup=markup  # اضافه کردن دکمه‌ها به همان پیام
        )
# هندلر برای مشاهده اهداف کوتاه مدت
@bot.callback_query_handler(func=lambda call: call.data == "view_short_term")
def view_short_term(call):
    with open(file_path, 'r') as file:
        data = json.load(file)
        if not data["short_term_goals"]:
            bot.send_message(call.message.chat.id, "شما هنوز هدف کوتاه مدتی ثبت نکرده‌اید.", reply_markup=main_menu_markup())
        else:
            markup = telebot.types.InlineKeyboardMarkup()
            for goal in data["short_term_goals"]:
                markup.add(telebot.types.InlineKeyboardButton(goal["subject"], callback_data=f"view_goal_{goal['subject']}"))
            markup.add(telebot.types.InlineKeyboardButton("بازگشت", callback_data="back"))
            bot.send_message(call.message.chat.id, "اهداف کوتاه مدت شما:", reply_markup=markup)

# هندلر برای مشاهده اهداف بلند مدت
@bot.callback_query_handler(func=lambda call: call.data == "view_long_term")
def view_long_term(call):
    with open(file_path, 'r') as file:
        data = json.load(file)
        if not data["long_term_goals"]:
            bot.send_message(call.message.chat.id, "شما هنوز هدف بلند مدتی ثبت نکرده‌اید.", reply_markup=main_menu_markup())
        else:
            markup = telebot.types.InlineKeyboardMarkup()
            for goal in data["long_term_goals"]:
                markup.add(telebot.types.InlineKeyboardButton(goal["subject"], callback_data=f"view_goal_{goal['subject']}"))
            
            # تورفتگی درست شد
            markup.add(telebot.types.InlineKeyboardButton("بازگشت", callback_data="back"))
            bot.send_message(call.message.chat.id, "اهداف بلند مدت شما:", reply_markup=markup)
# هندلر برای مشاهده اهداف پاس شده
@bot.callback_query_handler(func=lambda call: call.data == "view_passed_goals")
def view_passed_goals(call):
    with open(file_path, 'r') as file:
        data = json.load(file)
        if not data["passed_goals"]:
            bot.send_message(call.message.chat.id, "هنوز هیچ هدفی پاس نشده است.", reply_markup=main_menu_markup())
        else:
            markup = telebot.types.InlineKeyboardMarkup()
            for goal in data["passed_goals"]:
                markup.add(telebot.types.InlineKeyboardButton(goal["subject"], callback_data=f"view_goal_{goal['subject']}"))
            markup.add(telebot.types.InlineKeyboardButton("بازگشت", callback_data="back"))
            bot.send_message(call.message.chat.id, "اهداف پاس شده شما:", reply_markup=markup)

# هندلر برای نمایش اطلاعات هدف (اعم از کوتاه‌مدت یا بلندمدت یا پاس‌شده)
@bot.callback_query_handler(func=lambda call: call.data.startswith("view_goal_"))
def view_goal(call):
    goal_subject = call.data[len("view_goal_"):]
    with open(file_path, 'r') as file:
        data = json.load(file)
        goal_data = None
        for goal in data["short_term_goals"] + data["long_term_goals"] + data["passed_goals"]:
            if goal["subject"] == goal_subject:
                goal_data = goal
                break

        if goal_data:
            # استخراج تاریخ از دیتای JSON
            deadline_jalali = goal_data['deadline']
            
            # بررسی فرمت تاریخ و افزودن '/' در صورت لزوم
            if len(deadline_jalali) == 8 and '/' not in deadline_jalali:
                # فرمت YYYYMMDD را به YYYY/MM/DD تبدیل می‌کنیم
                deadline_jalali = f"{deadline_jalali[:4]}/{deadline_jalali[4:6]}/{deadline_jalali[6:]}"
            
            # قالب‌بندی بودجه
            budget = f"{int(goal_data['budget']):,} تومان"
            
            # محاسبه تعداد روز باقی‌مانده با استفاده از تبدیل به میلادی برای محاسبه
            if len(goal_data['deadline']) == 8:  # اگر تاریخ در فرمت YYYYMMDD باشد
                year = int(goal_data['deadline'][:4])
                month = int(goal_data['deadline'][4:6])
                day = int(goal_data['deadline'][6:8])
                deadline_gregorian = jdatetime.date(year, month, day).togregorian()
            else:
                # اگر تاریخ با '/' جدا شده باشد
                deadline_gregorian = jdatetime.date.fromisoformat(deadline_jalali.replace('/', '-')).togregorian()

            remaining_days = (deadline_gregorian - datetime.now().date()).days  # محاسبه روز باقی‌مانده

            # نمایش اطلاعات هدف
            goal_info = (
                  f"🔸🔸🔸🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔸🔸🔸\n\n"
                f"🎯 موضوع: {goal_data['subject']}\n"
                f"📋 توضیح: {goal_data['description']}\n"
                f"📆 تاریخ: {deadline_jalali}\n"  # نمایش تاریخ جلالی
                f"💣 اولویت: {goal_data['priority']}\n"
                f"💸 بودجه: {budget}"
            )

            markup = telebot.types.InlineKeyboardMarkup()
            
            # افزودن دکمه‌های مربوطه
            if goal_data in data["short_term_goals"] or goal_data in data["long_term_goals"]:
                markup.add(telebot.types.InlineKeyboardButton(f"⏳ روز باقی‌مانده: {remaining_days}  روز", callback_data="none"))
                markup.add(telebot.types.InlineKeyboardButton("✅ پاس شد ", callback_data=f"mark_passed_{goal_data['subject']}"))

            # دکمه چالش‌ها
            markup.add(telebot.types.InlineKeyboardButton("🔐  چالش‌ها", callback_data=f"challenges_{goal_data['subject']}"))
            markup.add(telebot.types.InlineKeyboardButton("🔙 بازگشت", callback_data="back"))
            
            bot.send_message(call.message.chat.id, goal_info, reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, "این هدف یافت نشد.", reply_markup=main_menu_markup())
            
# هندلر برای محاسبه مدت زمان باقی‌مانده تا سررسید
@bot.callback_query_handler(func=lambda call: call.data.startswith("remaining_days_"))
def remaining_days(call):
    goal_subject = call.data[len("remaining_days_"):]
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        goal_data = None
        for goal in data["short_term_goals"] + data["long_term_goals"]:
            if goal["subject"] == goal_subject:
                goal_data = goal
                break
        
        if goal_data:
            deadline = goal_data['deadline']
            try:
                if len(deadline) == 8 and deadline.isdigit():
                    # اگر تاریخ در فرمت شمسی است
                    year = int(deadline[:4])
                    month = int(deadline[4:6])
                    day = int(deadline[6:])
                    deadline_date = jdatetime.date(year, month, day).togregorian()
                else:
                    # اگر تاریخ در فرمت میلادی است
                    deadline_date = datetime.strptime(deadline, "%Y-%m-%d")

                remaining = (deadline_date - datetime.now()).days
                bot.send_message(call.message.chat.id, f"{remaining} روز تا رسیدن به هدف باقی مانده است.")
            except ValueError:
                bot.send_me

# هندلر چالش‌ها
@bot.callback_query_handler(func=lambda call: call.data.startswith("challenges_"))
def challenges_handler(call):
    goal_subject = call.data[len("challenges_"):]

    # خواندن فایل JSON
    with open(file_path, 'r') as file:
        data = json.load(file)

    goal_data = None
    for goal in data["short_term_goals"] + data["long_term_goals"]:
        if goal["subject"] == goal_subject:
            goal_data = goal
            break

    if goal_data:
        challenges = goal_data.get("challenges", [])

        # ایجاد دکمه‌ها بر اساس وجود یا عدم وجود چالش‌ها
        markup = telebot.types.InlineKeyboardMarkup()
        
        if challenges:
            for challenge in challenges:
                # تعیین سختی چالش با استفاده از دایره‌های رنگی
                difficulty_mapping = {
                    "easy": "🟢",
                    "medium": "🟡",
                    "hard": "🔴"
                }
                difficulty_icon = difficulty_mapping.get(challenge.get('difficulty', 'نامشخص'), 'نامشخص')

                # تعیین وضعیت چالش (پاس شده یا پاس نشده)
                current_status = challenge.get("status", "پاس نشده ❌")
                status_icon = "✅" if current_status == "پاس شده ✅" else "❌"

                # متن نهایی برای هر چالش به صورت: {دایره سختی} {نام چالش} {وضعیت}
                challenge_text = f"{difficulty_icon}  {challenge['title']}  {status_icon}"
                
                # اضافه کردن دکمه برای چالش
                markup.add(telebot.types.InlineKeyboardButton(challenge_text, callback_data=f"view_challenge_{challenge['title']}"))

        # دکمه برای ثبت چالش جدید
        markup.add(telebot.types.InlineKeyboardButton("ثبت چالش", callback_data=f"set_challenge_{goal_subject}"))
        # دکمه بازگشت
        markup.add(telebot.types.InlineKeyboardButton("بازگشت", callback_data="back"))

        bot.send_message(call.message.chat.id, "چالش‌های مرتبط با هدف را مشاهده کنید:", reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, "این هدف یافت نشد.", reply_markup=main_menu_markup())
# هندلر ثبت چالش

# هندلر ثبت چالش
@bot.callback_query_handler(func=lambda call: call.data.startswith("set_challenge_"))
def set_challenge_handler(call):
    goal_subject = call.data[len("set_challenge_"):]
    
    bot.send_message(call.message.chat.id, f"در حال ثبت چالش برای هدف: {goal_subject}")
    bot.send_message(call.message.chat.id, "لطفاً عنوان چالش را ارسال کنید:")
    bot.register_next_step_handler(call.message, set_challenge_details, goal_subject)

def set_challenge_details(message, goal_subject):
    challenge_title = message.text
    bot.send_message(message.chat.id, "لطفاً توضیحات چالش را ارسال کنید:")
    bot.register_next_step_handler(message, set_challenge_deadline, goal_subject, challenge_title)

# بررسی و ثبت تاریخ در فرمت‌های صحیح
def set_challenge_deadline(message, goal_subject, challenge_title):
    challenge_description = message.text
    bot.send_message(message.chat.id, "لطفاً مهلت چالش را به یکی از فرمت‌های 14030101 یا 1403/01/01 ارسال کنید:")
    bot.register_next_step_handler(message, validate_challenge_deadline, goal_subject, challenge_title, challenge_description)

def validate_challenge_deadline(message, goal_subject, challenge_title, challenge_description):
    deadline = message.text
    # بررسی فرمت تاریخ و تبدیل به فرمت 1403/01/01
    if re.match(r'^\d{4}/\d{2}/\d{2}$', deadline):
        formatted_deadline = deadline
    elif re.match(r'^\d{8}$', deadline):
        formatted_deadline = f"{deadline[:4]}/{deadline[4:6]}/{deadline[6:]}"
    else:
        bot.send_message(message.chat.id, "فرمت تاریخ نادرست است. لطفاً دوباره تلاش کنید:")
        bot.register_next_step_handler(message, validate_challenge_deadline, goal_subject, challenge_title, challenge_description)
        return

    # ذخیره چالش با تاریخ صحیح
    new_challenge = {
        "title": challenge_title,
        "description": challenge_description,
        "deadline": formatted_deadline,
        "status": "پاس نشده ❌",  # وضعیت چالش پیش‌فرض
        "difficulty": None  # سختی چالش فعلا نامشخص است
    }
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    for goal in data["short_term_goals"] + data["long_term_goals"]:
        if goal["subject"] == goal_subject:
            if "challenges" not in goal:
                goal["challenges"] = []
            goal["challenges"].append(new_challenge)
            break

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    # سوال در مورد سختی چالش
    ask_challenge_difficulty(message, goal_subject, challenge_title)

# سوال درباره سختی چالش
def ask_challenge_difficulty(message, goal_subject, challenge_title):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("🟢 آسان", callback_data=f"difficulty_easy_{goal_subject}_{challenge_title}"),
        telebot.types.InlineKeyboardButton("🟡 متوسط", callback_data=f"difficulty_medium_{goal_subject}_{challenge_title}"),
        telebot.types.InlineKeyboardButton("🔴 سخت", callback_data=f"difficulty_hard_{goal_subject}_{challenge_title}")
    )
    bot.send_message(message.chat.id, "میزان سختی انجام این چالش را چقدر می‌دانید؟", reply_markup=markup)

# هندلر ثبت سختی چالش
# هندلر ثبت سختی چالش
@bot.callback_query_handler(func=lambda call: call.data.startswith("difficulty_"))
def set_challenge_difficulty(call):
    difficulty, goal_subject, challenge_title = call.data.split("_")[1:]
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # یافتن چالش و ثبت میزان سختی
    for goal in data["short_term_goals"] + data["long_term_goals"]:
        if goal["subject"] == goal_subject:
            for challenge in goal["challenges"]:
                if challenge["title"] == challenge_title:
                    challenge["difficulty"] = difficulty
                    break
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    # ارسال پیام با نام چالش و میزان سختی و سپس بازگشت به صفحه اصلی
    bot.send_message(call.message.chat.id, f"چالش شما با نام '{challenge_title}' با میزان سختی '{difficulty}' ثبت شد.")
    
    # بازگشت خودکار به صفحه اصلی (می‌توانید صفحه اصلی را دوباره تعریف کنید)
    main_menu(call.message)

# هندلر نمایش مشخصات چالش
@bot.callback_query_handler(func=lambda call: call.data.startswith("view_challenge_"))
def view_challenge_handler(call):
    challenge_title = call.data[len("view_challenge_"):]
    
    with open(file_path, 'r') as file:
        data = json.load(file)
        
        challenge_data = None
        for goal in data["short_term_goals"] + data["long_term_goals"]:
            for challenge in goal.get("challenges", []):
                if challenge["title"] == challenge_title:
                    challenge_data = challenge
                    break
            if challenge_data:
                break
        
    if challenge_data:
        # تعیین سختی چالش و نمایش به زبان فارسی با دایره رنگی مناسب
        difficulty_mapping = {
            "easy": "🟢 آسان",
            "medium": "🟡 متوسط",
            "hard": "🔴 سخت"
        }
        difficulty_text = difficulty_mapping.get(challenge_data.get('difficulty', 'نامشخص'), 'نامشخص')

        # ایجاد پیام حاوی مشخصات چالش (بدون وضعیت)
        challenge_details = (
                  f"🔸🔸🔸🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔸🔸🔸\n\n"
            f"نام چالش: {challenge_data['title']}\n"
            f"توضیحات: {challenge_data['description']}\n"
            f"مهلت: {challenge_data['deadline']}\n"
            f"سختی: {difficulty_text}"
        )

        # اضافه کردن دکمه وضعیت و تغییر آن بین دو حالت
        current_status = challenge_data.get("status", "پاس نشده ❌")
        status_button_text = current_status  # دکمه اولیه بر اساس وضعیت فعلی

        # ایجاد دکمه‌ها برای تغییر وضعیت و بازگشت
        markup = telebot.types.InlineKeyboardMarkup()
        status_button = telebot.types.InlineKeyboardButton(status_button_text, callback_data=f"toggle_status_{challenge_title}")
        back_button = telebot.types.InlineKeyboardButton("بازگشت", callback_data="back_to_main")
        markup.add(status_button)
        markup.add(back_button)

        # ارسال پیام با جزئیات چالش و دکمه‌ها
        bot.send_message(call.message.chat.id, challenge_details, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_status_"))
def toggle_challenge_status(call):
    challenge_title = call.data[len("toggle_status_"):]
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    challenge_data = None
    for goal in data["short_term_goals"] + data["long_term_goals"]:
        for challenge in goal.get("challenges", []):
            if challenge["title"] == challenge_title:
                challenge_data = challenge
                break
        if challenge_data:
            break

    if challenge_data:
        # وضعیت فعلی چالش را بررسی کرده و تغییر وضعیت ایجاد می‌کنیم
        current_status = challenge_data.get("status", "پاس نشده ❌")
        if current_status == "پاس نشده ❌":
            new_status = "پاس شده ✅"
            notification_message = "وضعیت چالش به پاس شده ✅ تغییر کرد."
        else:
            new_status = "پاس نشده ❌"
            notification_message = "وضعیت چالش به پاس نشده ❌ تغییر کرد."
        
        # ذخیره وضعیت جدید در فایل JSON
        challenge_data["status"] = new_status
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        # آپدیت دکمه با وضعیت جدید
        markup = telebot.types.InlineKeyboardMarkup()
        status_button = telebot.types.InlineKeyboardButton(new_status, callback_data=f"toggle_status_{challenge_title}")
        back_button = telebot.types.InlineKeyboardButton("بازگشت", callback_data="back_to_main")
        markup.add(status_button)
        markup.add(back_button)

        # ویرایش پیام با دکمه جدید و ارسال نوتیفیکیشن به کاربر
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, notification_message)
    else:
        bot.send_message(call.message.chat.id, "چالش یافت نشد.")

# هندلر دکمه "بازگشت" برای بازگشت به منوی اصلی
@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main_handler(call):
    bot.send_message(call.message.chat.id, "بازگشت به منوی اصلی", reply_markup=main_menu_markup())
    

# اجرای ربات
bot.polling()   
