from tkinter import *
from PIL import ImageTk, Image
import os

# Operações para interface funcionar =====================================================================

def EntradaNomeArquivo():
    global NomeArquivo
    NomeArquivo = entry.get()
    win.destroy()

def EntradaOperacao():
    global Operacao
    Operacao = entry.get()
    win.destroy()

def EntradaNovoNomeArquivo():
    global NomeNovo
    NomeNovo = entry.get()
    win.destroy()

def EntradaOpcaoEspelhamento():
    global OpcaoEspelhamento
    OpcaoEspelhamento = entry.get()
    win.destroy()

def EntradaOpcaoQuantizacao():
    global OpcaoQuantizacao
    OpcaoQuantizacao = entry.get()
    win.destroy()

def MostrarImagens(ImagemAntiga, ImagemResultado):
    win = Tk()
    win.geometry("1080x720")

    im_tk_nova = ImageTk.PhotoImage(ImagemResultado)
    im_tk_antiga = ImageTk.PhotoImage(ImagemAntiga)
    
    label1 = Label(win, 
            text='Imagem Anterior: ', 
            font=('Arial', 13, 'bold'), 
            fg = 'white', 
            bg='black',
            image=im_tk_antiga,
            compound='bottom')

    label2 = Label(win, 
            text='Imagem Posterior: ', 
            font=('Arial', 13, 'bold'), 
            fg = 'white', 
            bg='black',
            image=im_tk_nova,
            compound='bottom')
        
    label3 = Label(win, 
            text='Para prosseguir basta fechar a janela!', 
            font=('Helvetica', 15))

    label3.pack(side=TOP)
    label1.pack(side=LEFT)
    label2.pack(side=RIGHT)

    win.mainloop()

# Funções sobre operações nas imagens ====================================================================

# Função 1, alterar nome de arquivo
def AlteraNomeArquivo(NomeNovo):
    os.rename(NomeArquivo, NomeNovo)

# Funcao 2, espelhamento vertical / horizontal
def Espelhamento(Opcao):
    im_nova = Image.new('RGB', (width, height), color = 'black')

    if(Opcao == '1' or Opcao =='2'):   
        for x in range(width):
            for y in range(height):
                ValorPixel = im.getpixel((x, y))    
                if(Opcao == '1'):   # Realizando espelhamento horizontal, altera x
                    novo_x = width - x - 1
                    im_nova.putpixel((novo_x, y), ValorPixel)  
                elif(Opcao == '2'): # Realizando espelhamento vertical, altera y
                    novo_y = height - y - 1
                    im_nova.putpixel((x, novo_y), ValorPixel)

    else:
        print("Opção inválida")

    MostrarImagens(im, im_nova)
    return im_nova

# Função 3, converter imagem para tons de cinza
def ConversaoTonsCinza():
    im_nova = Image.new('RGB', (width, height), color = 'black')

    for x in range(width):
        for y in range(height):
            r, g, b = im.getpixel((x, y))
            r = r * 0.2989  # Alterando os canais rgb de valor
            b = b * 0.5870
            g = g * 0.1140
            L = r + g + b
            ValorPixel = int(L), int(L), int(L) 
            im_nova.putpixel((x, y), ValorPixel)    # Coloca na nova imagem o valor de pixel cinza

    return im_nova

# Função 4, quantização 
def Quantizacao(NumeroTons):
    ConversaoTonsCinza()
    im_nova = Image.new('RGB', (width, height), color = 'black')

    MaiorPixel, MenorPixel = 0, 0

    for x in range(width):
        for y in range(height):    # Vasculhando a imagem para saber o maior valor de pixel e o menor valor de pixel
            L = im.getpixel((x, y))
            if(L[1] > MaiorPixel):
                MaiorPixel = L[1]
            if(L[1] < MenorPixel):
                MenorPixel = L[1]

    TamanhoIntervalo = MaiorPixel - MenorPixel + 1
    NumeroTons = int(NumeroTons) - 1
    TamanhoBin = TamanhoIntervalo / NumeroTons

    if(int(NumeroTons) >= TamanhoIntervalo):
        return im

    else:
        for x in range(width):
            for y in range(height):
                r, g, b = im.getpixel((x, y))
                Divisao = round(r / TamanhoBin) 
                r = Divisao * TamanhoBin
                g = r
                b = r
                ValorPixel = int(r), int(g), int(b)
                im_nova.putpixel((x, y), ValorPixel)
            
        MostrarImagens(im, im_nova)
        return im_nova

# Função 5, utilizada para salvar arquivos
def SalvaArquivo(NomeArquivo):
    im_nova.save(NomeArquivo)

# Função main =========================================================================================

#Inicializando interface

