# TPC5 - Máquina de Vending

- Autor: Francisco Macedo Ferreira - A100660

## Descrição do problema

Pretende-se um programa que simule o funcionamento de uma máquina de vending.

A seguir apresenta-se um exemplo de uma interação com a máquina, resultado da execução do código:

```
maq: 2024-03-20, Stock carregado, Estado atualizado.
maq: Bom dia. Estou disponível para atender o seu pedido.
>> LISTAR
maq: 
Código    Nome         Quantidade    Preço
--------  ---------  ------------  -------
A23       água 0.5L             8      0.7
>> MOEDA 1e, 20c, 5c, 5c .
maq: Saldo = 1e30c
>> SELECIONAR A23
maq: Pode retirar o produto dispensado "água 0.5L"
maq: Saldo = 60c
>> LISTAR
maq: 
Código    Nome         Quantidade    Preço
--------  ---------  ------------  -------
A23       água 0.5L             7      0.7
>> SELECIONAR A23
maq: Saldo insuficiente para "água 0.5L" (necessita de 70c)
maq: Saldo = 60c
>> SAIR
maq: Pode retirar o troco: 1x 50c, 1x 10c
maq: Até à próxima
```

O estado da máquina é guardado num ficheiro de texto [db.json](./db.json), que é carregado no início da execução do
programa e atualizado no final da execução do programa.