import cv2

def Nada(random):
    pass

def Cabecalho(Op, im, Ind, Ind2, Ind3):

    # Filtro Gaussiano
    if(Op == 1):
        if(Ind3):
            cv2.createTrackbar('Kernel', 'Imagem Resultado: ', 1, 257, Nada)

        TamKernel = cv2.getTrackbarPos('Kernel', 'Imagem Resultado: ')

        # Se o tamanho do kernel dado foi ímpar, aí sim poderemos realizar a operação com este kernel
        if(TamKernel % 2 == 1):
            TamKernel = (TamKernel, TamKernel)
        else:
            TamKernel = ((TamKernel -1), (TamKernel-1))

        return cv2.GaussianBlur(im, TamKernel, 0)
    
    # Filtro Canny
    elif(Op == 2):
        return cv2.Canny(im, 50, 140)

    # Filtro Sobel
    elif(Op == 3):
        gY = cv2.convertScaleAbs(cv2.Sobel(im, cv2.CV_16S, dx=0, dy=1, ksize=3))
        gX = cv2.convertScaleAbs(cv2.Sobel(im, cv2.CV_16S, dx=1, dy=0, ksize=3))
        return cv2.addWeighted(gY, 1/2, gX, 1/2, 0)

    # Ajuste de brilho
    elif(Op == 4):
        # Se não criou a trackbar, então orecisamos criá-la
        if(Ind):
            cv2.createTrackbar('Brilho', 'Imagem Resultado: ', 255, 2*255, Nada)

        Brilho = cv2.getTrackbarPos('Brilho', 'Imagem Resultado: ')

        # Corrigindo valor de brilho
        Brilho = Brilho - 255

        # Se queremos aumentar o brilho
        if (Brilho <= 0):
            MenorValorPixel = 0
            MaiorValorPixel = 255 + Brilho

        # Se queremos diminuir o brilho
        else:
            MenorValorPixel = Brilho
            MaiorValorPixel = 255

        # Soma dos dois vetores
        Array1Correcao = MaiorValorPixel / 255
        Array2Correcao = MenorValorPixel

        # Soma dos dois vetores
        return cv2.addWeighted(im, Array1Correcao, im, 0, Array2Correcao)

    # Ajuste de contraste
    elif(Op == 5):
        # Se não criou a trackbar, então precisamos criá-la
        if(Ind2):
            cv2.createTrackbar('Contraste', 'Imagem Resultado: ', 127, 2*127, Nada)
        
        Contraste = cv2.getTrackbarPos('Contraste', 'Imagem Resultado: ')

        # Corrigindo valor de contraste
        Contraste = Contraste - 127
        Array1Correcao = 200 * (Contraste + 127) / (127 * (200 - Contraste))
        Array2Correcao = 127 * (1 - Array1Correcao)

        # Soma dos dois vetores
        return cv2.addWeighted(im, Array1Correcao, im, 0, Array2Correcao)

    # Negativo da imagem
    elif(Op == 6):
        return cv2.convertScaleAbs(im, alpha=-1, beta=255)

    # Imagem em tons de cinza
    elif(Op == 7):
        return cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

    # Redimensionamento para metade
    elif(Op == 8):
        return cv2.resize(im, (int(im.shape[1]*1/2), int(im.shape[0]*1/2)))
    
    # Rotação em 90 graus no sentido horário
    elif(Op == 9):
        return cv2.rotate(im, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Espelhamento de vídeo horizontal
    elif(Op == 'H'):
        return cv2.flip(im, 1)

    # Espelhamento de vídeo vertical
    elif(Op == 'V'):
        return cv2.flip(im, 0)

Camera = 0

# Recebe imagem da câmera ligada ao dispositivo
Cap = cv2.VideoCapture(Camera)

# Se não houver câmeras conectadas, encerrar aplicação
if(Cap == None):
    quit()

VideoLargura = int(Cap.get(3))
VideoAltura = int(Cap.get(4))

# Mostrando menu de opções
print('1 - Filtro Gaussian Blur\n'
      '2 - Filtro Canny\n'
      '3 - Filtro Sobel\n'
      '4 - Ajuste de Brilho\n'
      '5 - Ajuste de Contraste\n'
      '6 - Negativo da Imagem\n'
      '7 - Converter em Tons de Cinza\n'
      '8 - Redimensionamento de Vídeo\n'
      '9 - Rotação em 90 graus\n'
      'H - Espelhamento de Vídeo Horizontal\n'
      'V - Espelhamento de Vídeo Vertical\n'
      'G - Gravação de Vídeo\n'
      'Esc - Encerrar Programa')

Operacao = 'E'
Comando = True
Indicador = True
Indicador2 = True
Indicador3 = True
Gravacao = False

while(Comando):

    # Lendo tecla pressionada pelo usuário
    Tecla = cv2.waitKey(1)
    ret, Imagem = Cap.read()

    # Se não houve nenhuma tecla pressionado, então a imagem resultado = imagem original
    if(Operacao == 'E'):
        cv2.imshow('Imagem Original: ', Imagem)
        ret2, NovaImagem = Cap.read()
        cv2.imshow('Imagem Resultado: ', NovaImagem)
    
    else:
        cv2.imshow('Imagem Original: ', Imagem)    
        NovaImagem = Cabecalho(Operacao, Imagem, Indicador, Indicador2, Indicador3)
        cv2.imshow('Imagem Resultado: ', NovaImagem)
        if(Operacao == 4):
            Indicador = False
        elif(Operacao == 5):
            Indicador2 = False
        elif(Operacao == 1):
            Indicador3 = False

    # Se estivermos gravando, devemos colocar a imagem editada como frame do vídeo
    if(Gravacao):
        Resultado.write(NovaImagem)

    # Operação de filtro gaussiano
    if(Tecla == ord('1')):
        Operacao = 1
             
    # Operação de filtro Canny
    elif(Tecla == ord('2')):
        Operacao = 2

    # Operação de filtro Sobel
    elif(Tecla == ord('3')):
        Operacao = 3

    # Operação de ajuste de brilho
    elif(Tecla == ord('4')):
        Operacao = 4

    # Operação de ajuste de contraste
    elif(Tecla == ord('5')):
        Operacao = 5

    # Operação de negativo da imagem
    elif(Tecla == ord('6')):
        Operacao = 6

    # Operação de converter para tons de cinza
    elif(Tecla == ord('7')):
        Operacao = 7
    
    # Operação de redimensionamento de vídeo
    elif(Tecla == ord('8')):
        Operacao = 8
    
    # Operação de rotação em 90 graus do vídeo
    elif(Tecla == ord('9')):
        Operacao = 9

    # Operação de Espelhamento Horizontal
    elif(Tecla == ord('H') or Tecla == ord('h')):
        Operacao = 'H'
    
    # Operação de Espelhamento Vertical
    elif(Tecla == ord('V') or Tecla == ord('v')):
        Operacao = 'V'
    
    elif(Tecla == ord('G') or Tecla == ord('g')):
        cv2.VideoWriter()
        Tamanho = (VideoLargura, VideoAltura)
        Resultado = cv2.VideoWriter('Video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 20.0, Tamanho)
        Gravacao = True
        
    # Encerra aplicação
    elif(Tecla == 27):
        Comando = False
        Cap.release()
        if(Gravacao):
            Resultado.release()
        cv2.destroyAllWindows()