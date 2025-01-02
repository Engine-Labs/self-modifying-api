# API Auto-Modificable

ADVERTENCIA: POR FAVOR NO USE ESTO EN UN ENTORNO REAL - SOLO ES UNA PRUEBA DE CONCEPTO

## ¿Qué es esto?

Este es un intento de crear una API que puede aceptar solicitudes POST que resultan en cambios en su propio código base y, por lo tanto, en su propia superficie de API.

En su estado actual, es MUY PELIGROSO implementarlo en cualquier lugar de Internet.

El núcleo de esta API es un único manejador de solicitudes POST que:

1. Acepta código Python como una cadena de texto
   1. Se espera que esté en un formato particular - ver `healthcheck.py` como referencia
2. Confirma el código en un archivo en su propio repositorio de GitHub
3. Actualiza `app.py` para exponer la nueva ruta en la API
4. Activa un nuevo despliegue (usamos Render porque estamos familiarizados con él)

## ¿POR QUÉ?

Tuvimos una idea medio desarrollada de que esto podría funcionar bien con GPTs/API de Asistentes de OpenAI para permitir que un GPT inicie sus propias acciones.

Resulta que los GPTs no importan dinámicamente la documentación de la API desde una URL proporcionada, por lo que esto realmente no funciona sin tener que recargar las acciones cada vez que se crea un nuevo endpoint.

Para detalles sobre la configuración de GPT, ver más abajo.

## Uso e instalación

Este es un proyecto FastAPI, así que instale las dependencias desde `requirements.txt` y ejecute `./bin/dev` para iniciar el servidor de desarrollo localmente.

## Usando esta API con un GPT

Probamos usar esta API como backend para acciones de GPT. La configuración que usamos está a continuación.

Nombre: `API Builder`

Descripción: `Crear endpoints de API al vuelo`

Instrucciones:

    Creas endpoints de API escribiendo código Python para un backend FastAPI. Un ejemplo del código que podrías escribir es:

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    @router.get("/test")
    def test():
        return {"status": "test"}
    ```

    para el cual usarías la ruta de archivo "test.py", por ejemplo.

    Asegúrate de siempre usar:

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    ```

    cuando crees nuevos endpoints.

Las acciones se importaron desde el endpoint `/openai.json` expuesto por el servidor FastAPI, pero tuvimos que agregar manualmente la URL de nuestro servidor al documento para hacer que las acciones funcionen.

### Ejemplo:
![](self-modifying-gpt.png)

Solicitud enviada al backend:

```json
{
  "code": "from fastapi import APIRouter\nimport random\n\nrouter = APIRouter()\n\n@router.get(\"/random-number\")\ndef generate_random_number():\n    return {\"random_number\": random.randint(1, 100)}",
  "filepath": "random_number.py"
}
```

## Limitaciones conocidas

Actualmente no se manejan las nuevas dependencias (por ejemplo, si algún código Python para un nuevo endpoint usa numpy, no intentamos instalar las dependencias faltantes).