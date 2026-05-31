# `🧠 services/`

> **Aqui ficam as regras de negócio.**  
> É uma das camadas mais importantes.

Responsabilidades:

> Tomar decisões.

### `Exemplo`

Regra:

```text
Somente gestores podem criar pedidos.
```

Essa lógica NÃO deve ficar:

* no endpoint
* no repository

Ela fica no service.

### `Exemplo visual`

```text
API
 │
 ▼
Service
 │
 ▼
Repository
 │
 ▼
Banco
```

## Conteúdo

 - [Em breve...](#)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
