# Contribuições do Grupo — Gestor de Vacinação

Disciplina: Sistemas Distribuídos e Mobile — UniRitter 2026/1

Divisão do trabalho por integrante, no back-end (API Django) e no front-end (app React Native).

---

## Guilherme Perlasca

**Back-end**
- Setup inicial do projeto Django, configuração (`settings`, banco, `.env`) e estrutura de apps.
- Módulos: Pacientes, Profissionais, Unidades de Saúde, Vacinas, Lotes e Perfis de Saúde (models, serializers, views e rotas).
- Autenticação: app `accounts` (login/cadastro web) e autenticação por token para o app.

**Front-end**
- Estrutura do app, navegação e componentes base (campos, seletor, estilos).
- Telas de Pacientes, Profissionais, Unidades, Vacinas, Lotes e Perfis.
- Tela de login e fluxo de autenticação no app.

---

## Fillipe Brito

**Back-end**
- Módulos: Calendário Vacinal, Atendimentos, Doses e Registros de Vacinação (models, serializers, views e rotas).
- Regras de negócio das doses (ordem, validade do lote, estoque e intervalo).

**Front-end**
- Telas de Calendário, Atendimentos, Doses e Registros.
- Formulários com seleção de vacina/lote e regras de dose.

---

## Daniel Chiaramonte

**Back-end**
- Módulos: Campanhas de Vacinação, Notificações e Situação Vacinal (models, serializers, views e rotas).

**Front-end**
- Telas de Campanhas, Notificações e Situação Vacinal.
- Seletores de data e formulários desses módulos.

---

## Trabalho em conjunto

- Padronização de validações e mensagens de erro entre back-end e front-end.
- Testes de integração (app consumindo a API) e ajustes de usabilidade.
- Controle de versão com Git (branches por feature, Pull Requests e Merges).
