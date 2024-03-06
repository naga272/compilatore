# Compiler with python
![Language](https://img.shields.io/badge/Spellcheck-Pass-green?style=flat) 
![Platform](https://img.shields.io/badge/OS%20platform%20supported-Linux-green?style=flat)
![Platform](https://img.shields.io/badge/OS%20platform%20-Linux-green?style=flat) 
![Language](https://img.shields.io/badge/Language-Python-yellowgreen?style=flat)  
![Language](https://img.shields.io/badge/Language-asm-blue?style=flat)
![Testing](https://img.shields.io/badge/PEP8%20CheckOnline-Passing-green) 
![Testing](https://img.shields.io/badge/Test-Pass-green)

## Descrizione
Programma che dato un file sorgente (.volt) con una determinata sintassi consente di tradurlo
in linguaggio macchina (codice nasm x64), poi compila il file asm generato e lo linka, generando l'eseguibile 

Istruzioni consentite all'interno del programma .volt:

- dichiarazioni variabili di tipo stringa e interi
// sono un commento opzionale
a = 12 + 25 * 89 / 100   // sono un commento opzionale
b = "Stringa"            // sono un commento opzionale

- dichiarazioni costanti di tipo intero:
%define costante 125

- incrementa velocemente una variabile:
a += 25 - 12             //sono un commento opzionale


## Requisiti
- python versione 3.11 o maggiore
- compilatore nasm (for download: sudo apt install nasm)
- linker ld (for download: sudo apt install ld)
- sistema operativo Unix-Like (cpu x64)

## Esecuzione
da shell scrivendo:
python3 compiler.py sorgente.volt eseguibile x64

oppure si puo fare da file bash

## Tags
nasm ld re compiler fullmatch try except with re
