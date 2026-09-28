# AvocaGym API

API REST para registrar treinos de academia (data, observações e exercícios executados, com séries, repetições e carga). O catálogo de exercícios em si é consultado pelo front-end diretamente na [wger.de](https://wger.de) — esta API só persiste o que o usuário efetivamente treinou.

Projeto desenvolvido como MVP de componentização/microsserviços (Cenário 1: Interface + API principal + API externa).

## Stack

- Python 3.11 + Flask
- Flask-RESTX (rotas + Swagger automático)
- Flask-SQLAlchemy + SQLite

## Instalação local

```bash
git clone <url-deste-repositorio>
cd avocagym-api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

A API sobe em `http://localhost:5000`, e o banco `treinos.db` (SQLite) é criado automaticamente na primeira execução.

## Rodando via Docker

```bash
docker build -t avocagym-api .
docker run -p 5000:5000 avocagym-api
```

## Documentação (Swagger)

Disponível em [`http://localhost:5000/docs`](http://localhost:5000/docs) assim que a aplicação estiver rodando.

## Rotas

| Método | Rota            | Descrição                                              |
|--------|-----------------|----------------------------------------------------------|
| GET    | `/treinos`      | Lista treinos, com filtro por `data` e paginação (`page`, `per_page`) |
| GET    | `/treinos/:id`  | Detalha um treino específico                             |
| POST   | `/treinos`      | Cria um novo treino com seus exercícios                  |
| PUT    | `/treinos/:id`  | Edita um treino existente                                 |
| DELETE | `/treinos/:id`  | Remove um treino                                          |

## Modelo de dados

- **Treino**: `id`, `data`, `observacao`
- **RegistroExercicio**: `id`, `treino_id`, `exercicio_wger_id` (referência ao exercício na wger.de), `nome_exercicio`, `series`, `repeticoes`, `carga_kg`
