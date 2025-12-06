from constants import *

class UIBuilder:
    def __init__(self):
        pass
    
    def create_welcome_message(self, name):
        """رسالة الترحيب"""
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": BOT_NAME,
                        "weight": "bold",
                        "size": "xxl",
                        "align": "center",
                        "color": "#00d9ff"
                    },
                    {
                        "type": "text",
                        "text": f"مرحباً {name}",
                        "size": "xl",
                        "align": "center",
                        "margin": "md",
                        "color": "#ffffff"
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": "تم تسجيلك بنجاح",
                        "size": "sm",
                        "align": "center",
                        "margin": "xl",
                        "color": "#94a1b2"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "استخدم القائمة في الخاص للتحكم بالإعدادات",
                                "size": "xs",
                                "color": "#b0c4de",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": "استخدم أوامر الألعاب في القروبات للعب",
                                "size": "xs",
                                "color": "#b0c4de",
                                "wrap": True,
                                "margin": "sm"
                            }
                        ],
                        "margin": "xl",
                        "paddingAll": "md",
                        "backgroundColor": "#1e3a5f",
                        "cornerRadius": "md"
                    }
                ],
                "paddingAll": "xl",
                "backgroundColor": "#1a1a2e"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": COPYRIGHT,
                        "size": "xxs",
                        "align": "center",
                        "color": "#6c757d"
                    }
                ],
                "backgroundColor": "#16213e"
            }
        }
    
    def create_main_menu(self, theme_name='dark'):
        """القائمة الرئيسية"""
        theme = THEMES[theme_name]
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": BOT_NAME,
                        "weight": "bold",
                        "size": "xxl",
                        "align": "center",
                        "color": theme['success']
                    },
                    {
                        "type": "text",
                        "text": "القائمة الرئيسية",
                        "size": "md",
                        "align": "center",
                        "margin": "sm",
                        "color": theme['text_secondary']
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            self._create_menu_button("احصائياتي", "data=stats", theme),
                            self._create_menu_button("الثيمات", "data=themes", theme),
                            self._create_menu_button("شرح الالعاب", "data=help", theme),
                            self._create_menu_button("عن البوت", "data=about", theme)
                        ],
                        "spacing": "sm",
                        "margin": "xl"
                    }
                ],
                "paddingAll": "xl",
                "backgroundColor": theme['primary']
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": COPYRIGHT,
                        "size": "xxs",
                        "align": "center",
                        "color": theme['text_secondary']
                    }
                ],
                "backgroundColor": theme['secondary']
            }
        }
    
    def create_themes_menu(self, current_theme):
        """قائمة الثيمات"""
        theme = THEMES[current_theme]
        
        theme_buttons = []
        for key, t in THEMES.items():
            is_current = key == current_theme
            button = {
                "type": "button",
                "style": "primary" if is_current else "secondary",
                "action": {
                    "type": "message",
                    "label": f"{'✓ ' if is_current else ''}{t['name_ar']}",
                    "text": f"ثيم:{key}"
                }
            }
            theme_buttons.append(button)
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "اختر الثيم",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "color": theme['success']
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": theme_buttons,
                        "spacing": "sm",
                        "margin": "xl"
                    }
                ],
                "paddingAll": "xl",
                "backgroundColor": theme['primary']
            }
        }
    
    def create_stats_card(self, stats, theme_name='dark'):
        """بطاقة الإحصائيات"""
        theme = THEMES[theme_name]
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"احصائيات {stats['name']}",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "color": theme['success']
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            self._create_stat_row("إجمالي الألعاب", str(stats['total_games']), theme),
                            self._create_stat_row("الفوز", str(stats['total_wins']), theme),
                            self._create_stat_row("معدل الفوز", f"{stats['win_rate']}%", theme),
                            self._create_stat_row("النقاط", str(stats['total_points']), theme)
                        ],
                        "spacing": "md",
                        "margin": "xl",
                        "paddingAll": "md",
                        "backgroundColor": theme['secondary'],
                        "cornerRadius": "md"
                    }
                ],
                "paddingAll": "xl",
                "backgroundColor": theme['primary']
            }
        }
    
    def create_game_help_card(self, game_key, game_info):
        """بطاقة شرح اللعبة"""
        theme = THEMES['dark']
        
        how_to_play = []
        for i, step in enumerate(game_info['how_to_play'], 1):
            how_to_play.append({
                "type": "text",
                "text": f"{i}. {step}",
                "size": "xs",
                "color": theme['text_secondary'],
                "wrap": True,
                "margin": "sm"
            })
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": game_info['name_ar'],
                        "weight": "bold",
                        "size": "xl",
                        "color": theme['success']
                    },
                    {
                        "type": "text",
                        "text": game_info['description'],
                        "size": "sm",
                        "color": theme['text_secondary'],
                        "wrap": True,
                        "margin": "sm"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"الأمر: {game_info['command']}",
                                "size": "xs",
                                "color": theme['warning'],
                                "flex": 0
                            }
                        ],
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"الصعوبة: {game_info['difficulty']}",
                                "size": "xs",
                                "color": theme['text_secondary'],
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": f"اللاعبين: {game_info['players']}",
                                "size": "xs",
                                "color": theme['text_secondary'],
                                "flex": 1
                            }
                        ],
                        "spacing": "sm"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "طريقة اللعب:",
                        "weight": "bold",
                        "size": "sm",
                        "color": theme['text'],
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": how_to_play,
                        "margin": "sm"
                    }
                ],
                "paddingAll": "xl",
                "backgroundColor": theme['primary']
            }
        }
    
    def create_game_question_flex(self, question, options, theme_name='dark'):
        """سؤال اللعبة مع أزرار"""
        theme = THEMES[theme_name]
        
        option_buttons = []
        for i, option in enumerate(options):
            option_buttons.append({
                "type": "button",
                "style": "secondary",
                "action": {
                    "type": "postback",
                    "label": option,
                    "data": f"answer={i}"
                }
            })
        
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": question,
                        "weight": "bold",
                        "size": "lg",
                        "wrap": True,
                        "color": theme['text']
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": option_buttons,
                        "spacing": "sm",
                        "margin": "xl"
                    }
                ],
                "paddingAll": "xl",
                "backgroundColor": theme['primary']
            }
        }
    
    def create_would_you_rather_flex(self, option1, option2, theme_name='dark'):
        """سؤال لو خيروك"""
        theme = THEMES[theme_name]
        
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "لو خيروك",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "color": theme['success']
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "style": "primary",
                                "action": {
                                    "type": "postback",
                                    "label": option1,
                                    "data": "choice=1"
                                }
                            },
                            {
                                "type": "text",
                                "text": "أو",
                                "align": "center",
                                "color": theme['text_secondary'],
                                "margin": "md"
                            },
                            {
                                "type": "button",
                                "style": "primary",
                                "action": {
                                    "type": "postback",
                                    "label": option2,
                                    "data": "choice=2"
                                },
                                "margin": "md"
                            }
                        ],
                        "margin": "xl"
                    }
                ],
                "paddingAll": "xl",
                "backgroundColor": theme['primary']
            }
        }
    
    def _create_menu_button(self, label, data, theme):
        """زر القائمة"""
        return {
            "type": "button",
            "style": "primary",
            "action": {
                "type": "postback",
                "label": label,
                "data": data
            },
            "color": theme['accent']
        }
    
    def _create_stat_row(self, label, value, theme):
        """صف الإحصائية"""
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": label,
                    "size": "sm",
                    "color": theme['text_secondary'],
                    "flex": 1
                },
                {
                    "type": "text",
                    "text": value,
                    "size": "sm",
                    "color": theme['success'],
                    "align": "end",
                    "weight": "bold"
                }
            ]
        }
