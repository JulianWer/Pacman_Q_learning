# Pacman Q-Learning

Dieses Projekt implementiert eine vereinfachte Version des klassischen Pac-Man-Spiels, bei der ein Agent mittels Q-Learning lernt, optimal zu navigieren. Das Ziel des Pac-Man-Agenten ist es, alle Kekse in einem Labyrinth zu fressen und dabei einem Geist auszuweichen.

## Funktionsweise

Das Projekt nutzt die Pygame-Bibliothek für die grafische Darstellung und die Logik des Spiels. Der Agent lernt durch Interaktion mit der Spielumgebung, indem er für seine Aktionen Belohnungen oder Bestrafungen erhält.

### Spiel-Logik

Das Spiel wird in Episoden ausgeführt. In jeder Episode versucht Pac-Man, alle Kekse zu fressen, ohne vom Geist gefangen zu werden oder das Zeitlimit zu überschreiten.

  - **Pac-Man**: Gesteuert durch den Q-Learning-Agenten. Bewegt sich durch das Labyrinth, um Kekse zu sammeln.
  - **Geist**: Verfolgt Pac-Man mit einer einfachen Logik, die darauf abzielt, den Abstand zu Pac-Man zu verringern.
  - **Kekse**: Im Labyrinth verteilt. Das Fressen eines Kekses gibt eine positive Belohnung.
  - **Wände**: Unpassierbare Hindernisse für Pac-Man und den Geist.

### Q-Learning-Agent

Der Agent trifft Entscheidungen auf der Grundlage einer Q-Tabelle, die die erwartete Belohnung für jede Aktion in jedem Zustand speichert.

  - **Zustand**: Definiert durch die Position von Pac-Man, die Position des Geistes und den Status der nahegelegenen Kekse. Der Keksstatus um Pac-Man herum (oben, unten, links, rechts) wird als Bitmaske kodiert.
  - **Aktionen**: Der Agent kann sich nach oben, unten, links oder rechts bewegen.
  - **Lernen**: Der Agent verwendet die Epsilon-Greedy-Strategie, um zwischen der Erkundung neuer Aktionen und der Ausnutzung bekannter guter Aktionen abzuwägen. Die Q-Tabelle wird nach jeder Aktion mithilfe der Bellman-Gleichung aktualisiert, die die erhaltene Belohnung und den maximalen Q-Wert des nächsten Zustands berücksichtigt.

### Belohnungsstruktur

Das Belohnungssystem ist so konzipiert, dass der Agent zu erwünschtem Verhalten motiviert wird:

  - **+100 Punkte**: für den Sieg durch das Fressen aller Kekse.
  - **+10 Punkte**: für das Fressen eines einzelnen Kekses.
  - **-0.1 Punkte**: für jeden Schritt, um den Agenten zu ermutigen, den schnellsten Weg zu finden.
  - **-20 Punkte**: bei Überschreitung der maximalen Anzahl von Schritten pro Episode.
  - **-50 Punkte**: bei einer Kollision mit dem Geist.

## Projektstruktur

Das Projekt ist in mehrere Python-Dateien aufgeteilt:

  - **`main.py`**: Der Haupteinstiegspunkt, der die Trainingsschleife startet und die Ergebnisse plottet.
  - **`game.py`**: Enthält die Hauptklasse `Game`, die die Spiellogik, den Spielzustand und das Rendern verwaltet.
  - **`game_objects.py`**: Definiert die Klassen für `Pacman` und `Ghost`, einschließlich ihrer Bewegung und ihres Aussehens.
  - **`q_learning_agent.py`**: Implementiert den `QLearningAgent`, der die Q-Tabelle verwaltet, Aktionen auswählt und aus Erfahrungen lernt.
  - **`constants.py`**: Speichert alle globalen Konstanten wie Bildschirmabmessungen, Farben und Q-Learning-Parameter.
  - **`.gitignore`**: Spezifiziert Dateien und Verzeichnisse, die von der Versionskontrolle ausgeschlossen werden sollen.

## Voraussetzungen

Stellen Sie sicher, dass die folgenden Python-Bibliotheken installiert sind:

  - **Pygame**: Für die Spiel-Engine und die grafische Darstellung.
  - **Matplotlib**: Zum Plotten der Trainingsergebnisse.
  - **NumPy**: Für die effiziente Verwaltung der Q-Tabelle und numerische Operationen.

Sie können die erforderlichen Bibliotheken mit dem folgenden Befehl installieren:

```bash
pip install pygame matplotlib numpy
```

## Ausführung

Um das Training des Pac-Man-Agenten zu starten, führen Sie die Hauptdatei aus:

```bash
python main.py
```

Während des Trainings wird der Fortschritt in der Konsole ausgegeben, einschließlich der Belohnung für jede Episode sowie der Anzahl der Siege und Niederlagen. Nach Abschluss des Trainings wird ein Diagramm angezeigt, das die Belohnung pro Episode und einen gleitenden Durchschnitt darstellt, um den Lernfortschritt zu visualisieren.
