# coding: utf-8

# ****************************************************************************
# * Software: Captura imagens utilizando um Raspberry Pi 3 e uma Raspberry   *
# *           Pi Camera v2.1. Processa imagens utilizando OpenCV 3.3.0. Cria *
# *           e salva arquivos PDF com as imagens processadas. Envia os      *
# *           arquivos PDF para uma memória externa (Ex: pen drive).         *
# * Versão:   0.5.2                                                          *
# * Data:     01-05-2018                                                     *
# * Última Atualização: 05-05-2018                                           *
# *                                                                          *
# * Autores: Ed' Wilson T. Ferreira                                          *
# *          Gabriel Bastos                                                  *
# *          Pammella Roberta                                                *
# *          Stévillis Sousa                                                 *
# * Sobre: Desenvolvido pelo Grupo de Pesquisa em Redes e Segurança - GPRS,  *
# *        Instituto Federal de Educação, Ciência e Tecnologia de Mato       *
# *        Grosso, Campus Cel. Octayde Jorge da Silva                        *
# * Nome do Projeto: Scanner de livro: Um protótipo de baixo custo para      *
# *                  contribuir na preservação da informação.                *
# ****************************************************************************

# Módulos para operações do sistema operacional e data
import datetime
import os

# Módulos para manipulação da imagem, OpenCV e Raspberry PiCamera
from scipy import ndimage
from pyimagesearch import imutils
from pyimagesearch.transform import four_point_transform
import cv2
# from picamera.array import PiRGBArray
# from picamera import PiCamera

from pdfgen import PDFGen  # Módulo para criação de PDF

# Módulo para configuração das GPIOs
# import RPi.GPIO as GPIO

# Módulo do lcd
# from lcd_module.main_lcd import escreve_lcd

import pyudev  # Módulo para monitoramento de USB

from threading import Thread  # Módulo para processamento paralelo


