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

def EntradaOpcaoBrilho():
    global OpcaoBrilho
    OpcaoBrilho = entry.get()
    win.destroy()

def EntradaOpcaoContraste():
    global OpcaoContraste
    OpcaoContraste = entry.get()
    win.destroy()

def EntradaOpcaoReducaoSx():
    global Sx
    Sx = entry.get()
    win.destroy()

def EntradaOpcaoReducaoSy():
    global Sy
    Sy = entry.get()
    win.destroy()

def EntradaOpcaoRotacao():
    global OpcaoRotacao
    OpcaoRotacao = entry.get()
    win.destroy()

def EntradaOpcaoFiltragem():
    global OpcaoFiltragem
    OpcaoFiltragem = entry.get()
    win.destroy()

def EntradaFiltro():
    global VetorFiltroOp
    VetorFiltroOp = entry.get()
    win.destroy()

def MostrarImagens(ImagemAntiga, ImagemResultado, OpcaoMostrar = 0):
    win = Tk()
    win.geometry("1080x720")

    im_tk_nova = ImageTk.PhotoImage(ImagemResultado)
    im_tk_antiga = ImageTk.PhotoImage(ImagemAntiga)
    
    # Mostrar duas imagens
    if(OpcaoMostrar == 0):
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

    # Mostrar histograma e imagem
    elif(OpcaoMostrar == 1):
        label1 = Label(win, 
                text='Imagem: ', 
                font=('Arial', 13, 'bold'), 
                fg = 'white', 
                bg='black',
                image=im_tk_antiga,
                compound='bottom')

        label2 = Label(win, 
                text='Histograma da imagem:\n'
                     'Pixels + escuros (0)     Pixels + claros: (255)\n'
                     ' <                                            > ', 
                font=('Arial', 9, 'bold'), 
                fg = 'white', 
                bg='black',
                image=im_tk_nova,
                compound='bottom')

    # Mostrar 2 histogramas
    elif(OpcaoMostrar == 2):
        label1 = Label(win, 
                text= 'Histograma da imagem anterior:\n'
                      'Pixels + escuros (0)     Pixels + claros: (255)\n'
                       ' <                                            > ', 
                font=('Arial', 9, 'bold'), 
                fg = 'white', 
                bg='black',
                image=im_tk_antiga,
                compound='bottom')

        label2 = Label(win, 
                text='Histograma da imagem resultado:\n '
                     'Pixels + escuros (0)     Pixels + claros: (255)\n'
                     ' <                                            > ', 
                font=('Arial', 9, 'bold'), 
                fg = 'white', 
                bg='black',
                image=im_tk_nova,
                compound='bottom')

    # Mostra dois histogramas (Usado para o matching)
    elif(OpcaoMostrar == 3):
        label1 = Label(win, 
                text='Histograma da imagem alvo:\n'
                     'Pixels + escuros (0)     Pixels + claros: (255)\n'
                     ' <                                            > ',
                font=('Arial', 9, 'bold'), 
                fg = 'white', 
                bg='black',
                image=im_tk_antiga,
                compound='bottom')

        label2 = Label(win, 
                text='Histograma alcançado:\n'
                     'Pixels + escuros (0)     Pixels + claros: (255)\n'
                     ' <                                            > ',  
                font=('Arial', 9, 'bold'), 
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

# Função auxiliar, calcula vetor histograma dado uma imagem
def CalculaHistograma(Imagem):
    Imagem = ConversaoTonsCinza(Imagem) # Transformar imagem em tons de cinza
    VetorHistograma = [0] * 256

    for x in range(width):
        for y in range(height):
            r, g, b = Imagem.getpixel((x, y)) # Nesse caso, como a imagem está em tons de cinza, r = g = b
            VetorHistograma[r] += 1
    
    return VetorHistograma

# Função auxiliar, calcula vetor cumulativo de um vetor 
def CalculaVetorCumulativo(Vetor):
    VetorCumulativo = [0] * 256
    FatorDeEscala = 255 / (height * width)

    for i in range(len(Vetor)):
        if(i == 0):
            VetorCumulativo[i] = Vetor[i] * FatorDeEscala
        else:
            VetorCumulativo[i] = VetorCumulativo[i-1] + (Vetor[i] * FatorDeEscala)
    
    return VetorCumulativo

# Função auxiliar, recebe o vetor de histograma e retorna imagem
def CriaImagemHistograma(Vetor):
    im_histograma = Image.new('RGB', (256, 256), color = 'white')

    # Normalizando VetorHistograma
    for i in range(len(Vetor)):
        Vetor[i] = round(Vetor[i] / 64)

    L = 255, 0, 0
    for i in range(len(Vetor)):
        for j in range(Vetor[i]):
            if(j < 256):
                im_histograma.putpixel((i, 255 - j), L)
    
    return im_histograma

# Retorna o índice do elemento em uma lista mais próximo do número dado
def AchaMaisProximo(Numero, Lista):
    MenorDiferenca = 256
    IndiceMenor = -1
    for i in range(len(Lista)):
        Diferenca = abs(Numero - Lista[i])
        if(Diferenca < MenorDiferenca):
            MenorDiferenca = Diferenca
            IndiceMenor = i

    return IndiceMenor

# Dado uma matriz (filtro), rotaciona o filtro em 180 graus
def RotacionarFiltro(Filtro):
    NovoFiltro = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for j in range(3):
            NovoFiltro[i][j] = Filtro[2 - i][2 - j]
    
    return NovoFiltro

# Função que converte uma string de 9 números em um kernel 3x3
def ConverterStringToFiltro(String):
    VetorNovo = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    String = String.replace(' ', '')
    Vetor = String.split(',')
    Contador = 0
    for i in range(3):
        for j in range(3):
            VetorNovo[i][j] = Vetor[Contador]
            Contador += 1
        
    return VetorNovo
            
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
def ConversaoTonsCinza(Imagem):
    width_, height_ = Imagem.size
    im_nova = Image.new('RGB', (width_, height_), color = 'black')

    for x in range(width_):
        for y in range(height_):
            r, g, b = Imagem.getpixel((x, y))
            r = r * 0.2989  # Alterando os canais rgb de valor
            b = b * 0.5870
            g = g * 0.1140
            L = r + g + b
            ValorPixel = int(L), int(L), int(L) 
            im_nova.putpixel((x, y), ValorPixel)    # Coloca na nova imagem o valor de pixel cinza

    return im_nova

# Função 4, quantização 
def Quantizacao(NumeroTons):
    ConversaoTonsCinza(im)
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


# Função 6, mostra histograma
def MostraHistograma(Imagem):
    im_nova = Image.new('RGB', (256, 256), color = 'white')
    Vetor = CalculaHistograma(im)
    im_nova = CriaImagemHistograma(Vetor)
    Imagem = ConversaoTonsCinza(Imagem)
    MostrarImagens(Imagem, im_nova, 1)

# Função 7, ajusta brihlo da imagem
def AjustarBrilho(AjusteBrilho):
    im_nova = Image.new('RGB', (width, height), color = 'black')

    AjusteBrilho = float(AjusteBrilho)

    for x in range(width):
        for y in range(height):
            r, g, b = im.getpixel((x, y))
            r = round(r + AjusteBrilho)  # Alterando os canais rgb de valor
            b = round(b + AjusteBrilho)
            g = round(g + AjusteBrilho)
            ValorPixel = int(r), int(g), int(b) 
            im_nova.putpixel((x, y), ValorPixel)    # Coloca na nova imagem o valor de pixel cinza

    MostrarImagens(im, im_nova)

    return im_nova

# Função 8, ajusta contraste da imagem
def AjustarContraste(AjusteContraste):
    im_nova = Image.new('RGB', (width, height), color = 'black')

    AjusteContraste = float(AjusteContraste)

    for x in range(width):
        for y in range(height):
            r, g, b = im.getpixel((x, y))
            r = round(r * AjusteContraste)  # Alterando os canais rgb de valor
            b = round(b * AjusteContraste)
            g = round(g * AjusteContraste)
            ValorPixel = int(r), int(g), int(b) 
            im_nova.putpixel((x, y), ValorPixel)    # Coloca na nova imagem o valor de pixel cinza

    MostrarImagens(im, im_nova)

    return im_nova

# Função 9, calcular negativo da imagem
def CalcularNegativo():
    im_nova = Image.new('RGB', (width, height), color = 'black')
    for x in range(width):
        for y in range(height):
            r, g, b = im.getpixel((x, y))
            r = 255 - r
            g = 255 - g
            b = 255 - b
            ValorPixel = r, g, b
            im_nova.putpixel((x, y), ValorPixel)
    
    MostrarImagens(im, im_nova)

    return im_nova

# Função 10, equalização de histogramas
def EqualizacaoHistogramas():
    im_nova = Image.new('RGB', (width, height), color = 'black')
    Vetor = CalculaHistograma(im)
    HistogramaCumulativo = CalculaVetorCumulativo(Vetor) # Gerando histograma cumulativo

    for x in range(width):
        for y in range(height):
            r, g, b = im.getpixel((x, y))
            r = round(HistogramaCumulativo[r])
            g = r
            b = r
            ValorPixel = r, g, b
            im_nova.putpixel((x, y), ValorPixel)
    
    # Mostrando imagem prévia (em preto e branco) e posterior
    im_1 = ConversaoTonsCinza(im)
    MostrarImagens(im_1, im_nova)

    VetorCumulativo = CalculaHistograma(im_nova)
    im_histograma_previo = CriaImagemHistograma(Vetor)
    im_histograma_posterior = CriaImagemHistograma(VetorCumulativo)

    # Mostrando histograma prévio e posterior
    MostrarImagens(im_histograma_previo, im_histograma_posterior, 2)

    return im_nova

# Função 11, Matching de Histogramas
def MatchingHistogramas(im, im_2):
    im_nova = Image.new('RGB', (width, height), color = 'black')
    im = ConversaoTonsCinza(im) # Converter para imagem monocromática ambas imagens dadas, im = imagem que queremos fazer matching com im_2
    im_2 = ConversaoTonsCinza(im_2)

    VetorImagemInicial = CalculaHistograma(im)
    VetorImagemAlvo= CalculaHistograma(im_2)

    VetorCumulativoInicial = CalculaVetorCumulativo(VetorImagemInicial)
    VetorCumulativoAlvo= CalculaVetorCumulativo(VetorImagemAlvo)

    HM = [0] * 256

    # Aqui devemos achar o tom de cinza mais próximo do VetorCumulativoMatching e colocar na imagem
    for i in range(len(VetorCumulativoAlvo)):
         HM[i] = AchaMaisProximo(VetorCumulativoInicial[i], VetorCumulativoAlvo)

    for x in range(width):
        for y in range(height):
            r, g, b = im.getpixel((x, y))
            ValorPixel = HM[r], HM[r], HM[r]
            im_nova.putpixel((x, y), ValorPixel)

    MostrarImagens(im_2, im_nova)

    VetorAlcancado = CalculaHistograma(im_nova)
    im_histograma_alcancado = CriaImagemHistograma(VetorAlcancado)
    im_histograma_alvo = CriaImagemHistograma(VetorImagemAlvo)

    MostrarImagens(im_histograma_alvo, im_histograma_alcancado, 3)

    return im_nova

# Função 12, reduzir uma imagem (zoom out)
def ReduzirImagem(Sx, Sy):

    width_destino = round(width / Sx)
    height_destino = round(height / Sy)
    
    im_nova = Image.new('RGB', (width_destino, height_destino), color = 'black')

    for x in range(width):
        for y in range(height):
            r_sum, g_sum, b_sum = 0, 0, 0

            if((x % Sx == 0) and (y % Sy == 0)):
            # Definindo retângulo que realiará a média sobre os pixels da imagem
                for i in range(Sx):
                    for j in range(Sy):

                        PosicaoPixelX = x+i
                        PosicaoPixelY = y+j

                        if((PosicaoPixelX < width) and (PosicaoPixelY < height)):
                            r, g, b = im.getpixel((PosicaoPixelX, PosicaoPixelY))

                        r_sum = r_sum + r
                        g_sum = g_sum + g
                        b_sum = b_sum + b

                r = round(r_sum / (Sx * Sy))
                g = round(g_sum / (Sx * Sy))
                b = round(b_sum / (Sx * Sy))

                ValorPixel = r,g,b

                PosicaoPixelX = round(x / Sx)
                PosicaoPixelY = round(y / Sy)
                if(PosicaoPixelX < width_destino and PosicaoPixelY < height_destino):
                    im_nova.putpixel((PosicaoPixelX, PosicaoPixelY), ValorPixel)

    MostrarImagens(im, im_nova)
    
    return im_nova

# Função 13, ampliar uma imagem (zoom in)
def AmpliarImagem():
    width_destino = width * 2
    height_destino = height * 2 # A operação funciona ampliando a imagem em 4x a cada execução da instrução, portanto devemos multiplicar dimensões
    im_nova = Image.new('RGB', (width_destino, height_destino), color = 'black')

    for x in range(width_destino):
        for y in range(height_destino):
            if(x % 2 == 0 and y % 2 == 0):
                r,g,b = im.getpixel((x/2, y/2))
                ValorPixel = r, g, b
                im_nova.putpixel((x, y), ValorPixel)

    # Agora devemos realizar a média para preencher todas as LINHAS
    for x in range(width_destino):
        for y in range(height_destino):
            if(x % 2 == 0 and y % 2 == 1):
                if(y+1 < height_destino):
                    r1,g1,b1 = im_nova.getpixel((x, y+1))
                    r2,g2,b2 = im_nova.getpixel((x, y-1))
                    ValorPixel = round((r1 + r2) / 2), round((g1 + g2) / 2), round((b1 + b2) / 2)
                    im_nova.putpixel((x, y), ValorPixel)
    
    # Agora devemos preencher todas as COLUNAS restantes
    for x in range(width_destino):
        for y in range(height_destino):
            if((x % 2 == 1 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 0)):
                if(x+1 < width_destino):
                    r1,g1,b1 = im_nova.getpixel((x+1, y))
                    r2,g2,b2 = im_nova.getpixel((x-1, y))
                    ValorPixel = round((r1 + r2) / 2), round((g1 + g2) / 2), round((b1 + b2) / 2)
                    im_nova.putpixel((x, y), ValorPixel)

    MostrarImagens(im, im_nova)

    return im_nova

# Função 14, rotação de imagem
def RotacaoImagem(Imagem, OpcaoRotacao):
    width_, height_ = Imagem.size     # Verificando tamanho da imagem, altura e largura
    im_nova = Image.new('RGB', (height_, width_), color = 'black')
    OpcaoRotacao = int(OpcaoRotacao)

    # Rotação para direita
    if(OpcaoRotacao == 1):
        for x in range(width_):
            for y in range(height_):
                r, g, b = Imagem.getpixel((x, y))
                ValorPixel = r, g, b
                im_nova.putpixel((height_ - y - 1, x), ValorPixel)    
    
    # Senão rotacionar para esquerda
    elif(OpcaoRotacao == 2):
        for x in range(width_):
            for y in range(height_):
                r, g, b = Imagem.getpixel((x, y))
                ValorPixel = r, g, b
                im_nova.putpixel((y, width - x - 1), ValorPixel)    # Coloca na nova imagem o valor de pixel cinza

    MostrarImagens(im, im_nova)
    return im_nova

#Função 15, filtragem de imagem
def ConvolucaoImagem(Imagem, Opcao, VetorFiltro):
    if(Opcao != '1'):
        Imagem = ConversaoTonsCinza(Imagem) # Só aplicaremos a convolução a imagens de luminância
    width_, height_ = Imagem.size     # Verificando tamanho da imagem, altura e largura
    im_nova = Image.new('RGB', (width_, height_), color = 'black')
    
    # Gaussiano
    if(Opcao == '1'):
        VetorFiltro = [[0.0625, 0.125, 0.0625], [0.125, 0.25, 0.125], [0.0625, 0.125, 0.0625]]
    # Laplaciano
    elif(Opcao == '2'):
        VetorFiltro = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]
    # Passa alta genérico
    elif(Opcao == '3'):
        VetorFiltro = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
    # Prewitt Hx
    elif(Opcao == '4'):
        VetorFiltro = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    # Prewitt Hy
    elif(Opcao == '5'):
        VetorFiltro = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
    # Sobel Hx
    elif(Opcao == '6'):
        VetorFiltro = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    # Sobel Hy
    elif(Opcao == '7'):
        VetorFiltro = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]       
    # Senão o filtro é arbitrário e já foi dado na chamada da função

    VetorFiltro = RotacionarFiltro(VetorFiltro)

    for x in range(width_):
        for y in range(height_):
            # Filtro varre os pixels da vizinhança
            ValorPixelR, ValorPixelG, ValorPixelB = 0, 0, 0
            for i in range(3):
                for j in range(3):
                    if(x + 2 < width_ and y + 2 < height_):
                        r, g, b = Imagem.getpixel((x + i, y + j))
                        ValorPixelR = ValorPixelR + (float(VetorFiltro[i][j]) * r)
                        ValorPixelG = ValorPixelG + (float(VetorFiltro[i][j]) * g)
                        ValorPixelB = ValorPixelB + (float(VetorFiltro[i][j]) * b)
            L = round(ValorPixelR), round(ValorPixelG), round(ValorPixelB)
            im_nova.putpixel((x, y), L)
        
    if(Opcao == '2' or Opcao == '4' or Opcao == '4' or Opcao == '5' or Opcao == '6' or Opcao == '7'):
        for x in range(width_):
            for y in range(height_):
                r, g, b = im_nova.getpixel((x, y))
                r = r + 127
                g = r
                b = r
                ValorPixel = r, g, b
                im_nova.putpixel((x, y), ValorPixel)

    MostrarImagens(Imagem, im_nova)

    return im_nova


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
    width, height = im.size     # Verificando tamanho da imagem, altura e largura 
    win = Tk()
    win.geometry("1080x500")
    frame = Frame(win)
    frame.pack(side="top", expand=True, fill="both")
    entry = Entry(frame, font=('Helvetica', 15))
    entry.place(x=430,y=420) # Adicionar + ou = 30 no valor de y a cada opção que colocar
    Label(frame, text= "\nDigite o número da operação que deseja realizar ou '0' para encerrar a aplicação:\n"
                        "1 - Renomear o arquivo\n"
                        "2 - Espelhamento vertical / horizontal\n"
                        "3 - Conversão de imagem colorida para tons de cinza\n"
                        "4 - Quantização (de tons) sobre as imagens em tons de cinza\n"
                        "5 - Salvar imagem\n"
                        "6 - Calculo de histograma\n"
                        "7 - Ajuste de brilho\n" 
                        "8 - Ajuste de contraste\n"
                        "9 - Negativo da imagem\n"
                        "10 - Equalização Histograma\n"
                        "11 - Matching de histogramas de duas imagens\n"
                        "12 - Zoom out na imagem\n"
                        "13 - Zoom in na imagem (4x)\n"
                        "14 - Rotação de imagem em +- 90°\n"
                        "15 - Filtragem",
                        font=('Helvetica', 15)).pack(pady=20)
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
        im_nova = ConversaoTonsCinza(im)
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
    
    # OP cálculo de histograma
    elif(Operacao == '6'):
        MostraHistograma(im)

    # OP ajuste de brilho
    elif(Operacao == '7'):
        win = Tk()
        win.geometry("600x250")
        frame = Frame(win)
        frame.pack(side="top", expand=True, fill="both")
        entry = Entry(frame, font=('Helvetica', 15))
        entry.place(x=185,y=60)
        Label(frame, text= 'Digite o valor de brilho a ser somado na imagem: ',
                            font=('Helvetica', 15)).pack(pady=20)
        Button(frame, text="submit", font=('Helvetica bold', 10), 
        command = EntradaOpcaoBrilho).pack(pady=20)
        win.mainloop()

        im_nova = AjustarBrilho(OpcaoBrilho)

    #OP ajuste de contraste
    elif(Operacao == '8'):
        win = Tk()
        win.geometry("600x250")
        frame = Frame(win)
        frame.pack(side="top", expand=True, fill="both")
        entry = Entry(frame, font=('Helvetica', 15))
        entry.place(x=185,y=60)
        Label(frame, text= 'Digite o valor de contraste a ser colocado na imagem: ',
                            font=('Helvetica', 15)).pack(pady=20)
        Button(frame, text="submit", font=('Helvetica bold', 10), 
        command = EntradaOpcaoContraste).pack(pady=20)
        win.mainloop()

        im_nova = AjustarContraste(OpcaoContraste)
        im = im_nova

    # OP calcular negativo
    elif(Operacao == '9'):
        im_nova = CalcularNegativo()
        im = im_nova

    # OP de equalização de histogramas
    elif(Operacao == '10'):
        im_nova = EqualizacaoHistogramas()
        im = im_nova
    
    # OP de matching de histogramas
    elif(Operacao == '11'):
        win = Tk()
        win.geometry("600x250")
        frame = Frame(win)
        frame.pack(side="top", expand=True, fill="both")
        entry = Entry(frame, font=('Helvetica bold', 15))
        entry.place(x=185,y=50)
        Label(frame, text="Digite o nome do arquivo que deseja fazer o matching: ", font=('Helvetica',15)).pack(pady=20)
        Button(frame, text="submit", font=('Helvetica bold', 10), command = EntradaNomeArquivo).pack(pady=20)
        win.mainloop()

        if(os.path.isfile(NomeArquivo)):    # Arquivo existe
            im_2 = Image.open(NomeArquivo)
            width, height = im.size     # Verificando tamanho da imagem, altura e largura

        im = MatchingHistogramas(im, im_2)

    # OP de zoom out
    elif(Operacao == '12'):
        win = Tk()
        win.geometry("600x250")
        frame = Frame(win)
        frame.pack(side="top", expand=True, fill="both")
        entry = Entry(frame, font=('Helvetica', 15))
        entry.place(x=185,y=60)
        Label(frame, text= "Digite o fator de redução de x: ",
                            font=('Helvetica', 15)).pack(pady=20)
        Button(frame, text="submit", font=('Helvetica bold', 10),
        command = EntradaOpcaoReducaoSx).pack(pady=20)
        win.mainloop()

        win = Tk()
        win.geometry("600x250")
        frame = Frame(win)
        frame.pack(side="top", expand=True, fill="both")
        entry = Entry(frame, font=('Helvetica', 15))
        entry.place(x=185,y=60)
        Label(frame, text= "Digite o fator de redução de y: ",
                            font=('Helvetica', 15)).pack(pady=20)
        Button(frame, text="submit", font=('Helvetica bold', 10),
        command = EntradaOpcaoReducaoSy).pack(pady=20)
        win.mainloop()

        im = ReduzirImagem(int(Sx), int(Sy))
    
    # OP de zoom in (4x)
    elif(Operacao == '13'):
        im = AmpliarImagem()

    # OP de rotação de imagem
    elif(Operacao == '14'):
        win = Tk()
        win.geometry("600x250")
        frame = Frame(win)
        frame.pack(side="top", expand=True, fill="both")
        entry = Entry(frame, font=('Helvetica', 15))
        entry.place(x=185,y=80)
        Label(frame, text= "1 - Rotação de 90° para direita\n"
                           "2 - Rotação de 90° para esquerda",
                            font=('Helvetica', 15)).pack(pady=20)
        Button(frame, text="submit", font=('Helvetica bold', 10),
        command = EntradaOpcaoRotacao).pack(pady=20)
        win.mainloop()

        im = RotacaoImagem(im, OpcaoRotacao)

    # OP de filtragem de imagem
    elif(Operacao == '15'):
        VetorFiltragem = [[0,0,0],[0,1,0],[0,0,0]] # Valor padrão do vetor de filtro
        win = Tk()
        win.geometry("600x340")
        frame = Frame(win)
        frame.pack(side="top", expand=True, fill="both")
        entry = Entry(frame, font=('Helvetica', 15))
        entry.place(x=185,y=215)
        Label(frame, text= "1 - Filtro Gaussiano\n"
                           "2 - Filtro Laplaciano\n"
                           "3 - Filtro Passa alta genérico\n"
                           "4 - Prewitt Hx\n"
                           "5 - Prewitt Hy\n"
                           "6 - Sobel Hx\n"
                           "7 - Sobel Hy\n"
                           "8 - Digitar outra opção de filtro",
                            font=('Helvetica', 15)).pack(pady=20)
        Button(frame, text="submit", font=('Helvetica bold', 10),
        command = EntradaOpcaoFiltragem).pack(pady=20)
        win.mainloop()

        if(OpcaoFiltragem == '8'):
            win = Tk()
            win.geometry("800x250")
            frame = Frame(win)
            frame.pack(side="top", expand=True, fill="both")
            entry = Entry(frame, font=('Helvetica', 15))
            entry.place(x=185,y=80)
            Label(frame, text= "Digite abaixo o filtro 3x3 seguindo o exemplo dado de um filtro passa alta:\n"
                            "Ex: 0,-1,0,-1,4,-1,0,-1,0",    
                                font=('Helvetica', 15)).pack(pady=20)
            Button(frame, text="submit", font=('Helvetica bold', 10),
            command = EntradaFiltro).pack(pady=20)
            win.mainloop()
            VetorFiltragem = ConverterStringToFiltro(VetorFiltroOp)

        im = ConvolucaoImagem(im, OpcaoFiltragem, VetorFiltragem)

    # Encerando aplicação
    elif(Operacao == '0'):
        break

    else:
        print("") # Printando vazio somente para repetir o laço, já que a opção foi inválida