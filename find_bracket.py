with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

start_index = text.find('child: SelectionArea(child: CustomScrollView(')
if start_index == -1:
    print('Not found')
else:
    open_count = 0
    in_string = False
    string_char = ''
    escape = False
    end_idx = -1
    for i in range(start_index, len(text)):
        char = text[i]
        if escape:
            escape = False
            continue
        if char == '\\':
            escape = True
            continue
            
        if char in ('"', "'"):
            if not in_string:
                in_string = True
                string_char = char
            elif string_char == char:
                in_string = False
                
        if not in_string:
            if char == '(':
                open_count += 1
            elif char == ')':
                open_count -= 1
                if open_count == 1:
                    end_idx = i
                    break
    
    if end_idx != -1:
        print(f"Index: {end_idx}")
        print("Surrounding text:")
        print(text[end_idx-100:end_idx+100])
