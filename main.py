import tkinter as tk
from tkinter import ttk, messagebox


class AutomatoPilha:
    def __init__(self, estados, alfabeto, alfabeto_pilha, transicoes, estado_inicial, estados_finais, simbolo_inicial_pilha):
        self.estados = estados
        self.alfabeto = alfabeto
        self.alfabeto_pilha = alfabeto_pilha
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais
        self.simbolo_inicial_pilha = simbolo_inicial_pilha

    def processar_cadeia(self, cadeia):
        estado_atual = self.estado_inicial
        pilha = [self.simbolo_inicial_pilha]

        for simbolo in list(cadeia) + [""]:
            topo_pilha = pilha[-1] if pilha else None
            transicao = (
                self.transicoes.get((estado_atual, simbolo, topo_pilha))
                or self.transicoes.get((estado_atual, "", topo_pilha))
            )

            if not transicao:
                return "Cadeia rejeitada"

            prox_estado, acao_pilha = transicao
            estado_atual = prox_estado

            if pilha and topo_pilha:
                pilha.pop()

            if acao_pilha != "":
                pilha.extend(reversed(acao_pilha))

        return "Cadeia aceita" if estado_atual in self.estados_finais and (not pilha or pilha == ["Z"]) else "Cadeia rejeitada"


def criar_automato():
    try:
        estados = entry_estados.get().split(",")
        alfabeto = entry_alfabeto.get().split(",")
        alfabeto_pilha = entry_alfabeto_pilha.get().split(",")
        estado_inicial = entry_estado_inicial.get()
        estados_finais = entry_estados_finais.get().split(",")
        simbolo_inicial_pilha = entry_simbolo_inicial_pilha.get()

        transicoes_raw = text_transicoes.get("1.0", tk.END).strip().split("\n")
        transicoes = {}

        for transicao in transicoes_raw:
            origem, simbolo, topo, destino, acao_pilha = map(str.strip, transicao.split(","))
            transicoes[(origem, simbolo, topo)] = (destino, acao_pilha)

        global automato
        automato = AutomatoPilha(estados, alfabeto, alfabeto_pilha, transicoes, estado_inicial, estados_finais, simbolo_inicial_pilha)

        messagebox.showinfo("Sucesso", "Autômato a Pilha configurado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao configurar o automato: {e}")


def processar_cadeia():
    try:
        cadeia = entry_cadeia.get()
        resultado = automato.processar_cadeia(cadeia)
        messagebox.showinfo("Resultado", resultado)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar a cadeia: {e}")


root = tk.Tk()
root.title("Simulador de Autômato a Pilha")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_estados = ttk.Label(frame, text="Estados (separados por vírgula):")
label_estados.grid(row=0, column=0, sticky=tk.W)
entry_estados = ttk.Entry(frame, width=30)
entry_estados.grid(row=0, column=1, sticky=tk.W)

label_alfabeto = ttk.Label(frame, text="Alfabeto (separado por vírgula):")
label_alfabeto.grid(row=1, column=0, sticky=tk.W)
entry_alfabeto = ttk.Entry(frame, width=30)
entry_alfabeto.grid(row=1, column=1, sticky=tk.W)

label_alfabeto_pilha = ttk.Label(frame, text="Alfabeto da pilha (separado por vírgula):")
label_alfabeto_pilha.grid(row=2, column=0, sticky=tk.W)
entry_alfabeto_pilha = ttk.Entry(frame, width=30)
entry_alfabeto_pilha.grid(row=2, column=1, sticky=tk.W)

label_estado_inicial = ttk.Label(frame, text="Estado inicial:")
label_estado_inicial.grid(row=3, column=0, sticky=tk.W)
entry_estado_inicial = ttk.Entry(frame, width=30)
entry_estado_inicial.grid(row=3, column=1, sticky=tk.W)

label_estados_finais = ttk.Label(frame, text="Estados finais (separados por vírgula):")
label_estados_finais.grid(row=4, column=0, sticky=tk.W)
entry_estados_finais = ttk.Entry(frame, width=30)
entry_estados_finais.grid(row=4, column=1, sticky=tk.W)

label_simbolo_inicial_pilha = ttk.Label(frame, text="Símbolo inicial da pilha:")
label_simbolo_inicial_pilha.grid(row=5, column=0, sticky=tk.W)
entry_simbolo_inicial_pilha = ttk.Entry(frame, width=30)
entry_simbolo_inicial_pilha.grid(row=5, column=1, sticky=tk.W)

label_transicoes = ttk.Label(frame, text="Transições (origem,símbolo,topo,destino,ação_pilha):")
label_transicoes.grid(row=6, column=0, sticky=tk.W)
text_transicoes = tk.Text(frame, height=5, width=40)
text_transicoes.grid(row=6, column=1, sticky=tk.W)

button_criar = ttk.Button(frame, text="Criar Autômato", command=criar_automato)
button_criar.grid(row=7, column=0, columnspan=2)

label_cadeia = ttk.Label(frame, text="Cadeia a ser processada:")
label_cadeia.grid(row=8, column=0, sticky=tk.W)
entry_cadeia = ttk.Entry(frame, width=30)
entry_cadeia.grid(row=8, column=1, sticky=tk.W)

button_processar = ttk.Button(frame, text="Processar Cadeia", command=processar_cadeia)
button_processar.grid(row=9, column=0, columnspan=2)

root.mainloop()
