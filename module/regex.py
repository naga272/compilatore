import re


memory_register = {
    # ha il compito di ricordarsi il nome della variabili, il loro valore e la posizione nello stack, 
    # così durante la fase di compilazione posso eseguie gia alcuni calcoli basilari
    # chiave : [value, stack_position]
}

commento_re             = r"\s*\/\/\s*.*\n?"
var_name                = r"\s*\_*[A-Za-z]+(\_*\w*)*\s*"
assegnamento            = r"\s*\_*[A-Za-z]+(\w*)\s*\=\s.+"
espressione_matematica  = r"\s*\d+\s*([\-\*\+\/\%]\s*\d+\s*)*\s*\n*"
stringa                 = r"\s*\"(.*\s*)*\"\s*\n*"


# %define <var_name> <value> <commento_opzionale>
costanti    = r"\%define\s*" + var_name + "(\d+)" + "(\s*\/\/.*)*\n*" # per ora accettano solo int

fast_add    = var_name + "\s*\+\=\s*.+\n*"
fast_sub    = var_name + "\s*\-\=\s*.+\n*"


# if (condition)
#   statement
# else do
#   statement
# endif

if_re       = r"\s*if\s*\(.+\)\s*\n"
else_do     = r"\s*else\s+do\s*\n"
endif       = r"\s*endif\s*\n*"
