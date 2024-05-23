# TPC6: GIC

- Autor: Francisco Macedo Ferreira - A100660

## Descrição do Problema

Pretende-se que se desenvolva uma GIC simples para o seguinte exemplo:

```
?a
b = a*2 / (27-3)
!a+b
c = a*b / (a/b)
```

## Solução

```
T =  {'?', '!', '=', '+', '-', '*', '/', '(', ')', id, num}
N = {S, Exp1, Exp2, Exp3, Op1, Op2}
S = S
P = {
    S -> '?' id               Lookahead = {'?'}
      | '!' Exp1              Lookahead = {'!'}
      | id '=' Exp1           Lookahead = {id}
    Exp1 -> Exp2 Op1          Lookahead = {'(', num, id}
    Op1 -> '+' Exp1           Lookahead = {'+'}
        | '-' Exp1            Lookahead = {'-'}
        | &                   Lookahead = {')', &}
    Exp2 -> Exp3 Op2          Lookahead = {'(', num, id}
    Op2 -> '*' Exp2           Lookahead = {'*'}
        | '/' Exp2            Lookahead = {'/'}
        | &                   Lookahead = {'+', '-', ')', &}
    Exp3 -> '(' Exp1 ')'      Lookahead = {'('}
        | num                 Lookahead = {num}
        | id                  Lookahead = {id}
}
```
