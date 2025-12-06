def play_word(self, event, user_id, group_id):
        """لعبة كلمة"""
        word = random.choice(self.words)
        shuffled = ''.join(random.sample(word, len(word)))
        
        # التأكد من أن الكلمة مبعثرة فعلاً
        while shuffled == word:
            shuffled = ''.join(random.sample(word, len(word)))
        
        # حفظ اللعبة
        self.db.create_active_game(group_id, 'word', {
            'word': word,
            'shuffled': shuffled,
            'answered': False
        })
        
        self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"رتب الحروف لتكوين كلمة صحيحة:\n\n{shuffled}")
        )
    
    def play_reverse(self, event, user_id, group_id):
        """لعبة عكس"""
        word = random.choice(self.words)
        reversed_word = word[::-1]
        
        # حفظ اللعبة
        self.db.create_active_game(group_id, 'reverse', {
            'word': word,
            'answered': False
        })
        
        self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"ما هي الكلمة؟\n\n{reversed_word}")
        )
    
    def play_category(self, event, user_id, group_id, category):
        """لعبة الفئات (مدن، دول، حيوانات)"""
        if category == 'cities':
            data = self.cities
            name = "مدينة"
        elif category == 'countries':
            data = self.countries
            name = "دولة"
        else:
            data = self.animals
            name = "حيوان"
        
        letter = random.choice(list(data.keys()))
        
        # حفظ اللعبة
        self.db.create_active_game(group_id, category, {
            'letter': letter,
            'valid_answers': data[letter],
            'answered': False
        })
        
        self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"اذكر {name} يبدأ بحرف:\n\n{letter}")
        )
    
    def start_lariat_game(self, event, user_id, group_id):
        """بدء لعبة لوريت"""
        try:
            profile = self.line_bot_api.get_profile(user_id)
            name = profile.display_name
        except:
            name = "اللاعب"
        
        # التحقق من وجود لعبة نشطة
        existing = self.db.get_lariat_game(group_id)
        if existing:
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="يوجد لعبة لوريت نشطة بالفعل")
            )
            return
        
        # كلمة البداية
        first_word = random.choice(self.words)
        
        # إنشاء اللعبة
        self.db.create_lariat_game(group_id, first_word, [user_id])
        
        last_letter = first_word[-1]
        self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f"بدأت لعبة لوريت\n\n{name} بدأ بكلمة: {first_word}\n\nالدور التالي: اكتب كلمة تبدأ بحرف {last_letter}"
            )
        )
    
    def start_mafia_game(self, event, user_id, group_id):
        """بدء لعبة المافيا"""
        try:
            profile = self.line_bot_api.get_profile(user_id)
            name = profile.display_name
        except:
            name = "اللاعب"
        
        # التحقق من وجود لعبة نشطة
        existing = self.db.get_mafia_game(group_id)
        if existing:
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="يوجد لعبة مافيا نشطة بالفعل")
            )
            return
        
        self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f"لعبة المافيا\n\nيحتاج من 5 إلى 10 لاعبين\n\n{name} انضم للعبة\n\nأرسل 'انضم' للمشاركة\nأرسل 'ابدأ' لبدء اللعبة"
            )
        )
        
        # إنشاء لعبة مافيا مؤقتة
        self.db.create_active_game(group_id, 'mafia_lobby', {
            'players': [user_id],
            'ready': False
        })
    
    def handle_postback(self, event, data, user_id, source_id, is_group):
        """معالجة الأزرار"""
        
        if data == 'data=stats':
            # عرض الإحصائيات
            stats = self.db.get_user_stats(user_id)
            theme = self.db.get_user_theme(user_id)
            stats_flex = self.ui.create_stats_card(stats, theme)
            
            self.line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text='احصائياتك', contents=stats_flex)
            )
        
        elif data == 'data=themes':
            # عرض الثيمات
            current_theme = self.db.get_user_theme(user_id)
            themes_flex = self.ui.create_themes_menu(current_theme)
            
            self.line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text='الثيمات', contents=themes_flex)
            )
        
        elif data.startswith('answer='):
            # إجابة سؤال
            if not is_group:
                return
            
            answer_idx = int(data.split('=')[1])
            game_data = self.db.get_active_game(source_id, 'trivia')
            
            if game_data and not game_data['answered']:
                correct = answer_idx == game_data['question']['answer']
                
                try:
                    profile = self.line_bot_api.get_profile(user_id)
                    name = profile.display_name
                except:
                    name = "اللاعب"
                
                if correct:
                    points = GAME_SETTINGS['points_correct']
                    self.db.update_user_stats(user_id, won=True, points=points)
                    self.db.record_game_stat(user_id, 'trivia', 'win', points)
                    
                    message = f"إجابة صحيحة {name}\n+{points} نقطة"
                else:
                    points = GAME_SETTINGS['points_wrong']
                    self.db.update_user_stats(user_id, points=points)
                    self.db.record_game_stat(user_id, 'trivia', 'lose', points)
                    
                    correct_answer = game_data['question']['options'][game_data['question']['answer']]
                    message = f"إجابة خاطئة {name}\nالإجابة الصحيحة: {correct_answer}"
                
                game_data['answered'] = True
                self.db.update_active_game(source_id, 'trivia', game_data)
                
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=message)
                )
        
        elif data.startswith('choice='):
            # لو خيروك
            if not is_group:
                return
            
            choice = data.split('=')[1]
            game_data = self.db.get_active_game(source_id, 'wouldyourather')
            
            if game_data:
                try:
                    profile = self.line_bot_api.get_profile(user_id)
                    name = profile.display_name
                except:
                    name = "اللاعب"
                
                chosen_option = game_data['options'][0] if choice == '1' else game_data['options'][1]
                
                self.db.record_game_stat(user_id, 'wouldyourather', 'played', 5)
                self.db.update_user_stats(user_id, points=5)
                
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"{name} اختار:\n{chosen_option}")
                )
    
    def check_active_game_answer(self, event, text, user_id, group_id):
        """التحقق من إجابات الألعاب النشطة"""
        
        try:
            profile = self.line_bot_api.get_profile(user_id)
            name = profile.display_name
        except:
            name = "اللاعب"
        
        # لعبة رياضيات
        math_game = self.db.get_active_game(group_id, 'math')
        if math_game and not math_game['answered']:
            try:
                answer = int(text)
                if answer == math_game['answer']:
                    points = GAME_SETTINGS['points_correct']
                    self.db.update_user_stats(user_id, won=True, points=points)
                    self.db.record_game_stat(user_id, 'math', 'win', points)
                    
                    math_game['answered'] = True
                    self.db.update_active_game(group_id, 'math', math_game)
                    
                    self.line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=f"إجابة صحيحة {name}\n+{points} نقطة")
                    )
                    return
            except:
                pass
        
        # لعبة احزر
        guess_game = self.db.get_active_game(group_id, 'guess')
        if guess_game:
            try:
                guess = int(text)
                guess_game['attempts'] += 1
                
                if guess == guess_game['number']:
                    points = GAME_SETTINGS['points_win']
                    self.db.update_user_stats(user_id, won=True, points=points)
                    self.db.record_game_stat(user_id, 'guess', 'win', points)
                    self.db.delete_active_game(group_id, 'guess')
                    
                    self.line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=f"مبروك {name}\nالرقم صحيح: {guess}\n+{points} نقطة")
                    )
                    return
                
                elif guess_game['attempts'] >= guess_game['max_attempts']:
                    self.db.delete_active_game(group_id, 'guess')
                    self.line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=f"انتهت المحاولات\nالرقم الصحيح كان: {guess_game['number']}")
                    )
                    return
                
                else:
                    hint = "أكبر" if guess < guess_game['number'] else "أصغر"
                    remaining = guess_game['max_attempts'] - guess_game['attempts']
                    
                    self.db.update_active_game(group_id, 'guess', guess_game)
                    
                    self.line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=f"الرقم {hint}\nالمحاولات المتبقية: {remaining}")
                    )
                    return
            except:
                pass
        
        # لعبة كلمة
        word_game = self.db.get_active_game(group_id, 'word')
        if word_game and not word_game['answered']:
            if text.strip() == word_game['word']:
                points = GAME_SETTINGS['points_correct']
                self.db.update_user_stats(user_id, won=True, points=points)
                self.db.record_game_stat(user_id, 'word', 'win', points)
                
                word_game['answered'] = True
                self.db.update_active_game(group_id, 'word', word_game)
                
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"إجابة صحيحة {name}\nالكلمة: {word_game['word']}\n+{points} نقطة")
                )
                return
        
        # لعبة عكس
        reverse_game = self.db.get_active_game(group_id, 'reverse')
        if reverse_game and not reverse_game['answered']:
            if text.strip() == reverse_game['word']:
                points = GAME_SETTINGS['points_correct']
                self.db.update_user_stats(user_id, won=True, points=points)
                self.db.record_game_stat(user_id, 'reverse', 'win', points)
                
                reverse_game['answered'] = True
                self.db.update_active_game(group_id, 'reverse', reverse_game)
                
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"إجابة صحيحة {name}\nالكلمة: {reverse_game['word']}\n+{points} نقطة")
                )
                return
        
        # ألعاب الفئات
        for category in ['cities', 'countries', 'animals']:
            cat_game = self.db.get_active_game(group_id, category)
            if cat_game and not cat_game['answered']:
                if text.strip() in cat_game['valid_answers']:
                    points = GAME_SETTINGS['points_correct']
                    self.db.update_user_stats(user_id, won=True, points=points)
                    self.db.record_game_stat(user_id, category, 'win', points)
                    
                    cat_game['answered'] = True
                    self.db.update_active_game(group_id, category, cat_game)
                    
                    self.line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=f"إجابة صحيحة {name}\n{text}\n+{points} نقطة")
                    )
                    return
        
        # لعبة لوريت
        lariat = self.db.get_lariat_game(group_id)
        if lariat:
            last_letter = lariat['current_word'][-1]
            word = text.strip()
            
            # التحقق من صحة الكلمة
            if word[0] == last_letter and word not in lariat['used_words'] and len(word) > 1:
                # تحديث اللعبة
                players = lariat['players']
                current_idx = players.index(lariat['current_player'])
                next_idx = (current_idx + 1) % len(players)
                next_player = players[next_idx]
                
                self.db.update_lariat_game(group_id, word, next_player)
                
                points = 5
                self.db.update_user_stats(user_id, points=points)
                self.db.record_game_stat(user_id, 'lariat', 'played', points)
                
                new_last_letter = word[-1]
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"{name}: {word}\n\nالدور التالي: كلمة تبدأ بحرف {new_last_letter}")
                )
                return
        
        # لعبة المافيا - انضمام
        mafia_lobby = self.db.get_active_game(group_id, 'mafia_lobby')
        if mafia_lobby and text == 'انضم':
            if user_id not in mafia_lobby['players']:
                mafia_lobby['players'].append(user_id)
                self.db.update_active_game(group_id, 'mafia_lobby', mafia_lobby)
                
                count = len(mafia_lobby['players'])
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"{name} انضم للعبة\nعدد اللاعبين: {count}")
                )
                return
        
        # بدء لعبة المافيا
        if mafia_lobby and text == 'ابدأ':
            players_count = len(mafia_lobby['players'])
            
            if players_count < GAME_SETTINGS['min_players_mafia']:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"يحتاج 5 لاعبين على الأقل")
                )
                return
            
            # توزيع الأدوار
            players = mafia_lobby['players']
            roles = self.assign_mafia_roles(players)
            
            # إنشاء اللعبة
            self.db.delete_active_game(group_id, 'mafia_lobby')
            self.db.create_mafia_game(group_id, players, roles)
            
            # إرسال الأدوار للاعبين
            for player_id, role in roles.items():
                try:
                    role_text = self.get_role_description(role)
                    self.line_bot_api.push_message(
                        player_id,
                        TextSendMessage(text=f"دورك في اللعبة:\n{role_text}")
                    )
                except:
                    pass
            
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="بدأت لعبة المافيا\nتم إرسال الأدوار للاعبين في الخاص\n\nالليلة الأولى")
            )
    
    def assign_mafia_roles(self, players):
        """توزيع أدوار المافيا"""
        roles = {}
        player_list = players.copy()
        random.shuffle(player_list)
        
        count = len(players)
        mafia_count = max(1, count // 3)
        
        # المافيا
        for i in range(mafia_count):
            roles[player_list[i]] = 'mafia'
        
        # الطبيب
        if count >= 7:
            roles[player_list[mafia_count]] = 'doctor'
            roles[player_list[mafia_count + 1]] = 'detective'
            start_citizens = mafia_count + 2
        elif count >= 5:
            roles[player_list[mafia_count]] = 'doctor'
            start_citizens = mafia_count + 1
        else:
            start_citizens = mafia_count
        
        # المواطنين
        for i in range(start_citizens, count):
            roles[player_list[i]] = 'citizen'
        
        return roles
    
    def get_role_description(self, role):
        """وصف الدور"""
        descriptions = {
            'mafia': 'أنت من المافيا\nهدفك: القضاء على جميع المواطنين',
            'doctor': 'أنت الطبيب\nيمكنك إنقاذ شخص كل ليلة',
            'detective': 'أنت المحقق\nيمكنك الكشف عن دور شخص كل ليلة',
            'citizen': 'أنت مواطن\nحاول اكتشاف المافيا'
        }
        return descriptions.get(role, '')
