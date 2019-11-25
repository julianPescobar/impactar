import os
import glob
import zipfile as zip
import datetime
import shutil
try:
    import sqlalchemy
except:
    print('No tenes instalado sqlalchemy, por favor "pip3 install sqlalchemy"')
    exit(0)

def repstr(str,len):
    return (str*len)[0:len]

os.system('clear')
now = datetime.datetime.now().strftime('%D_%H_%M_%S')
print('\033[0mWorking dir: \033[1;32;40m',os.getcwd())
ok = '0'
while ok != 'S':
    path = input('\033[0mPath al paquete: ' + '\033[1;33;40m')
    ok = input('\033[0mEl path \033[1;33;40m' + path + '\033[0m está bien? S/N   \033[1;33;40m')

ok = '0'
print('\033[0mPath Paquete: \033[1;32;40m',path)
while ok != 'S':
    path2 = input('\033[0mPath al sitio: ' + '\033[1;33;40m')
    ok = input('\033[0mEl path \033[1;33;40m' + path2 + '\033[0m está bien? S/N   \033[1;33;40m')


print('\033[1;45;40m  ==============='+repstr('=',(len(path)+len(path2)//2)))
print('\033[1;45;40m  >Path Paquete: \033[1;32;40m',path)
print('\033[1;45;40m  >Path Sitio:   \033[1;32;40m',path2)
print('\033[1;45;40m  ==============='+repstr('=',(len(path)+len(path2)//2)))

backupfiles = []
print('Chequeando existencias en carpeta destino:')

files1 = [f for f in glob.glob(path + '**/*.*',recursive=True)]
for f in files1:  
    file = f.replace(path,path2)
    if os.path.exists(file):
        print('\033[0mCheck>', file, '\033[1;32;40mExiste, backupeado')
        backupfiles.append(file)
    else:
        print('\033[0mCheck>', file, '\033[1;31;40mNo existe')

haybackup = len(backupfiles)

if haybackup > 0:
    print('\033[1;32;40mCreando backup...')
    filename = path2+'backup_'+now.replace('/','_')+'.zip'
    zf = zip.ZipFile(filename,mode='w')
    for f in backupfiles:
        print('\033[1;34;40mzipeando>>>\033[0m',f)
        zf.write(f)
    zf.close()
    print('\033[1;32;40mBackup finalizado: \033[1;45;40m',filename)
#files2 = [f for f in glob.glob(path2 + '**/*',recursive=True)]
#for f in files2:
#    print(f)

print('Impactando componentes NOSQL')
files1 = [f for f in glob.glob(path + '**/*.*', recursive=True)]
for f in files1:  
    if not f.endswith('.sql'):
        file = f.replace(path,path2)
        if os.path.exists(file):
            print('\033[0mStatus>', file, '\033[1;32;40mExiste... Reemplazado')
            shutil.copyfile(f,file)
        else:
            print('\033[0mStatus>', file, '\033[1;31;40mNo existe... Agregado')
            shutil.copyfile(f,file)

print('Impactando Componentes SQL')
files1 = [f for f in glob.glob(path + '**/*.sql', recursive=True)]
for f in files1:  
    print(f)