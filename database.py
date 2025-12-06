import sqlite3
from datetime import datetime
import json

class Database:
    def __init__(self, db_name='bot65.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """تهيئة قاعدة البيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                theme TEXT DEFAULT 'dark',
                total_games INTEGER DEFAULT 0,
                total_wins INTEGER DEFAULT 0,
                total_points INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الألعاب النشطة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id TEXT NOT NULL,
                game_type TEXT NOT NULL,
                game_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(group_id, game_type)
            )
        ''')
        
        # جدول إحصائيات الألعاب
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_stats (
                stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                game_type TEXT NOT NULL,
                result TEXT,
                points INTEGER DEFAULT 0,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # جدول لعبة لوريت
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lariat_games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id TEXT NOT NULL,
                current_word TEXT,
                used_words TEXT,
                players TEXT,
                current_player TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول لعبة المافيا
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mafia_games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id TEXT NOT NULL,
                players TEXT,
                roles TEXT,
                phase TEXT DEFAULT 'night',
                day_number INTEGER DEFAULT 1,
                alive_players TEXT,
                votes TEXT,
                actions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # وظائف المستخدمين
    def is_user_registered(self, user_id):
        """التحقق من تسجيل المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def register_user(self, user_id, name):
        """تسجيل مستخدم جديد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (user_id, name) VALUES (?, ?)
            ''', (user_id, name))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_user_theme(self, user_id):
        """الحصول على ثيم المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT theme FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result['theme'] if result else 'dark'
    
    def update_user_theme(self, user_id, theme):
        """تحديث ثيم المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET theme = ? WHERE user_id = ?', (theme, user_id))
        conn.commit()
        conn.close()
    
    def get_user_stats(self, user_id):
        """الحصول على إحصائيات المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, total_games, total_wins, total_points,
                   created_at, last_active
            FROM users WHERE user_id = ?
        ''', (user_id,))
        result = cursor.fetchone()
        
        if result:
            stats = dict(result)
            # حساب معدل الفوز
            win_rate = (stats['total_wins'] / stats['total_games'] * 100) if stats['total_games'] > 0 else 0
            stats['win_rate'] = round(win_rate, 1)
            
            # احصائيات الألعاب المختلفة
            cursor.execute('''
                SELECT game_type, COUNT(*) as count, SUM(points) as points
                FROM game_stats
                WHERE user_id = ?
                GROUP BY game_type
            ''', (user_id,))
            
            stats['games_breakdown'] = {}
            for row in cursor.fetchall():
                stats['games_breakdown'][row['game_type']] = {
                    'count': row['count'],
                    'points': row['points'] or 0
                }
            
            conn.close()
            return stats
        
        conn.close()
        return None
    
    def update_user_stats(self, user_id, won=False, points=0):
        """تحديث إحصائيات المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if won:
            cursor.execute('''
                UPDATE users 
                SET total_games = total_games + 1,
                    total_wins = total_wins + 1,
                    total_points = total_points + ?,
                    last_active = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (points, user_id))
        else:
            cursor.execute('''
                UPDATE users 
                SET total_games = total_games + 1,
                    total_points = total_points + ?,
                    last_active = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (points, user_id))
        
        conn.commit()
        conn.close()
    
    def record_game_stat(self, user_id, game_type, result, points=0):
        """تسجيل إحصائية لعبة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO game_stats (user_id, game_type, result, points)
            VALUES (?, ?, ?, ?)
        ''', (user_id, game_type, result, points))
        conn.commit()
        conn.close()
    
    # وظائف الألعاب النشطة
    def create_active_game(self, group_id, game_type, game_data=None):
        """إنشاء لعبة نشطة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        data_json = json.dumps(game_data) if game_data else None
        
        try:
            cursor.execute('''
                INSERT INTO active_games (group_id, game_type, game_data)
                VALUES (?, ?, ?)
            ''', (group_id, game_type, data_json))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_active_game(self, group_id, game_type):
        """الحصول على لعبة نشطة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT game_data FROM active_games
            WHERE group_id = ? AND game_type = ?
        ''', (group_id, game_type))
        result = cursor.fetchone()
        conn.close()
        
        if result and result['game_data']:
            return json.loads(result['game_data'])
        return None
    
    def update_active_game(self, group_id, game_type, game_data):
        """تحديث لعبة نشطة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        data_json = json.dumps(game_data)
        cursor.execute('''
            UPDATE active_games SET game_data = ?
            WHERE group_id = ? AND game_type = ?
        ''', (data_json, group_id, game_type))
        conn.commit()
        conn.close()
    
    def delete_active_game(self, group_id, game_type):
        """حذف لعبة نشطة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM active_games
            WHERE group_id = ? AND game_type = ?
        ''', (group_id, game_type))
        conn.commit()
        conn.close()
    
    def has_active_game(self, group_id):
        """التحقق من وجود لعبة نشطة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) as count FROM active_games
            WHERE group_id = ?
        ''', (group_id,))
        result = cursor.fetchone()
        conn.close()
        return result['count'] > 0
    
    # وظائف لعبة لوريت
    def create_lariat_game(self, group_id, first_word, players):
        """إنشاء لعبة لوريت"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO lariat_games (group_id, current_word, used_words, players, current_player)
            VALUES (?, ?, ?, ?, ?)
        ''', (group_id, first_word, json.dumps([first_word]), json.dumps(players), players[0]))
        conn.commit()
        conn.close()
    
    def get_lariat_game(self, group_id):
        """الحصول على لعبة لوريت"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lariat_games WHERE group_id = ?', (group_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'current_word': result['current_word'],
                'used_words': json.loads(result['used_words']),
                'players': json.loads(result['players']),
                'current_player': result['current_player']
            }
        return None
    
    def update_lariat_game(self, group_id, word, next_player):
        """تحديث لعبة لوريت"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        game = self.get_lariat_game(group_id)
        if game:
            used_words = game['used_words']
            used_words.append(word)
            
            cursor.execute('''
                UPDATE lariat_games
                SET current_word = ?, used_words = ?, current_player = ?
                WHERE group_id = ?
            ''', (word, json.dumps(used_words), next_player, group_id))
            conn.commit()
        
        conn.close()
    
    def delete_lariat_game(self, group_id):
        """حذف لعبة لوريت"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM lariat_games WHERE group_id = ?', (group_id,))
        conn.commit()
        conn.close()
    
    # وظائف لعبة المافيا
    def create_mafia_game(self, group_id, players, roles):
        """إنشاء لعبة مافيا"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mafia_games (group_id, players, roles, alive_players, votes, actions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (group_id, json.dumps(players), json.dumps(roles), 
              json.dumps(players), '{}', '{}'))
        conn.commit()
        conn.close()
    
    def get_mafia_game(self, group_id):
        """الحصول على لعبة مافيا"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM mafia_games WHERE group_id = ?', (group_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'players': json.loads(result['players']),
                'roles': json.loads(result['roles']),
                'phase': result['phase'],
                'day_number': result['day_number'],
                'alive_players': json.loads(result['alive_players']),
                'votes': json.loads(result['votes']),
                'actions': json.loads(result['actions'])
            }
        return None
    
    def update_mafia_game(self, group_id, game_data):
        """تحديث لعبة مافيا"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE mafia_games
            SET phase = ?, day_number = ?, alive_players = ?, votes = ?, actions = ?
            WHERE group_id = ?
        ''', (game_data['phase'], game_data['day_number'],
              json.dumps(game_data['alive_players']),
              json.dumps(game_data['votes']),
              json.dumps(game_data['actions']),
              group_id))
        conn.commit()
        conn.close()
    
    def delete_mafia_game(self, group_id):
        """حذف لعبة مافيا"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM mafia_games WHERE group_id = ?', (group_id,))
        conn.commit()
        conn.close()
