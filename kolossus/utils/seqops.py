
# s is string, i is index for substitution
# w is width (assume odd window), pad is padding character 
# assume odd w 
def extract_window(s, i, w, pad):
    nchars = w // 2
    prefix = [None for _ in range(nchars)]
    suffix = [None for _ in range(nchars)]
    for j in range(nchars):
        # handle prefix 
        if i - j - 1 < 0:
            prefix[-j - 1] = pad
        else:
            prefix[-j - 1] = s[i - j - 1]

        # handle suffix 
        if i + j + 1 >= len(s):
            suffix[j] = pad
        else:
            suffix[j] = s[i + j + 1]

    return ''.join(prefix + [s[i]] + suffix)
            

def chop(s, n):
    i = 0
    out = []
    while i < len(s):
        out.append(s[i:i+n])
        i += n
    return out
