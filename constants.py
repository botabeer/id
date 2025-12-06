# معلومات البوت
BOT_NAME = "بوت 65"
BOT_VERSION = "1.0.0"
COPYRIGHT = "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025"

# الثيمات المتاحة
THEMES = {
    'dark': {
        'name_ar': 'داكن',
        'primary': '#1a1a2e',
        'secondary': '#16213e',
        'accent': '#0f3460',
        'text': '#ffffff',
        'text_secondary': '#94a1b2',
        'success': '#00d9ff',
        'warning': '#ffd700',
        'danger': '#ff6b6b',
        'glass_bg': 'rgba(26, 26, 46, 0.7)',
        'glass_border': 'rgba(255, 255, 255, 0.1)'
    },
    'light': {
        'name_ar': 'فاتح',
        'primary': '#ffffff',
        'secondary': '#f5f5f5',
        'accent': '#e8e8e8',
        'text': '#1a1a2e',
        'text_secondary': '#6c757d',
        'success': '#00b894',
        'warning': '#fdcb6e',
        'danger': '#d63031',
        'glass_bg': 'rgba(255, 255, 255, 0.7)',
        'glass_border': 'rgba(0, 0, 0, 0.1)'
    },
    'blue': {
        'name_ar': 'أزرق',
        'primary': '#0a1929',
        'secondary': '#1e3a5f',
        'accent': '#2e5090',
        'text': '#ffffff',
        'text_secondary': '#b0c4de',
        'success': '#00d4ff',
        'warning': '#ffa726',
        'danger': '#ff5252',
        'glass_bg': 'rgba(10, 25, 41, 0.7)',
        'glass_border': 'rgba(0, 212, 255, 0.2)'
    },
    'calm': {
        'name_ar': 'هادئ',
        'primary': '#2d3436',
        'secondary': '#636e72',
        'accent': '#b2bec3',
        'text': '#dfe6e9',
        'text_secondary': '#b2bec3',
        'success': '#00b894',
        'warning': '#fdcb6e',
        'danger': '#d63031',
        'glass_bg': 'rgba(45, 52, 54, 0.7)',
        'glass_border': 'rgba(178, 190, 195, 0.2)'
    }
}

# أوامر الألعاب
GAME_COMMANDS = [
    'صراحة', 'جرأة', 'لو خيروك', 'سؤال', 'احزر', 'رياضيات', 
    'كلمة', 'عكس', 'مدن', 'دول', 'حيوانات', 'لوريت', 'مافيا',
    '/truth', '/dare', '/wouldyourather', '/question', '/guess',
    '/math', '/word', '/reverse', '/cities', '/countries', '/animals',
    '/lariat', '/mafia'
]

