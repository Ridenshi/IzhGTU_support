LEXICON: dict[str, str] = {
    '/start': 'Здраствуйте!\nЧем я могу вам помочь?',
    '/help': 'WIP',
    '/exit': 'Вы вышли из сессии',
    'request': 'Введите запрос'
}
TOPICS: dict[str, dict[str, str]] = {
    'Компьютер': {
        'software',
        'internet',
        'antivirus',
        'periphery',
        'breaking'
    },
    'Принтер':{
        'drivers',
        'breaking',
        'other'
    },
    'Проектор':{
        'diagnostic',
        'other'
    },
    'Другое':{'other'}
}