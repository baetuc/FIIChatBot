"""
    Autori: Cip Baetu, Sebastian Ciobanu
"""

from textblob import TextBlob


def correct(phrase):
    return str(TextBlob(phrase).correct())
