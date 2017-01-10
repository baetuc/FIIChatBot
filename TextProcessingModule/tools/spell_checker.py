"""
    Autori: Cip Baetu, Sebastian Ciobanu
"""

from autocorrect import spell


def correct(phrase):
    return str(spell(phrase))
