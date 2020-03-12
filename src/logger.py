import urllib.request
import json
import matplotlib
import matplotlib.pyplot as plt

#URLS
urlNazione = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json'
urlProvince = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json'


# ------------------------------------------------------- Casi totali Italia

def plot_nazione():
# Get data file

    req = urllib.request.Request(urlNazione)
    r = urllib.request.urlopen(req).read()

    # Parse response
    data = json.loads(r.decode('utf-8'))

    # Extract  desired field
    total = []
    for dic in data:
        total.append(int(dic['totale_casi']))

    # Plot Data
    plt.plot(total)
    plt.title('Casi Totali Italia')
    plt.grid(True)
    plt.show()

# ------------------------------------------------------- Casi totali province

def search(provincia, dic):
    return [element['totale_casi'] for element in dic if element['denominazione_provincia'] == provincia]

def plot_province():

    province = [ 'Bergamo', 'Milano', 'Brescia', 'Roma', 'Napoli', 'Lodi']

    # Get data file
    req = urllib.request.Request(urlProvince)
    r = urllib.request.urlopen(req).read()

    # Parse response
    data = json.loads(r.decode('utf-8'))

    # Extracta data
    for provincia in province:
        data_provincia = search(provincia, data)
        plt.plot(data_provincia, label = provincia)
        print(data_provincia)

    # Plot data
    plt.legend()
    plt.title('Casi Totali Province')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    #plot_nazione()
    plot_province()
