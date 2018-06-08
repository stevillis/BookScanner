# coding: utf-8

# ****************************************************************************
# * Software: Captura imagens utilizando um Raspberry Pi 3 e uma Raspberry   *
# *           Pi Camera v2.1. Processa imagens utilizando OpenCV 3.3.0. Cria *
# *           e salva arquivos PDF com as imagens processadas. Envia os      *
# *           arquivos PDF para uma memória externa (Ex: pen drive).         *
# * Versão:   0.7.3                                                          *
# * Data:     12-12-2017                                                     *
# * Última Atualização: 08-06-2018                                           *
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

# Adição manual de PATH dos módulos não built-in utilizados
import sys

sys.path.append('/home/pi/.local/lib/python3.5/site-packages')
sys.path.append('/usr/local/lib/python3.5/dist-packages')

# Módulos para operações do sistema operacional e data
import datetime
import os
import shutil

# Módulos para manipulação da imagem, OpenCV e Raspberry PiCamera
from pyimagesearch import imutils
from pyimagesearch.transform import four_point_transform
import cv2
# from picamera.array import PiRGBArray
# from picamera import PiCamera

from pdfgen import PDFGen  # Módulo para criação de PDF

# Módulo para configuração das GPIOs
# import RPi.GPIO as GPIO

# Módulo do lcd
from lcd_module.main_lcd import escreve_lcd


