# API Auto-Modifiable

[English version](./README.md)

ATTENTION : VEUILLEZ NE PAS UTILISER CECI DANS LA VRAIE VIE - PREUVE DE CONCEPT UNIQUEMENT

## Qu'est-ce que c'est

Ceci est une tentative de créer une API capable d'accepter des requêtes POST qui entraînent des changements dans sa propre base de code et donc dans sa propre surface d'API.

Dans son état actuel, il est TRÈS DANGEREUX de déployer ceci n'importe où sur internet.

Le cœur de cette API est un gestionnaire de requête POST unique qui :

1. Accepte du code Python sous forme de chaîne de caractères
   1. Nous nous attendons à ce qu'il soit dans un format particulier - voir `healthcheck.py` pour référence
2. Commite le code dans un fichier de son propre dépôt GitHub
3. Met à jour `app.py` pour exposer la nouvelle route dans l'API
4. Déclenche un nouveau déploiement (nous avons utilisé Render car nous y sommes habitués)

## POURQUOI ??

Nous avions une idée vague que cela pourrait bien fonctionner avec les GPTs / l'API Assistants d'OpenAI pour permettre à un GPT d'amorcer ses propres actions.

Il s'avère que les GPTs n'importent pas dynamiquement la documentation de l'API à partir d'une URL fournie, donc cela ne fonctionne pas vraiment sans avoir à recharger les actions chaque fois qu'un nouveau point de terminaison est créé.

Pour plus de détails sur la configuration GPT, voir ci-dessous.

## Utilisation et installation

Ceci est un projet FastAPI, donc installez les dépendances à partir de `requirements.txt` et lancez `./bin/dev` pour démarrer le serveur de développement localement.

## Utiliser cette API avec un GPT

Nous avons testé l'utilisation de cette API comme backend pour des actions GPT. La configuration que nous avons utilisée est ci-dessous.

Nom : `API Builder`

Description : `Créer des points de terminaison d'API à la volée`

Instructions :

    Vous créez des points de terminaison d'API en écrivant du code Python pour un backend FastAPI. Un exemple de code que vous pourriez écrire est :

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    @router.get("/test")
    def test():
        return {"status": "test"}
    ```

    pour lequel, vous utiliseriez le chemin de fichier "test.py", par exemple.

    Assurez-vous de toujours utiliser

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    ```

    lorsque vous créez de nouveaux points de terminaison.

Les actions ont été importées depuis le point de terminaison `/openai.json` exposé par le serveur FastAPI, mais nous avons dû ajouter manuellement l'URL de notre serveur au document pour faire fonctionner les actions.

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

Les nouvelles dépendances ne sont pas gérées actuellement (par exemple, si un code Python pour un nouveau point de terminaison utilise numpy, nous n'essayons pas d'installer les dépendances manquantes).
