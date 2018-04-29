# coding: utf-8
import datetime

from fpdf import FPDF


class PDFGen(FPDF):
    def __init__(self):
        """ Construtor da classe """

        super(PDFGen, self).__init__()

        self.now = datetime.datetime.now()  # Obtém data e hora atuais
        self.day = str(self.now.day)  # Dia atual
        # Adiciona um 0 ao mês atual se este tiver apenas um dígito. Ex: Jan (mês 1) vira mês 01
        self.month = '0' + str(self.now.month) if len(str(self.now.month)) == 1 else str(self.now.month)
        self.year = str(self.now.year)  # Ano atual

        self.title = str(self.day) + str(self.month) + str(self.year)  # Título do PDF
        self.logo = 'logo_ifmt.png'  # Caminho do logo do PDF

        # Define um apelido para o número total de páginas. Será substituído quando o documento for fechado
        self.alias_nb_pages()
        # self.add_page()  # Adiciona uma nova página ao documento
        # self.set_font('Times', '', 12)

    def header(self):
        '''
        Cabeçalho da página.
        :return: None
        '''
        self.image(self.logo, 10, 8, 33)  # Logo do PDF
        self.set_font('Arial', 'B', 14)  # Fonte Arial, negrito, tamanho 14
        self.cell(80)  # Área retangular (Move para a direita 80 pixels)
        self.cell(30, 10, self.title)  # Define o título da página
        self.ln(20)  # Quebra a linha com espaçamento 20 pixels

    def footer(self):
        '''
        Rodapé da página. None
        :return:
        '''
        self.set_y(-15)  # 1.5 cm de distância da parte inferior da página
        self.set_font('Arial', 'I', 8)  # Fonte Arial, Itálico, tamanho 8
        # self.image('logo_ifmt.png', x=0, y=0, h=10)
        self.cell(0, 10, 'Digitalizado em: {}/{}/{}'.format(self.day, self.month, self.year))
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')  # Número da página

    def add_image(self, image, x=None, y=None, w=0, h=0):
        '''
        :param image: Imagem a ser inserida na página
        :param x: Coordenada x, começando no canto superior esquerdo.
        :param y: Coordenada y, começando no canto superior esquerdo.
        :param w: Largura da imagem. Se não especificada, é assumida a largura original da imagem.
        :param h: Altura da imagem. Se não especificada, é assumida a altura original da imagem.
        :return: None
        '''
        self.add_page()
        self.image(image, x, y, w, h)

    def get_date(self):
        '''
        Obtém data, hora, minutos e segundos atuais.
        :return: Uma string no formato AAAA-MM-DD-HH-mm-ss
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

    def salva_pdf(self, diretorio, nome):
        '''
        Salva o arquivo PDF no diretório especificado com o nome espcificado.
        :param diretorio: Diretório onde o arquivo PDF deve ser salvo.
        :param nome: Nome do arquivo PDF. Especificar a extensão .pdf é opcional.
        :return: None
        '''
        if '.pdf' in nome:
            self.output(diretorio + nome)
        else:
            self.output(diretorio + nome + '.pdf')


pdf = PDFGen()  # Cria uma instância da classe PDFGen

for x in range(10):
    pdf.add_image('logo_ifmt.png', x=0, y=25)

try:
    pdf.salva_pdf(diretorio='pdfs/', nome='PDF teste2.pdf')
except PermissionError  as pe:
    print(pe)

# for i in range(1, 41):
#    pdf.cell(0, 10, 'Escrevendo o número da linha' + str(i), 0, 1)
