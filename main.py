from tkinter import *
from tkinter import ttk
import json
from PIL import Image, ImageTk

# Instanciando Janela
window = Tk()
window.geometry("640x540")
window.title("Coliseu de Clãs - Editor de Jogadores")

# Carregar a imagem original
original_image = Image.open("logo.png")

count = 0

with open("lista.json", "r") as file:
    data = json.load(file)
    jogadores = data["jogadores"]

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

    # Limpa a lista de jogadores e mostra novamente
    listaJogadores.delete(0, END)
    mostrarJogadores(data["jogadores"])


def removerJogador():
    jogadorParaApagar = listaJogadores.curselection()
    if jogadorParaApagar:
        indice = jogadorParaApagar[0]
        del data["jogadores"][indice]

        with open("lista.json", "w") as file:
            json.dump(data, file, indent=4)

        # Limpa a lista de jogadores e mostra novamente
        listaJogadores.delete(0, END)
        mostrarJogadores(data["jogadores"])
    


listaJogadores = Listbox(window,width=70)
def mostrarJogadores(players):
    for index, jogador in enumerate(players):
        listaJogadores.insert(index,f"{index + 1}. {jogador['nome']} - {jogador['clan']} - {jogador['custo']} - {jogador['lenda']} - {jogador['hierarquia']}")

mostrarJogadores(jogadores)
# Redimensionar a imagem para o tamanho desejado
nova_largura = 100
nova_altura = 100
imagem_redimensionada = original_image.resize((nova_largura, nova_altura))

# Converter a imagem redimensionada para o formato suportado pelo Tkinter
imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)

# Criação dos Widgets na Janela
nomeJogador = Entry(window,font=("Arial",8),width=50)
hierarquiaJogador = ttk.Combobox(window, values=["Lider","Co-Lider","Membro"])
clansJogador = ttk.Combobox(window, values=["Bichos do Mato","Vasco","Inimigos da Moda","Firebirds","Complexo do Corinthians","Strawberry Tea","Aurora","Cruzeiro","Ranked Beasts","Patota da Moneymatch"])
custoJogador = ttk.Combobox(window, values=[10,20,30,40,50,60,70,80,90,100,110,120])
lendaJogador = ttk.Combobox(window,values=["desconhecido","bodvar", "cassidy", "orion", "lord vraxx", "gnash", "queen nai", "hattori", "sir roland", "scarlet", "thatch", "ada", "sentinel", "lucien", "teros", "brynn", "asuri", "barraza", "ember", "azoth", "koji", "ulgrim", "diana", "jhala", "kor", "wu shang", "val", "ragnir", "cross", "mirage", "nix", "mordex", "yumiko", "artemis", "caspian", "sidra", "xull", "kaya", "isaiah", "jiro", "lin fei", "zariel", "rayman", "dusk", "fait", "thor", "petra", "vector", "volkov", "onyx", "jaeyun", "mako", "magyar", "reno", "munin", "arcadia", "ezio", "tezca", "thea", "red raptor", "loki", "seven", "vivi"])

nomeLabel = Label(window,text="Nome do Jogador",foreground="#FFC857",background="#1C1C1C",font=("Arial",13))
hierarquiaLabel = Label(window,text="Hierarquia",foreground="#FFC857",background="#1C1C1C",font=("Arial"))
clansLabel = Label(window,text="Clãs",foreground="#FFC857",background="#1C1C1C",font=("Arial",13))
custoLabel = Label(window,text="Custo",foreground="#FFC857",background="#1C1C1C",font=("Arial",13))
lendaLabel = Label(window,text="Lenda",foreground="#FFC857",background="#1C1C1C",font=("Arial",13))

adicionarLabel = Label(window,text="Jogador adicionado com Sucesso!",foreground="green",background="#1C1C1C",font=("Arial",10))
removerLabel = Label(window,text="Jogador removido com Sucesso!",foreground="green",background="#1C1C1C",font=("Arial",10))

listaJogadoresLabel = Label(window,text="Lista de Jogadores",foreground="#FFC857",background="#1C1C1C",font=("Arial",13))

adicionar = Button(window,text="Adicionar Jogador",
                background="#111111",
                foreground="#FFC857", 
                activebackground="#FFC857",
                activeforeground="#111111",
                bd=0,
                command=adicionarJogador,
                font=("Arial", 16, "bold"))
remover = Button(window,text="Remover Jogador",
                background="#111111",
                foreground="#FFC857", 
                activebackground="#FFC857",
                activeforeground="#111111",
                bd=0,
                command=removerJogador,
                font=("Arial", 16, "bold"))

imagem = Label(image=imagem_tk,background="#1C1C1C")

# Renderizando os Widgets na Janela
imagem.place(x=0,y=0)
nomeJogador.place(x=130,y=50)
hierarquiaJogador.place(x=130,y=80)
clansJogador.place(x=130,y=115)
custoJogador.place(x=130,y=150)
lendaJogador.place(x=130,y=185)

listaJogadores.place(x=130,y=290)

nomeLabel.place(x=125,y=25)
hierarquiaLabel.place(x=275,y=80)
clansLabel.place(x=275,y=115)
custoLabel.place(x=275,y=150)
lendaLabel.place(x=275,y=185)
listaJogadoresLabel.place(x=130,y=260)




adicionar.place(x=130,y=215)
remover.place(x=130,y=470)

# Ícone da Janela
icon = PhotoImage(file="logo.png")
window.iconphoto(True, icon)
window.config(background="#1C1C1C")

# Fazer display na tela da janela
window.mainloop()
