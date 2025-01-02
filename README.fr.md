# API Auto-Modifiable

⚠️ ATTENTION : VEUILLEZ NE PAS UTILISER CECI EN PRODUCTION - PREUVE DE CONCEPT UNIQUEMENT

## Qu'est-ce que c'est ?

C'est une tentative de créer une API capable d'accepter des requêtes POST qui entraînent des modifications de sa propre base de code et, par conséquent, de sa propre interface API.

Dans son état actuel, il est TRÈS DANGEREUX de déployer ceci sur Internet.

Le cœur de cette API est un gestionnaire de requêtes POST unique qui :

1. Accepte du code Python sous forme de chaîne de caractères
   1. Le code doit suivre un format particulier - voir `healthcheck.py` comme référence
2. Commit le code dans un fichier de son propre dépôt GitHub
3. Met à jour `app.py` pour exposer la nouvelle route dans l'API
4. Déclenche un nouveau déploiement (nous avons utilisé Render car nous le connaissons bien)

## POURQUOI ??

Nous avions une idée à moitié développée que cela pourrait bien fonctionner avec les GPTs/l'API Assistants d'OpenAI pour permettre à un GPT d'amorcer ses propres actions.

Il s'avère que les GPTs n'importent pas dynamiquement la documentation de l'API depuis une URL fournie, donc cela ne fonctionne pas vraiment sans avoir à recharger les actions à chaque fois qu'un nouvel endpoint est créé.

Pour plus de détails sur la configuration GPT, voir ci-dessous.

## Utilisation et installation

C'est un projet FastAPI, donc installez les dépendances depuis `requirements.txt` et exécutez `./bin/dev` pour démarrer le serveur de développement localement.

## Utilisation de cette API avec un GPT

Nous avons testé l'utilisation de cette API comme backend pour les actions GPT. La configuration que nous avons utilisée est ci-dessous.

Nom : `API Builder`

Description : `Créer des endpoints API à la volée`

Instructions :

    Vous créez des endpoints API en écrivant du code Python pour un backend FastAPI. Voici un exemple du code que vous pourriez écrire :

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    @router.get("/test")
    def test():
        return {"status": "test"}
    ```

    pour lequel vous utiliseriez le chemin de fichier "test.py", par exemple.

    Assurez-vous de toujours utiliser :

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    ```

    lorsque vous créez de nouveaux endpoints.

Les actions ont été importées depuis l'endpoint `/openai.json` exposé par le serveur FastAPI, mais nous avons dû ajouter manuellement l'URL de notre serveur au document pour faire fonctionner les actions.

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

Les nouvelles dépendances ne sont actuellement pas gérées (par exemple, si un nouveau code Python pour un endpoint utilise numpy, nous n'essayons pas d'installer les dépendances manquantes).