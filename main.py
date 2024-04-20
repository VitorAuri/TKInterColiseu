import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import json
from PIL import Image, ImageTk
import requests

# Instanciando Janela
window = tk.Tk()
window.geometry("1240x600")
window.title("Coliseu de Clãs - Editor de Jogadores")
url = "https://api.npoint.io/73701443fb9f9a913c0b"

lendas = ["desconhecido","bodvar", "cassidy", "orion", "lord vraxx", "gnash", "queen nai", "hattori", "sir roland", "scarlet", "thatch", "ada", "sentinel", "lucien", "teros", "brynn", "asuri", "barraza", "ember", "azoth", "koji", "ulgrim", "diana", "jhala", "kor", "wu shang", "val", "ragnir", "cross", "mirage", "nix", "mordex", "yumiko", "artemis", "caspian", "sidra", "xull", "kaya", "isaiah", "jiro", "lin fei", "zariel", "rayman", "dusk", "fait", "thor", "petra", "vector", "volkov", "onyx", "jaeyun", "mako", "magyar", "reno", "munin", "arcadia", "ezio", "tezca", "thea", "red raptor", "loki", "seven", "vivi"]
clans = ["Bichos do Mato","Vasco","Inimigos da Moda","Firebirds","Complexo do Corinthians","Strawberry Tea","Aurora","Cruzeiro","Ranked Beasts","Patota da Moneymatch"]

# Carregar a imagem original
ImagemColiseu = Image.open("logo.png")
tamanho_desejado = (500, 500)
ImagemRedimensionada = ImagemColiseu.resize(tamanho_desejado)
ImagemTK =  ImageTk.PhotoImage(ImagemRedimensionada)
ImagemRenderizada = tk.Label(image=ImagemTK,background="#1C1C1C")
ImagemRenderizada.place(x=560,y=-120)

count = 0

with open("lista.json", "r") as file:
    data = json.load(file)
    jogadores = data["jogadores"]


def reiniciarPrograma():
    python = sys.executable
    os.execl(python, python, * sys.argv)
    
def obterListaAtualizada():
    response = requests.get(url)
    if response.status_code == 200:
        with open("lista.json", "w") as file:
            data = response.json()
            json.dump(data, file, indent=4)
    else:
        print("Falha ao obter lista de jogadores, código de erro:", response.status_code)

    listaJogadores.delete(*listaJogadores.get_children())
    mostrarJogadores(data["jogadores"])

def confirmarAtualizacao():
    confirmacao = messagebox.askyesno("Confirmação", "Deseja realmente obter a lista atualizada de jogadores?\n\nA lista salva em seu computador será sobrescrita pela a que está hospedada, significando que você pode perder alterações feitas.\n\n(O programa será reiniciado)")
    if confirmacao:
        obterListaAtualizada()
        reiniciarPrograma()

def adicionarJogador():
    nome = nomeJogador.get()
    hierarquia = hierarquiaJogador.get()
    clan = clansJogador.get()
    custo = int(custoJogador.get())
    lenda = lendaJogador.get()

    data["jogadores"].append({
        "nome": nome,
        "hierarquia": hierarquia,
        "custo": custo,
        "clan": clan,
        "lenda": lenda
    })

    with open("lista.json", "w") as file:
        json.dump(data, file, indent=4)

    listaJogadores.delete(*listaJogadores.get_children())
    mostrarJogadores(data["jogadores"])

def removerJogador():
    jogadorParaApagar = listaJogadores.selection()
    if jogadorParaApagar:
        indice = listaJogadores.index(jogadorParaApagar)
        del data["jogadores"][indice]

        with open("lista.json", "w") as file:
            json.dump(data, file, indent=4)

        listaJogadores.delete(*listaJogadores.get_children())
        mostrarJogadores(data["jogadores"])

def editarJogador():
    jogadorSelecionado = listaJogadores.selection()
    if jogadorSelecionado:
        indice = listaJogadores.index(jogadorSelecionado)
        jogador = data["jogadores"][indice]

        popup = tk.Toplevel(window)
        popup.title("Editar Jogador")
        popup.geometry("300x200")

        tk.Label(popup, text="Nome do Jogador:").grid(row=0, column=0, padx=5, pady=5)
        nome_edit = tk.Entry(popup)
        nome_edit.insert(tk.END, jogador["nome"])
        nome_edit.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(popup, text="Hierarquia:").grid(row=1, column=0, padx=5, pady=5)
        hierarquia_edit = ttk.Combobox(popup, values=["Lider", "Co-Lider", "Membro"])
        hierarquia_edit.set(jogador["hierarquia"])
        hierarquia_edit.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(popup, text="Clã:").grid(row=2, column=0, padx=5, pady=5)
        clans_edit = ttk.Combobox(popup, values=clans)
        clans_edit.set(jogador["clan"])
        clans_edit.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(popup, text="Custo:").grid(row=3, column=0, padx=5, pady=5)
        custo_edit = ttk.Combobox(popup, values=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])
        custo_edit.set(jogador["custo"])
        custo_edit.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(popup, text="Lenda:").grid(row=4, column=0, padx=5, pady=5)
        lenda_edit = ttk.Combobox(popup, values=lendas)
        lenda_edit.set(jogador["lenda"])
        lenda_edit.bind("<KeyRelease>", lambda event, lenda_widget=lenda_edit: autoComplete(event, lenda_widget))
        lenda_edit.grid(row=4, column=1, padx=5, pady=5)

        def salvar_edicao():
            jogador["nome"] = nome_edit.get()
            jogador["hierarquia"] = hierarquia_edit.get()
            jogador["clan"] = clans_edit.get()
            jogador["custo"] = custo_edit.get()
            jogador["lenda"] = lenda_edit.get()

            data["jogadores"][indice] = jogador

            listaJogadores.item(jogadorSelecionado, values=(jogador["nome"], jogador["clan"], jogador["hierarquia"], jogador["custo"], jogador["lenda"]))

            popup.destroy()

        tk.Button(popup, text="Salvar", command=salvar_edicao).grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(popup, text="Cancelar", command=popup.destroy).grid(row=5, column=1, columnspan=2, padx=5, pady=5)


