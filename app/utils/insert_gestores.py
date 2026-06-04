"""
Initial manager data loader.

Responsible for inserting default managers into the database.

From Root dir run the command below:
python -m app.utils.insert_gestores
"""

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.gestor import Gestor

GESTORES = [
    {
        "nome": "Izoneide Fidelis Virgínio",
        "telefone": "+55 83 9835-4221",
        "escola": "Rafael Clementino (Sítio Coelho)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Cristiane Alves Carneiro",
        "telefone": "+55 83 9644-4858",
        "escola": "Celso Carneiro (Conjunto Dona Toinha)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Josefa Geane Aparecida Gonçalves da Silva",
        "telefone": "+55 83 9942-1403",
        "escola": "Creche Tia Tida (Próximo a Loja de Paulinho do Alumúnio)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maria das Dores Vicente Dionísio",
        "telefone": "+55 83 9636-8970",
        "escola": "Creche Socorro Viana (Matadouro)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maurino Cassiano Filho",
        "telefone": "+55 83 9415-6146",
        "escola": "Creche José Passos (Conjunto Dona Toinha)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Valdilânia da Silva Pereira",
        "telefone": "+55 83 9887-3609",
        "escola": "Creche Olívia Bronzeado (Bela Vista 1)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maria da Penha Diniz Alves",
        "telefone": "+55 83 9937-2545",
        "escola": "Creche Wilson Pereira (Lagoa do Mato)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maria das Dôres de Melo Silva",
        "telefone": "+55 83 9652-0259",
        "escola": "Antônio Carneiro (Subida do Palma)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Rosa Balbino da Silva",
        "telefone": "+55 83 9377-7902",
        "escola": "Escola Paulo Freire (Assentamento Oziel Pereira)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "José Laurentino Neto",
        "telefone": "+55 83 9911-0162",
        "escola": "Escola Estanislau Eloy (Deixar no Geraldão)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Elenice Batista da Silva Lima",
        "telefone": "+55 83 9194-7649",
        "escola": "Escola Gercina Eloy (Rua da prefeitura)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Ivone de Souza Nunes Neta",
        "telefone": "+55 83 9607-9805",
        "escola": "Escola José Delfino (Sítio Queimadas)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Sandra Batista Fernandes",
        "telefone": "+55 83 9950-3073",
        "escola": "Escola Pedro Batista (Lagoa do Mato)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "João Lucas Soares da Silva",
        "telefone": "+55 83 8198-3189",
        "escola": "Escola Júlia Vitório",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maria Poliana de Souza Lima",
        "telefone": "+55 83 9887-0576",
        "escola": "Escola Maria Batista (Lagoa do Mato)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Célia Maria da Silva Lima da Silva",
        "telefone": "+55 83 9627-6526",
        "escola": "Escola Margarida de Almeida (Lagoa do Mato)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Daniela Raiane Batista da Silva",
        "telefone": "+55 83 9314-1714",
        "escola": "Escola José Cazuza (Sítio lajedo do teteu)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Roberlânia Marinho",
        "telefone": "+55 83 9987-2282",
        "escola": "Escola Manoel Joca (Deixar na casa da merenda)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Aline Costa",
        "telefone": "+55 83 8167-2070",
        "escola": "Escola Severino Bronzeado (Lagoa do Jogo)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
]


def insert_gestores() -> None:
    """
    Insert default managers into database.
    """

    db: Session = SessionLocal()

    try:
        for gestor_data in GESTORES:

            # Skip existing phone numbers
            gestor_exists = (
                db.query(Gestor)
                .filter(
                    Gestor.telefone == gestor_data["telefone"]
                )
                .first()
            )

            if gestor_exists:
                continue

            gestor = Gestor(**gestor_data)

            db.add(gestor)

        db.commit()

        print(
            "Managers inserted successfully."
        )

    finally:
        db.close()


if __name__ == "__main__":
    insert_gestores()
