def alternate_case(text):
    cased_characters = []
    for idx, ch in enumerate(text):
        if idx % 2 == 0:
            cased_characters.append(ch.upper())
        else:
            cased_characters.append(ch)
    return "".join(cased_characters)