def autoComplete(event, lenda_widget):
    current_text = lenda_widget.get()
    # Obtém todos os valores da combobox
    all_values = lenda_widget['values']
    
    # Verifica se a tecla pressionada é uma tecla de exclusão
    is_delete_key = event.keysym in ["BackSpace", "Delete"]

    # Verifica se o texto atual não está vazio e a tecla pressionada não é uma tecla de exclusão
    if current_text and not is_delete_key:
        # Filtra os valores que começam com o texto atual
        filtered_values = [value for value in all_values if value.startswith(current_text)]
        if filtered_values:
            # Seleciona o primeiro valor filtrado
            lenda_widget.set(filtered_values[0])
            # Define a seleção do texto para o final
            lenda_widget.selection_range(len(current_text), tk.END)

def mostrarJogadores(jogadores):
    for jogador in jogadores:
        listaJogadores.insert("", "end", values=(jogador['nome'], jogador['clan'], jogador['hierarquia'], jogador['custo'], jogador['lenda']))

listaJogadores = ttk.Treeview(window, columns=("Jogador", "Clã", "Hierarquia", "Custo", "Lenda"), show="headings")
mostrarJogadores(jogadores)
listaJogadoresLabel = tk.Label(window, text="Lista de Jogadores", foreground="#FFC857", background="#1C1C1C", font=("Arial", 13))
listaJogadores.place(x=130, y=290)
listaJogadoresLabel.place(x=130, y=260)
listaJogadores.heading("Jogador", text="Jogador")
listaJogadores.heading("Clã", text="Clã")
listaJogadores.heading("Hierarquia", text="Hierarquia")
listaJogadores.heading("Custo", text="Custo")
listaJogadores.heading("Lenda", text="Lenda")
scrollbar = ttk.Scrollbar(window, orient="vertical", command=listaJogadores.yview)
scrollbar.place(x=1140,y=290,height=225)
listaJogadores.configure(yscrollcommand=scrollbar.set)

nomeJogador = tk.Entry(window, font=("Arial", 8), width=50)
nomeLabel = tk.Label(window, text="Nome do Jogador", foreground="#FFC857", background="#1C1C1C", font=("Arial", 13))
nomeJogador.place(x=130, y=50)
nomeLabel.place(x=125, y=25)

hierarquiaJogador = ttk.Combobox(window, values=["Lider","Co-Lider","Membro"])
hierarquiaLabel = tk.Label(window, text="Hierarquia", foreground="#FFC857", background="#1C1C1C", font=("Arial"))
hierarquiaJogador.place(x=130, y=80)
hierarquiaLabel.place(x=275, y=80)

clansJogador = ttk.Combobox(window, values=clans)
clansLabel = tk.Label(window, text="Clãs", foreground="#FFC857", background="#1C1C1C", font=("Arial", 13))
clansJogador.place(x=130, y=115)
clansLabel.place(x=275, y=115)

custoJogador = ttk.Combobox(window, values=[10,20,30,40,50,60,70,80,90,100,110,120])
custoLabel = tk.Label(window, text="Custo", foreground="#FFC857", background="#1C1C1C", font=("Arial", 13))
custoJogador.place(x=130, y=150)
custoLabel.place(x=275, y=150)

lendaJogador = ttk.Combobox(window, values=lendas)
lendaLabel = tk.Label(window, text="Lenda", foreground="#FFC857", background="#1C1C1C", font=("Arial", 13))
lendaJogador.bind("<KeyRelease>", lambda event: autoComplete(event, lendaJogador))
lendaJogador.place(x=130, y=185)
lendaLabel.place(x=275, y=185)

adicionar = tk.Button(window, text="Adicionar Jogador", background="#111111", foreground="#FFC857", activebackground="#FFC857", activeforeground="#111111", bd=0, command=adicionarJogador, font=("Arial", 16, "bold"))
adicionar.place(x=130, y=215)

editar = tk.Button(window,text="Editar Jogador",background="#111111", foreground="#FFC857", activebackground="#FFC857", activeforeground="#111111", bd=0, command=editarJogador, font=("Arial", 16, "bold"))
editar.place(x=130, y=530)

remover = tk.Button(window, text="Remover Jogador", background="#111111", foreground="#FFC857", activebackground="#FFC857", activeforeground="#111111", bd=0, command=removerJogador, font=("Arial", 16, "bold"))
remover.place(x=340, y=530)

obterAtt = tk.Button(window, text="Obter lista Atualizada", background="#111111", foreground="#FFC857", activebackground="#FFC857", activeforeground="#111111", bd=0, command=confirmarAtualizacao, font=("Arial", 16, "bold"))
obterAtt.place(x=580, y=530)


icon = tk.PhotoImage(file="logo.png")
window.iconphoto(True, icon)
window.config(background="#1C1C1C")
window.mainloop()
