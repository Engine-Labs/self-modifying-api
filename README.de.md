# Selbstmodifizierende API

Hinweis: Dies ist die deutsche Fassung der README. Die englische Version findest du in `README.md`.

WARNUNG: BITTE NICHT IN PRODUKTIONSUMGEBUNGEN VERWENDEN – NUR EIN PROOF OF CONCEPT

## Was ist das?

Dies ist ein Versuch, eine API zu bauen, die POST-Anfragen akzeptiert, die wiederum Änderungen an ihrem eigenen Code vornehmen und damit ihre eigene API-Oberfläche verändern.

In ihrem aktuellen Zustand ist es SEHR GEFÄHRLICH, dies irgendwo öffentlich ins Internet zu deployen.

Der Kern dieser API ist ein einzelner POST-Request-Handler, der:

1. Python-Code als String entgegennimmt
   1. Wir erwarten ein bestimmtes Format – siehe `healthcheck.py` als Referenz
2. Den Code als Datei in das eigene GitHub-Repository committet
3. Die `app.py` aktualisiert, um die neue Route in der API verfügbar zu machen
4. Eine neue Bereitstellung auslöst (wir haben Render verwendet, weil wir damit vertraut sind)

## WARUM??

Wir hatten die halbgar gebliebene Idee, dass das mit GPTs bzw. OpenAI's Assistants API gut funktionieren könnte, um es einem GPT zu erlauben, seine eigenen Actions zu bootstrappen.

Es stellte sich heraus, dass GPTs API-Dokumentationen nicht dynamisch von einer bereitgestellten URL importieren. Deshalb funktioniert das nicht wirklich, ohne die Actions jedes Mal neu zu laden, wenn ein neuer Endpoint erstellt wird.

Details zur GPT-Konfiguration findest du unten.

## Nutzung und Installation

Dies ist ein FastAPI-Projekt. Installiere die Abhängigkeiten aus `requirements.txt` und starte den lokalen Entwicklungsserver mit `./bin/dev`.

## Verwendung dieser API mit einem GPT

Wir haben getestet, diese API als Backend für GPT-Aktionen zu verwenden. Die von uns verwendete Konfiguration ist unten beschrieben.

Name: `API Builder`

Beschreibung: `API-Endpunkte spontan erzeugen`

Anweisungen:

    Du erstellst API-Endpunkte, indem du Python-Code für ein FastAPI-Backend schreibst. Ein Beispiel für den Code, den du schreiben könntest, ist:

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    @router.get("/test")
    def test():
        return {"status": "test"}
    ```

    Dafür würdest du beispielsweise den Dateipfad "test.py" verwenden.

    Achte darauf, immer

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    ```

    zu verwenden, wenn du neue Endpunkte erstellst.

Die Actions wurden vom Endpoint `/openai.json` importiert, der vom FastAPI-Server bereitgestellt wird. Wir mussten jedoch unsere Server-URL manuell in das Dokument eintragen, damit die Actions funktionieren.

### Beispiel

![](self-modifying-gpt.png)

Anfrage, die an das Backend gesendet wurde:

```json
{
  "code": "from fastapi import APIRouter\nimport random\n\nrouter = APIRouter()\n\n@router.get(\"/random-number\")\ndef generate_random_number():\n    return {\"random_number\": random.randint(1, 100)}",
  "filepath": "random_number.py"
}
```

## Bekannte Einschränkungen

Neue Abhängigkeiten werden derzeit nicht automatisch behandelt (z. B. wenn Python-Code für einen neuen Endpunkt `numpy` verwendet, versuchen wir nicht, fehlende Abhängigkeiten zu installieren).
