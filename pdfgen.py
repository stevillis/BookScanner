# coding: utf-8

# ****************************************************************************
# * Software: Módulo para criação de arquivos no formato PDF                 *
# * Versão:   0.2.8                                                          *
# * Data:     01-05-2018                                                     *
# * Última Atualização: 01-05-2018                                           *
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

import datetime

from fpdf import FPDF


class PDFGen(FPDF):
    def __init__(self):
        """ Construtor da classe """

        super(PDFGen, self).__init__(orientation='L', unit='mm', format='a3')

        self.now = datetime.datetime.now()  # Obtém data e hora atuais
        # Adiciona um 0 ao dia atual se este tiver apenas um dígito. Ex: Dia 1 vira dia 01
        self.day = '0' + str(self.now.day) if len(str(self.now.day)) == 1 else str(self.now.day)
        # Adiciona um 0 ao mês atual se este tiver apenas um dígito. Ex: Jan (mês 1) vira mês 01
        self.month = '0' + str(self.now.month) if len(str(self.now.month)) == 1 else str(self.now.month)
        self.year = str(self.now.year)  # Ano atual

        # self.title = str(self.day) + str(self.month) + str(self.year)  # Título do PDF
        self.logo = 'logo_ifmt.png'  # Caminho do logo do PDF

        # self.add_page(orientation='L') # orientation: P (Portrait) ou L (Landscape)
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
        # self.set_font('Arial', 'B', 14)  # Fonte Arial, negrito, tamanho 14
        # self.cell(80)  # Área retangular (Move para a direita 80 pixels)
        # self.cell(30, 10, self.title)  # Define o título da página
        # self.ln(20)  # Quebra a linha com espaçamento 20 pixels

    def footer(self):
        '''
        Rodapé da página.
        :return: None.
        '''
        self.set_y(-15)  # 1.5 cm de distância da parte inferior da página
        self.set_font('Arial', 'I', 8)  # Fonte Arial, Itálico, tamanho 8
        # self.image('logo_ifmt.png', x=0, y=0, h=10)
        self.cell(0, 10, 'Digitalizado em: {}/{}/{}'.format(self.day, self.month, self.year))
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')  # Número da página

    def add_image(self, diretorio, image, x=None, y=None, w=0, h=0):
        '''
        Adiciona uma imagem a uma nova página do PDF.
        :param diretorio: Diretório onde a imagem se encontra.
        :param image: Imagem a ser inserida na página
        :param x: Coordenada x, começando no canto superior esquerdo.
        :param y: Coordenada y, começando no canto superior esquerdo.
        :param w: Largura da imagem. Se não especificada, é assumida a largura original da imagem.
        :param h: Altura da imagem. Se não especificada, é assumida a altura original da imagem.
        :return: None
        '''
        self.add_page()
        self.image(diretorio + image, x, y, w, h)

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
