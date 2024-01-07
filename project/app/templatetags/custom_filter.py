from django import template

register = template.Library()

CURRENCY_SYMBOLS = {
    'rub': '₽',
    'usd': '$',
}


@register.filter()
def currency(value, code='rub'):
    postfix = CURRENCY_SYMBOLS[code]

    return f'{value} {postfix}'


bad_words = [
    'плохо',
]


@register.filter()
def censor(value):
    for i in bad_words:
        value = value.lower().replace(i.lower(), '***')
    return f'{value}'