class Scanner():
    def __init__(self):
        """ Construtor da classe Scanner: inicializa constantes e configura gpios
        """
        super().__init__()

        # ========== ========== # Inicialização das variáveis ========== ==========
        # escreve_lcd('Inicializando...')

        self.INI_CAMERA = 'Inicializando \ncamera'
        self.AGUARDANDO = 'Aguardando \ninstrucao'

        self.CAP_IMG = 'Capturando \nimagem'
        self.ROT_IMG = 'Rotacionando \nimagem'
        self.REDIM_IMG = 'Redimensionando \na imagem'
        self.SAVE_IMG = 'Salvando \nimagem'
        self.IMG_SAVE = 'Imagem salva'

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

        self.CRIANDO_DIRETORIO_IMG = 'Criando direto-\nrio de imagens'

        self.ALERT_POS_CAM = 'Ajuste a posicao\n da camera'
        self.ALERT_DIRETORIO_DUPLICADO = 'Diretorio \nduplicado'
        self.ALERT_NOME_PDF_DUPLICADO = 'Nome PDF \nduplicado'
        self.ALERT_PDF_SEM_CONTEUDO = 'Precisa de pelo\nmenos uma imagem'

        self._cria_diretorios('imagens', 'pdfs')  # Cria o diretório para imagens
        self._remover_imgs()
        self._remover_pdfs()

        # Variável de controle de evento USB
        # self.estado_usb = ''
        self.nome_pdf_criado = ''

        # Inicializa a câmera
        # self.camera = PiCamera()

        # ========== ========== # Configuração dos pinos do Raspberry ========== ==========
        """
        # Configura os pinos para a numeração de GPIOs
        GPIO.setmode(GPIO.BCM)

        # Configura as GPIOs como entrada
        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Adiciona detecção de evento nas GPIOs, com delay de 300ms
        GPIO.add_event_detect(21, GPIO.FALLING, callback=self.capturar_imagem,
                              bouncetime=300)
        GPIO.add_event_detect(20, GPIO.FALLING, callback=self.criar_pdf,
                              bouncetime=300)
        GPIO.add_event_detect(16, GPIO.FALLING, callback=self.copiar_pdf_pendrive,
                              bouncetime=300)
        GPIO.add_event_detect(7, GPIO.FALLING, callback=self.cancela_scan,
                              bouncetime=300)
        """
        # Teste de imagem capturada
        # self.img_teste = 'images/page1.jpg'
        self.img_teste = 'images/original1523547772.6299927.jpg'

        # escreve_lcd(self.AGUARDANDO)

    """def run(self):
        '''
        Método que é executado quando a Thread é iniciada.
        :return: None
        '''

        self._evento_usb()
    """

    # ========== ========== Definições dos métodos ========== ==========

    def capturar_imagem(self, channel):
        '''
        Faz a captura da imagem e o processamento para detecção de bordas e cotornos. Direciona a imagem para a
        aplicação de filtros e armazenamento da imagem.
        :param channel: Utilizado para tratamento de evento com o botão (Ignorado no processamento de imagem).
        :return: None.
        '''

        # self.camera.start_preview() # inicializa o preview da imagem
        # selfcamera.resolution = (1024, 768) # resolução da imagem

        # captura = PiRGBArray(self.camera)  # Instância do formato de captura a ser obtido.

        # camera.capture(captura, format="bgr")  # Configura a captura da câmera para o formato BGR.
        # img = captura.array  # Converte o formato da imagem para o formato a ser usado com o OpenCV.
        # self.img_original = img.copy()  # Faz uma cópia da imagem capturada e inicializa o atributo img_original.

        # Área de teste
        # escreve_lcd(self.CAP_IMG)
        print(self.CAP_IMG)
        img_original = cv2.imread(self.img_teste)  # Faz a leitura de uma imagem teste

        # escreve_lcd(self.ROT_IMG)
        print(self.ROT_IMG)
        img_rotacionada = ndimage.rotate(img_original, 180)  # Rotaciona a imagem original em 180º

        img_recortada = self._detectar_contornos(img_rotacionada)
        # Enquanto não detectar 4 pontos (aproximação de um retângulo) de contorno na imagem, não prossegue
        while img_recortada is False:
            # escreve_lcd(scanner.N_DETECT_BORDAS)
            print(scanner.N_DETECT_BORDAS)
            # escreve_lcd(scanner.ALERT_POS_CAM)
            print(scanner.ALERT_POS_CAM)

            img_original = cv2.imread(scanner.img_teste)
            img_recortada = scanner.detectar_contornos(img_original)
        else:
            # escreve_lcd(scanner.BORDAS_DETECT)
            print(scanner.BORDAS_DETECT)

            # Chama a função para aplicar filtos (processo final)
            self._aplicar_filtros(img_recortada)

    def _detectar_contornos(self, img):
        '''
        Detecta bordas e contornos na imagem, retornando a imagem recortada nas dimensões do contorno mais externo
        detectado.
        :param img: Utilizada para detecção de bordas.
        :return: A imagem recortada com as dimensões onde contorno mais exterior foi detectado na imagem ou False caso
        não seja detectado um contorno em volta da página.
        '''

        # Redimensionamento da imagem para melhor processamento.
        # escreve_lcd(self.REDIM_IMG)
        print(self.REDIM_IMG)
        ratio = img.shape[0] / 500.0  # Proporção para redimensionamento.
        img_reduzida = imutils.resize(img, height=500)  # Redimensionamento proporcional.

        # escreve_lcd(self.DETECT_BORDAS)
        print(self.DETECT_BORDAS)
        # Conversão da imagem para escala monocromática
        img_gray = cv2.cvtColor(img_reduzida, cv2.COLOR_BGR2GRAY)
        # Aplicação do filtro Gaussiano para melhorar detecção de bordas.
        img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
        img_canny = cv2.Canny(img_blur, 75, 200)  # Detecta bordas na imagem

        # escreve_lcd(self.DETECT_CONTORNOS)
        print(self.DETECT_CONTORNOS)
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

    def _aplicar_filtros(self, img):
        '''
        Aplica filtros à imagem para melhorar a qualidade da imagem e salva a imagem.
        :param img: Imagem à ser processada.
        :return: None.
        '''
        # escreve_lcd(self.APLICA_FILTROS)
        print(self.APLICA_FILTROS)

        # Filtro Gaussiano aplicado para atenuação de ruídos na imagem
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Conversão da imagem para a escala monocromática
        # img_blur = cv2.GaussianBlur(img_blur, (1,1), 0)

        # Equalização de luminosidade da imagem
        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(3,3))
        # img_clahe = clahe.apply(img_gray)

        # Threshold adaptativo aplicado para deixar a imagem com aspecto de scaneada
        # img_thresh = cv2.adaptiveThreshold(img_clahe, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        # cv2.THRESH_BINARY, 13, 10)

        # escreve_lcd(self.AGUARDANDO)
        print(self.AGUARDANDO)

        cv2.imshow('Resultado', img_gray)
        # cv2.imwrite(str(time.time())+'.jpg', img_gray)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()

        self._salvar_imagem(img_gray)

    def _salvar_imagem(self, img):
        '''
        Faz o armazenamento da imagem.
        :param img: Imagem a ser salva.
        :return: None.
        '''

        # escreve_lcd(self.SAVE_IMG)
        print(self.SAVE_IMG)
        nome_arquivo = 'foto-' + self._obter_data() + '.jpg'

        # Verifica se o nome de arquivo já existe
        if os.path.exists(nome_arquivo):  # Se existir, atualiza data/hora
            nome_arquivo = 'foto-' + self._obter_data() + '.jpg'
            cv2.imwrite(nome_arquivo, img)
        else:
            cv2.imwrite(nome_arquivo, img)

        # escreve_lcd(self.IMG_SAVE)
        print(self.IMG_SAVE)

    def _obter_data(self):
        '''
        Obtém data, hora, minutos e segundos atuais.
        :return: Uma string no formato AAAA-MM-DD-HH-mm-ss.
        '''
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

    def _cria_diretorios(self, *args):
        '''
        Cria um diretório para as imagens e para os PDFs.
        :param args: Lista com nomes de diretórios a serem criados.
        :return: None.
        '''

        for diretorio in args:
            # escreve_lcd(self.CRIANDO_DIRETORIO_IMG)
            print(self.CRIANDO_DIRETORIO_IMG)

            if not os.path.exists(diretorio):  # Se o diretório não existir, então pode ser criado.
                try:
                    os.makedirs(diretorio)  # Cria um diretório com o nome gerado.
                except OSError:  # Caso o diretório exista, é feita a tentativa de criar um diretório com o nome atualizado.
                    #  escreve_lcd(self.ALERT_DIRETORIO_DUPLICADO)
                    print('Não foi possível criar o diretório')
                    pass

    def _remover_imgs(self):
        '''
        Remove o diretório especificado e ignora o erro de exclusão de arquivos somente de leitura. A exclusão do
        diretório, assim como dos arquivos presentes no mesmo, é permanente.
        :return:  None.
        '''
        diretorio_imgs = './imagens'
        for file in os.listdir(diretorio_imgs):
            os.remove(diretorio_imgs + '/' + file)
            print(file, 'removido')

    def _remover_pdfs(self):
        '''
        Remove todos os arquivos PDF do diretório pdfs.
        :return: None.
        '''
        diretorio_pdf = './pdfs'
        for file in os.listdir(diretorio_pdf):
            os.remove(diretorio_pdf + '/' + file)
            print(file, 'removido')

    def criar_pdf(self):
        '''
        Cria um PDF com as imagens capturadas.
        :param diretorio: Diretório onde o PDF deve ser salvo.
        :param nome: Nome do PDF a ser salvo.
        :return: None
        '''
        lista_imagens = self._listar_imagens('./imagens')
        print(lista_imagens)
        if len(lista_imagens) == 0:  # Verifica se existe pelo menos uma imagem para criar o PDF.
            # escreve_lcd(self.ALERT_PDF_SEM_CONTEUDO)
            print(self.ALERT_PDF_SEM_CONTEUDO)
        else:
            # escreve_lcd(self.CRIANDO_PDF)
            print(self.CRIANDO_PDF)
            pdf = PDFGen()  # Objeto do tipo PDFGen usar os metódos de criação do PDF.
            # Adiciona todas as imagens presentes na lista lista_imagens, uma em cada página do PDF.
            for img in lista_imagens:
                pdf.add_image(diretorio='./imagens', imagem=img, w=405, h=265)

            # Tenta salvar o PDF. Caso o nome do arquivo já exista, um novo nome para o arquivo é criado.
            try:
                nome_pdf = 'pdf-' + self._obter_data()
                self.nome_pdf_criado = nome_pdf + '.pdf'                
                pdf.salva_pdf(diretorio='pdfs/', nome=nome_pdf)
                print(self.PDF_CRIADO)
            except PermissionError:
                # escreve_lcd(self.ALERT_NOME_PDF_DUPLICADO)
                print(self.ALERT_NOME_PDF_DUPLICADO)
                nome_pdf = 'pdf-' + self._obter_data()
                self.nome_pdf_criado = nome_pdf + '.pdf'
                pdf.salva_pdf(diretorio='pdfs/', nome=nome_pdf)
                print(self.PDF_CRIADO)
            self._copiar_pdf_pendrive()

            # escreve_lcd(self.PDF_CRIADO)
            

    def _copiar_pdf_pendrive(self):
        '''
        Copia o arquivo PDF criado na pasta pdfs para a unidade de armazenamento conectada à USB.
        :return: None.
        '''
        # escreve_lcd(self.COPIANDO_PENDRIVE)
        if self._montar_unidade():
            arquivo = 'pdfs/' + self.nome_pdf_criado
            try:
                print('Copiando', arquivo)
                os.system('sudo cp -r ' + arquivo + ' /media/usb')
                print('PDF copiado!')
            except OSError as ose:
                print(ose)
        else:
            print('Precisa conectar o pen drive!')

        # escreve_lcd(self.PDF_COPIADO)

    def _finalizar_scan(self, channel):
        '''
        Reinicializa o processo de escaneamento, permitindo outro ser iniciado ou a finalização do programa.
        :param channel: Utilizado para tratamento de evento com o botão (Ignorado neste método).
        :return: None.
        '''
        self._cria_diretorios('imagens', 'pdfs')  # Cria o diretório para imagens
        # Apaga o diretório com as imagens capturadas para gerar o PDF corrente.
        self._remover_imgs()
        self._remover_pdfs()  # Apaga todos os arquivos PDF criados no diretório pdfs

        # Variável de controle de evento USB
        # self.estado_usb = ''
        self.nome_pdf_criado = ''

        # escreve_lcd(self.SCAN_CANCELADO)

    def _listar_imagens(self, diretorio):
        '''
        Lista os arquivos com extensão .jpg os ordena em uma lista.
        :param diretorio: Diretório onde as imagens devem ser buscadas.
        :return: Uma lista ordenada com os nomes das imagens em ordem ascendente.
        '''
        # Cria uma lista com todos os arquivos com extensão .jpg presentes no diretório especificado.
        lista_imagens = []
        for file in os.listdir(diretorio):
            lista_imagens.append(file)

        lista_imagens.sort()  # Ordena as imagens
        return lista_imagens

    """def _evento_usb(self):
        '''
        Monitora as portas USBs, esperando um dispositivo de armazenamento ser conetado.
        :return: None.
        '''
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb')

        for device in iter(monitor.poll, None):
            if device.action == 'add':
                print('{} connected'.format(device))
                self.estado_usb = 'conectado'
            if device.action == 'remove':
                print('{} desconnected'.format(device))
                self.estado_usb = 'desconectado'
    """

    def _montar_unidade(self):
        '''
        Monta uma unidade de armazenamento, se esta estiver conectada à USB, em /media/usb.
        :return: True se a unidade de armazenamento foi montada, False caso contrário.
        '''
        # if self.estado_usb == 'conectado':
        try:
            os.system('sudo mount /dev/sda1 /media/usb')
            return True
        except OSError as ose:
            print(ose)
            print('Unidade de armazenamento desconectada!')
            return False

    def _desmontar_unidade(self):
        '''
        Desmonta uma unidade de armazenamento se esta estiver conectada à USB.
        :return: None.
        '''
        # if self.estado_usb == 'conectado':
        try:
            os.system('sudo umont /media/usb')
        except OSError as ose:
            print(ose)
            print('Unidade de armazenamento desconectada!')

    def _desligar_raspberry(self):
        pass
        '''
        Desmonta a unidade de armazenamento, caso esteja montada, e desliga o Raspberry.
        :return: None
        '''
        # self._desmontar_unidade()
        # TODO Configuração de hardware para desligamento do Raspberry.


# ========== ========== Função principal ========== ==========
if __name__ == '__main__':

    scanner = Scanner()  # Cria um objeto scanner para manipular as operações do processamento de imagem.
    # scanner.start() # Inicia a Thread que verifica evento USB
    botao = input('Aguardando instrução: ')
    while botao != 'x':
        if botao == 'a':
            scanner.criar_pdf()
        botao = input('Aguardando instrução: ')
