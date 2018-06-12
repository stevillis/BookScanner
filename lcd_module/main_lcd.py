# coding: utf-8

# ****************************************************************************
# * Software: Módulo para escrever mensagens em display LCD 16x2 ou 20x4     *
# * Versão:   0.1.3                                                          *
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

import time

# Pinos de configuração do Raspberry Pi (GPIOs)
lcd_rs = 26
lcd_en = 19
lcd_d4 = 13
lcd_d5 = 6
lcd_d6 = 5
lcd_d7 = 11

# Número de linhas e colunas do display
lcd_columns = 16
lcd_rows = 2


def escreve_lcd(msg):
    '''
    Escreve a mensagem especificada no display.
    :param msg: Mensagem a ser escrita.
    :return: None.
    '''

    # Inicializa o LCD utilizando os pinos definidos acima
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

    lcd.clear()  # Limpa o que tiver escrito no LCD
    lcd.message(msg)  # Escreve a mensagem no LCD
    time.sleep(2)  # Delay de 2s


def limpa_lcd():
    '''
    Apaga a mensagem que estiver escrita no display.
    :return: None.
    '''

    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
    lcd.clear()


if __name__ == '__main__':
    import Adafruit_CharLCD as LCD  # Módulo que implementa as funções de leitura/escrita do LCD

    escreve_lcd('teste')
else:
    import sys

    # Relative import: adding module to the path
    sys.path.insert(0, 'lcd_module')
    import Adafruit_CharLCD as LCD
