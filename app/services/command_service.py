# app/services/command_service.py

"""
Resumo do módulo:
Fornece funções para validação de comandos recebidos pela
aplicação.

Descrição estendida:
Este módulo contém regras responsáveis por verificar se uma
mensagem recebida corresponde a um comando suportado pelo
sistema.

Antes da validação, o texto é normalizado para evitar
diferenças causadas por espaços extras ou letras maiúsculas e
minúsculas.

Responsabilidades principais:
- Validar comandos recebidos
- Normalizar mensagens antes da validação
- Identificar comandos suportados
- Registrar informações de depuração

Componentes principais:
- is_valid_command

Dependências:
- app.utils.logger.print_separator

Efeitos colaterais:
- Escreve logs de depuração na saída padrão

Entrada/Saída:
- Entrada: conteúdo textual da mensagem
- Saída: indicador booleano de validade

Estratégia de tratamento de erros:
- Utiliza validações defensivas para tratar valores nulos
- Evita processamento de mensagens vazias

Considerações de performance:
- Executa apenas operações simples de string
- Não realiza acesso a banco de dados ou APIs externas

Notas de concorrência:
- Não mantém estado compartilhado
- Seguro para execução concorrente
- Logs podem ser intercalados em execuções simultâneas

Exemplo de uso:
if is_valid_command("/gas"):
    process_command()

Limitações:
- Reconhece apenas comandos previamente cadastrados
- Não interpreta argumentos ou parâmetros

Versão/manutenção:
- Novos comandos devem ser adicionados à lista de comandos
  suportados.
"""


def is_valid_command(
    text: str | None,
) -> bool:
    """
    Verifica se um texto corresponde a um comando válido.

    Args:
        text (str | None):
            Conteúdo textual da mensagem recebida.

    Returns:
        bool:
            True quando o texto corresponde a um comando
            suportado pelo sistema.

            False quando o texto está vazio ou não corresponde
            a um comando válido.

    Raises:
        Nenhuma exceção é gerada diretamente pela função.

    Observações:
        O texto é normalizado por meio da remoção de espaços
        excedentes e conversão para letras minúsculas antes da
        validação.

    Efeitos colaterais:
        - Escreve logs de depuração na saída padrão.
        - Registra o resultado da validação.

    Exemplos:
        is_valid_command("/gas")
        # True

        is_valid_command(" /AGUA ")
        # True

        is_valid_command("Olá")
        # False

    Avisos:
        Apenas comandos cadastrados internamente são aceitos.

    Limitações:
        Não interpreta argumentos.
        Não realiza validações semânticas do comando.
    """

    print("\nCOMMAND VALIDATION PROCESS:")

    # Empty messages
    if not text:
        print("A mensagem (text) de alguma maneira veio vazia (None)")
        return False

    # Normalize text
    text = text.strip().lower()

    # Supported commands
    is_valid = text in {
        "/gas",
        "/agua",
    }

    if is_valid:
        print(f"Comando válido: {text}")
    else:
        print(f"Comando inválido: {text}")

    return is_valid
