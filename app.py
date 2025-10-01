from flask import Flask, request, abort
import os
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

try:
    bot_info = line_bot_api.get_bot_info()
    BOT_ID = bot_info.user_id
except Exception:
    BOT_ID = "غير متاح (تاكد من التوكن)"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    group_id = None
    if event.source.type == "group":
        group_id = event.source.group_id
    elif event.source.type == "room":
        group_id = event.source.room_id
    text = event.message.text.strip().lower()
    reply_text = None

    if text in ["id", "معرفي"]:
        reply_text = f"🆔 USER ID: {user_id.upper()}"
    elif text in ["idg", "معرف_القروب"]:
        if group_id:
            reply_text = f"🆔 GROUP/ROOM ID: {group_id.upper()}"
        else:
            reply_text = "❌ هذا الامر يعمل فقط داخل قروب او روم"
    elif text in ["idall", "الكل"]:
        if group_id:
            try:
                if event.source.type == "group":
                    member_ids = line_bot_api.get_group_member_ids(group_id)
                else:
                    member_ids = line_bot_api.get_room_member_ids(group_id)
                members_text = []
                for uid in member_ids:
                    try:
                        if event.source.type == "group":
                            profile = line_bot_api.get_group_member_profile(group_id, uid)
                        else:
                            profile = line_bot_api.get_room_member_profile(group_id, uid)
                        members_text.append(f"🆔 {profile.display_name.upper()} — {uid.upper()}")
                    except:
                        members_text.append(f"🆔 {uid.upper()}")
                reply_text = (
                    f"🆔 GROUP/ROOM ID: {group_id.upper()}\n"
                    f"🆔 BOT ID: {BOT_ID.upper()}\n\n"
                    "🆔 MEMBERS:\n" + "\n".join(members_text)
                )
            except Exception as e:
                reply_text = f"⚠️ خطأ اثناء جلب الاعضاء: {str(e).upper()}"
        else:
            reply_text = "❌ هذا الامر يعمل فقط داخل قروب او روم"
    elif text in ["help", "مساعدة"]:
        reply_text = (
            "📌 اوامر البوت:\n"
            "1️⃣ ID → معرفك\n"
            "2️⃣ IDG → معرف القروب/الروم\n"
            "3️⃣ IDALL → جميع المعرفات\n"
            "4️⃣ HELP → عرض الاوامر"
        )

    if reply_text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
