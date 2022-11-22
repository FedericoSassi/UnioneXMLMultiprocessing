# Importo le librerie necessarie
import xml.etree.ElementTree as ET
import pandas as pd
import os
import time
import multiprocessing

# Snapshot del Time di inizio procedura
start_time = time.time()

# Percorso cartella origine file
folder = '../scr/' 

# Counter 
counter = 1

# Nomi delle colonne per il csv
colonne = [
    'File'
    , 'Distributore'
    , 'POD'
    , 'Tensione'
    , 'DaCompetenza'
    , 'ACompentenza'
    , 'Quantità'
    , 'Componente'
]

# Creo un DataFrame da usare per la formazione del csv
df = pd.DataFrame(
    columns = colonne
)

# Creo il csv da compilare
df.to_csv(path_or_buf='XmlUnito.csv',index=False)

# Recupero l'elenco dei file presenti nella cartella di orginine
filesXML = os.listdir(folder)

# Definisco una funzione che elabora il singolo file
def ElaborazioneXML(file,counter):
    
    # Definisco il path del file da elaborare
    path = folder + file

    # Creo un dizionario dove salvare i campi della riga da aggiungere al file csv
    dictNewRow = {}
    
    # Salvo in una variabile le dimensioni del file che sto lavorando
    file_size = os.path.getsize(path) / 1000000

    # Creo il dataFrame da usare per esportare i dati nel csv
    dfFile = pd.DataFrame()

    # Stampo l'inizio del lavoro sul file con le info di esso
    print(f'#### {counter} Inizio lavoro su file: {file} - {file_size} bytes ####')

    # Salvo nel dizionario il nome del file
    dictNewRow['File'] = file
    
    # inizio parse XML
    tree = ET.parse(source = path)
    root = tree.getroot()

    # Salvo nel dizionario il nome del distributore
    dictNewRow['Distributore'] = root.find('TestataFlusso/TRagioneSocialeMittente').text

    # Ciclo i nodi 'Fatture' per estrarre i dati
    for child in root.findall('Fatture'):
        
        # Ciclo i child 'DettaglioPDO' per estrarre i dati
        for dettaglioPDO in child.findall('DettaglioPOD'):

            # Salvo i dati PDO e Tensione nel dizionario
            dictNewRow['POD'] = dettaglioPDO.find('DCodicePod').text
            dictNewRow['Tensione'] = dettaglioPDO.find('DatiTecniciCommerciali/DDTTensione').text
        
            # Ciclo i nodi 'Corrispettivi' per estrarre i dati
            for corrispettivo in dettaglioPDO.findall('Corrispettivi'):
                
                # Salvo il dato del componente
                componente = corrispettivo.find('DComponente').text
                
                # Se la componente è quella richiesta aggiungo i dati nel dizionario
                if componente == '€/kWh':

                    # Aggiungo i dati che voglio estrarre nel dizionario
                    dictNewRow['DaCompetenza'] = corrispettivo.find('DPeriodoCompetenzaDa').text
                    dictNewRow['ACompentenza'] = corrispettivo.find('DPeriodoCompetenzaA').text
                    dictNewRow['Quantità'] = corrispettivo.find('DQuantita').text
                    dictNewRow['Componente'] = corrispettivo.find('DComponente').text

                    # Converto il dizionario in Series
                    newRow = pd.Series(dictNewRow)

                    # Concateno il dataframe con la series per avere i dati da salvare in csv
                    dfFile = pd.concat([dfFile,newRow.to_frame().T])

    # Scrivo sul csv i dati estratti
    dfFile.to_csv(path_or_buf='XmlUnito.csv',index=False,mode='a',header=False)

    # Stampo la fine lavoro del file
    print(f'#### {counter} Fine lavoro su file: {file} - {file_size} bytes ####')

# Lancio dello script
if __name__ == '__main__':

    # definisco array per i processi
    processes = []

    # Ciclo l'elenco dei file XML
    for file in filesXML:
        
        # Salvo il processo per il file in corso
        p = multiprocessing.Process(target=ElaborazioneXML, args=(file,counter))

        # Incremento il counter di file in lavorazione
        counter += 1

        # Aggiungo il processo all'array dei processi
        processes.append(p)

        # Lancio il processo
        p.start()
        
    # Ciclo i processi
    for process in processes:

        # Metto in Join i processi
        process.join()

    # Stampo i secondi totali che ha impiegato la procedura solo per vanità e controllo
    print("--- %s seconds ---" % (time.time() - start_time))