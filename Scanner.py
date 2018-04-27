# coding: utf-8

# Import dos pacotes necessários
from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils

# OpenCV e Raspberry PiCamera
import cv2
from scipy import ndimage

# from picamera.array import PiRGBArray
# from picamera import PiCamera

# Módulo do lcd
from lcd_module.main_lcd import escreve_lcd

import datetime
import os
import errno

import RPi.GPIO as GPIO


class Scanner:
    def __init__(self):
        """ Construtor da classe Scanner: inicializa constantes e configura gpios
        """

        escreve_lcd('Inicializando...')

        self.INI_CAMERA = 'Inicializando \ncamera'
        self.AGUARDANDO = 'Aguardando \ninstrucao'

        self.CAP_IMG = 'Capturando \nimagem'
        self.ROT_IMG = 'Rotacionando \nimagem'
        self.REDIM_IMG = 'Redimensionando \na imagem'
        self.SAVE_IMG = 'Salvando \nimagem'

        self.DETECT_BORDAS = 'Detectanto \nbordas...'
        self.DETECT_CONTORNOS = 'Detectando \ncontornos'
        self.N_DETECT_BORDAS = 'Bordas do livro \nnao detectadas'
        self.BORDAS_DETECT = 'Bordas do livro \necontradas'
        self.APLICA_FILTROS = 'Aplicando \nfiltros'

        self.CRIANDO_PDF = 'Criando PDF com\nas imagens'
        self.PDF_CRIADO = 'PDF criado com \nsucesso'

        self.COPIANDO_PENDRIVE = 'Copiando PDF \npara o pendrive'
        self.PDF_COPIADO = 'PDF copiado para\no pendrive'

        self.SCAN_CANCELADO = 'Escaneamento \ncancelado'

        self.CRIANDO_DIRETORIO = 'Criando novo \ndiretorio'

        self.ALERT_POS_CAM = 'Ajuste a posicao\n da camera'
        self.ALERT_DIRETORIO_DUPLICADO = 'Diretorio \nduplicado'

        self.diretorio_pdf = ''
        self.diretorio_img = ''

        # Cria os diretórios para imagens e pdfs
        self.cria_diretorio('images/images-')
        self.cria_diretorio('pdf/pdf-')

        # Inicializa a câmera
        # self.camera = PiCamera()

        # Configura os pinos para a numeração de GPIOs
        GPIO.setmode(GPIO.BCM)

        # Configura as GPIOs como entrada
        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Adiciona detecção de evento nas GPIOs, com delay de 300ms
        GPIO.add_event_detect(21, GPIO.FALLING, callback=self.captura_imagem,
                              bouncetime=300)
        GPIO.add_event_detect(20, GPIO.FALLING, callback=self.cria_pdf,
                              bouncetime=300)
        GPIO.add_event_detect(16, GPIO.FALLING, callback=self.copia_pendrive,
                              bouncetime=300)
        GPIO.add_event_detect(7, GPIO.FALLING, callback=self.cancela_scan,
                              bouncetime=300)

        # Teste de imagem capturada
        # self.img_teste = 'images/page1.jpg'
        self.img_teste = 'images/original1523547772.6299927.jpg'

        escreve_lcd(self.AGUARDANDO)

    # ========== ========== Definições dos métodos ========== ==========

    def captura_imagem(self, channel):
        '''
        :param camera: Instância da Camera usada para capturar a imagem.
        :return: A imagem capturada no formato adequado para o processamento com o OpenCV.
        '''

        # self.camera.start_preview() # inicializa o preview da imagem
        # selfcamera.resolution = (1024, 768) # resolução da imagem

        # captura = PiRGBArray(self.camera)  # Instância do formato de captura a ser obtido.

        # camera.capture(captura, format="bgr")  # Configura a captura da câmera para o formato BGR.
        # img = captura.array  # Converte o formato da imagem para o formato a ser usado com o OpenCV.
        # self.img_original = img.copy()  # Faz uma cópia da imagem capturada e inicializa o atributo img_original.

        # Área de teste
        escreve_lcd(self.CAP_IMG)
        img_original = cv2.imread(self.img_teste)  # Faz a leitura de uma imagem teste

        escreve_lcd(self.ROT_IMG)
        img_rotacionada = ndimage.rotate(img_original, 180)  # Rotaciona a imagem original em 180º

        img_recortada = scanner.detecta_contornos(img_rotacionada)
        while img_recortada is False:  # Enquanto não detectar 4 pontos (aproximação de um retângulo) de contorno na imagem        
            escreve_lcd(scanner.N_DETECT_BORDAS)
            escreve_lcd(scanner.ALERT_POS_CAM)

            img_original = cv2.imread(scanner.img_teste)
            img_recortada = scanner.detecta_contornos(img_original)
        else:
            escreve_lcd(scanner.BORDAS_DETECT)

        # Chama a função para aplicar filtos (processo final)
        img_filtrada = scanner.aplica_filtros(img_recortada)

        # Área de teste       

        # cv2.imwrite('original' + str(datetime.datetime.now()) + '.jpg',
        # img)  # Salva a imagem com o nome composto com a data.

    def salva_imagem(self, img):
        '''
        :param img: Imagem a ser salva
        :return: None
        '''

        nome_arquivo = self.diretorio_img + '/foto-' + self.get_date() + '.jpg'

        # Verifica se o nome de arquivo já existe
        if os.path.exists(nome_arquivo):  # Se existir, atualiza data/hora
            nome_arquivo = self.diretorio_img + '/foto-' + self.get_date() + '.jpg'
            cv2.imwrite(nome_arquivo, img)
        else:
            cv2.imwrite(nome_arquivo, img)

    def detecta_contornos(self, img):
        '''
        Detecta bordas e contornos na imagem, retornando a imagem recortada nas dimensões do contornos mais externo
        detectado.
        :param img: Utilizada para detecção de bordas.
        :return: A imagem recortada com as dimensões onde contorno mais exterior foi detectado na imagem.
        '''

        # Redimensionamento da imagem para melhor processamento.
        escreve_lcd(self.REDIM_IMG)
        ratio = img.shape[0] / 500.0  # Proporção para redimensionamento.
        img_reduzida = imutils.resize(img, height=500)  # Redimensionamento proporcional.

        escreve_lcd(self.DETECT_BORDAS)
        # Conversão da imagem para escala monocromática
        img_gray = cv2.cvtColor(img_reduzida, cv2.COLOR_BGR2GRAY)
        # Aplicação do filtro Gaussiano para melhorar detecção de bordas.
        img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
        img_canny = cv2.Canny(img_blur, 75, 200)  # Detecta bordas na imagem

        escreve_lcd(self.DETECT_CONTORNOS)
        # Detecta os contornos da imagem e seleciona os 5 maiores contornos detectados.
        (_, cnts, _) = cv2.findContours(img_canny.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        # Iteração entre os contornos detectados para determinar qual representa o contorno da página.
        for c in cnts:
            peri = cv2.arcLength(c, True)  # Aproximação do contorno por arco.
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)  # Aproximação poligonal.

            # Se o contorno aproximado tem 4 pontos, então os pontos correspondem às bordas da imagem.
            if len(approx) == 4:
                contornos = approx
                img_recortada = four_point_transform(img, contornos.reshape(4, 2) * ratio)

                return img_recortada  # Retorna os pontos que definem as dimensões da borda e a
            else:
                return False

    def aplica_filtros(self, img):
        escreve_lcd(self.APLICA_FILTROS)

        # Filtro Gaussiano aplicado para atenuação de ruídos na imagem
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Conversão da imagem para a escala monocromática
        # img_blur = cv2.GaussianBlur(img_blur, (1,1), 0)

        # Equalização de luminosidade da imagem
        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(3,3))
        # img_clahe = clahe.apply(img_gray)

        # Threshold adaptativo aplicado para deixar a imagem com aspecto de scaneada
        # img_thresh = cv2.adaptiveThreshold(img_clahe, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        # cv2.THRESH_BINARY, 13, 10)

        escreve_lcd(self.AGUARDANDO)

        cv2.imshow('Resultado', img_gray)
        # cv2.imwrite(str(time.time())+'.jpg', img_gray)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()

        self.salva_imagem(img_gray)

    def get_date(self):
        temp = str(datetime.datetime.now())  # Obtém data e hora atual.
        temp = temp.replace(' ', ':')  # Sobrescreve espaço e coloca :
        temp = temp.replace(':', '-')  # Sobrescreve : e coloca -
        list_temp = []
        for i in temp:
            if i != '.':
                list_temp.append(i)  # Adiciona os elementos da string que são diferentes de . e para caso encontre .
            else:
                break
        return ''.join(list_temp)  # Converte a lista para string

    def cria_diretorio(self, tipo):
        escreve_lcd(self.CRIANDO_DIRETORIO)

        nome_diretorio = tipo + self.get_date()
        print(nome_diretorio)
        if not os.path.exists(nome_diretorio):
            try:
                os.makedirs(nome_diretorio)
                if tipo.startswith('pdf'):
                    self.diretorio_pdf = nome_diretorio
                else:
                    self.diretorio_img = nome_diretorio
            except OSError as ose:
                if ose.errno != errno.EEXIST:
                    escreve_lcd(self.ALERT_DIRETORIO_DUPLICADO)
                    self.cria_diretorio()

    def cria_pdf(self, channel):
        escreve_lcd(self.CRIANDO_PDF)
        # TODO implementar criação do PDF com as imagens
        escreve_lcd(self.PDF_CRIADO)

    def copia_pendrive(self, channel):
        escreve_lcd(self.COPIANDO_PENDRIVE)
        # TODO implementar detecção de pendrive e cópia de arquivo
        escreve_lcd(self.PDF_COPIADO)

    def cancela_scan(self, channel):
        escreve_lcd(self.SCAN_CANCELADO)


# ========== ========== Função principal ========== ==========
if __name__ == '__main__':

    # Chama a função para capturar imagem
    # img_original = captura_imagem(camera)

    scanner = Scanner()  # Cria um objeto scanner para manipular as operações do processamento de imagem.
    while True:
        pass
    # img_original = cv2.imread(scanner.img_teste)  # Faz a leitura de uma imagem teste
    # img_rotacionada = ndimage.rotate(img_original, 180)  # Rotaciona a imagem original em 180º

    # Chama a função para detectar bordas
    """img_recortada = scanner.detecta_contornos(img_rotacionada)
    while img_recortada is False:  # Enquanto não detectar 4 pontos (aproximação de um retângulo) de contorno na imagem        
        escreve_lcd(scanner.N_DETECT_BORDAS)
        escreve_lcd(scanner.ALERT_POS_CAM)
        img_original = cv2.imread(scanner.img_teste)
        img_recortada = scanner.detecta_contornos(img_original)
    else:        
        escreve_lcd(scanner.BORDAS_DETECT)"""

    # Chama a função para aplicar filtos (processo final)
    # img_filtrada = scanner.aplica_filtros(img_recortada)
    # print(scanner.get_date())
