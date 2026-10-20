import json
import os

ARQUIVO = "produtos.json"
SENHA_ADMIN = "061023"  # use a mesma senha do seu código original


def carregar():
    if not os.path.exists(ARQUIVO):
        return {}
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar(produtos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=4)


def calcular_total(subtotal):
    desconto = subtotal * 0.10 if subtotal >= 100 else 0
    return desconto, subtotal - desconto