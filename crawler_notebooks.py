import re

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

#Esse programa vai retornar um documento com os preços requisitados no zoom, na hora, dos notebooks da dell e samsung

URL_DELL_G5 = 'https://www.zoom.com.br/search?q=dell%20g5'
URL_ODYSSEY = 'https://www.zoom.com.br/search?q=Notebook%20samgung%20odyssey'
URL_AVELL_C62 = 'https://www.zoom.com.br/search?q=Avell%20LIV%20C62'
URL_ASPIRE_NITRO_5 = 'https://www.zoom.com.br/search?q=Notebook%20Aspire%20Nitro%205%20AN515-43'
URL_NAVE = 'https://www.zoom.com.br/search?page=1&hierarchicalMenu%5BcategoryHierarchy.lvl0%5D=Inform%C3%A1tica&configure%5BruleContexts%5D%5B0%5D=search_page&configure%5BhitsPerPage%5D=36&configure%5BclickAnalytics%5D=true&configure%5BanalyticsTags%5D%5B0%5D=undefined&configure%5BanalyticsTags%5D%5B1%5D=undefined&configure%5BanalyticsTags%5D%5B2%5D=page_type%3Asearch_page&configure%5BanalyticsTags%5D%5B3%5D=brand%3Azoom&configure%5BuserToken%5D=102cdfc3-316f-4e38-9e10-f62d6a9599c5&q=Notebook%20Gamer%20NAVE'
URL_DELL_G5_B = 'https://www.buscape.com.br/search?page=1&range%5Bprice%5D%5Bmin%5D=2020&range%5Bprice%5D%5Bmax%5D=10262&configure%5BruleContexts%5D%5B0%5D=search_page&configure%5BhitsPerPage%5D=36&configure%5BclickAnalytics%5D=true&configure%5BanalyticsTags%5D%5B0%5D=undefined&configure%5BanalyticsTags%5D%5B1%5D=undefined&configure%5BanalyticsTags%5D%5B2%5D=page_type%3Asearch_page&configure%5BanalyticsTags%5D%5B3%5D=brand%3Abuscape&configure%5BuserToken%5D=3f155ba6-880e-4f49-8b6c-bb4948423459&q=Dell%20G5'
URL_ODYSSEY_B = 'https://www.buscape.com.br/search?page=1&hierarchicalMenu%5BcategoryHierarchy.lvl0%5D=Inform%C3%A1tica&configure%5BruleContexts%5D%5B0%5D=search_page&configure%5BhitsPerPage%5D=36&configure%5BclickAnalytics%5D=true&configure%5BanalyticsTags%5D%5B0%5D=undefined&configure%5BanalyticsTags%5D%5B1%5D=undefined&configure%5BanalyticsTags%5D%5B2%5D=page_type%3Asearch_page&configure%5BanalyticsTags%5D%5B3%5D=brand%3Abuscape&configure%5BuserToken%5D=3f155ba6-880e-4f49-8b6c-bb4948423459&q=samsung%20odyssey'
URL_AVELL_C62_B = 'https://www.buscape.com.br/search?q=Notebook%20Avell%20LIV%20C62'
URL_ASPIRE_NITRO_5_B = 'https://www.buscape.com.br/search?page=1&range%5Bprice%5D%5Bmin%5D=3811&configure%5BruleContexts%5D%5B0%5D=search_page&configure%5BhitsPerPage%5D=36&configure%5BclickAnalytics%5D=true&configure%5BanalyticsTags%5D%5B0%5D=undefined&configure%5BanalyticsTags%5D%5B1%5D=undefined&configure%5BanalyticsTags%5D%5B2%5D=page_type%3Asearch_page&configure%5BanalyticsTags%5D%5B3%5D=brand%3Abuscape&configure%5BuserToken%5D=3f155ba6-880e-4f49-8b6c-bb4948423459&q=Notebook%20aspire%20Nitro%205'
URL_NAVE_B = 'https://www.buscape.com.br/search?page=1&range%5Bprice%5D%5Bmin%5D=1772&configure%5BruleContexts%5D%5B0%5D=search_page&configure%5BhitsPerPage%5D=36&configure%5BclickAnalytics%5D=true&configure%5BanalyticsTags%5D%5B0%5D=undefined&configure%5BanalyticsTags%5D%5B1%5D=undefined&configure%5BanalyticsTags%5D%5B2%5D=page_type%3Asearch_page&configure%5BanalyticsTags%5D%5B3%5D=brand%3Abuscape&configure%5BuserToken%5D=3f155ba6-880e-4f49-8b6c-bb4948423459&q=Notebook%20Gamer%20Nave'


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

