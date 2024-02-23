import fileinput
import re

stdin = "\n".join(fileinput.input())

symbols_regex = r'(on|off|=|\d+)'
symbols = re.findall(symbols_regex, stdin, flags=re.IGNORECASE)

state = True
current = 0

for symbol in symbols:
    if symbol.lower() == 'on':
        state = True
    elif symbol.lower() == 'off':
        state = False
    elif symbol.isdigit() and state:
        current += int(symbol)
    elif symbol == '=':
        print(f'Soma: {current}')
