
def card_is_valid(num):
    digits = [int(c) for c in num if c.isdigit()]
    checksum = digits.pop()
    digits.reverse()
    doubled = [2*d for d in digits[0::2]]
    total  = 0
    for d in doubled:
        if d > 9:
            total += d-9
        else:
            total += d
    total += sum(digits[1::2])
    #total = sum(d-9 if d > 9 else d for d in doubled) + sum(digits[1::2])
    return (total * 9) % 10 == checksum

# valid: 49927398716
# invalid: 49927398717