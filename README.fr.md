# API auto-modifiante

AVERTISSEMENT : NE PAS UTILISER EN PRODUCTION — PREUVE DE CONCEPT UNIQUEMENT

## Qu'est-ce que c'est ?

Ceci est une tentative de créer une API qui peut accepter des requêtes POST
qui entraînent des modifications de son propre code source et donc de sa
surface d'API.

Dans son état actuel, il est TRÈS DANGEREUX de la déployer sur Internet.

Le cœur de cette API est un unique gestionnaire de requête POST qui :

1. Accepte du code Python sous forme de chaîne
   1. On s'attend à un format particulier — voir `healthcheck.py` pour référence
2. Commit le code dans un fichier de son propre dépôt GitHub
3. Met à jour `app.py` pour exposer la nouvelle route dans l'API
4. Déclenche un nouveau déploiement (nous avons utilisé Render par habitude)

## POURQUOI ??

Nous avions une idée à moitié aboutie : cela pourrait bien fonctionner avec les GPTs / l'Assistants API d'OpenAI
pour permettre à un GPT d'amorcer ses propres actions.

Il s'avère que les GPTs n'importent pas dynamiquement la documentation d'API à partir d'une URL fournie,
ce qui fait que cela ne fonctionne pas vraiment sans recharger les actions à chaque fois qu'un
nouvel endpoint est créé.

Pour les détails sur la configuration du GPT, voir ci-dessous.

## Installation et utilisation

C'est un projet FastAPI. Installez les dépendances depuis `requirements.txt` et
exécutez `./bin/dev` pour démarrer le serveur de développement en local.

## Utiliser cette API avec un GPT

Nous avons testé cette API comme backend pour des actions GPT. La configuration utilisée est ci-dessous.

Nom : `API Builder`

Description : `Créer des endpoints d'API à la volée`

Instructions :

    Vous créez des endpoints d'API en écrivant du code Python pour un backend FastAPI. Un exemple de code que vous pourriez écrire :

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    @router.get("/test")
    def test():
        return {"status": "test"}
    ```

    pour lequel vous utiliseriez le chemin de fichier "test.py", par exemple.

    Assurez-vous d'utiliser toujours :

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    ```

    lorsque vous créez de nouveaux endpoints.

Les actions ont été importées depuis l'endpoint `/openai.json` exposé par le serveur FastAPI, mais nous
avons dû ajouter manuellement l'URL de notre serveur au document pour que les actions fonctionnent.

### Exemple :
![](self-modifying-gpt.png)

Requête envoyée au backend :

```json
{
  "code": "from fastapi import APIRouter\nimport random\n\nrouter = APIRouter()\n\n@router.get(\"/random-number\")\ndef generate_random_number():\n    return {\"random_number\": random.randint(1, 100)}",
  "filepath": "random_number.py"
}
```

## Limites connues

Les nouvelles dépendances ne sont pas gérées pour le moment (par exemple, si du code Python pour un nouvel endpoint
utilise numpy, nous n'essayons pas d'installer les dépendances manquantes).
