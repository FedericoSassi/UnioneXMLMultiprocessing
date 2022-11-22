# Contenuti
1. [Introduzione al progetto](README.md#introduzione-al-progetto)
2. [Richiesta](README.md#richiesta)
3. [Specifiche dati](README.md#specifiche-dati)
4. [Conclusione](README.md#conclusione)
5. [Macchina utilizzata](README.md#macchina-utilizzata)
6. [Possibili implementazioni](README.md#possibili-implementazioni)

# Introduzione al progetto

Il progetto prevede l'elaborazione di file XML con l'estrazione di alcuni dati tramite la libreria MultiProcessing.
Creando il file CSV completo delle informazioni necessarie.

## Richiesta

L'azienda ha la necessità di estrarre alcuni dati da numerosi file XML per poter eseguire controlli incrociati.

Il problema della lavorazione si identifica nella grande quantità di file da processare e nelle dimensioni di alcuni di essi.
Si è provato con Excel ma visto l'enorme numero di righe presenti non si è potuto fare.

## Elaborazione

Utilizzando lo script nel progetto, tutti i file sono stati elaborati in circa 11 minuti producendo il file csv completo.
Questo file ha una dimensione di circa 2.800.000 righe, pertanto anche i calcoli per i controlli incrociati sono stati eseguiti con l'utilizzo di python.

Questo lo script utilizzato -> [Script Multiprocessing]()

## Macchina utilizzata

Nel progetto si è utilizzata una macchina virtuale con le seguenti specifiche:
- SO: Linux / Ubuntu
- CPU: 16
- RAM: 256 mb

Si è scelto questo tipo di macchina perché è a disposizione dell'azienda e per la mole di file, sia di numero che di dimensione, che vengono elaborati.

## Possibili implementazioni

Il progetto è impostato per girare una tantum, però le possibili implementazioni sono tante.
Una su tutte è la schedulazione di Job che ciclicamente caricano i dati su un Database in stile ETL, così da poterli analizzare o utilizzare in task di controllo.
