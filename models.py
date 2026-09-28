from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Treino(db.Model):
    __tablename__ = "treinos"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    observacao = db.Column(db.String(255), nullable=True)

    exercicios = db.relationship(
        "RegistroExercicio",
        backref="treino",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data.isoformat(),
            "observacao": self.observacao,
            "exercicios": [e.to_dict() for e in self.exercicios],
        }


class RegistroExercicio(db.Model):
    __tablename__ = "registros_exercicio"

    id = db.Column(db.Integer, primary_key=True)
    treino_id = db.Column(db.Integer, db.ForeignKey("treinos.id"), nullable=False)
    exercicio_wger_id = db.Column(db.Integer, nullable=False)
    nome_exercicio = db.Column(db.String(120), nullable=False)
    series = db.Column(db.Integer, nullable=False)
    repeticoes = db.Column(db.Integer, nullable=False)
    carga_kg = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "treino_id": self.treino_id,
            "exercicio_wger_id": self.exercicio_wger_id,
            "nome_exercicio": self.nome_exercicio,
            "series": self.series,
            "repeticoes": self.repeticoes,
            "carga_kg": self.carga_kg,
        }