class Scanner:
    def __init__(self):
        """ Construtor da classe Scanner: inicializa constantes e configura gpios
        """

        # ========== ========== # Inicialização das variáveis ========== ==========
        escreve_lcd('Inicializando...')
        print('Inicializando...')

        '''
        Usado para câmera usb
        if cv2.VideoCapture(0).isOpened():
            cv2.VideoCapture(0).release()
        self.cap = cv2.VideoCapture(0)  
        print(self.cap)'''

        self.AGUARDANDO = 'Aguardando \ninstrucao'  # Mensagem padrão após cada operação realizada

        self._criar_diretorios('imagens', 'pdfs')  # Cria o diretório para imagens e pdfs caso não existam.

        # Variável de controle de evento USB
        self.estado_usb = ''
        self.nome_pdf_criado = ''

        self._remover_conteudo_diretorio('./imagens',
                                         './pdfs')  # Apaga o conteúdo presente nos diretórios imagens e pdfs

        # ========== ========== # Configuração dos pinos do Raspberry ========== ==========

        '''# Configura os pinos para a numeração de GPIOs
        GPIO.setmode(GPIO.BCM)

        #
        # Configura as GPIOs como entrada
        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Adiciona detecção de evento nas GPIOs, com delay de 300ms
        GPIO.add_event_detect(21, GPIO.FALLING, callback=self.capturar_imagem,
                              bouncetime=1000)
        GPIO.add_event_detect(20, GPIO.FALLING, callback=self.criar_pdf,
                              bouncetime=1000)
        GPIO.add_event_detect(16, GPIO.FALLING, callback=self.apagar_ultima_imagem,
                              bouncetime=1000)
        '''
        # ========== ========== # Configuração dos pinos do Raspberry ========== ==========

        escreve_lcd(self.AGUARDANDO)
        print(self.AGUARDANDO)

        # ========== ========== Definições dos métodos ========== ==========

    def capturar_imagem(self, channel):
        '''
        Faz a captura da imagem e o processamento para detecção de bordas e cotornos. Direciona a imagem para a
        aplicação de filtros e armazenamento da imagem.
        :param channel: Utilizado para tratamento de evento com o botão (Ignorado no processamento de imagem).
        :return: None.

        escreve_lcd('Capturando \nimagem')
        print('Capturando \nimagem')
        try:
            # Inicializa a câmera
            camera = PiCamera()
            # camera.stop_preview() # Finaliza o preview da imagem
            camera.resolution = (1920, 1080)  # resolução da imagem 1920x1080

            captura = PiRGBArray(camera)  # Instância do formato de captura a ser obtido.

            camera.capture(captura, format="bgr")  # Configura a captura da câmera para o formato BGR.
            img = captura.array  # Converte o formato da imagem para o formato a ser usado com o OpenCV.
            # cv2.imshow('Captura', img)
            # cv2.waitKey(5000)
            # cv2.destroyAllWindows()

            escreve_lcd('Processando \nimagem')
            print('Processando \nimagem')

            img_rotacionada = ndimage.rotate(img, 180)  # Rotaciona a imagem original em 180º
            img_recortada = self._detectar_contornos(img_rotacionada)
            # Enquanto não detectar 4 pontos (aproximação de um retângulo) de contorno na imagem, não prossegue
            if img_recortada is False:
                escreve_lcd('Ajuste a posicao\nda camera')
                print('Ajuste a posicao\n da camera')
            else:  # Em caso de detecção das bordas da folha, aplicam-se filtros na imagem e salva a mesma
                self._aplicar_filtros(img_recortada)

            camera.close()  # Finaliza o processo de captura da câmera
        except:
            escreve_lcd('Erro de captura')
            print('Erro de captura')
            '''
        pass

    def _detectar_contornos(self, img):
        '''
        Detecta bordas e contornos na imagem, retornando a imagem recortada nas dimensões do contorno mais externo
        detectado.
        :param img: Utilizada para detecção de bordas.
        :return: A imagem recortada com as dimensões onde contorno mais exterior foi detectado na imagem ou False caso
        não seja detectado um contorno em volta da página.
        '''

        # Redimensionamento da imagem para melhor processamento.
        ratio = img.shape[0] / 500.0  # Proporção para redimensionamento.
        img_reduzida = imutils.resize(img, height=500)  # Redimensionamento proporcional.

        # Conversão da imagem para escala monocromática
        img_gray = cv2.cvtColor(img_reduzida, cv2.COLOR_BGR2GRAY)
        # Aplicação do filtro Gaussiano para melhorar detecção de bordas.
        img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
        img_canny = cv2.Canny(img_blur, 75, 200)  # Detecta bordas na imagem

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

        # Filtro Gaussiano aplicado para atenuação de ruídos na imagem
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Conversão da imagem para a escala monocromática
        # img_blur = cv2.GaussianBlur(img_blur, (1,1), 0)

        # Equalização de luminosidade da imagem
        # clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(1,1))
        # img_clahe = clahe.apply(img_gray)

        # Threshold adaptativo aplicado para deixar a imagem com aspecto de scaneada
        # img_thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 65, 10)    

        # cv2.imshow('Resultado', img_gray)
        # cv2.waitKey(5000)
        # cv2.destroyAllWindows()

        self._salvar_imagem(img_gray)

    def _salvar_imagem(self, img):
        '''
        Faz o armazenamento da imagem.
        :param img: Imagem a ser salva.
        :return: None.
        '''

        escreve_lcd('Salvando \nimagem')
        print('Salvando \nimagem')
        nome_arquivo = 'imagens/foto-' + self._obter_data() + '.jpg'

        # Verifica se o nome de arquivo já existe
        if os.path.exists(nome_arquivo):  # Se existir, atualiza data/hora
            nome_arquivo = 'imagens/foto-' + self._obter_data() + '.jpg'
            cv2.imwrite(nome_arquivo, img)
        else:
            cv2.imwrite(nome_arquivo, img)

        escreve_lcd('Imagem salva')
        print('Imagem salva')
        escreve_lcd(self.AGUARDANDO)
        print(self.AGUARDANDO)

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
                list_temp.append(
                    i)  # Adiciona os elementos da string que são diferentes de . (ponto) e para caso encontre . (ponto)
            else:
                break
        return ''.join(list_temp)  # Converte a lista para string

    def _criar_diretorios(self, *args):
        '''
        Cria um diretório para as imagens e para os PDFs.
        :param args: Lista com nomes de diretórios a serem criados.
        :return: None.
        '''

        for diretorio in args:
            if not os.path.exists(diretorio):  # Se o diretório não existir, então pode ser criado.
                try:
                    print('Criando diretório', diretorio)
                    os.makedirs(diretorio)  # Cria um diretório com o nome especificado
                except OSError:  # Erro ao criar o diretório                    
                    print('Não foi possível criar o diretório')

    def _remover_conteudo_diretorio(self, *args):
        '''
        Remove o conteúdo diretório especificado. A exclusão dos arquivos presentes no mesmo, é permanente.
        :return:  None.
        '''

        for diretorio in args:  # Para cada diretório, remove o conteúdo presente no mesmo
            for file in os.listdir(diretorio):  # Para cada arquivo presente no diretório, remove o mesmo
                os.remove(diretorio + '/' + file)
                print(file, 'removido')

    def criar_pdf(self, channel):
        '''
        Cria um PDF com as imagens capturadas.
        :param diretorio: Diretório onde o PDF deve ser salvo.
        :param nome: Nome do PDF a ser salvo.
        :return: None
        '''
        lista_imagens = self._listar_imagens('./imagens')
        if len(lista_imagens) == 0:  # Verifica se existe pelo menos uma imagem para criar o PDF.
            escreve_lcd('Precisa de pelo\nmenos uma imagem')
            print('Precisa de pelo\nmenos uma imagem')
            escreve_lcd(self.AGUARDANDO)
            print(self.AGUARDANDO)
        # elif len(os.listdir('./pdfs')) > 0: # Verifica se já existe pelo menos um PDF na pasta pdfs
        #    print(self.nome_pdf_criado, 'já existe')
        #    self._copiar_pdf_pendrive() # Se o arquivo já existe, então copia para o pendrive
        else:
            escreve_lcd('Criando PDF com\nas imagens')
            print('Criando PDF com\nas imagens')
            pdf = PDFGen()  # Objeto do tipo PDFGen usar os metódos de criação do PDF.
            # Adiciona todas as imagens presentes na lista lista_imagens, uma em cada página do PDF.
            for img in lista_imagens:
                pdf.add_image(diretorio='./imagens', imagem=img, w=405, h=265)

            # Tenta salvar o PDF. Caso o nome do arquivo já exista, um novo nome para o arquivo é criado.
            try:
                nome_pdf = 'pdf-' + self._obter_data() + '.pdf'
                self.nome_pdf_criado = nome_pdf
                pdf.salva_pdf(diretorio='pdfs/', nome=nome_pdf)
                escreve_lcd('PDF criado com \nsucesso')
                print('PDF criado com \nsucesso')

                tamanho_pdf = self._get_size_arquivo('pdfs/' + nome_pdf)
                escreve_lcd('Tamanho PDF:\n{:.2f} MB'.format(tamanho_pdf))
                print('Tamanho PDF:\n{:.2f} MB'.format(tamanho_pdf))

                self._copiar_pdf_pendrive()  # Copia o PDF para o pendrive
            except PermissionError as pe:
                escreve_lcd('Erro ao criar\n PDF')
                print(pe)

    def _copiar_pdf_pendrive(self):
        '''
        Copia o arquivo PDF criado na pasta pdfs para a unidade de armazenamento conectada à USB.
        :return: None.
        '''
        montou = self._montar_unidade()
        while not montou:
            escreve_lcd('Insira o\npendrive')
            print('Insira o\npendrive')
            montou = self._montar_unidade()
        else:
            try:
                escreve_lcd('Copiando PDF \npara o pendrive')
                print('Copiando PDF \npara o pendrive')

                pdf = './pdfs/' + self.nome_pdf_criado
                print(pdf)

                nome_pendrive = str(os.listdir('/media/pi/')[0])  # Obtém o nome do pendrive
                print('nome pendrive', nome_pendrive)

                os.system(
                    'sudo cp -a ' + pdf + ' /media/pi/' + nome_pendrive + '/')  # Copia o PDF para o

                escreve_lcd('PDF copiado para\no pendrive')
                print(self.nome_pdf_criado, 'copiado')

                # self._remover_conteudo_diretorio('./imagens', './pdfs') # Apaga o conteúdo presente nos diretórios imagens e pdfs

                escreve_lcd(self.AGUARDANDO)
                print(self.AGUARDANDO)
            except OSError as ose:
                escreve_lcd(str(ose))
                print(ose)

    def _get_size_arquivo(self, arquivo):
        '''
        Obtém o tamanho de um arquivo em MegaBytes.
        :param arquivo: O arquivo a ser determinado o tamanho.
        :return: O tamanho do arquivo em MegaBytes.
        '''
        try:
            BtoMB = (1 / (1024 * 1024))  # Conversão de Bytes para MegaBytes
            tamanho = os.path.getsize(arquivo)  # Tamanho do arquivo em Bytes
            tamanho = tamanho * BtoMB  # Converte Bytes para MegaBytes
            return tamanho
        except OSError as oes:
            print(oes)

    def _get_size_diretorio(self, diretorio):
        '''
        Obtém a quantidade de memória livre de um diretório em MB.
        :param diretorio: Diretório a ser determinado a quantidade de memória livre.
        :return: A quantidade de memória livre em MB.
        '''
        # total: Quantidade total de memória.
        # used: Memória usada.
        # free: Memória livre.

        BtoMB = (1 / (1024 * 1024))  # Conversão de Bytes para MegaBytes.
        res = shutil.disk_usage(diretorio)  # Retorna usage(total, used, free)

        free = res[2] * BtoMB  # Converte a memória livre de Bytes para MegaBytes

        return free  # Retorna a quantidade de memória livre em MB

    def _finalizar_scan(self):
        '''
        Reinicializa o processo de escaneamento, permitindo outro ser iniciado ou a finalização do programa.
        :return: None.
        '''
        self._criar_diretorios('imagens', 'pdfs',
                               '/home/pi/usb')  # Cria diretórios para imagens, pdfs e usb caso não existam
        # Apaga o diretório com as imagens capturadas para gerar o PDF corrente.

        # Variável de controle de evento USB
        self.nome_pdf_criado = ''

    def _listar_imagens(self, diretorio):
        '''
        Lista as imagens presentes no diretório especificado e as ordena em uma lista.
        :param diretorio: Diretório onde as imagens devem ser buscadas.
        :return: Uma lista ordenada com os nomes das imagens em ordem ascendente.
        '''
        # Cria uma lista com todos os arquivos presentes no diretório especificado.
        lista_imagens = []
        for file in os.listdir(diretorio):
            lista_imagens.append(file)

        lista_imagens.sort()  # Ordena as imagens
        return lista_imagens

    def _montar_unidade(self):
        '''
        Monta uma unidade de armazenamento, se esta estiver conectada à USB, em /media/usb.
        :return: True se a unidade de armazenamento foi montada, False caso contrário e None caso haja alguma exceção.
        '''

        try:
            file = open('boot/usb_temp.txt', 'r')  # Abre o arquivo usb_temp.txt em modo de leitura
            estado_usb = file.readline()  # Lê a primeira linha do arquivo usb_temp.txt

            if estado_usb == 'conectado':
                escreve_lcd('Pendrive\ndetectado')
                print('Pendrive\ndetectado')
                nome_pendrive = str(os.listdir('/media/pi/')[0])  # Obtém o nome do pendrive
                if os.path.ismount('/media/pi/' + nome_pendrive):
                    escreve_lcd('Pendrive\nconectado')
                    print('Pendrive\nconectado')
                    return True
                else:
                    escreve_lcd('Erro ao ler\npendrive')
                    print('Erro ao ler\npendrive')
                    return False
            elif estado_usb == 'desconectado':
                print('desconectado')
                return False
        except IOError as ioe:
            print(ioe)
            print('Erro de leitura/escrita do arquivo usb_temp.txt')
            return None
        except OSError as ose:
            print(ose)
            return None

    def _desmontar_unidade(self):
        '''
        Desmonta uma unidade de armazenamento se esta estiver conectada à USB.
        :return: None.
        '''
        if self.estado_usb == 'conectado':
            try:
                os.system('sudo umount /home/pi/usb')
            except OSError as ose:
                print(ose)
        else:
            print('Unidade de armazenamento desconectada!')

    def apagar_ultima_imagem(self, channel):
        '''
        Apaga a última imagem tirada e gravada na pasta imagens se existir alguma imagem na pasta.
        :param channel: Utilizado para tratamento de evento com o botão (Ignorado neste método).
        :return: None
        '''
        diretorio_imagens = './imagens'
        lista_imagens = self._listar_imagens(diretorio_imagens)
        if len(lista_imagens) == 0:
            escreve_lcd('Nenhuma imagem\na ser excluida')
            print('Nenhuma imagem\na ser excluida')
        else:
            escreve_lcd('Removendo\nultima imagem')
            print('Removendo\nultima imagem')
            os.remove(diretorio_imagens + '/' + lista_imagens[-1])
            print(lista_imagens[-1], 'removido')

        escreve_lcd(self.AGUARDANDO)
        print(self.AGUARDANDO)

    def ligar_desligar_raspberry(self):
        pass
        '''
        Desmonta a unidade de armazenamento, caso esteja montada, e liga/desliga o Raspberry.
        :return: None
        '''
        # self._desmontar_unidade()
        # TODO Configuração de hardware para desligamento do Raspberry.


# ========== ========== Função principal ========== ==========
if __name__ == '__main__':

    scanner = Scanner()  # Cria um objeto scanner para manipular as operações do processamento de imagem.
    while True:  # Executa o programa em um loop infinito, até que se pressione o botão para desligar.
        pass
