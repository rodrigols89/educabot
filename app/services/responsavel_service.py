# app/services/responsavel_service.py

"""
Resumo do módulo:
Fornece serviços relacionados à validação de responsáveis.

Descrição estendida:
Este módulo contém regras de negócio responsáveis por validar
a existência e a situação cadastral de um responsável antes da
execução de operações na aplicação.

O processo verifica se o responsável está cadastrado e se seu
cadastro encontra-se ativo no sistema.

Responsabilidades principais:
- Localizar responsáveis pelo telefone
- Validar existência do responsável
- Validar situação de ativação do responsável
- Registrar informações de depuração

Componentes principais:
- check_responsavel

Dependências:
- sqlalchemy.orm.Session
- app.models.responsavel.Responsavel
- app.repositories.responsavel_repository

Efeitos colaterais:
- Executa consultas no banco de dados
- Escreve logs de depuração na saída padrão

Entrada/Saída:
- Entrada: sessão ORM e telefone do responsável
- Saída: instância de Responsavel ou None

Estratégia de tratamento de erros:
- Não realiza tratamento explícito de exceções
- Erros do ORM são propagados ao chamador
- Utiliza retornos nulos para indicar falhas de validação

Considerações de performance:
- Executa uma única consulta por telefone
- O desempenho depende da indexação da coluna telefone

Notas de concorrência:
- Não mantém estado compartilhado
- Depende do gerenciamento da sessão SQLAlchemy
- Seguro para execução concorrente quando utilizado com
  sessões independentes

Exemplo de uso:
responsavel = check_responsavel(
    db=session,
    phone="83999999999"
)

if responsavel:
    processar_pedido()

Limitações:
- Valida apenas existência e status de ativação
- Não valida permissões específicas do responsável

Versão/manutenção:
- Novas validações de responsável devem ser implementadas
  nesta camada de serviço.
"""

from sqlalchemy.orm import Session

from app.models.responsavel import Responsavel
from app.repositories.responsavel_repository import (
    get_responsavel_by_phone,
)


def check_responsavel(
    db: Session,
    phone: str,
) -> Responsavel | None:
    """
    Verifica se um responsável existe e está ativo no sistema.

    Args:
        db (Session):
            Sessão ativa do SQLAlchemy utilizada para consulta.

        phone (str):
            Número de telefone utilizado para localizar o
            responsável.

    Returns:
        Responsavel | None:
            Instância de Responsavel quando o cadastro existir e
            estiver ativo.

            Retorna None quando o responsável não for encontrado
            ou estiver inativo.

    Raises:
        sqlalchemy.exc.SQLAlchemyError:
            Pode ser propagada caso ocorra falha durante a
            consulta ao banco de dados.

    Observações:
        A validação ocorre em duas etapas:

        - Verificação de existência do responsável.
        - Verificação de status ativo.

    Efeitos colaterais:
        - Executa consulta no banco de dados.
        - Escreve logs de depuração na saída padrão.

    Exemplos:
        responsavel = check_responsavel(
            db=session,
            phone="83999999999"
        )

        if responsavel:
            print(responsavel.nome)

        responsavel = check_responsavel(
            db=session,
            phone="00000000000"
        )

        if responsavel is None:
            print("Responsável inválido")

    Avisos:
        Um responsável encontrado, mas inativo, será tratado
        como inválido.

    Limitações:
        Não valida permissões específicas para realização de
        pedidos.
    """

    print("\nVALIDATE ORDER OWNER PROCESS:")

    responsavel = get_responsavel_by_phone(
        db=db,
        phone=phone,
    )

    if responsavel is None:
        print("Responsável pelo pedido não encontrado/cadastrado.")
        return None

    if not responsavel.ativo:
        print("Responsável não está ativo no sistema.")
        return None

    print("O responsável pelo pedido está ativo.")
    print(f"Nome: {responsavel.nome}")
    print(f"Telefone: {responsavel.telefone}")
    print(f"Instituição: {responsavel.instituicao}")

    return responsavel
