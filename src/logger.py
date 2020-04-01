import urllib.request
import json
import matplotlib
import matplotlib.pyplot as plt

# URLS
urlNazione = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json'
urlProvince = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json'

# Procincie definitions
province = [    {'town': 'Bergamo', 'color': 'red'},  #dodgerblue
                {'town': 'Brescia', 'color': 'lightskyblue'}, 
                {'town': 'Milano',  'color': 'royalblue'},
                {'town': 'Cremona', 'color': 'mediumseagreen'},
                {'town': 'Lodi',    'color': 'palegreen'}, 
                {'town': 'Roma',    'color': 'goldenrod'}, 
                {'town': 'Napoli',  'color': 'gold'}, 
                {'town': 'Bari',    'color': 'tan'},
            ]

# Graph constants
SINGLE_GRAPH = 0
THREE_COLUMNS_GRAPH_1 = 131
THREE_COLUMNS_GRAPH_2 = 132
THREE_COLUMNS_GRAPH_3 = 133

# ------------------------------------------------------- Casi totali Italia

def plot_nazione(graphType):

    # Get data file
    req = urllib.request.Request(urlNazione)
    r = urllib.request.urlopen(req).read()

    # Parse response
    data = json.loads(r.decode('utf-8'))

    # Extract  desired field
    total = []
    decessi = []
    for dic in data:
        total.append(int(dic['totale_casi']))
        decessi.append(int(dic['deceduti']))

    # Decide about plot type 
    if graphType != SINGLE_GRAPH:
        plt.subplot(graphType)

    # Plot Data
    plt.plot(total, label='Totale', marker='o', markersize=4, linewidth=2)
    plt.plot(decessi, label='Decessi', marker='o', color='orange', markersize=4, linewidth=2) 
    plt.legend()
    plt.title('Casi Totali Italia')
    plt.grid(True)
    if graphType == SINGLE_GRAPH:
        plt.show()

# ------------------------------------------------------- Casi totali province

def search(provincia, dic):
    return [element['totale_casi'] for element in dic if element['denominazione_provincia'] == provincia]

def plot_province(graphType):
 
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
        data_provincia = search(provincia['town'], data)
        print(data_provincia)
        plt.plot(data_provincia, label=provincia['town'], marker='o', color = provincia['color'], markersize=4, linewidth=2)

    # Set linear scale
    plt.yscale('linear')
    # Plot data
    plt.legend()
    plt.title('Casi Totali Province')
    plt.grid(True)
    if graphType == SINGLE_GRAPH:
        plt.show()    

# ------------------------------------------------------- Delta province lombarde

def search_lombardia(provincia, dic):
    return [element['totale_casi'] for element in dic if element['denominazione_provincia'] == provincia and element['denominazione_regione'] == 'Lombardia']

def plot_delta_province(graphType, week_average):
 
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
        data_provincia = search_lombardia(provincia['town'], data)
        delta = []
        previous_element = 0
        previous_delta_1 = 0
        previous_delta_2 = 0
        previous_delta_3 = 0
        previous_delta_4 = 0
        previous_delta_5 = 0
        previous_delta_6 = 0

        for element in data_provincia:
            # Daily delta
            daily_delta = element - previous_element
            previous_element = element
            # Add delta (daily or averaged)
            if week_average:
                delta.append((daily_delta + previous_delta_1 + previous_delta_2 + previous_delta_3 + previous_delta_4 + previous_delta_5 + previous_delta_6)/7)
                # Update history
                previous_delta_6 = previous_delta_5
                previous_delta_5 = previous_delta_4
                previous_delta_4 = previous_delta_3
                previous_delta_3 = previous_delta_2
                previous_delta_2 = previous_delta_1
                previous_delta_1 = daily_delta
            else:
                delta.append(daily_delta)
        plt.plot(delta, label=provincia['town'], marker='o', color = provincia['color'], markersize=4, linewidth=2)

    # Set linear scale
    plt.yscale('linear')
    # Plot data
    plt.legend()
    plt.title('Nuovi Casi Province Lombarde')
    plt.grid(True)
    if graphType == SINGLE_GRAPH:
        plt.show()    

# ------------------------------------------------------- Main

if __name__ == '__main__':
    plot_nazione(THREE_COLUMNS_GRAPH_1)
    plot_province(THREE_COLUMNS_GRAPH_2)
    plot_delta_province(THREE_COLUMNS_GRAPH_3, week_average = True)
    plt.show()