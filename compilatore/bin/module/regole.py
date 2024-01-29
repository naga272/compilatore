
import re


void_row = r"\s*\n?"
commento = r"\s*(\/\/.*)?\n?"


# caratteristiche file sorgente
name_file_sr = [
    r".+(\.sor)$"           # estensione nome file sorgente .sor
]


# caratteristiche delle variabili
syntax_var = [
    r"\s*\_*[A-Za-z]+(\w*\_*)*",                        # nome variabili
    r"\s*=\s*",                                         # assegnazione
    r"\"([^\"]*[.]*)*\"\s*\n*",                         # caso stringhe
    r"\s*\d+\s*([\-\*\+\/\%]\s*+\s*\d+\s*)*\s*\n*"      # caso numeri interi
]
