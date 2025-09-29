# API Auto-Modifiable

AVERTISSEMENT : VEUILLEZ NE PAS UTILISER CECI DANS LA VIE RÉELLE - PROOF OF CONCEPT UNIQUEMENT

## Qu'est-ce que c'est

Ceci est une tentative de créer une API qui peut accepter des requêtes POST qui entraînent des modifications de son propre codebase et donc de sa propre surface d'API.

Dans son état actuel, c'est TRÈS DANGEREUX à déployer n'importe où sur Internet.

Le cœur de cette API est un gestionnaire de requêtes POST unique qui :

1. Accepte du code Python sous forme de chaîne de caractères
   1. Nous nous attendons à ce qu'il soit dans un format particulier - voir `healthcheck.py` pour référence
2. Committe le code dans un fichier de son propre dépôt GitHub
3. Met à jour `app.py` pour exposer la nouvelle route dans l'API
4. Déclenche un nouveau déploiement (nous avons utilisé Render car nous le connaissons bien)

## POURQUOI ??

Nous avons eu une idée à moitié aboutie que cela pourrait bien fonctionner avec les GPTs/l'API Assistants d'OpenAI pour permettre à un GPT de démarrer ses propres actions.

Il s'avère que les GPTs n'importent pas dynamiquement la documentation de l'API à partir d'une URL fournie, donc cela ne fonctionne pas vraiment sans avoir à recharger les actions chaque fois qu'un nouveau point de terminaison est créé.

Pour plus de détails sur la configuration GPT, voir ci-dessous.

## Utilisation et installation

Ceci est un projet FastAPI, alors installez les dépendances de `requirements.txt` et exécutez `./bin/dev` pour démarrer le serveur de développement localement.

## Utiliser cette API avec un GPT

Nous avons testé cette API comme backend pour les actions GPT. La configuration que nous avons utilisée est ci-dessous.

Nom : `API Builder`

Description : `Crée des points de terminaison API à la volée`

Instructions :

    Vous créez des points de terminaison API en écrivant du code Python pour un backend FastAPI. Un exemple du code que vous pourriez écrire est :

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    @router.get("/test")
    def test():
        return {"status": "test"}
    ```

    pour lequel vous utiliseriez le chemin de fichier "test.py", par exemple.

    Assurez-vous de toujours utiliser

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    ```

    lorsque vous créez de nouveaux points de terminaison.

Les actions ont été importées du point de terminaison `/openai.json` exposé par le serveur FastAPI, mais nous avons dû ajouter manuellement notre URL de serveur au document pour que les actions fonctionnent.

### Exemple :
![](self-modifying-gpt.png)

Requête envoyée au backend :

```json
{
  "code": "from fastapi import APIRouter\nimport random\n\nrouter = APIRouter()\n\n@router.get(\"/random-number\")\ndef generate_random_number():\n    return {\"random_number\": random.randint(1, 100)}",
  "filepath": "random_number.py"
}
```

## Limitations connues

Les nouvelles dépendances ne sont pas actuellement gérées (par exemple, si du code Python pour un nouveau point de terminaison utilise numpy, nous n'essayons pas d'installer les dépendances manquantes).
