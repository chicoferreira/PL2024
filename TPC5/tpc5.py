from dataclasses import dataclass
from datetime import datetime

from tabulate import tabulate
import ply.lex as lex
import json


@dataclass
class Produto:
    cod: str
    nome: str
    quant: int
    preco: float


def prettify_saldo(saldo):
    integer_part = int(saldo)
    decimal_part = int(round((saldo - integer_part) * 100))
    if decimal_part == 0:
        return f"{integer_part}e"
    if integer_part == 0:
        return f"{decimal_part:02d}c"
    return f"{integer_part}e{decimal_part:02d}c"


coins = [2.00, 1.00, .50, .20, .10, .05, .02, .01]


def calculate_saldo_in_coins(saldo) -> list[int]:
    result = []
    for coin in coins:
        result.append(int(saldo // coin))
        saldo %= coin
    return result


class MaquinaVendas:
    tokens = (
        'LISTAR',
        'SALDO',
        'SAIR',
        'MOEDA_VALOR',
        'PRODUTO_COD',
    )

    states = (
        ('inserirmoeda', 'exclusive'),
        ('selecionarproduto', 'exclusive'),
    )

    t_ANY_ignore = ' \t\n'
    t_inserirmoeda_ignore = ', \t\n'

    def __init__(self):
        self.lexer = None
        self.exit = False
        self.saldo = 0.0
        self.stock = []
        self.load_stock()
        date = datetime.now().strftime("%Y-%m-%d")
        self.out(f"{date}, Stock carregado, Estado atualizado.")
        self.out("Bom dia. Estou disponível para atender o seu pedido.")

    def load_stock(self):
        with open("db.json", encoding="utf8") as f:
            self.stock = [Produto(**p) for p in json.load(f)]

    def save_stock(self):
        with open("db.json", "w", encoding="utf8") as f:
            json.dump([p.__dict__ for p in self.stock], f, ensure_ascii=False, indent=4)

    def t_begin_inserirmoeda(self, t):
        r'MOEDA'
        t.lexer.begin('inserirmoeda')

    def t_inserirmoeda_MOEDA_VALOR(self, t):
        r'2e|1e|50c|20c|10c|5c|2c|1c'
        if t.value[-1] == 'c':
            t.value = int(t.value[:-1]) / 100
        elif t.value[-1] == 'e':
            t.value = int(t.value[:-1])

        self.saldo += t.value

        return t

    def t_inserirmoeda_exit(self, t):
        r'\.'
        self.print_saldo()
        t.lexer.begin('INITIAL')

    def t_begin_selecionarproduto(self, t):
        r'SELECIONAR'
        t.lexer.begin('selecionarproduto')

    def t_selecionarproduto_PRODUTO_COD(self, t):
        r'[A-Z][0-9]{2}'
        t.lexer.begin('INITIAL')
        for produto in self.stock:
            if produto.cod == t.value:
                if produto.quant <= 0:
                    self.out(f"Produto {produto.nome} esgotado")
                    return t
                if produto.preco > self.saldo:
                    self.out(
                        f"Saldo insuficiente para \"{produto.nome}\" (necessita de {prettify_saldo(produto.preco)})")
                    self.print_saldo()
                    return t

                self.saldo -= produto.preco
                produto.quant -= 1
                self.out(f"Pode retirar o produto dispensado \"{produto.nome}\"")
                self.print_saldo()
                return t
        self.out("Produto inexistente")
        return t

    def t_ANY_error(self, t):
        print("Caractere ilegal '%s'" % t.value[0])
        t.lexer.skip(1)

    def t_LISTAR(self, t):
        r'LISTAR'
        self.out("")
        print(tabulate([[p.cod, p.nome, p.quant, p.preco] for p in self.stock],
                       headers=["Código", "Nome", "Quantidade", "Preço"]))
        return t

    def t_SALDO(self, t):
        r'SALDO'

        self.print_saldo()
        return t

    def print_saldo(self):
        self.out(f"Saldo =", prettify_saldo(self.saldo))

    def t_SAIR(self, t):
        r'SAIR'
        self.exit = True

        trocos = [f"{n}x {prettify_saldo(coins[i])}" for i, n in enumerate(calculate_saldo_in_coins(self.saldo)) if
                  n > 0]
        if len(trocos) > 0:
            self.out("Pode retirar o troco: " + ", ".join(trocos))
        self.out("Até à próxima")
        self.save_stock()
        return t

    def build(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()

    def out(self, *content):
        print("maq:", *content)


def main():
    maquina = MaquinaVendas()
    maquina.build()

    while not maquina.exit:
        data = input(">> ")
        maquina.input(data)

        while True:
            tok = maquina.token()
            if not tok:
                break


if __name__ == '__main__':
    main()