# معلومات الألعاب
GAMES_INFO = {
    'truth': {
        'name_ar': 'صراحة',
        'name_en': 'Truth',
        'command': 'صراحة',
        'description': 'أسئلة صراحة ممتعة للتعارف والمرح',
        'how_to_play': [
            'استخدم الأمر "صراحة" في القروب',
            'سيظهر لك سؤال صراحة عشوائي',
            'أجب بصراحة وشارك إجابتك',
            'يمكن تكرار الأمر للحصول على أسئلة جديدة'
        ],
        'difficulty': 'سهل',
        'players': 'لاعب واحد أو أكثر',
        'type': 'social'
    },
    'dare': {
        'name_ar': 'جرأة',
        'name_en': 'Dare',
        'command': 'جرأة',
        'description': 'تحديات جريئة وممتعة للأصدقاء',
        'how_to_play': [
            'استخدم الأمر "جرأة" في القروب',
            'سيظهر لك تحدي جرأة عشوائي',
            'قم بتنفيذ التحدي إذا قبلت',
            'شارك صورة أو فيديو للتحدي إن أمكن'
        ],
        'difficulty': 'متوسط',
        'players': 'لاعب واحد أو أكثر',
        'type': 'social'
    },
    'wouldyourather': {
        'name_ar': 'لو خيروك',
        'name_en': 'Would You Rather',
        'command': 'لو خيروك',
        'description': 'اختيارات صعبة بين خيارين',
        'how_to_play': [
            'استخدم الأمر "لو خيروك" في القروب',
            'اختر بين الخيار الأول أو الثاني',
            'اضغط على الزر المناسب لاختيارك',
            'شاهد اختيارات الآخرين'
        ],
        'difficulty': 'سهل',
        'players': 'لاعب واحد أو أكثر',
        'type': 'social'
    },
    'question': {
        'name_ar': 'سؤال',
        'name_en': 'Question',
        'command': 'سؤال',
        'description': 'أسئلة ثقافية متنوعة',
        'how_to_play': [
            'استخدم الأمر "سؤال" في القروب',
            'اقرأ السؤال بعناية',
            'اختر الإجابة الصحيحة من الأزرار',
            'ستظهر النتيجة فوراً'
        ],
        'difficulty': 'متوسط',
        'players': 'لاعب واحد أو أكثر',
        'type': 'trivia'
    },
    'math': {
        'name_ar': 'رياضيات',
        'name_en': 'Math',
        'command': 'رياضيات',
        'description': 'تحديات رياضية لتنشيط العقل',
        'how_to_play': [
            'استخدم الأمر "رياضيات" في القروب',
            'احسب الناتج الصحيح',
            'أرسل الإجابة رقماً فقط',
            'الإجابة الصحيحة تحصل على نقاط'
        ],
        'difficulty': 'متوسط',
        'players': 'لاعب واحد أو أكثر',
        'type': 'puzzle'
    },
    'guess': {
        'name_ar': 'احزر',
        'name_en': 'Guess',
        'command': 'احزر',
        'description': 'احزر الرقم الصحيح من 1-100',
        'how_to_play': [
            'استخدم الأمر "احزر" لبدء اللعبة',
            'حاول تخمين الرقم بين 1 و 100',
            'ستحصل على تلميحات (أكبر/أصغر)',
            'أول من يحزر يفوز'
        ],
        'difficulty': 'سهل',
        'players': 'لاعب واحد أو أكثر',
        'type': 'puzzle'
    },
    'word': {
        'name_ar': 'كلمة',
        'name_en': 'Word',
        'command': 'كلمة',
        'description': 'رتب الحروف لتكوين كلمة صحيحة',
        'how_to_play': [
            'استخدم الأمر "كلمة" في القروب',
            'رتب الحروف المبعثرة',
            'أرسل الكلمة الصحيحة',
            'أول إجابة صحيحة تفوز'
        ],
        'difficulty': 'متوسط',
        'players': 'لاعب واحد أو أكثر',
        'type': 'word'
    },
    'reverse': {
        'name_ar': 'عكس',
        'name_en': 'Reverse',
        'command': 'عكس',
        'description': 'اكتب الكلمة بالعكس',
        'how_to_play': [
            'استخدم الأمر "عكس" في القروب',
            'اقرأ الكلمة المعكوسة',
            'أرسل الكلمة الأصلية الصحيحة',
            'السرعة والدقة مهمة'
        ],
        'difficulty': 'سهل',
        'players': 'لاعب واحد أو أكثر',
        'type': 'word'
    },
    'cities': {
        'name_ar': 'مدن',
        'name_en': 'Cities',
        'command': 'مدن',
        'description': 'اذكر مدينة تبدأ بالحرف المعطى',
        'how_to_play': [
            'استخدم الأمر "مدن" في القروب',
            'اقرأ الحرف المطلوب',
            'أرسل اسم مدينة تبدأ بهذا الحرف',
            'أول إجابة صحيحة تحصل على نقاط'
        ],
        'difficulty': 'متوسط',
        'players': 'لاعب واحد أو أكثر',
        'type': 'knowledge'
    },
    'countries': {
        'name_ar': 'دول',
        'name_en': 'Countries',
        'command': 'دول',
        'description': 'اذكر دولة تبدأ بالحرف المعطى',
        'how_to_play': [
            'استخدم الأمر "دول" في القروب',
            'اقرأ الحرف المطلوب',
            'أرسل اسم دولة تبدأ بهذا الحرف',
            'الإجابات الصحيحة تحصل على نقاط'
        ],
        'difficulty': 'سهل',
        'players': 'لاعب واحد أو أكثر',
        'type': 'knowledge'
    },
    'animals': {
        'name_ar': 'حيوانات',
        'name_en': 'Animals',
        'command': 'حيوانات',
        'description': 'اذكر حيوان يبدأ بالحرف المعطى',
        'how_to_play': [
            'استخدم الأمر "حيوانات" في القروب',
            'اقرأ الحرف المطلوب',
            'أرسل اسم حيوان يبدأ بهذا الحرف',
            'كن سريعاً للحصول على النقاط'
        ],
        'difficulty': 'سهل',
        'players': 'لاعب واحد أو أكثر',
        'type': 'knowledge'
    },
    'lariat': {
        'name_ar': 'لوريت',
        'name_en': 'Lariat',
        'command': 'لوريت',
        'description': 'لعبة الكلمات المتسلسلة - آخر حرف يكون أول حرف للكلمة التالية',
        'how_to_play': [
            'استخدم الأمر "لوريت" لبدء اللعبة',
            'سيعطيك البوت كلمة للبدء',
            'اكتب كلمة تبدأ بآخر حرف من الكلمة السابقة',
            'يجب أن تكون الكلمة صحيحة ولم تستخدم من قبل',
            'اللاعب الذي لا يجد كلمة يخسر'
        ],
        'difficulty': 'متوسط',
        'players': 'لاعبان أو أكثر',
        'type': 'word'
    },
    'mafia': {
        'name_ar': 'مافيا',
        'name_en': 'Mafia',
        'command': 'مافيا',
        'description': 'لعبة المافيا الشهيرة - اكتشف من هي المافيا قبل أن تقضي عليك',
        'how_to_play': [
            'يحتاج 5-10 لاعبين للبدء',
            'استخدم الأمر "مافيا" لبدء اللعبة',
            'سيتم توزيع الأدوار (مافيا، مواطنين، طبيب، محقق)',
            'في الليل: المافيا تختار ضحية، الطبيب ينقذ، المحقق يكشف',
            'في النهار: الجميع يصوت على من يشكون أنه مافيا',
            'المافيا تفوز إذا قضت على جميع المواطنين',
            'المواطنون يفوزون إذا اكتشفوا جميع المافيا'
        ],
        'difficulty': 'صعب',
        'players': '5-10 لاعبين',
        'type': 'strategy'
    }
}

# رسائل النظام
SYSTEM_MESSAGES = {
    'not_registered': 'يجب التسجيل أولاً. أرسل "تسجيل"',
    'group_only': 'هذا الأمر يعمل في القروبات فقط',
    'private_only': 'هذا الأمر يعمل في الخاص فقط',
    'game_active': 'يوجد لعبة نشطة حالياً. انتظر حتى تنتهي',
    'no_active_game': 'لا يوجد لعبة نشطة حالياً',
    'invalid_command': 'أمر غير صحيح. أرسل "القائمة" لعرض الأوامر'
}

# إعدادات الألعاب
GAME_SETTINGS = {
    'timeout': 60,  # ثانية
    'min_players_mafia': 5,
    'max_players_mafia': 10,
    'points_correct': 10,
    'points_wrong': -2,
    'points_win': 50
}
