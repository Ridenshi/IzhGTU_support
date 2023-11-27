LEXICON: dict[str, str] = {
    '/start': 'Здраствуйте!\nЧем я могу вам помочь?',
    '/help': 'WIP',
    '/exit': 'Вы вышли из сессии',
    'request': 'Введите запрос'
}
TOPICS = {
    'Компьютер', 'Принтер', 'Проектор', 'Другое'
}
DOWN_TOPICS = {
    'Компьютер': {
        'software',
        'internet',
        'antivirus',
        'periphery',
        'breaking'
    },
    'Принтер': {
        'drivers',
        'breaking',
        'other'
    },
    'Проектор': {
        'diagnostic',
        'other'
    },
    'Другое': {'other'}
}
