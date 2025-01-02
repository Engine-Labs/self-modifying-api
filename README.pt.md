# API Auto-Modificável

AVISO: POR FAVOR, NÃO USE ISTO EM PRODUÇÃO - APENAS PROVA DE CONCEITO

## O que é isto

Esta é uma tentativa de criar uma API que pode aceitar requisições POST que resultam em
alterações em seu próprio código-fonte e, consequentemente, em sua própria interface de API.

No seu estado atual, é MUITO PERIGOSO implantar isso em qualquer lugar na internet.

O núcleo desta API é um único manipulador de requisições POST que:

1. Aceita código Python como string
   1. Esperamos que esteja em um formato específico - veja `healthcheck.py` como referência
2. Faz commit do código em um arquivo no seu próprio repositório GitHub
3. Atualiza `app.py` para expor a nova rota na API
4. Dispara uma nova implantação (usamos o Render porque estamos familiarizados com ele)

## POR QUÊ??

Tivemos uma ideia meio crua de que isso poderia funcionar bem com GPTs/API de Assistentes da OpenAI
para permitir que um GPT inicialize suas próprias ações.

Descobrimos que os GPTs não importam dinamicamente a documentação da API de uma URL fornecida,
então isso não funciona realmente sem ter que recarregar as ações toda vez que um
novo endpoint é criado.

Para detalhes sobre a configuração do GPT, veja abaixo.

## Uso e instalação

Este é um projeto FastAPI, então instale as dependências do `requirements.txt` e
execute `./bin/dev` para iniciar o servidor de desenvolvimento localmente.

## Usando esta API com um GPT

Testamos usar esta API como backend para ações do GPT. A configuração que usamos está abaixo.

Nome: `API Builder`

Descrição: `Crie endpoints de API em tempo real`

Instruções:

    Você cria endpoints de API escrevendo código Python para um backend FastAPI. Um exemplo do código que você pode escrever é:

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    @router.get("/test")
    def test():
        return {"status": "test"}
    ```

    para o qual você usaria o caminho do arquivo "test.py", por exemplo.

    Certifique-se de sempre usar

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    ```

    quando criar novos endpoints.

As ações foram importadas do endpoint `/openai.json` exposto pelo servidor FastAPI, mas
tivemos que adicionar manualmente nossa URL do servidor ao documento para fazer as ações funcionarem.

### Exemplo:
![](self-modifying-gpt.png)

Requisição enviada ao backend:

```json
{
  "code": "from fastapi import APIRouter\nimport random\n\nrouter = APIRouter()\n\n@router.get(\"/random-number\")\ndef generate_random_number():\n    return {\"random_number\": random.randint(1, 100)}",
  "filepath": "random_number.py"
}
```

## Limitações conhecidas

Novas dependências não são tratadas atualmente (por exemplo, se algum código Python para um novo endpoint
usa numpy, não tentamos instalar as dependências ausentes).