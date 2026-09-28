from datetime import datetime

from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields

from models import db, Treino, RegistroExercicio

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///treinos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
db.init_app(app)

api = Api(
    app,
    version="1.0",
    title="AvocaGym API",
    description=(
        "API para registrar treinos de academia. "
        "O catálogo de exercícios é consultado pelo front-end na wger.de "
        "(https://wger.de/api/v2/exercise/); aqui só persistimos o que o "
        "usuário efetivamente treinou."
    ),
    doc="/docs",
)

ns = api.namespace("treinos", description="Operações de treino")

exercicio_model = api.model("RegistroExercicio", {
    "exercicio_wger_id": fields.Integer(required=True, description="ID do exercício na wger.de"),
    "nome_exercicio": fields.String(required=True),
    "series": fields.Integer(required=True),
    "repeticoes": fields.Integer(required=True),
    "carga_kg": fields.Float(required=False),
})

treino_model = api.model("Treino", {
    "data": fields.String(required=True, description="Data do treino (YYYY-MM-DD)"),
    "observacao": fields.String(required=False),
    "exercicios": fields.List(fields.Nested(exercicio_model), required=False),
})


def _monta_exercicios(payload_exercicios):
    return [
        RegistroExercicio(
            exercicio_wger_id=ex["exercicio_wger_id"],
            nome_exercicio=ex["nome_exercicio"],
            series=ex["series"],
            repeticoes=ex["repeticoes"],
            carga_kg=ex.get("carga_kg"),
        )
        for ex in payload_exercicios
    ]


@ns.route("")
class TreinoList(Resource):
    @ns.doc(params={
        "data": "Filtra treinos por data exata (YYYY-MM-DD)",
        "page": "Número da página (default 1)",
        "per_page": "Itens por página (default 10)",
    })
    def get(self):
        """Lista treinos, com filtro por data e paginação"""
        query = Treino.query

        data_filtro = request.args.get("data")
        if data_filtro:
            query = query.filter(
                Treino.data == datetime.strptime(data_filtro, "%Y-%m-%d").date()
            )

        query = query.order_by(Treino.data.desc())

        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "total": paginated.total,
            "page": page,
            "per_page": per_page,
            "treinos": [t.to_dict() for t in paginated.items],
        }

    @ns.expect(treino_model)
    def post(self):
        """Cria um novo treino com seus exercícios"""
        payload = request.json

        treino = Treino(
            data=datetime.strptime(payload["data"], "%Y-%m-%d").date(),
            observacao=payload.get("observacao"),
        )
        treino.exercicios = _monta_exercicios(payload.get("exercicios", []))

        db.session.add(treino)
        db.session.commit()

        return treino.to_dict(), 201


@ns.route("/<int:treino_id>")
class TreinoDetail(Resource):
    def get(self, treino_id):
        """Busca um treino pelo ID"""
        treino = Treino.query.get_or_404(treino_id)
        return treino.to_dict()

    @ns.expect(treino_model)
    def put(self, treino_id):
        """Edita um treino existente (substitui data, observação e exercícios)"""
        treino = Treino.query.get_or_404(treino_id)
        payload = request.json

        treino.data = datetime.strptime(payload["data"], "%Y-%m-%d").date()
        treino.observacao = payload.get("observacao")

        treino.exercicios.clear()
        treino.exercicios.extend(_monta_exercicios(payload.get("exercicios", [])))

        db.session.commit()
        return treino.to_dict()

    def delete(self, treino_id):
        """Remove um treino"""
        treino = Treino.query.get_or_404(treino_id)
        db.session.delete(treino)
        db.session.commit()
        return {"mensagem": "Treino removido"}, 200


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
