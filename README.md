# MVG live

![Lint](https://github.com/mkapra/MVG-Live/workflows/Python%20Lint/badge.svg)

Shows MVG live data.

Example:
```python
from mvgdepartures import Departures

departures_marienplatz = Departures("Marienplatz")
print(departures_marienplatz)
```

Output:
```
now      : S2       - Erding
now      : S4       - Geltendorf
In 1  min: S8       - Flughafen München
In 1  min: U6       - Klinikum Großhadern
In 2  min: S1       - Flughafen München
In 2  min: S1       - Freising
In 3  min: S1       - Leuchtenbergring
In 3  min: S1       - Leuchtenbergring
In 4  min: U6       - Garching, Forschungszentrum
In 4  min: S8       - Herrsching
In 5  min: S4       - Trudering
In 6  min: U3       - Fürstenried West
In 8  min: U3       - Moosach
In 8  min: S3       - Holzkirchen
In 8  min: S2       - Altomünster
In 10 min: S6       - Tutzing
In 11 min: U6       - Klinikum Großhadern
In 12 min: S7       - Wolfratshausen
In 13 min: S7       - Aying
In 14 min: U6       - Fröttmaning
```
