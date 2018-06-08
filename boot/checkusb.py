# coding: utf-8

# ****************************************************************************
# * Software: Verifica quando um pendrive é conectado/desconectado na porta  *
# *           USB. É executado no boot do sistema e independe da aplicação   *
# *           principal (scanner.py). Utiliza um arquivo temporário onde é   *
# *           escrito a informação sobre o estado de conexão do pendrive, se *
# *           está conectado ou desconectado.                                *
# * Versão:   0.0.3                                                          *
# * Data:     09-05-2018                                                     *
# * Última Atualização: 09-05-2018                                           *
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


import sys

sys.path.append('/home/pi/.local/lib/python3.5/site-packages')  # Adiciona o PATH para encontrar o módulo pyudev

import pyudev

# Inicia o arquivo usb_temp.txt considerando USB desconectado
file = open('usb_temp.txt', 'w')
file.write('desconectado')
file.close()

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

for device in iter(monitor.poll, None):
    file = open('usb_temp.txt', 'w')
    if device.action == 'add':
        print('conectado')
        file.write('conectado')
    if device.action == 'remove':
        print('desconectado')
        file.write('descontectado')
    file.close()
