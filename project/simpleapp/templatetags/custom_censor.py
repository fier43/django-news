from django import template

# {% load custom_censor %}

register = template.Library()


@register.filter()
def censor(value):
    mat = ["банан", "помидор"]

    save_value = []

    words = value.split(' ')

    for word in words:
        a_word = word.lower()
        if a_word in mat:
            lene = len(word)
            wor = []
            for x in word[: -(lene - 1)]:
                wor.append(x)

            for a in range(lene - 1):
                wor.append("*")

            wor =  ''.join(wor)
            save_value.append(wor)

        else:
            save_value.append(word)

    save_value = ' '.join(save_value)
    return save_value
