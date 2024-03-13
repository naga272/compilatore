
import platform
import sys
import re


def stampa(row, n_row) -> str:
    parametri = re.sub(r"\s*print\s+", "", row)
    parametri = parametri.split(",") 
    return f"call print"