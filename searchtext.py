import string

alpho_dict = {}

for i in range(26):
    alpho_dict[string.ascii_letters[i]] = string.ascii_letters[i + 26]
for i in range(26, 52):
    alpho_dict[string.ascii_letters[i]] = string.ascii_letters[i - 26]


def search_pattern(pattern, text, case_sensitive=False):
    texts = []
    pat, start = 0, 0
    should_search = False
    for index, letter in enumerate(text):
        if should_search:
            try:
                if case_sensitive:
                    if letter != pattern[pat]:
                        should_search = False
                        pat = 0
                        start = 0
                    else:
                        if pat == len(pattern) - 1:
                            texts.append([pattern, start, index+1])
                            should_search = False
                            pat = 0
                            start = 0
                            continue
                        else:
                            pat += 1
                            continue
                elif not case_sensitive:
                    if letter != pattern[pat] and (alpho_dict[letter] != pattern[pat]):
                        should_search = False
                        pat = 0
                        start = 0
                    else:
                        if pat == len(pattern) - 1:
                            texts.append([pattern, start, index+1])
                            should_search = False
                            pat = 0
                            start = 0
                            continue
                        else:
                            pat += 1
                            continue
            except:
                should_search = False
                pat = 0
                start = 0
        
        if not case_sensitive:
            if letter == pattern[pat] or alpho_dict.get(letter) == pattern[pat]:
                should_search = True
                start = index
                if pat == len(pattern) - 1:
                    texts.append([pattern, start, index+1])
                    should_search = False
                    pat = 0
                    start = 0
                else:
                    pat += 1
        elif case_sensitive:
            if letter == pattern[pat] or alpho_dict.get(letter):
                should_search = True
                start = index
                if pat == len(pattern) - 1:
                    texts.append([pattern, start, index+1])
                    should_search = False
                    pat = 0
                    start = 0
                else: pat += 1

    return texts

if __name__ == "__main__":
    with open('test.txt', 'r') as f:
        lines = f.readlines()

    for i in lines:
        print(search_pattern('zzz', i), i)