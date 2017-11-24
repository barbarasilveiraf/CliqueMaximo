import os
from subprocess import Popen, PIPE

#leitura do diretorio
path = "C:/Users/Barbara/PycharmProjects/Testes_TP_Final_PAA/"
files = [f for f in os.listdir(path) if f.endswith('.edges')]



#executar o programa
for f in files:
    file = open("resultadoTestes_"+f+".txt", "w")
    #os.system('python cliqueMaximo.py '+ (path+f))
    #script_path = os.path.join("python", 'cliqueMaximo.py '+ (path+f))
    #p = Popen([sys.executable, '-u', script_path],stdout=PIPE, stderr=STDOUT, bufsize=1)
    for x in range(1, 11): #executar 10 vezes cada arquivo
        pipe = Popen('python '+ 'cliqueMaximo.py '+ (path+f), shell=True, stdout=PIPE).stdout
        output = pipe.read()
        texto = str(output).replace(r"\r\n", ";").replace("b'", "").replace("'", "")
        file.write(texto)
        file.write("\n")
    file.close()


