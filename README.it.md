[English](README.md) | Italiano

# API Automodificante

ATTENZIONE: SI PREGA DI NON USARLA NELLA VITA REALE - SOLO PROVA DI CONCETTO

## Cos'è questo

Questo è un tentativo di creare un'API che possa accettare richieste POST che
comportano modifiche al proprio codice e quindi alla propria superficie API.

Nel suo stato attuale, è MOLTO PERICOLOSO da implementare ovunque su internet.

Il nucleo di questa API è un singolo gestore di richieste POST che:

1. Accetta del codice Python come stringa
   1. Ci aspettiamo che sia in un formato particolare - vedi `healthcheck.py` per riferimento
2. Esegue il commit del codice in un file nel proprio repository GitHub
3. Aggiorna `app.py` per esporre la nuova rotta nell'API
4. Attiva una nuova distribuzione (abbiamo usato Render perché ci è familiare)

## PERCHÉ??

Avevamo un'idea a metà che questo potesse funzionare bene con i GPT/OpenAI's
Assistants API per consentire a un GPT di avviare le proprie azioni.

Si scopre che i GPT non importano dinamicamente la documentazione API da un URL
fornito, quindi questo non funziona davvero senza dover ricaricare le azioni
ogni volta che viene creato un nuovo endpoint.

Per i dettagli sulla configurazione del GPT, vedere di seguito.

## Utilizzo e installazione

Questo è un progetto FastAPI, quindi installa le dipendenze da `requirements.txt`
e avvia `./bin/dev` per avviare il server di sviluppo localmente.

## Utilizzo di questa API con un GPT

Abbiamo testato l'utilizzo di questa API come backend per le azioni GPT.
La configurazione che abbiamo utilizzato è la seguente.

Nome: `API Builder`

Descrizione: `Crea endpoint API al volo`

Istruzioni:

    Creerai endpoint API scrivendo codice Python per un backend FastAPI.
    Un esempio del codice che potresti scrivere è:

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    @router.get("/test")
    def test():
        return {"status": "test"}
    ```

    per il quale useresti il percorso del file "test.py", ad esempio.

    Assicurati di usare sempre

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    ```

    quando crei nuovi endpoint.

Le azioni sono state importate dall'endpoint `/openai.json` esposto dal server
FastAPI, ma abbiamo dovuto aggiungere manualmente l'URL del nostro server al
documento per far funzionare le azioni.

### Esempio:
![](self-modifying-gpt.png)

Richiesta inviata al backend:

```json
{
  "code": "from fastapi import APIRouter\nimport random\n\nrouter = APIRouter()\n\n@router.get(\"/random-number\")\ndef generate_random_number():\n    return {\"random_number\": random.randint(1, 100)}",
  "filepath": "random_number.py"
}
```

## Limitazioni note

Le nuove dipendenze non sono attualmente gestite (ad esempio, se un codice
Python per un nuovo endpoint utilizza numpy, non tentiamo di installare
dipendenze mancanti).
