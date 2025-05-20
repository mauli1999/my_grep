import sys
def check_token_match(char, token):
    if token == r"\d":
        return char.isdigit()
    
    elif token == r"\w":
        return char.isalnum() or char == "_"
    
    elif token.startswith('[^') and token.endswith(']'):
        excluded_chars = token[2:-1]
        return char not in excluded_chars
                            
    elif token.startswith('[') and token.endswith(']'):
        allowed_chars = token[1:-1]
        return char in allowed_chars
    
    else:
        return char == token

def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        if pattern == r"\d":
            return any(char.isdigit() for char in input_line)
        elif pattern == r"\w":
            return any(char.isalnum() or char == '_' for char in input_line)
        else:
            return pattern in input_line
    
    tokens = []
    i = 0
    anchored_start = False
    anchored_end = False
    if pattern.startswith('^'):
        anchored_start = True
        pattern = pattern[1:]
    if pattern.endswith('$'):
        anchored_end = True
        pattern = pattern[:-1]

    while i < len(pattern):
        if pattern[i] == '\\':
            tokens.append(pattern[i:i+2])
            i+=2
        elif pattern[i] == '[':
            end = pattern.find(']',i)
            if end == -1:
                raise RuntimeError("Unclosed character class")
            tokens.append(pattern[i:end+1])
            i =end+1
        elif pattern[i] == '+':
            if not tokens:
                raise RuntimeError("Nothing to repeat with '+'")
            tokens[-1] = (tokens[-1],'+')
            i+=1
        else:
            tokens.append(pattern[i])
            i+=1
    print("Tokens:", tokens, file=sys.stderr)


    if anchored_start and anchored_end :
        if len(input_line)!= len(tokens):
            return False
        for i,token in enumerate(tokens):
            if not check_token_match(input_line[i],token):
                return False
        return True
        
    elif anchored_start:
        if len(input_line) < len(tokens):
            return False
        

        matched = True
        for i,token in enumerate(tokens):
            if not check_token_match(input_line[i],token):
                matched = False
                break
        
        return matched
    
    elif anchored_end:
        start= len(input_line) - len(tokens)
        
        if start < 0:
            return False

        matched = True
        for i,token in enumerate(tokens):
            if not check_token_match(input_line[start+i],token):
                matched = False
                break
        
        return matched
    
    else:
        for start in range(len(input_line)-len(tokens)+1):
            matched = True
            input_index = start
            token_index = 0

            while token_index < len(tokens):
                token = tokens[token_index]

                if isinstance(token,tuple) and token[1]=='+':
                    subtoken = token[0]
                    
                    if input_index >= len(input_line) or not check_token_match(input_line[input_index],subtoken):
                        matched = False
                        break
                    
                    while input_index < len(input_line) and check_token_match(input_line[input_index],subtoken):
                        input_index+=1
                    token_index+=1

                else:
                    if input_index >= len(input_line) or not check_token_match(input_line[input_index],token):
                        matched = False
                        break
                    input_index+=1
                    token_index+=1

            if token_index == len(tokens):
                return True
        return False
    
def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    print("Logs from your program will appear here!", file=sys.stderr)

    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()