win = Tk()
win.geometry("600x250")
frame = Frame(win)
frame.pack(side="top", expand=True, fill="both")
entry = Entry(frame, font=('Helvetica bold', 15))
entry.place(x=185,y=50)
Label(frame, text="Digite o nome do arquivo: ", font=('Helvetica',15)).pack(pady=20)
Button(frame, text="submit", font=('Helvetica bold', 10), command = EntradaNomeArquivo).pack(pady=20)
win.mainloop()

if(os.path.isfile(NomeArquivo)):    # Arquivo existe
    im = Image.open(NomeArquivo)
    width, height = im.size     # Verificando tamanho da imagem, altura e largura
    Operacao = -1   # Operação inicia em -1 para não ser equivalente a 0 e fazer o laço while
else:
    Operacao = '0'  # Arquivo não existe então não entra no laço

while(Operacao != '0'):

    # Mostrando menu na tela do usuário utilizando 
    win = Tk()
    win.geometry("1080x500")
    frame = Frame(win)
    frame.pack(side="top", expand=True, fill="both")
    entry = Entry(frame, font=('Helvetica', 15))
    entry.place(x=430,y=190)
    Label(frame, text= "\nDigite o número da operação que deseja realizar ou '0' para encerrar a aplicação:\n"
                        "1 - Renomear o arquivo\n"
                        "2 - Espelhamento vertical / horizontal\n"
                        "3 - Conversão de imagem colorida para tons de cinza\n"
                        "4 - Quantização (de tons) sobre as imagens em tons de cinza\n"
                        "5 - Salvar imagem", font=('Helvetica', 15)).pack(pady=20)
    Button(frame, text="submit", font=('Helvetica bold', 10), command = EntradaOperacao).pack(pady=20)
    win.mainloop()
    
    # OP de alterar nome de arquivo
    if(Operacao == '1'):

        # Operações sobre interface
        win = Tk()
        win.geometry("600x250")
        frame = Frame(win)
        frame.pack(side="top", expand=True, fill="both")
        entry = Entry(frame, font=('Helvetica', 15))
        entry.place(x=185,y=50)
        Label(frame, text= "Digite o novo nome do arquivo: ", font=('Helvetica', 15)).pack(pady=20)
        Button(frame, text="submit", font=('Helvetica bold', 10), command = EntradaNovoNomeArquivo).pack(pady=20)
        win.mainloop()

        im.close()  # Devemos fechar o arquivo, visto que é impossível alterar o nome dele com ele aberto
        AlteraNomeArquivo(NomeNovo)
        NomeArquivo = NomeNovo
        im = Image.open(NomeNovo)   #Abrindo novamente arquivo, agora com novo nome
    
    # OP de espelhamento
    elif(Operacao == '2'):
        win = Tk()
        win.geometry("600x250")
        frame = Frame(win)
        frame.pack(side="top", expand=True, fill="both")
        entry = Entry(frame, font=('Helvetica', 15))
        entry.place(x=185,y=80)
        Label(frame, text= "Opção '1' - Espelhamento horizontal\n"
                            "Opção '2' - Espelhamento vertical",
                             font=('Helvetica', 15)).pack(pady=20)
        Button(frame, text="submit", font=('Helvetica bold', 10), 
        command = EntradaOpcaoEspelhamento).pack(pady=20)
        win.mainloop()

        im_nova = Espelhamento(OpcaoEspelhamento)
        im = im_nova
        
    # OP de converter imagem para tons de cinza
    elif(Operacao == '3'):
        im_nova = ConversaoTonsCinza()
        MostrarImagens(im, im_nova)
        im = im_nova

    # OP de quantização dos tons de cinza
    elif(Operacao == '4'):
        win = Tk()
        win.geometry("600x250")
        frame = Frame(win)
        frame.pack(side="top", expand=True, fill="both")
        entry = Entry(frame, font=('Helvetica', 15))
        entry.place(x=185,y=60)
        Label(frame, text= "Digite o número de tons a ser utilizado no processo de quantização: ",
                            font=('Helvetica', 15)).pack(pady=20)
        Button(frame, text="submit", font=('Helvetica bold', 10), 
        command = EntradaOpcaoQuantizacao).pack(pady=20)
        win.mainloop()

        im_nova = Quantizacao(OpcaoQuantizacao)
        im = im_nova
    
    # OP salvando arquivo
    elif(Operacao == '5'):
        win = Tk()
        win.geometry("600x250")
        frame = Frame(win)
        frame.pack(side="top", expand=True, fill="both")
        entry = Entry(frame, font=('Helvetica', 15))
        entry.place(x=185,y=60)
        Label(frame, text= "Digite o novo nome do arquivo: ",
                            font=('Helvetica', 15)).pack(pady=20)
        Button(frame, text="submit", font=('Helvetica bold', 10),
        command = EntradaNomeArquivo).pack(pady=20)
        win.mainloop()

        SalvaArquivo(NomeArquivo)
    
    # Encerando aplicação
    elif(Operacao == '0'):
        break

    else:
        print("") # Printando vazio somente para repetir o laço, já que a opção foi inválida