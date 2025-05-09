
import sys 


def main():
    s = "aagctt"

    print(s)
    print('chop by 1:', chop(s, 1))
    print('chop by 2:', chop(s, 2))
    print('chop by 3:', chop(s, 3))
    print('chop by 4:', chop(s, 4))

    subs_valid = [('a', 'b', 0), ('g', 'b', 2)] 
    print("applying valid subs!")
    print(apply_subs(s, subs_valid))

    subs_invalid = [('a', 'b', 0), ('c', 'b', 2)]
    print("applying invalid subs!")
    try:
        print(apply_subs(s, subs_invalid))
        print("This isn't good, should've thrown an assertion error")
        sys.exit(1)
    except AssertionError as e:
        print("Good, raised assertion error!")

    


def chop(s, n):
    i = 0
    out = []
    while i < len(s):
        out.append(s[i:i+n])
        i += n
    return out


def apply_subs(s, subs, zero_based=True):
    """
    Apply substitution mutations to a string. 

    Input:
        - s (str or Bio.Seq.Seq object): sequence to which we apply mutations. 
        - subs [list[tuple]]: each tuple is 3-tuple: (from, to, position)
    """
    # positions to which to apply mutation
    if zero_based:
        submap = {t[2]: (t[0], t[1]) for t in subs}
    else:
        submap = {t[2]-1: (t[0], t[1]) for t in subs}

    # output variable 
    out = []

    # remember to add a try-catch for invalid subs 
    for i, c in enumerate(s):
        a, b = submap.get(i, (c, c))
        assert s[i] == a
        out.append(b)

    return ''.join(out)


if __name__ == '__main__': 
    main()
