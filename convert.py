from string import *
#definitivamente no sacado de stackoverflow
def int_to_base(n, N):
    """ Return base N representation for int n. """
    base_n_digits = digits + ascii_lowercase + ascii_uppercase
    result = ""
    if n < 0:
        sign = "-"
        n = -n
    else:
        sign = ""
    while n > 0:
        q, r = divmod(n, N)
        result += base_n_digits[r]
        n = q
    if result == "":
        result = "0"
    return sign + "".join(reversed(result))