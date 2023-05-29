import re

def solution(msg):
    """Decrypts encrypted message.
    
    Decrypts messages encrypted using a modified Atbash cipher where
    every lowercase letter [a..z] is replaced with the corresponding
    one in [z..a], while every other character (including uppercase
    letters and punctuation) is left untouched.

    Examples:

    >>> print solution("vmxibkgrlm")
    encryption
    >>> print solution("wrw blf hvv ozhg mrtsg'h vkrhlwv?")
    did you see last night's episode?
    >>> print solution("Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!")
    Yeah! I can't believe Lance lost his job at the colony!!
    """

    # "Map" lowercase ASCII letters a-z to integer values 1-26.
    # This allows for the use of a simpler math function than
    # if a-z were mapped to 0-25.
    base_value = ord('a') - 1

    decrypted = []
    for c in msg:
        if re.match('^[a-z]$', c):
            x = ord(c) - base_value
            d_c = chr((-x % 26) + (base_value + 1))
            decrypted.append(d_c)
        else:
            decrypted.append(c)
    return ''.join(decrypted)

import doctest
doctest.testmod()