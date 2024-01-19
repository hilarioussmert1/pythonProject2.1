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


forbidden_words = [
    'блин',
    'bad',
]


@register.filter
def hide_forbidden(value):
    words = value.split()
    bad_list = []
    for word in words:
        if word in forbidden_words:
            bad_list.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            bad_list.append(word)
    return " ".join(bad_list)
