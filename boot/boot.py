# coding: utf-8

# ****************************************************************************
# * Software: Script para ligar/desligar o Raspberry.                        *
# * Referência: Youtube. 'RetroPie Add A Power Button / Switch Raspberry Pi 1*
# *             2 3'. <https://www.youtube.com/watch?v=4nTuzIY0i3k>          *
# * Versão:   0.0.1                                                          *
# * Data:     30-04-2018                                                     *
# * Última Atualização: 18-09-2018                                           *
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

# We will use the pin numbering to match the pins on the Pi, instead of the
# GPIO pin outs (makes it easier to keep track of things)
GPIO.setmode(GPIO.BCM)  # GPIO.setmode(GPIO.BOARD)

# use the same pin that is used to reset button (one button to rule them all!)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
oldButtonState1 = True

while True:
    # grab the current button state
    buttonState1 = GPIO.input(3)

    # check to see if button has been pushed
    if buttonState1 != oldButtonState1 and buttonState1 == False:
        subprocess.call("shutdown -h now", shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        oldButtonState1 = buttonState1

    time.sleep(.1)

# coding: utf-8
import RPi.GPIO as GPIO
import time
import subprocess

# We will use the pin numbering to match the pins on the Pi, instead of the
# GPIO pin outs (makes it easier to keep track of things)
GPIO.setmode(GPIO.BCM)  # GPIO.setmode(GPIO.BOARD)

# use the same pin that is used to reset button (one button to rule them all!)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
oldButtonState1 = True

while True:
    # grab the current button state
    buttonState1 = GPIO.input(3)

    # check to see if button has been pushed
    if buttonState1 != oldButtonState1 and buttonState1 == False:
        subprocess.call("shutdown -h now", shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        oldButtonState1 = buttonState1

    time.sleep(.1)
