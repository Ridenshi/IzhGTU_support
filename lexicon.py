LEXICON: dict[str, str] = {
    '/start': 'Здраствуйте!\nЧем я могу вам помочь?',
    '/help': 'WIP',
    'photo': 'WIP',
    'request': 'Введите запрос'
}
TOPICS: dict[str, dict[str, str]] = {
    'computer': {
        'software',
        'internet',
        'antivirus',
        'periphery',
        'breaking'
    },
    'printer':{
        'drivers',
        'breaking',
        'other'
    },
    'projector':{
        'diagnostic',
        'other'
    },
    'other':{'other'}
}