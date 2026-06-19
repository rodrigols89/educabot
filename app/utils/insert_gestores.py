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
        "nome": "Rose (Secretaria de Educação)",
        "telefone": "558396192515",
        "escola": "Secretaria de Educação",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Matheus Melo (Recepcionista)",
        "telefone": "558393858828",
        "escola": "Secretaria de Educação",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Tatiana Meira (Recepcionista)",
        "telefone": "558399502009",
        "escola": "Secretaria de Educação",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Izoneide Fidelis Virgínio",
        "telefone": "558398354221",
        "escola": "Rafael Clementino (Sítio Coelho)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Cristiane Alves Carneiro",
        "telefone": "558396444858",
        "escola": "Celso Carneiro (Conjunto Dona Toinha)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Josefa Geane Aparecida Gonçalves da Silva",
        "telefone": "558399421403",
        "escola": "Creche Tia Tida (Próximo a Loja de Paulinho do Alumúnio)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maria das Dores Vicente Dionísio",
        "telefone": "558396368970",
        "escola": "Creche Socorro Viana (Matadouro)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maurino Cassiano Filho",
        "telefone": "558394156146",
        "escola": "Creche José Passos (Conjunto Dona Toinha)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Valdilânia da Silva Pereira",
        "telefone": "558398873609",
        "escola": "Creche Olívia Bronzeado (Bela Vista 1)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Thayane Lopes Miranda Baracho Prazeres",
        "telefone": "558394029840",
        "escola": "Creche Olívia Bronzeado (Bela Vista 1)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maria da Penha Diniz Alves",
        "telefone": "558399372545",
        "escola": "Creche Wilson Pereira (Lagoa do Mato)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maria das Dôres de Melo Silva",
        "telefone": "558396520259",
        "escola": "Antônio Carneiro (Subida do Palma)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Rosa Balbino da Silva",
        "telefone": "558393777902",
        "escola": "Escola Paulo Freire (Assentamento Oziel Pereira)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Larissa da Silva",
        "telefone": "558399156766",
        "escola": "Escola Paulo Freire (Assentamento Oziel Pereira)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "José Laurentino Neto",
        "telefone": "558399110162",
        "escola": "Escola Estanislau Eloy (Deixar no Geraldão)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Sirley Arruda",
        "telefone": "558391709146",
        "escola": "Escola Estanislau Eloy (Deixar no Geraldão)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Elenice Batista da Silva Lima",
        "telefone": "558391947649",
        "escola": "Escola Gercina Eloy (Rua da prefeitura)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Rafaela Souto",
        "telefone": "558398025950",
        "escola": "Escola Gercina Eloy (Rua da prefeitura)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Ivone de Souza Nunes Neta",
        "telefone": "558396079805",
        "escola": "Escola José Delfino (Sítio Queimadas)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Sandra Batista Fernandes",
        "telefone": "558399503073",
        "escola": "Escola Pedro Batista (Lagoa do Mato)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "João Lucas Soares da Silva",
        "telefone": "5583981983189",
        "escola": "Escola Júlia Vitório",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Luzeni Oliveira Querino",
        "telefone": "558396553837",
        "escola": "Escola Júlia Vitório",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maria Poliana de Souza Lima",
        "telefone": "558398870576",
        "escola": "Escola Maria Batista (Lagoa do Mato)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Célia Maria da Silva Lima da Silva",
        "telefone": "558396276526",
        "escola": "Escola Margarida de Almeida (Lagoa do Mato)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Gabryella Freire Monteiro",
        "telefone": "558396241207",
        "escola": "Escola Margarida de Almeida (Lagoa do Mato)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Daniela Raiane Batista da Silva",
        "telefone": "558393141714",
        "escola": "Escola José Cazuza (Sítio lajedo do teteu)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Roberlânia Marinho",
        "telefone": "558399872282",
        "escola": "Escola Manoel Joca (Deixar na casa da merenda)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Aline Costa",
        "telefone": "5583981672070",
        "escola": "Escola Severino Bronzeado (Deixar na casa da merenda)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
]


def insert_gestores() -> None:

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
