# Visuelle Analytik von Fußballspielen - Trajektorien
### Autoren: Ralf Stickl, Bastian Klein, Johannes Klaußner
---
## How to - Ausführung der Anwendung

Um das Programm ausführen zu können, müssen folgende Dinge installiert sein:

### Backend:
* Python 3.10. (or later) Environment - https://www.python.org/downloads/
* Flask 2.0 - https://flask.palletsprojects.com/en/2.0.x/installation/
* flask-cors - https://flask-cors.readthedocs.io/en/latest/
* NumPy - https://numpy.org/install/

### Frontend (siehe auch _Fontend ohne Installation_):
* Node.js 16  - https://nodejs.org/en/
* Yarn via - https://classic.yarnpkg.com/lang/en/docs/install/#windows-stable
  ```js
  npm install --global yarn
  ```
### Datensätze:
Es stehen die Datensätze für zwei Spiele zur Verfügung. Aufgrund der Größe der Rohdatensätze sind diese nicht mit im Repository vorhanden, sondern müssen separat heruntergeladen werden. Die Datensätze sind hier verfügbar: https://github.com/metrica-sports/sample-data/tree/master/data

Die Datenordner "Sample\_Game\_1" und "Sample\_Game\_2" können im Programm verwendet werden, wenn sie sich im Ordner `.\python-backend\gameData` befinden.

Hinweis: "Sample\_Game\_3" ist nicht mit unserem Programm kompatibel, da dieses Spiel im FIFA-Standardformat und nicht im Metrica-Format bereit gestellt wurde.

## Ausführung
Sind alle Voraussetzungen installiert, müssen Frontend und Backend separat gestartet werden.

Das Backend wird über die Konsole im Verzeichnispfad `.\python-backend` mit 
```python
~\python-backend> flask run
```
ausgeführt.

Das Frontend wird über die Konsole im Verzeichnispfad `.\soccer-vis-formation` mit 
```python
~\soccer-vis-formation> yarn serve
```

ausgeführt.

Alternativ kann das Programm auch ohne Installation der Frontend-Voraussetzungen über folgende Website gestartet werden. Das Backend muss aber dennoch lokal gestartet werden.
### Fontend ohne Installation:
Das Frontend ist über die githubpage https://sektion09.github.io/sport-vis-soccer/#/ abrufbar und kann dort verwendet werden.
