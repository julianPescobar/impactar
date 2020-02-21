import os
import glob
import zipfile as zip
import datetime
import shutil
import sys,getopt

def manual():
    clearScreen = ''
    if os.name == 'nt':
        clearScreen = 'cls'
    else:
        clearScreen = 'clear'
    #boludeces para la consola
    def repstr(str,len):
        return (str*len)[0:len]

    def clrparse(str):
        return '\033[1;30;40m'+str+'\033[1;35;40m'

    def errorparse(str):
        return '\033[1;31;40m'+str+'\033[0m'

    def validparse(str):
        return '\033[1;32;40m'+str+'\033[0m'
    #Variables globales
    opcion = 0
    has_entorno = 0
    nombrecfg = '-'
    rutasitio = ''
    serversql = ''
    usr = ''
    pwd = ''
    db = ''
    sqlfolder = ''
    aspfolder =''
    #Limpiamos pantalla
    os.system(clearScreen)

    #1 - bup and deploy
    #2 - usar cfg
    #3 - crear cfg
    #4 - salir
    while not opcion in('1','2','3','4','5'):
        opcion = input('\033[4;40;40mimpactar:\033[0m\n\033[1;30;40mMi Config: \033[1;35;40m'+nombrecfg+'\n\033[1;30;40m1)\033[1;35;40m Backup & Deploy\n\033[1;30;40m2) \033[1;35;40mUsar Config\n\033[1;30;40m3) \033[1;35;40mCrear Config\n\033[1;30;40m4) \033[1;35;40mRollbacks\n\033[1;30;40m5) \033[1;35;40mSalir\n\033[1;30;40mSu opcion: \033[1;35;40m')
        os.system(clearScreen)
        
        #OPCION 5
        if opcion == '5':
            exit(0)

        #OPCION 3
        if opcion == '3':
            print(clrparse('Creando Config Nueva:'))
            nombrecfg = input(clrparse('Nombre Config: '))
            rutasitio = input(clrparse('Path al sitio: '))
            serversql = input(clrparse('Server SQL: '))
            usr = input(clrparse('User SQL: '))
            pwd = input(clrparse('Pass SQL: '))
            db = input(clrparse('Database: '))
            sqlfolder = input(clrparse('Folder containing SQL Files: '))
            aspfolder = input(clrparse('Folder containing ASP Files: '))

            print(
                clrparse(' ############')+'\n',
                clrparse('Nombre Config: ')+nombrecfg+'\n',
                clrparse('Path al sitio: ')+rutasitio+'\n',
                clrparse('Server SQL: ')+serversql+'\n',
                clrparse('Database: ')+db+'\n',
                clrparse('Look for .SQL Files in: ')+sqlfolder+'\n',
                clrparse('Look for .ASP Files in: ')+aspfolder+'\n',
                clrparse('############'),
            )
            opt = input(clrparse('La cfg es correcta? S/N: '))
            if opt == 'S':
                f = open(nombrecfg+'.icfg','w+')
                f.write(rutasitio+'\r\n')
                f.write(serversql+'\r\n')
                f.write(db+'\r\n')
                f.write(usr+'\r\n')
                f.write(pwd+'\r\n')
                f.write(sqlfolder+'\r\n')
                f.write(aspfolder+'\r\n')
                f.close()
            else:
                print('ok, cancelando.')
            opcion = '0'

        if opcion == '2':
            cfgs = [f for f in glob.glob(os.getcwd() + '**/*.icfg', recursive=True)]
            if len(cfgs) > 0:
                print('Se encontraron estas configs:')
                for f in cfgs:
                    print(os.path.basename(f).replace('.icfg',''))
                select = input(clrparse('Cual Cfg usar?: '))
                cfgs = [f for f in glob.glob(os.getcwd() + '**/'+select+'.icfg', recursive=True)]
                if len(cfgs) > 0:
                    f = open(cfgs[0],'r')
                    nombrecfg = select
                    lines = f.read().splitlines()
                    rutasitio = lines[0].replace('\r\n','')
                    serversql = lines[1].replace('\r\n','')
                    db = lines[2].replace('\r\n','')
                    usr = lines[3].replace('\r\n','')
                    pwd = lines[4].replace('\r\n','')
                    sqlfolder = lines[5].replace('\r\n','')
                    aspfolder = lines[6].replace('\r\n','')
                    has_entorno = 1
                    os.system(clearScreen)
                else:
                    print(errorparse('No existe esa config ingresada.'))
            else:
                print(errorparse('No se encontraron Cfgs.'))
            opcion = '0'

        ##OPCION 1
        #Si elegimos deployar y backupear y tenemos un entorno seteado..
        if opcion == '1' and has_entorno == 1:
            now = datetime.datetime.now().strftime('%D_%H_%M_%S')
            print(clrparse('Working Dir:'),os.getcwd())
            ok = '0'
            while ok != 'S':
                path = input(clrparse('Path al paquete: '))
                ok = input(clrparse('El path '+ path+ ' está bien? S/N: '))

            ok = '0'
            print(clrparse('Path Paquete: '),path)
            
            print(clrparse('Path al Sitio: '),rutasitio)
            

            print(clrparse('  ==============='+repstr('=',(len(path)+len(rutasitio)//2))))
            print(clrparse('  >Path Paquete: '),path)
            print(clrparse('  >Path Sitio:   ')+rutasitio)
            print(clrparse('  ==============='+repstr('=',(len(path)+len(rutasitio)//2))))
            print(clrparse('Chequeando si existen las carpetas:'))
            patherror = 0
            if os.path.isdir(path):
                print(clrparse(path), ':', validparse('OK'))
            else:
                print(clrparse(path), ':', errorparse('ERROR'))
                patherror = patherror +1

            if os.path.isdir(rutasitio):
                print(clrparse(rutasitio)+ ':',validparse('OK'))
            else:
                print(clrparse(rutasitio)+ ':', errorparse('ERROR'))
                patherror = patherror +1
            
            if patherror > 0:
                print(errorparse('alguno de los path no existe. Abortando.'))
                exit(0)
            backupfiles = []
            print('Chequeando existencias en carpeta destino:')

            files1 = [f for f in glob.glob(path + '**/*.*',recursive=True)]
            for f in files1:  
                file = f.replace(path,rutasitio)
                if os.path.exists(file):
                    print('\033[0mCheck>', file, '\033[1;32;40mExiste, backupeado')
                    backupfiles.append(file)
                else:
                    print('\033[0mCheck>', file, '\033[1;31;40mNo existe')

            haybackup = len(backupfiles)

            if haybackup > 0:
                print('\033[1;32;40mCreando backup...')
                filename = rutasitio+'backup_'+now.replace('/','_')+'.zip'
                zf = zip.ZipFile(filename,mode='w')
                for f in backupfiles:
                    print('\033[1;34;40mzipeando>>>\033[0m',f)
                    zf.write(f)
                zf.close()
                print('\033[1;32;40mBackup finalizado: \033[1;45;40m',filename)
                
            #files2 = [f for f in glob.glob(rutasitio + '**/*',recursive=True)]
            #for f in files2:
            #    print(f)

            print('Impactando componentes NOSQL')
            files1 = [f for f in glob.glob(path + '**/*.*', recursive=True)]
            for f in files1:  
                if not f.endswith('.sql'):
                    file = f.replace(path,rutasitio)
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
        elif opcion == '1' and has_entorno == 0:
            print('\033[1;31;40mNo podes usar esta opción sin antes haber elegido un entorno.\033[0m')
            opcion = '0'

#para ejecutar el script con parametros
def main(argv):
    arg1 = ''
    arg2 = ''
    opts = ''
    args = ''
    try:
       opts,args = getopt.getopt(argv,'hi:o:m',['ifile=','ofile=','manual='])
    except getopt.GetoptError:
        sys.exit()
    for opt,arg in opts:
        if opt == '-h':
            print('impactar.py -m <cfg manual> -i <path paquete> -o <cfg sitio>')
            sys.exit()
        elif opt in ('-i','--ifile'):
            arg1 = arg
            print(arg1)
        elif opt in ('-o','--ofile'):
            arg2 = arg
        elif opt in ('-m','--manual'):
            manual()
        else:
            print('comando no encontrado')
        
if __name__ == "__main__":
   main(sys.argv[1:])

