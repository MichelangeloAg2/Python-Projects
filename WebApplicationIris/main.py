from flask import Flask, render_template, request
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris

app = Flask(__name__, template_folder='templates')

#Caricamento del dataset iris
iris = load_iris()
X, y = iris.data, iris.target

#Creazione del modello Decision Tree
clf = DecisionTreeClassifier()

#Addestramento del modello
clf.fit(X, y)

#Gestione root del nostro applicativo Flask
@app.route('/')
def home():
    return render_template('index.html')

#Gestione della route quando il form richiamerà predict
@app.route('/predict', methods = ['POST'])
def predict():
    #Creiamo una variabile per i dati
    features = [float(x) for x in request.form.values()]
    features = [features] #Aggiunta di una lista esterna per mantenere la coerenza della struttura
    prediction = clf.predict(features)[0]
    flower_names = ['Setosa', 'Versicolor', 'Virginica']
    predicted_flower = flower_names[prediction]

    #Richiamo della pagina per i risultati
    return render_template('result.html', prediction = predicted_flower)

#Avvio dell'applicativo Flask (Web App)
if __name__ == '__main__':
    app.run(debug=True)