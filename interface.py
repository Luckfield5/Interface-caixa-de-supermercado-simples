import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from logica import carregar, salvar, calcular_total, SENHA_ADMIN

class Caixa(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Caixa de Supermercado")
        self.produtos = carregar()
        self.subtotal = 0.0

        topo = ttk.Frame(self, padding=10)
        topo.pack(fill="x")
        self.combo = ttk.Combobox(topo, values=sorted(self.produtos), state="readonly")
        self.combo.pack(side="left", padx=5)
        self.qtd = ttk.Spinbox(topo, from_=1, to=999, width=5)
        self.qtd.set(1)
        self.qtd.pack(side="left", padx=5)
        ttk.Button(topo, text="Adicionar item", command=self.adicionar_item).pack(side="left")
        
        self.tabela = ttk.Treeview(self, columns=("produto", "qtd", "valor"),
                                   show="headings", height=10)
        for col, titulo in (("produto", "Produto"), ("qtd", "Qtd"), ("valor", "Valor")):
            self.tabela.heading(col, text=titulo)
        self.tabela.pack(fill="both", expand=True, padx=10)
        
        self.lbl_total = ttk.Label(self, text="Subtotal: R$ 0.00", font=("Arial", 16, "bold"))
        self.lbl_total.pack(pady=10)

        ttk.Button(self, text="Finalizar compra", command=self.finalizar).pack(pady=2)
        ttk.Button(self, text="Cadastrar novo produto (Admin)", command=self.cadastrar).pack(pady=2)
    def adicionar_item(self):
        nome = self.combo.get()
        if not nome:
            messagebox.showwarning("Aviso", "Escolha um produto.")
            return
        try:
            qtd = int(self.qtd.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade Inválida!.")
            return
        valor = self.produtos[nome] * qtd
        self.subtotal += valor
        self.tabela.insert("", "end", values=(nome, qtd, f"R$ {valor:.2f}"))
        self.lbl_total.config(text=f"Subtotal: R$ {self.subtotal:.2f}")

    def finalizar(self):
        desconto, total = calcular_total(self.subtotal)
        messagebox.showinfo("Compra",
                             f"Subtotal: R$ {self.subtotal:.2f}\n"
                             f"Desconto: R$ {desconto:.2f}\n"
                             f"Total: R$ {total:.2f}")
        self.tabela.delete(*self.tabela.get_children())
        self.subtotal = 0.0
        self.lbl_total.config(text="Subtotal: R$ 0.00")
    
    def cadastrar(self):
        if simpledialog.askstring("Admin", "Senha:", show="*") != SENHA_ADMIN:
           messagebox.showerror("Erro", "Senha incorreta.")
           return
        nome = simpledialog.askstring("Produto", "Nome do produto:")
        preco = simpledialog.askstring("Produto", "Preço:")
        try:
            self.produtos[nome.strip().lower()] = float(preco.replace("," , "."))
        except (ValueError, AttributeError):
            messagebox.showerror( "Erro", "Dados inválidos.")
            return
        salvar(self.produtos)
        self.combo["values"] = sorted(self.produtos)

if __name__ == "__main__":
    Caixa().mainloop()
