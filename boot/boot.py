# coding: utf-8

# ****************************************************************************
# * Software: Script para ligar/desligar o Raspberry.                        *
# * Referência: Youtube. 'RetroPie Add A Power Button / Switch Raspberry Pi 1*
# *             2 3'. <https://www.youtube.com/watch?v=4nTuzIY0i3k>          *
# * Versão:   0.0.1                                                          *
# * Data:     30-04-2018                                                     *
# * Última Atualização: 12-06-2018                                           *
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

import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)  # Configura os pinos com numeração GPIO

GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configura GPIO3 como entrada em nível alto
oldButtonState1 = True  # Inicializa o estado anterior do botão

while True:
    buttonState1 = GPIO.input(3)  # Guarda o estado atual do botão

    # Verifica se o botão foi pressionado
    if buttonState1 != oldButtonState1 and buttonState1 == False:
        # Desliga o raspberry caso o mesmo esteja ligado
        subprocess.call("shutdown -h now", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        oldButtonState1 = buttonState1

    time.sleep(.1)
