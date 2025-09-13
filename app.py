from flask import Flask, request, abort
from dotenv import load_dotenv
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# تحميل المتغيرات من ملف .env
load_dotenv()

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("aErk1lTQiebIf/P1d8JQllkU1eebylaSAKQZTkYW3d50WeLncmTlIMyFX9rvttNg347TH6SsLwKSGZTKIxv+JmIFPeye/tK2us6/npBfeYkdkti5YhNz/wJzYszW12IikIDfi5NT1oMeXBRmAL8C0wdB04t89/1O/w1cDnyilFU=")
LINE_CHANNEL_SECRET = os.getenv("1841e7af13a02de5400ade57c3fb9bc1")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# قائمة الحظر
blacklist = set()

# استقبال Webhook
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
    text = event.message.text.strip()

    # أمر id
    if text == "id":
        user_id = event.source.user_id
        reply = f"🆔 ID الخاص بك:\n{user_id}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

    # أمر تحقق الأدمن
    elif text == "تحقق الأدمن":
        try:
            group_id = event.source.group_id
            bot_profile = line_bot_api.get_group_member_profile(group_id, event.source.user_id)

            if hasattr(bot_profile, "role") and bot_profile.role == "admin":
                reply = "✅ البوت أدمن في هذا القروب"
            else:
                reply = "❌ البوت ليس أدمن في هذا القروب"
        except Exception as e:
            reply = f"⚠️ خطأ أثناء التحقق: {e}"

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

    # أمر طرد بالمنشن
    elif text.startswith("طرد @"):
        try:
            group_id = event.source.group_id
            name = text.replace("طرد @", "").strip()

            members = line_bot_api.get_group_member_ids(group_id)
            found = False
            for uid in members:
                profile = line_bot_api.get_group_member_profile(group_id, uid)
                if profile.display_name == name:
                    line_bot_api.kick_group_member(group_id, uid)
                    reply = f"🚫 تم طرد {name}"
                    found = True
                    break

            if not found:
                reply = f"❌ العضو @{name} غير موجود"

        except Exception as e:
            reply = f"⚠️ فشل الطرد: {e}"

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

    # أمر حظر بالمنشن
    elif text.startswith("حظر @"):
        try:
            group_id = event.source.group_id
            name = text.replace("حظر @", "").strip()

            members = line_bot_api.get_group_member_ids(group_id)
            found = False
            for uid in members:
                profile = line_bot_api.get_group_member_profile(group_id, uid)
                if profile.display_name == name:
                    blacklist.add(uid)
                    reply = f"⛔ تم حظر {name}"
                    found = True
                    break

            if not found:
                reply = f"❌ العضو @{name} غير موجود"

        except Exception as e:
            reply = f"⚠️ فشل الحظر: {e}"

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

    # أمر رفع الحظر بالمنشن
    elif text.startswith("رفع الحظر @"):
        try:
            group_id = event.source.group_id
            name = text.replace("رفع الحظر @", "").strip()

            members = line_bot_api.get_group_member_ids(group_id)
            found = False
            for uid in members:
                profile = line_bot_api.get_group_member_profile(group_id, uid)
                if profile.display_name == name:
                    if uid in blacklist:
                        blacklist.remove(uid)
                        reply = f"✅ تم رفع الحظر عن {name}"
                    else:
                        reply = f"ℹ️ {name} غير موجود في قائمة الحظر"
                    found = True
                    break

            if not found:
                reply = f"❌ العضو @{name} غير موجود"

        except Exception as e:
            reply = f"⚠️ فشل رفع الحظر: {e}"

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))


if __name__ == "__main__":
    app.run(port=8000)
