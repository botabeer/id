from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
from database import Database
from ui_builder import UIBuilder
from game_manager import GameManager
from constants import *

app = Flask(__name__)

# إعداد LINE Bot
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# تهيئة الأنظمة
db = Database()
ui = UIBuilder()
game_manager = GameManager(db, ui, line_bot_api)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()
    
    # التحقق من نوع المصدر
    is_group = hasattr(event.source, 'group_id')
    source_id = event.source.group_id if is_group else user_id
    
    # الأوامر العامة (تعمل في الخاص والقروب)
    if text == 'تسجيل' or text == '/register':
        handle_register(event, user_id)
        return
    
    if text == 'انسحب' or text == '/leave':
        handle_leave(event, user_id, source_id, is_group)
        return
    
    # التحقق من التسجيل
    if not db.is_user_registered(user_id):
        if text in GAME_COMMANDS or text.startswith('/'):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='⚠️ يجب التسجيل أولاً\nأرسل كلمة "تسجيل" للبدء',
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label='تسجيل', text='تسجيل'))
                    ])
                )
            )
        return
    
    # أوامر الخاص فقط
    if not is_group:
        if text == 'القائمة' or text == '/menu':
            show_main_menu(event, user_id)
            return
        
        if text == 'الثيمات' or text == '/themes':
            show_themes_menu(event, user_id)
            return
        
        if text.startswith('ثيم:'):
            change_theme(event, user_id, text)
            return
        
        if text == 'احصائياتي' or text == '/stats':
            show_user_stats(event, user_id)
            return
        
        if text == 'شرح الالعاب' or text == '/help':
            show_games_help(event)
            return
    
    # أوامر الألعاب (تعمل في القروب فقط)
    if is_group:
        game_manager.handle_game_command(event, text, user_id, source_id)

@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data
    
    is_group = hasattr(event.source, 'group_id')
    source_id = event.source.group_id if is_group else user_id
    
    if not db.is_user_registered(user_id):
        return
    
    game_manager.handle_postback(event, data, user_id, source_id, is_group)

def handle_register(event, user_id):
    """معالجة التسجيل"""
    try:
        profile = line_bot_api.get_profile(user_id)
        name = profile.display_name
        
        if db.is_user_registered(user_id):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f'مرحباً {name}\nأنت مسجل بالفعل')
            )
            return
        
        db.register_user(user_id, name)
        
        # رسالة ترحيب بتصميم Flex
        welcome_flex = ui.create_welcome_message(name)
        
        line_bot_api.reply_message(
            event.reply_token,
            [
                FlexSendMessage(alt_text='مرحباً بك', contents=welcome_flex),
                TextSendMessage(
                    text='للبدء، أرسل "القائمة" في الخاص أو استخدم أوامر الألعاب في القروب',
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label='القائمة', text='القائمة')),
                        QuickReplyButton(action=MessageAction(label='شرح الالعاب', text='شرح الالعاب'))
                    ])
                )
            ]
        )
    except Exception as e:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f'حدث خطأ أثناء التسجيل')
        )

def handle_leave(event, user_id, source_id, is_group):
    """معالجة الانسحاب من اللعبة"""
    if not is_group:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='⚠️ هذا الأمر يعمل في القروبات فقط')
        )
        return
    
    result = game_manager.leave_game(user_id, source_id)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result)
    )

def show_main_menu(event, user_id):
    """عرض القائمة الرئيسية"""
    theme = db.get_user_theme(user_id)
    menu_flex = ui.create_main_menu(theme)
    
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text='القائمة الرئيسية', contents=menu_flex)
    )

def show_themes_menu(event, user_id):
    """عرض قائمة الثيمات"""
    current_theme = db.get_user_theme(user_id)
    themes_flex = ui.create_themes_menu(current_theme)
    
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text='الثيمات', contents=themes_flex)
    )

def change_theme(event, user_id, text):
    """تغيير الثيم"""
    theme_name = text.split(':')[1]
    
    if theme_name in THEMES:
        db.update_user_theme(user_id, theme_name)
        theme = THEMES[theme_name]
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f'تم تغيير الثيم إلى: {theme["name_ar"]}',
                quick_reply=QuickReply(items=[
                    QuickReplyButton(action=MessageAction(label='القائمة', text='القائمة'))
                ])
            )
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='⚠️ ثيم غير صحيح')
        )

def show_user_stats(event, user_id):
    """عرض إحصائيات اللاعب"""
    stats = db.get_user_stats(user_id)
    theme = db.get_user_theme(user_id)
    stats_flex = ui.create_stats_card(stats, theme)
    
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text='احصائياتك', contents=stats_flex)
    )

def show_games_help(event):
    """عرض شرح الألعاب"""
    help_messages = []
    
    for game_name, game_info in GAMES_INFO.items():
        help_flex = ui.create_game_help_card(game_name, game_info)
        help_messages.append(
            FlexSendMessage(alt_text=f'شرح {game_info["name_ar"]}', contents=help_flex)
        )
    
    line_bot_api.reply_message(event.reply_token, help_messages[:5])

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
