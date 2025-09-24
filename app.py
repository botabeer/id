from flask import Flask, request, abort
import os
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# تحميل المتغيرات من .env
load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# جلب ID البوت نفسه
try:
    bot_info = line_bot_api.get_bot_info()
    BOT_ID = bot_info.user_id
except Exception:
    BOT_ID = "غير متاح (تأكد من التوكن)"


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

    text = event.message.text.strip()

    # ----- أوامر IDs -----
    if text == "معرفي":
        reply_text = f"👤 User ID: {user_id}"

    elif text == "معرف_البوت":
        reply_text = f"🤖 Bot ID: {BOT_ID}"

    elif text == "معرف_القروب":
        if group_id:
            reply_text = f"👥 Group/Room ID: {group_id}"
        else:
            reply_text = "❌ الأمر يعمل فقط داخل قروب أو روم"

    elif text == "اعضاء" and group_id:
        try:
            if event.source.type == "group":
                member_ids = line_bot_api.get_group_member_ids(group_id)
            else:
                member_ids = line_bot_api.get_room_member_ids(group_id)

            members_text = []
            for uid in member_ids:
                try:
                    profile = line_bot_api.get_group_member_profile(group_id, uid)
                    members_text.append(f"{profile.display_name} — {uid}")
                except:
                    members_text.append(uid)

            reply_text = "👥 أعضاء القروب:\n" + "\n".join(members_text)

        except Exception as e:
            reply_text = f"⚠️ خطأ أثناء جلب الأعضاء: {str(e)}"

    elif text == "مساعدة":
        reply_text = (
            "📌 أوامر البوت الخاصة بالمعرفات:\n\n"
            "• id → يظهر User ID + Bot ID + Group/Room ID\n"
            "• معرفي → يظهر معرفك الشخصي\n"
            "• معرف_البوت → يظهر معرف البوت\n"
            "• معرف_القروب → يظهر معرف القروب/الروم\n"
            "• اعضاء → يظهر قائمة بأعضاء القروب (مع الاسم + ID)\n"
            "• أي رسالة أخرى → يظهر كل المعرفات معاً"
        )

    elif text == "id":
        if group_id:
            reply_text = f"👤 User ID: {user_id}\n🤖 Bot ID: {BOT_ID}\n👥 Group/Room ID: {group_id}"
        else:
            reply_text = f"👤 User ID: {user_id}\n🤖 Bot ID: {BOT_ID}\n(خاص، لا يوجد Group ID)"

    else:
        # الرد الافتراضي: كل المعرفات
        if group_id:
            reply_text = f"👤 User ID: {user_id}\n🤖 Bot ID: {BOT_ID}\n👥 Group/Room ID: {group_id}"
        else:
            reply_text = f"👤 User ID: {user_id}\n🤖 Bot ID: {BOT_ID}\n(خاص، لا يوجد Group ID)"

    # إرسال الرد
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
