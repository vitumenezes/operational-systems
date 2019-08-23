import psutil
import pprint
import time
import os
import signal

def getListOfProcessSortedByMemory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
           # pprint.pprint(pinfo)
           pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
           # Append dict to list
           listOfProcObjects.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass

    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)

    return listOfProcObjects

def getProcess():
    '''
    Imprime na tela os processos em execucao
    '''
    # lista de processos
    listOfRunningProcess = getListOfProcessSortedByMemory()

    listProc = (elem for elem in listOfRunningProcess if elem['name'] == 'python3')

    os.system('clear')
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    print('MEMORYUSAGE\tPID\tUSERNAME\tNAME')
    for elem in listProc:
        print(elem['vms'], '\t', elem['pid'], '\t', elem['username'], '\t', elem['name'])

    killProcess()

def killProcess():
    process = input('Digite o PID do processo:')
    os.kill(int(process), signal.SIGKILL)
    getProcess()

def processFunc():
    while True:
        pass

def main():
    pid = os.fork()
    if pid < 0:
        print("Erro")
    elif pid > 0:
        getProcess()
    else:
        processFunc()

if __name__ == '__main__':
    main()
