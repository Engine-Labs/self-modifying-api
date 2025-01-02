# Selbstmodifizierende API

WARNUNG: BITTE NICHT IM PRODUKTIVEINSATZ VERWENDEN - NUR EIN PROOF OF CONCEPT

## Was ist das?

Dies ist ein Versuch, eine API zu erstellen, die POST-Anfragen akzeptieren kann, die zu Änderungen in ihrer eigenen Codebasis und damit ihrer eigenen API-Oberfläche führen.

In seinem aktuellen Zustand ist es SEHR GEFÄHRLICH, dies irgendwo im Internet zu deployen.

Der Kern dieser API ist ein einzelner POST-Request-Handler, der:

1. Python-Code als String akzeptiert
   1. Der Code muss in einem bestimmten Format vorliegen - siehe `healthcheck.py` als Referenz
2. Den Code in einer Datei im eigenen GitHub-Repository speichert
3. Die `app.py` aktualisiert, um die neue Route in der API verfügbar zu machen
4. Ein neues Deployment auslöst (wir haben Render verwendet, da wir damit vertraut sind)

## WARUM??

Wir hatten die halbausgegorene Idee, dass dies gut mit GPTs/OpenAIs Assistants API funktionieren könnte,
um einem GPT zu ermöglichen, seine eigenen Aktionen zu bootstrappen.

Es stellte sich heraus, dass GPTs keine API-Dokumentation dynamisch von einer bereitgestellten URL importieren,
sodass dies nicht wirklich funktioniert, ohne die Aktionen bei jeder neuen Endpoint-Erstellung neu laden zu müssen.

Details zur GPT-Konfiguration finden Sie weiter unten.

## Verwendung und Installation

Dies ist ein FastAPI-Projekt. Installieren Sie die Abhängigkeiten aus `requirements.txt` und
führen Sie `./bin/dev` aus, um den Entwicklungsserver lokal zu starten.

## Verwendung dieser API mit einem GPT

Wir haben diese API als Backend für GPT-Aktionen getestet. Die von uns verwendete Konfiguration ist unten aufgeführt.

Name: `API Builder`

Beschreibung: `Erstelle API-Endpoints im laufenden Betrieb`

Anweisungen:

    Sie erstellen API-Endpoints, indem Sie Python-Code für ein FastAPI-Backend schreiben. Ein Beispiel für den Code, den Sie schreiben könnten, ist:

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    @router.get("/test")
    def test():
        return {"status": "test"}
    ```

    wofür Sie zum Beispiel den Dateipfad "test.py" verwenden würden.

    Stellen Sie sicher, dass Sie immer

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    ```

    verwenden, wenn Sie neue Endpoints erstellen.

Die Aktionen wurden vom `/openai.json`-Endpoint importiert, der vom FastAPI-Server bereitgestellt wird,
aber wir mussten unsere Server-URL manuell zum Dokument hinzufügen, damit die Aktionen funktionieren.

### Beispiel:
![](self-modifying-gpt.png)

Anfrage an das Backend:

```json
{
  "code": "from fastapi import APIRouter\nimport random\n\nrouter = APIRouter()\n\n@router.get(\"/random-number\")\ndef generate_random_number():\n    return {\"random_number\": random.randint(1, 100)}",
  "filepath": "random_number.py"
}
```

## Bekannte Einschränkungen

Neue Abhängigkeiten werden derzeit nicht behandelt (z.B. wenn Python-Code für einen neuen Endpoint
numpy verwendet, versuchen wir nicht, fehlende Abhängigkeiten zu installieren).