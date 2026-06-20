# app/utils/insert_gestores.py

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.gestor import Gestor

GESTORES = [
    {
        "nome": "Glória Costureira",
        "telefone": "558396241663",
        "instituicao": "Ateliê da Glória",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Rose (Secretaria de Educação)",
        "telefone": "558396192515",
        "instituicao": "Secretaria de Educação",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Matheus Melo (Recepcionista)",
        "telefone": "558393858828",
        "instituicao": "Secretaria de Educação",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Tatiana Meira (Recepcionista)",
        "telefone": "558399502009",
        "instituicao": "Secretaria de Educação",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Izoneide Fidelis Virgínio (Gestor)",
        "telefone": "558398354221",
        "instituicao": "Rafael Clementino (Sítio Coelho)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Cristiane Alves Carneiro (Gestor)",
        "telefone": "558396444858",
        "instituicao": "Celso Carneiro (Conjunto Dona Toinha)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Josefa Geane Aparecida Gonçalves da Silva (Gestor)",
        "telefone": "558399421403",
        "instituicao": "Creche Tia Tida (Próximo a Loja de Paulinho do Alumúnio)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maria das Dores Vicente Dionísio (Gestor)",
        "telefone": "558396368970",
        "instituicao": "Creche Socorro Viana (Matadouro)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maurino Cassiano Filho (Gestor)",
        "telefone": "558394156146",
        "instituicao": "Creche José Passos (Conjunto Dona Toinha)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Valdilânia da Silva Pereira (Gestor)",
        "telefone": "558398873609",
        "instituicao": "Creche Olívia Bronzeado (Bela Vista 1)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Thayane Lopes Miranda Baracho Prazeres (Vice Gestor)",
        "telefone": "558394029840",
        "instituicao": "Creche Olívia Bronzeado (Bela Vista 1)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maria da Penha Diniz Alves (Gestor)",
        "telefone": "558399372545",
        "instituicao": "Creche Wilson Pereira (Lagoa do Mato)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maria das Dôres de Melo Silva (Gestor)",
        "telefone": "558396520259",
        "instituicao": "Antônio Carneiro (Subida do Palma)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Rosa Balbino da Silva (Gestor)",
        "telefone": "558393777902",
        "instituicao": "Escola Paulo Freire (Assentamento Oziel Pereira)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Larissa da Silva (Secretária Adm.)",
        "telefone": "558399156766",
        "instituicao": "Escola Paulo Freire (Assentamento Oziel Pereira)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "José Laurentino Neto (Gestor)",
        "telefone": "558399110162",
        "instituicao": "Escola Estanislau Eloy (Deixar no Geraldão)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Sirley Arruda (Vice Gestor)",
        "telefone": "558391709146",
        "instituicao": "Escola Estanislau Eloy (Deixar no Geraldão)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Elenice Batista da Silva Lima (Gestor)",
        "telefone": "558391947649",
        "instituicao": "Escola Gercina Eloy (Rua da prefeitura)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Rafaela Souto (Vice Gestor)",
        "telefone": "558398025950",
        "instituicao": "Escola Gercina Eloy (Rua da prefeitura)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Ivone de Souza Nunes Neta (Gestor)",
        "telefone": "558396079805",
        "instituicao": "Escola José Delfino (Sítio Queimadas)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Sandra Batista Fernandes (Gestor)",
        "telefone": "558399503073",
        "instituicao": "Escola Pedro Batista (Lagoa do Mato)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "João Lucas Soares da Silva (Gestor)",
        "telefone": "5583981983189",
        "instituicao": "Escola Júlia Vitório",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Luzeni Oliveira Querino (Vice Gestor)",
        "telefone": "558396553837",
        "instituicao": "Escola Júlia Vitório",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Maria Poliana de Souza Lima (Gestor)",
        "telefone": "558398870576",
        "instituicao": "Escola Maria Batista (Lagoa do Mato)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Célia Maria da Silva Lima da Silva (Gestor)",
        "telefone": "558396276526",
        "instituicao": "Escola Margarida de Almeida (Lagoa do Mato)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Gabryella Freire Monteiro (Vice Gestor)",
        "telefone": "558396241207",
        "instituicao": "Escola Margarida de Almeida (Lagoa do Mato)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Daniela Raiane Batista da Silva (Gestor)",
        "telefone": "558393141714",
        "instituicao": "Escola José Cazuza (Sítio lajedo do teteu)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Roberlânia Marinho (Gestor)",
        "telefone": "558399872282",
        "instituicao": "Escola Manoel Joca (Deixar na casa da merenda)",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    },
    {
        "nome": "Aline Costa (Gestor)",
        "telefone": "5583981672070",
        "instituicao": "Escola Severino Bronzeado (Deixar na casa da merenda)",
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
