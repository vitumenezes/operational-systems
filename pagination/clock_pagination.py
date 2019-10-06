from itertools import cycle
from threading import Thread, Lock
from time import sleep, time
from os import system


STOP = False # global para ser vista pela thread


def printList(page_list):
    '''
    Printa todas as páginas e seus respectivos bits R
    '''
    print('=========== Páginas ===========')

    for i, page in enumerate(page_list):
        print('\nPágina: %d \tBit R: %d' % (i, page[1]))

    print('\n=========== Páginas ===========')


def searchPage(page_list):
    '''
    Função auxiliar para buscar a primeira ocorrencia de página com bit R = 0
    '''
    for page in cycle(page_list):
        if page[1] == 0:
            return page
        else:
            page[1] = 0


def attPages(page_list, lock):
    '''
    Atualiza as páginas que possuem bit R = 1
    O trabalho é feito por uma thread
    '''

    while True:
        sleep(10)

        lock.acquire() # Lock to be an atomic section
        for page in page_list:
            if (page[1] == 1):
                page[1] = 0
        lock.release() # Release

        # verifica se o programa foi encerrado
        global STOP
        if STOP:
            exit(0)


def menu(page_list, lock):
    '''
    Menu de opções. Quando uma opção é escolhida, ele se chama novamente
    (exceto quando for para sair do programa)
    '''

    opc = input("\nOpções:\n1 - Adicionar Página:\n2 - Listar Páginas\nQualquer outra coisa - SAIR\n\nDigite sua opção: ")

    # inicio de regiao critica
    lock.acquire()
    if opc == '1':
        if(len(page_list) < 10):
            page_list.append([time(), 1])
        else:
            print('\nUma pagina precisou ser removida')
            page = searchPage(page_list)
            page_list.remove(page)
            page_list.append([time(), 1])
    elif opc == '2':
        printList(page_list)
    else:
        lock.release()
        global STOP
        STOP = True
        exit(0)
    lock.release() # fim da regiao critica

    menu(page_list, lock)


def main():
    '''
    Função principal para criar a thread de atualização e a lista de páginas
    '''
    page_list = []
    lock = Lock()
    att_pages = Thread(target=attPages, args=(page_list, lock))
    att_pages.start()

    menu(page_list, lock)

if __name__ == '__main__':
    main()
