# app/models/responsavel.py

"""
Resumo do módulo:
Define o modelo ORM Responsavel utilizado pelo sistema.

Descrição estendida:
Este módulo contém a entidade Responsavel, responsável por
representar pessoas autorizadas a realizar pedidos de gás e
água.

Além dos dados de identificação e contato, o modelo armazena
as permissões de cada responsável e seu status de ativação.

Responsabilidades principais:
- Mapear a tabela "responsavel"
- Armazenar dados de identificação
- Controlar permissões para pedidos
- Controlar status de ativação do responsável

Componentes principais:
- Responsavel

Dependências:
- sqlalchemy
- app.db.base.Base

Efeitos colaterais:
- Registra o mapeamento ORM da tabela "responsavel"
- Contribui para a definição do schema do banco de dados

Entrada/Saída:
- Entrada: dados fornecidos pela aplicação ou banco de dados
- Saída: instâncias ORM da entidade Responsavel

Estratégia de tratamento de erros:
- Não realiza tratamento explícito de erros
- Depende da camada ORM e da camada de serviço

Considerações de performance:
- Utiliza índice na chave primária
- Utiliza índice e restrição de unicidade no telefone

Notas de concorrência:
- O modelo não é thread-safe por si só
- A segurança em concorrência depende da sessão ORM utilizada

Exemplo de uso:
responsavel = Responsavel(
    nome="Maria Silva",
    telefone="83999999999",
    instituicao="Escola Municipal",
    pode_pedir_gas=True
)

Limitações:
- Não implementa regras de negócio
- Não valida permissões de uso
- Não valida formato de telefone

Versão/manutenção:
- Alterações no schema devem ser refletidas nas migrations
- Mudanças nas permissões exigem revisão das regras de negócio
"""

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)

from app.db.base import Base


class Responsavel(Base):
    """
    Resumo da classe:
    Modelo ORM que representa um responsável no sistema.

    Propósito:
    Armazenar informações de identificação, contato e
    permissões de usuários autorizados a realizar pedidos.

    Atributos:
        id (int): Identificador único do responsável.
        nome (str): Nome do responsável.
        telefone (str): Telefone de contato único.
        instituicao (str): Instituição vinculada ao responsável.
        pode_pedir_gas (bool): Indica permissão para pedir gás.
        pode_pedir_agua (bool): Indica permissão para pedir água.
        ativo (bool): Indica se o responsável está ativo.

    Visão geral dos métodos:
        Herda os métodos e comportamentos ORM da classe Base.

    Observações:
        O telefone possui restrição de unicidade para evitar
        cadastros duplicados.

    Exemplo de uso:
        responsavel = Responsavel(
            nome="João Silva",
            telefone="83999999999",
            instituicao="Secretaria Municipal"
        )

        responsavel = Responsavel(
            nome="Maria Oliveira",
            telefone="83888888888",
            instituicao="Escola Municipal",
            pode_pedir_gas=True,
            pode_pedir_agua=True
        )

    Notas sobre concorrência:
        Não é thread-safe isoladamente.
        O controle de concorrência depende da sessão ORM.

    Considerações de design:
        Mantém apenas dados relacionados ao responsável e suas
        permissões.
        Regras de autorização devem permanecer em camadas
        superiores da aplicação.
    """

    __tablename__ = "responsavel"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    nome = Column(
        String(255),
        nullable=False,
    )

    telefone = Column(
        String(20),
        nullable=False,
        unique=True,
        index=True,
    )

    instituicao = Column(
        String(255),
        nullable=False,
    )

    pode_pedir_gas = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    pode_pedir_agua = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    ativo = Column(
        Boolean,
        default=True,
        nullable=False,
    )
