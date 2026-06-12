#Importare le librerie Flask
from flask import Flask, render_template, request, redirect, url_for, app

#Importare il modulo per la connessione al DB-MySQL
import mysql.connector

#Inizializza l'applicazione Flask
app = Flask(__name__, template_folder='templates')

"""Creare il DB e le tabelle per il software.
Funzione per creare il Database e le tabelle se non esistono"""

def create_database():
    try:
        #Connessione al server MySQLper eseguire la query
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="pythonuser",
            password="1234",
            port=3307
        )
        #creazione del cursore per eseguire la query
        cursor = connection.cursor()

        #Creazione Query per creare il DB se non esiste
        cursor.execute("CREATE DATABASE IF NOT EXISTS libreria")

        #Query per la creazione della tabella libri SE non esiste
        #Richiamiamo oggetto cursor.
        cursor.execute("USE libreria")
        cursor.execute("CREATE TABLE IF NOT EXISTS libri (id INT AUTO_INCREMENT PRIMARY KEY, titolo VARCHAR (255), autore VARCHAR(255), genere VARCHAR(255), descrizione TEXT)")

        #Conferma delle modifiche al DB
        connection.commit()
        #Chiudi la connessione al DB
        cursor.close()
        connection.close()

        print("Database e tabelle creati con successo!")
    except Exception as e:
        print("Si è verificato un errore durante la creazione del DB:", e)

#Esecuzione della funzione per creare il DB e le tabelle a esso associate
create_database()

#Configurazione della connessione al DB
db = mysql.connector.connect(
    host="127.0.0.1",
    user="pythonuser",
    password="1234",
    database="libreria",
    port=3307
)

#Creazione del cursore per eseguire le query sull'oggetto DB
cursor = db.cursor()

#Vista per la visualizzazione della lista dei libri sulla pagina index
@app.route("/")
def index():
    #eseguire la query SQL per la visualizzazione dei libri
    cursor.execute("SELECT * FROM libri")
    #Ottenere tutti i risultati della query e memorizzarli in una variabile libri
    libri = cursor.fetchall() #Array list
    #Restituire il template index.html passando la lista di libri
    return render_template("index.html", libri = libri)

#Vista per aggiunta di un nuovo libro
@app.route('/aggiungi', methods=['GET','POST'])
def aggiungi():
    #Verifica se la richiesta è un POST
    if request.method == 'POST':
        #Ottiene i dati inseriti nel form
        titolo = request.form['titolo']
        autore = request.form['autore']
        genere = request.form['genere']
        descrizione = request.form['descrizione']

        #Esegue la query per l'inserimento dei dati
        cursor.execute("INSERT INTO libri(titolo, autore, genere, descrizione) VALUES (%s, %s, %s, %s)", (titolo, autore, genere, descrizione))
        #Conferma delle modifiche sul DB
        db.commit()
        #Reindirizza utente alla pagina principale.
        return redirect(url_for('index'))
    #Se la richiesta non è un POST, carica la pagina aggiungi.html
    return render_template("aggiungi.html")

#Vista per la modifica di un libro
@app.route('/modifica/<int:id>', methods=['GET', 'POST'])#dobbiamo fare un'operazione di cast, per id del libro
def modifica_libro(id):
    #Eseguire una Query per selezionare il libro con ID specificato
    cursor.execute("SELECT * FROM libri WHERE id = %s", (id,))
    libro = cursor.fetchone()

    #Verificare se la richiesta è un POST per l'invio dati
    if request.method == 'POST':
        #Ottenere i dati inseriti nel FORM
        titolo = request.form['titolo']
        autore = request.form['autore']
        genere = request.form['genere']
        descrizione = request.form['descrizione']

        #Eseguire la query per aggiornamento del DB (Quindi il record su cui stiamo facendo la modifica)
        cursor.execute("UPDATE libri SET titolo=%S, genere=%s, autore=%s, descrizione=%s WHERE id=%s", (titolo, genere, autore, descrizione, id))
        #Conferma delle modifiche al DB
        db.commit()
        #Reindirizzare l'utente alla pagina principale
        return redirect(url_for('index'))
    #Se la richiesta non è POST(primo caricamento per la modifica della pagina)
    return render_template("modifica.html", libro=libro)

#Vista per l'eliminazione del libro
@app.route('/elimina/<int:id>')
def elimina_libro(id):
    #Esecuzione della query per l'eliminazione del libro dal DB
    cursor.execute("DELETE FROM libri WHERE id =%s", (id,))
    #Conferma della modifica sul DB
    db.commit()
    #Ricarica la pagina index con l'elenco aggiornato
    return redirect(url_for('index'))
#Avvio dell'applicazione Flask in modalità debug. Una volta terminato il processo, togliere il debug.

if __name__ == '__main__':
    app.run(debug=True)
