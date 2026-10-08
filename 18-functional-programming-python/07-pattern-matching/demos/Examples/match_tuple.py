def match_tuple(t):
    if t[0] == 42:
        #don't care what t[1] is
        ...
    elif t == (1,2):
        # both elements match
        ...
    elif t[1] == 43:
        # don't care what t[0] is
        ...
