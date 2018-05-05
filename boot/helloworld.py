import datetime

file = open('teste.txt', 'a')


file.write(str(datetime.datetime.now())+'\n')

file.close()
