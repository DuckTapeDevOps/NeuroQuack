def sanitize_text(text, max_length):
    text = text.lstrip()
    if len(text) > max_length:
        text = text[:max_length] + ".."
    return text