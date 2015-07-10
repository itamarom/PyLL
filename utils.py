def find_closing(text, start, open='(', close=')'):
    assert(text[start] == open)
    count = 1
    current = start + 1
    while count:
        if text[current] == open:
            count += 1
        elif text[current] == close:
            count -= 1
            
        current += 1
        
    return current
        