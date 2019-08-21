import psutil, pprint, time, os

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


def main():
    while True:
        listOfRunningProcess = getListOfProcessSortedByMemory()
        print('MEMORYUSAGE\tPID\tUSERNAME\tNAME')
        for elem in listOfRunningProcess[:15] :
            print(elem['vms'], '\t', elem['pid'], '\t', elem['username'], '\t', elem['name'])
        time.sleep(1)
        os.system('clear')


if __name__ == '__main__':
    main()
