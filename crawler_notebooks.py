import re

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

#Esse programa vai retornar um documento com os preços requisitados no zoom, na hora, dos notebooks da dell e samsung

URL_DELL_G5 = 'https://www.zoom.com.br/search?q=dell%20g5'
URL_ODYSSEY = 'https://www.zoom.com.br/search?q=Notebook%20samgung%20odyssey'


def request(url):
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta.text
        else:
            print("Link INVALIDO!!!!")
    except ConnectionError:
        print("Erro de conexão ocorreu ao fazer request")

def parsing(resposta_texto):
    try:
        soup = BeautifulSoup(resposta_texto,'html.parser')
        return soup
    except Exception as error:
        print("Erro de execução do parsing\nERRO: {}".format(error))

def buscar_descricao(soup):

    try:
        descricao_notebook = soup.find_all('a',class_ = 'name')
        lista_descricao = []
        for descr in descricao_notebook:
            lista_descricao.append(descr.get_text())
        try:
            preco_notebook = soup.find_all('span', class_='mainValue')
            lista_precos = []
            for valores in preco_notebook:
                lista_precos.append(valores.get_text())
            lista_completa = [lista_descricao, lista_precos]
            return lista_completa
        except:
            print("Erro na busca do preco")
    except:
        print("Erro na busca da descricao")


def save(nome_do_arquivo,lista):
    try:
        lista_descricao = lista[0]
        lista_preco = lista[1]
        with open(nome_do_arquivo,'w') as file:
            for i in range(len(lista_descricao)):
                file.write('{}'.format(lista_descricao[i]))
                file.write('\n')
                file.write('Preco:{}'.format(lista_preco[i]))
                file.write('\n')
                file.write('\n')
                file.write('\n')

    except Exception as error:
        print("Erro de abertura do arquivo\nERRO:{}".format(error))

def graph_prices(lista_de_precos):
    lista_aux = []
    for i in range(len(lista_de_precos)):
        regex = re.findall(r"\d{0,2}[.]\d{3}",lista_de_precos[i]) #faz um regex para retirar o R$ e pegar apenas o numero
        auxiliar = float(regex[0])*1000 #transforma a string em um float
        lista_aux.append(auxiliar) #Transformando os preços de string em inteiros
    x = range(len(lista_aux))
    plt.plot(x,lista_aux) #plotando o grafico dos preços
    plt.show()

def menu():
    print("-------------------------")
    print("Escolha a marca do notebook ou sair do programa:")
    print("1 - Dell")
    print("2 - Samsung")
    print("3 - Gráfico dos preços")
    print("4 - Sair do programa")
    print("-------------------------")

if __name__ == "__main__":

    while True:
        menu()
        escolha = int(input())
        if escolha == 1:

            resposta = request(URL_DELL_G5)
            soup = parsing(resposta)
            lista_dell = buscar_descricao(soup)
            save('descricao_e_precos_dell.doc',lista_dell)
        elif escolha == 2:

            resposta = request(URL_ODYSSEY)
            soup = parsing(resposta)
            lista_samsung = buscar_descricao(soup)
            save('descricao_e_precos_samsung.doc',lista_samsung)

        elif escolha == 3:
            a = input("Escolha : \na - Notebook Dell G5\nb - Notebook Samgung Odyssey")

            if a == 'a':
                resposta = request(URL_DELL_G5)
                soup = parsing(resposta)
                lista_dell = buscar_descricao(soup)
                graph_prices(lista_dell[1])

            elif a == 'b':
                resposta = request(URL_ODYSSEY)
                soup = parsing(resposta)
                lista_samsung = buscar_descricao(soup)
                graph_prices(lista_samsung[1])

            else:
                print("Insira opcao valida")
        elif escolha == 4:
            print("Bye")
            break

        else:
            print("Faça uma escolha válida")