import urllib.request
import json
import matplotlib
import matplotlib.pyplot as plt

# URLS
urlNazione = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json'
urlProvince = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json'

# Graph constants
SINGLE_GRAPH = 0
TWO_COLUMNS_GRAPH_1 = 121
TWO_COLUMNS_GRAPH_2 = 122

# ------------------------------------------------------- Casi totali Italia

def plot_nazione(graphType):

    # Get data file
    req = urllib.request.Request(urlNazione)
    r = urllib.request.urlopen(req).read()

    # Parse response
    data = json.loads(r.decode('utf-8'))

    # Extract  desired field
    total = []
    for dic in data:
        total.append(int(dic['totale_casi']))

    # Decide about plot type 
    if graphType != SINGLE_GRAPH:
        plt.subplot(graphType)

    # Plot Data
    plt.plot(total, marker='o', markersize=4)
    plt.title('Casi Totali Italia')
    plt.grid(True)
    if graphType == SINGLE_GRAPH:
        plt.show()

# ------------------------------------------------------- Casi totali province

def search(provincia, dic):
    return [element['totale_casi'] for element in dic if element['denominazione_provincia'] == provincia]

def plot_province(graphType):

    province = [ 'Bergamo', 'Milano', 'Brescia', 'Roma', 'Napoli', 'Lodi']

    # Get data file
    req = urllib.request.Request(urlProvince)
    r = urllib.request.urlopen(req).read()

    # Parse response
    data = json.loads(r.decode('utf-8'))
    
    # Decide about plot type 
    if graphType != SINGLE_GRAPH:
        plt.subplot(graphType)

    # Extract data
    for provincia in province:
        data_provincia = search(provincia, data)
        plt.plot(data_provincia, label=provincia, marker='o', markersize=4)

    # Plot data
    plt.legend()
    plt.title('Casi Totali Province')
    plt.grid(True)
    if graphType == SINGLE_GRAPH:
        plt.show()    

# ------------------------------------------------------- Main

if __name__ == '__main__':
    plot_nazione(TWO_COLUMNS_GRAPH_1)
    plot_province(TWO_COLUMNS_GRAPH_2)
    plt.show()