def graph_prices(lista_de_precos,titulo):
    lista_aux = []
    for i in range(len(lista_de_precos)):
        regex = re.findall(r"\d{0,2}[.]\d{3}",lista_de_precos[i]) #faz um regex para retirar o R$ e pegar apenas o numero
        auxiliar = (float(regex[0]))*1000 #transforma a string em um float
        lista_aux.append(auxiliar) #Transformando os preços de string em inteiros
    x = range(0,len(lista_aux))
    plt.title(titulo)
    plt.xlabel = 'Modelo'
    plt.ylabel = 'Preco'
    plt.scatter(x,lista_aux,color = 'green',marker = '.',s = 200)
    plt.plot(x,lista_aux,color = 'blue') #plotando o grafico dos preços
    plt.show()
    plt.savefig('Gráfico.png',dpi = 1200)

def menu():
    print("-------------------------")
    print("Escolha uma opcao valida:")
    print("1 - Documento com modelos e precos")
    print("2 - Gráfico dos preços")
    print("3 - Sair do programa")
    print("-------------------------")

if __name__ == "__main__":

    while True:
        menu()
        escolha = int(input())
        if escolha == 1:
            b = input('Escolha o site de buscas:\na - Zoom\nb - Buscape:\n')
            if b == 'a':
                a = input("Escolha : \na - Notebook Dell G5\nb - Notebook Samgung Odyssey\nc - Notebook Avell C62\nd - Notebook Aspire Nitro 5\ne - Notebook Nave")
                if a == 'a':
                    resposta = request(URL_DELL_G5)
                    soup = parsing(resposta)
                    lista_dell = buscar_descricao(soup)
                    save('descricao_e_precos_dell_zoom.doc',lista_dell)

                elif a == 'b':
                    resposta = request(URL_ODYSSEY)
                    soup = parsing(resposta)
                    lista_samsung = buscar_descricao(soup)
                    save('descricao_e_precos_odyssey_zoom.doc',lista_samsung)

                elif a == 'c':
                    resposta = request(URL_AVELL_C62)
                    soup = parsing(resposta)
                    lista_avell = buscar_descricao(soup)
                    save('descricao_e_precos_avell_zoom.doc', lista_avell)

                elif a == 'd':
                    resposta = request(URL_ASPIRE_NITRO_5)
                    soup = parsing(resposta)
                    lista_aspire = buscar_descricao(soup)
                    save('descricao_e_precos_aspire_zoom.doc', lista_aspire)

                elif a == 'e':
                    resposta = request(URL_NAVE)
                    soup = parsing(resposta)
                    lista_nave = buscar_descricao(soup)
                    save('descricao_e_precos_nave_zoom.doc', lista_nave)

            if b == 'b':
                a = input(
                    "Escolha : \na - Notebook Dell G5\nb - Notebook Samgung Odyssey\nc - Notebook Avell C62\nd - Notebook Aspire Nitro 5\ne - Notebook Nave")
                if a == 'a':
                    resposta = request(URL_DELL_G5_B)
                    soup = parsing(resposta)
                    lista_dell = buscar_descricao(soup)
                    save('descricao_e_precos_dell_buscape.doc', lista_dell)

                elif a == 'b':
                    resposta = request(URL_ODYSSEY_B)
                    soup = parsing(resposta)
                    lista_samsung = buscar_descricao(soup)
                    save('descricao_e_precos_odyssey_buscape.doc', lista_samsung)

                elif a == 'c':
                    resposta = request(URL_AVELL_C62_B)
                    soup = parsing(resposta)
                    lista_avell = buscar_descricao(soup)
                    save('descricao_e_precos_avell_buscape.doc', lista_avell)

                elif a == 'd':
                    resposta = request(URL_ASPIRE_NITRO_5_B)
                    soup = parsing(resposta)
                    lista_aspire = buscar_descricao(soup)
                    save('descricao_e_precos_aspire_buscape.doc', lista_aspire)

                elif a == 'e':
                    resposta = request(URL_NAVE_B)
                    soup = parsing(resposta)
                    lista_nave = buscar_descricao(soup)
                    save('descricao_e_precos_nave_buscape.doc', lista_nave)

        elif escolha == 2:
            b = input('Escolha o site de buscas:\na - Zoom\nb - Buscape:\n')
            if b == 'a':
                a = input("Escolha : \na - Notebook Dell G5\nb - Notebook Samgung Odyssey\nc - Notebook Avell C62\nd - Notebook Aspire Nitro 5\ne - Notebook Nave")

                if a == 'a':
                    resposta = request(URL_DELL_G5)
                    soup = parsing(resposta)
                    lista_dell = buscar_descricao(soup)
                    graph_prices(lista_dell[1],'Dell G5')

                elif a == 'b':
                    resposta = request(URL_ODYSSEY)
                    soup = parsing(resposta)
                    lista_samsung = buscar_descricao(soup)
                    graph_prices(lista_samsung[1],'Samgung Odyssey')

                elif a == 'c':
                    resposta = request(URL_AVELL_C62)
                    soup = parsing(resposta)
                    lista_avell = buscar_descricao(soup)
                    graph_prices(lista_avell[1], 'Avell C62')

                elif a == 'd':
                    resposta = request(URL_ASPIRE_NITRO_5)
                    soup = parsing(resposta)
                    lista_aspire = buscar_descricao(soup)
                    graph_prices(lista_aspire[1], 'Aspire Nitro 5')

                elif a == 'e':
                    resposta = request(URL_NAVE)
                    soup = parsing(resposta)
                    lista_nave = buscar_descricao(soup)
                    graph_prices(lista_nave[1], 'Nave')
                else:
                    print("Insira opcao valida")

            elif b == 'b':

                a = input("Escolha : \na - Notebook Dell G5\nb - Notebook Samgung Odyssey\nc - Notebook Avell C62\nd - Notebook Aspire Nitro 5\ne - Notebook Nave")

                if a == 'a':
                    resposta = request(URL_DELL_G5_B)
                    soup = parsing(resposta)
                    lista_dell = buscar_descricao(soup)
                    graph_prices(lista_dell[1], 'Dell G5')

                elif a == 'b':
                    resposta = request(URL_ODYSSEY_B)
                    soup = parsing(resposta)
                    lista_samsung = buscar_descricao(soup)
                    graph_prices(lista_samsung[1], 'Samgung Odyssey')

                elif a == 'c':
                    resposta = request(URL_AVELL_C62_B)
                    soup = parsing(resposta)
                    lista_avell = buscar_descricao(soup)
                    graph_prices(lista_avell[1], 'Avell C62')

                elif a == 'd':
                    resposta = request(URL_ASPIRE_NITRO_5_B)
                    soup = parsing(resposta)
                    lista_aspire = buscar_descricao(soup)
                    graph_prices(lista_aspire[1], 'Aspire Nitro 5')

                elif a == 'e':
                    resposta = request(URL_NAVE_B)
                    soup = parsing(resposta)
                    lista_nave = buscar_descricao(soup)
                    graph_prices(lista_nave[1], 'Nave')
                else:
                    print("Insira opcao valida")


            else:
                print("Opcao invalida")
        elif escolha == 3:
            print("Bye")
            break

        else:
            print("Faça uma escolha válida")