# coding: utf-8

# ****************************************************************************
# * Software: Módulo para criação de arquivos no formato PDF                 *
# * Versão:   0.3.0                                                          *
# * Data:     05-05-2018                                                     *
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

from fpdf import FPDF


class PDFGen(FPDF):
    def __init__(self):
        """ Construtor da classe """

        super(PDFGen, self).__init__(orientation='L', unit='mm', format='a3')

        # Define um apelido para o número total de páginas. Será substituído quando o documento for fechado
        self.alias_nb_pages()

    def add_image(self, diretorio, imagem, x=None, y=None, w=0, h=0):
        '''
        Adiciona uma imagem a uma nova página do PDF.
        :param diretorio: Diretório onde a imagem se encontra.
        :param imagem: Imagem a ser inserida na página
        :param x: Coordenada x, começando no canto superior esquerdo.
        :param y: Coordenada y, começando no canto superior esquerdo.
        :param w: Largura da imagem. Se não especificada, é assumida a largura original da imagem.
        :param h: Altura da imagem. Se não especificada, é assumida a altura original da imagem.
        :return: None
        '''
        self.add_page()
        self.image(diretorio + '/' + imagem, x, y, w, h)

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
