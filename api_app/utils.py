
def card_is_valid(num):
    try: # make all as integers
        digits = [int(c) for c in num]
    except ValueError: # if not digit
        return False 
    checksum = digits.pop()
    digits.reverse()
    double = [2*d for d in digits[0::2]]
    total  = 0
    for d in double:
        if d > 9:
            total += d-9
        else:
            total += d
    total += sum(digits[1::2])
    if (total * 9) % 10 == checksum:
        return True
    else:
        return False

# example:
# valid: 49927398716
# invalid: 49927398717
