# app/repositories/responsavel_repository.py

"""
Resumo do módulo:
Fornece operações de acesso a dados relacionadas à entidade
Responsavel.

Descrição estendida:
Este módulo implementa funções de consulta para recuperação de
dados da tabela de responsáveis utilizando SQLAlchemy ORM.

Seu objetivo é centralizar operações de persistência e
consulta, isolando a camada de acesso a dados das demais
camadas da aplicação.

Responsabilidades principais:
- Consultar responsáveis no banco de dados
- Encapsular consultas ORM
- Fornecer operações de acesso à entidade Responsavel

Componentes principais:
- get_responsavel_by_phone

Dependências:
- sqlalchemy.orm.Session
- app.models.responsavel.Responsavel

Efeitos colaterais:
- Executa consultas no banco de dados

Entrada/Saída:
- Entrada: sessão SQLAlchemy e parâmetros de consulta
- Saída: instâncias de Responsavel ou None

Estratégia de tratamento de erros:
- Não realiza tratamento explícito de exceções
- Propaga exceções da camada ORM para o chamador

Considerações de performance:
- A consulta utiliza o campo telefone, que deve possuir índice
  para melhor desempenho.

Notas de concorrência:
- A segurança em concorrência depende da sessão SQLAlchemy
  utilizada pela aplicação.

Exemplo de uso:
responsavel = get_responsavel_by_phone(
    db=session,
    phone="83999999999"
)

Limitações:
- Implementa apenas consultas simples
- Não realiza validações de entrada

Versão/manutenção:
- Novas consultas relacionadas à entidade Responsavel devem
  ser adicionadas neste módulo.
"""

from sqlalchemy.orm import Session

from app.models.responsavel import Responsavel


def get_responsavel_by_phone(
    db: Session,
    phone: str,
) -> Responsavel | None:
    """
    Obtém um responsável a partir do número de telefone.

    Args:
        db (Session):
            Sessão ativa do SQLAlchemy utilizada para executar
            a consulta.

        phone (str):
            Número de telefone utilizado como critério de busca.

    Returns:
        Responsavel | None:
            Instância de Responsavel quando encontrada ou None
            caso não exista registro correspondente.

    Raises:
        sqlalchemy.exc.SQLAlchemyError:
            Pode ser propagada caso ocorra alguma falha durante
            a execução da consulta.

    Observações:
        A consulta retorna apenas o primeiro registro
        encontrado.

    Efeitos colaterais:
        Executa uma operação de leitura no banco de dados.

    Exemplos:
        responsavel = get_responsavel_by_phone(
            db=session,
            phone="83999999999"
        )

        if responsavel:
            print(responsavel.nome)

        responsavel = get_responsavel_by_phone(
            db=session,
            phone="00000000000"
        )
    """

    return (
        db.query(Responsavel)
        .filter(
            Responsavel.telefone == phone
        )
        .first()
    )
