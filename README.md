# 💉 Gestor de Vacinação — Back-end

<div align="center">

![Status](https://img.shields.io/badge/status-concluído-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.17-red)
![Oracle](https://img.shields.io/badge/Oracle_DB-OCI-F80000?logo=oracle&logoColor=white)

**API REST distribuída para gestão completa de campanhas e registros de vacinação.**

</div>

---

## 📋 Sobre o Projeto

O **Gestor de Vacinação** é uma API REST desenvolvida com Django e Django REST Framework, estruturada em microserviços independentes. O sistema centraliza o controle de pacientes, profissionais de saúde, unidades, vacinas, lotes, atendimentos, registros de aplicação e campanhas — cobrindo todos os fluxos do calendário vacinal nacional.

O projeto foi desenvolvido como parte da **Avaliação A3** da Unidade Curricular **Sistemas Distribuídos e Mobile** — UniRitter / Ânima Educação, seguindo boas práticas de engenharia de software com controle de versão distribuído via Git (branching por feature, Pull Requests e Merges obrigatórios), arquitetura desacoplada por apps Django e banco de dados **Oracle Database** hospedado na nuvem **Oracle OCI**.

---

## 🏗️ Arquitetura

```
2026-1-SDM-Segunda-Noite-ZS-10/
├── core/                        # Configurações centrais do projeto
│   ├── settings.py              # Configurações, Oracle OCI, django-environ
│   ├── urls.py                  # Roteamento central da API
│   └── wsgi.py
├── apps/                        # Microserviços / Apps Django
│   ├── pessoas/                 # Pacientes e Profissionais de Saúde
│   ├── unidades/                # Unidades de Saúde
│   ├── vacinas/                 # Vacinas e Lotes
│   ├── perfis/                  # Perfil Clínico do Paciente
│   ├── calendario/              # Calendário Vacinal Nacional
│   ├── atendimentos/            # Atendimentos e Doses Aplicadas
│   ├── registros/               # Registro Oficial de Vacinação
│   ├── campanhas/               # Campanhas de Vacinação
│   ├── notificacoes/            # Notificações ao Paciente
│   └── situacao/                # Situação Vacinal por Paciente
├── .env                         # Variáveis de ambiente (não versionado)
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## 🚀 Tecnologias

| Tecnologia | Versão | Finalidade |
|---|---|---|
| Python | 3.11 | Linguagem principal |
| Django | 5.2 | Framework web |
| Django REST Framework | 3.17 | API REST / serialização JSON |
| Oracle Database | OCI Cloud | Banco de dados em produção |
| django-environ | 0.13 | Variáveis de ambiente via `.env` |
| Miniconda | — | Gerenciamento de ambiente virtual |
| Git | — | Controle de versão distribuído |

---

## 📦 Apps e Modelos

| App | Modelos | Relacionamentos principais |
|---|---|---|
| `pessoas` | `Paciente`, `ProfissionalSaude` | Herança de `Pessoa` (abstract) |
| `unidades` | `UnidadeSaude` | Base para profissionais e lotes |
| `vacinas` | `Vacina`, `LoteVacina` | FK: Vacina → LoteVacina |
| `perfis` | `PerfilSaude` | OneToOne com Paciente |
| `calendario` | `CalendarioVacinal` | FK: Vacina |
| `atendimentos` | `Atendimento`, `DoseAtendimento` | FK: Paciente, Profissional, Unidade |
| `registros` | `RegistroVacinacao` | FK: todas as entidades principais |
| `campanhas` | `CampanhaVacinacao` | ManyToMany com Vacina |
| `notificacoes` | `Notificacao` | FK: Paciente |
| `situacao` | `SituacaoVacinal` | FK: Paciente, Vacina, Calendario |

---

## ⚙️ Configuração e Execução Local

### Pré-requisitos

- [Miniconda](https://docs.anaconda.com/miniconda/) instalado
- Git configurado
- Acesso ao Oracle OCI (ou SQLite para desenvolvimento local)

### 1. Clonar o repositório

```bash
git clone https://github.com/anleaes/2026-1-SDM-Segunda-Noite-ZS-10.git
cd 2026-1-SDM-Segunda-Noite-ZS-10
```

### 2. Criar e ativar o ambiente virtual

```bash
conda create -n vacinas python=3.11 -y
conda activate vacinas
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie o arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-secret-key-aqui
DEBUG=True
ORACLE_DSN=seu_dsn_oracle_oci
ORACLE_USER=ADMIN
ORACLE_PASSWORD=sua-senha
```

### 5. Aplicar migrations

```bash
python manage.py migrate
```

### 6. Subir o servidor

```bash
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000/`

---

## 🔐 Autenticação

A API exige autenticação. São aceitos dois métodos:

- **Token** (usado pelo app mobile): obtenha o token no login e envie no header
  `Authorization: Token <seu-token>`.
- **Sessão** (usada pelo painel web de testes em `/`): login por formulário.

| Endpoint | Método | Descrição |
|---|---|---|
| `/api/auth/login/` | `POST` | Recebe `username` e `password`, devolve `token` + dados do usuário |
| `/api/auth/logout/` | `POST` | Invalida o token atual |

```bash
# Exemplo de login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "professor", "password": "vacinas123"}'
# -> {"token": "abc123...", "usuario": {"id": 1, "username": "professor"}}
```

---

## 🌐 Endpoints da API

Todos os endpoints suportam `GET`, `POST`, `PUT`, `PATCH` e `DELETE` e exigem autenticação.

| Recurso | URL Base |
|---|---|
| Pacientes | `/api/pessoas/pacientes/` |
| Profissionais de Saúde | `/api/pessoas/profissionais/` |
| Unidades de Saúde | `/api/unidades/` |
| Vacinas | `/api/vacinas/` |
| Lotes de Vacinas | `/api/vacinas/lotes/` |
| Perfis de Saúde | `/api/perfis/` |
| Calendário Vacinal | `/api/calendario/` |
| Atendimentos | `/api/atendimentos/` |
| Doses por Atendimento | `/api/atendimentos/doses/` |
| Registros de Vacinação | `/api/registros/` |
| Campanhas de Vacinação | `/api/campanhas/` |
| Notificações | `/api/notificacoes/` |
| Situação Vacinal | `/api/situacao/` |

### Regras de negócio aplicadas

- **Doses / Registros**: o lote precisa pertencer à vacina, estar dentro da validade e
  com estoque; a ordem da dose respeita o total de doses da vacina; não há doses
  duplicadas para o mesmo paciente; o intervalo mínimo entre doses é validado.
- **Registro**: só em atendimento `realizado`; decrementa o estoque do lote ao criar e
  devolve ao excluir.
- **Vacina**: quantidade de doses entre 1 e 10.
- **E-mail e CPF** únicos, com mensagens de erro claras.

---

## 🔀 Padrão Git

Branching por feature com PR e Merge obrigatórios:

```
main
├── feature/<app>-models        # Model + migrations
├── feature/<app>-serializers   # ModelSerializer
├── feature/<app>-views         # ModelViewSet
└── feature/<app>-urls          # DefaultRouter + urls
```

Cada branch possui mínimo de **2 commits + push + PR + Merge**.

---

## 👥 Desenvolvedores

| Nome | GitHub | Responsabilidade |
|---|---|---|
| Guilherme Perlasca | [@guiperlasca](https://github.com/guiperlasca) | Setup, pessoas, unidades, vacinas, perfis |
| Fillipe Brito | [@FillipeBrito1](https://github.com/FillipeBrito1) | Calendario, atendimentos, registros |
| Daniel Chiaramonte | [@danielchiaramonte](https://github.com/danielchiaramonte) | Campanhas, notificacoes, situacao |

---

## 📅 Cronograma de Entregas

| Entrega | Prazo | Status |
|---|---|---|
| Diagrama de Classes | 18/05/2026 | ✅ Concluído |
| Back-end funcional | 25/05/2026 | ✅ Concluído |
| Front-end React Native | 01/06/2026 | 🔄 Em desenvolvimento |
| Apresentação final | 08/06/2026 | ⏳ Aguardando |

---

## 📄 Contexto Acadêmico

Disciplina: **Sistemas Distribuídos e Mobile** — UniRitter / Ânima Educação  
Professor: **Antonio Leães** — Semestre 2026/1

Repositório front-end: [2026-1-SDM-Segunda-Noite-ZS-10-RN](https://github.com/anleaes/2026-1-SDM-Segunda-Noite-ZS-10-RN)
