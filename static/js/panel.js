// Token CSRF — vem do template Django
// const CSRF_TOKEN é definido no HTML

var API = "/api";

// Recurso selecionado atualmente
var cur = "unidades";

// Id do registro em edição (null = criando um novo)
var editId = null;

// Cache dos registros listados, para preencher o form ao editar
var rowsCache = [];

// Definição de todos os recursos da API
var R = {
  unidades: {
    label: "Unidades",
    path: "/unidades/",
    fields: [["nome","Nome"],["endereco","Endereço"],["bairro","Bairro"],["telefone","Telefone"],["horario_funcionamento","Horário"],["ativa","Ativa","bool"]],
    cols: ["id","nome","bairro","telefone","horario_funcionamento","ativa"]
  },
  pacientes: {
    label: "Pacientes",
    path: "/pessoas/pacientes/",
    fields: [["nome","Nome"],["email","E-mail"],["telefone","Telefone"],["cpf","CPF"],["data_nascimento","Nascimento","date"],["ativo","Ativo","bool"]],
    cols: ["id","nome","cpf","email","telefone","data_nascimento","ativo"]
  },
  profissionais: {
    label: "Profissionais",
    path: "/pessoas/profissionais/",
    fields: [["nome","Nome"],["email","E-mail"],["telefone","Telefone"],["unidade_saude","Unidade","fk","/unidades/"],["registro_profissional","Registro"],["cargo","Cargo"],["ativo","Ativo","bool"]],
    cols: ["id","nome","cargo","unidade_saude_nome","registro_profissional","ativo"]
  },
  vacinas: {
    label: "Vacinas",
    path: "/vacinas/",
    fields: [["nome","Nome"],["fabricante","Fabricante"],["doenca_prevenida","Doença prevenida"],["quantidade_doses","Qtd doses","num"],["intervalo_dias","Intervalo (dias)","num"],["ativa","Ativa","bool"]],
    cols: ["id","nome","fabricante","doenca_prevenida","quantidade_doses","ativa"]
  },
  lotes: {
    label: "Lotes",
    path: "/vacinas/lotes/",
    fields: [["vacina","Vacina","fk","/vacinas/"],["unidade_saude","Unidade","fk","/unidades/"],["numero_lote","Nº lote"],["data_validade","Validade","date"],["quantidade_disponivel","Qtd disponível","num"]],
    cols: ["id","numero_lote","vacina_nome","unidade_saude_nome","data_validade","quantidade_disponivel"]
  },
  perfis: {
    label: "Perfis",
    path: "/perfis/",
    fields: [["paciente","Paciente","fk","/pessoas/pacientes/"],["grupo_risco","Grupo de risco","bool"],["gestante","Gestante","bool"],["alergias","Alergias"],["observacoes","Observações"]],
    cols: ["id","paciente_nome","grupo_risco","gestante","alergias"]
  },
  calendario: {
    label: "Calendário",
    path: "/calendario/",
    fields: [["vacina","Vacina","fk","/vacinas/"],["idade_minima_meses","Idade mín (meses)","num"],["idade_maxima_meses","Idade máx (meses)","num"],["publico_alvo","Público-alvo"],["dose_recomendada","Dose recomendada"],["obrigatoria","Obrigatória","bool"]],
    cols: ["id","vacina_nome","idade_minima_meses","idade_maxima_meses","publico_alvo","dose_recomendada","obrigatoria"]
  },
  atendimentos: {
    label: "Atendimentos",
    path: "/atendimentos/",
    fields: [["paciente","Paciente","fk","/pessoas/pacientes/"],["unidade_saude","Unidade","fk","/unidades/"],["profissional","Profissional","fk","/pessoas/profissionais/"],["data_atendimento","Data","datetime"],["status","Status","choice",[["agendado","Agendado"],["realizado","Realizado"],["cancelado","Cancelado"]]],["observacao","Observação"]],
    cols: ["id","paciente_nome","unidade_saude_nome","profissional_nome","data_atendimento","status"]
  },
  doses: {
    label: "Doses",
    path: "/atendimentos/doses/",
    fields: [["atendimento","Atendimento","fk","/atendimentos/"],["vacina","Vacina","fk","/vacinas/"],["lote","Lote","fk","/vacinas/lotes/"],["ordem_dose","Ordem da dose"],["observacao","Observação"]],
    cols: ["id","atendimento","vacina_nome","lote_numero","ordem_dose"]
  },
  registros: {
    label: "Registros",
    path: "/registros/",
    fields: [["paciente","Paciente","fk","/pessoas/pacientes/"],["vacina","Vacina","fk","/vacinas/"],["lote","Lote","fk","/vacinas/lotes/"],["profissional","Profissional","fk","/pessoas/profissionais/"],["unidade_saude","Unidade","fk","/unidades/"],["atendimento","Atendimento","fk","/atendimentos/"],["data_aplicacao","Data aplicação","date"],["dose","Dose"],["observacao","Observação"]],
    cols: ["id","paciente_nome","vacina_nome","lote_numero","data_aplicacao","dose","unidade_saude_nome"]
  },
  campanhas: {
    label: "Campanhas",
    path: "/campanhas/",
    fields: [["nome","Nome"],["descricao","Descrição"],["data_inicio","Início","date"],["data_fim","Fim","date"],["publico_alvo","Público-alvo"],["ativa","Ativa","bool"],["vacinas","Vacinas","m2m","/vacinas/"]],
    cols: ["id","nome","data_inicio","data_fim","publico_alvo","ativa"]
  },
  notificacoes: {
    label: "Notificações",
    path: "/notificacoes/",
    fields: [["paciente","Paciente","fk","/pessoas/pacientes/"],["titulo","Título"],["mensagem","Mensagem"],["tipo","Tipo","choice",[["lembrete","Lembrete"],["alerta","Alerta"],["informativo","Informativo"]]],["lida","Lida","bool"]],
    cols: ["id","paciente_nome","titulo","tipo","data_envio","lida"]
  },
  situacao: {
    label: "Situação Vacinal",
    path: "/situacao/",
    fields: [["paciente","Paciente","fk","/pessoas/pacientes/"],["vacina","Vacina","fk","/vacinas/"],["calendario_vacinal","Calendário","fk","/calendario/"],["status","Status","choice",[["em_dia","Em Dia"],["pendente","Pendente"],["atrasado","Atrasado"]]],["observacao","Observação"]],
    cols: ["id","paciente_nome","vacina_nome","status","data_verificacao"]
  }
};

// Converte resposta da API em lista
function asList(d) {
  if (Array.isArray(d)) return d;
  if (d && d.results) return d.results;
  return [];
}

// Monta um rótulo legível para uma opção de seleção (FK/M2M),
// já que nem todo recurso tem campo "nome" (ex.: calendário, atendimento).
function rotuloOpcao(item) {
  if (item.nome) return item.nome;
  if (item.titulo) return item.titulo;
  if (item.numero_lote) return item.numero_lote + (item.vacina_nome ? " (" + item.vacina_nome + ")" : "");
  if (item.dose_recomendada) return (item.vacina_nome ? item.vacina_nome + " - " : "") + item.dose_recomendada + (item.publico_alvo ? " (" + item.publico_alvo + ")" : "");
  if (item.paciente_nome) return "#" + item.id + " - " + item.paciente_nome + (item.data_atendimento ? " (" + String(item.data_atendimento).slice(0, 10) + ")" : "");
  return "#" + item.id;
}

// Mostra mensagem de sucesso ou erro
function msg(texto, sucesso) {
  var m = document.getElementById("msg");
  m.textContent = texto;
  m.className = sucesso ? "ok" : "err";
  if (sucesso) {
    setTimeout(function() { m.className = ""; }, 3000);
  }
}

// Faz chamada à API
function api(path, opts) {
  if (!opts) opts = {};
  opts.credentials = 'same-origin';
  // Adiciona token CSRF em POST, PUT, DELETE
  if (opts.method && opts.method !== "GET") {
    if (!opts.headers) opts.headers = {};
    opts.headers["X-CSRFToken"] = CSRF_TOKEN;
  }
  return fetch(API + path, opts).then(function(res) {
    if (res.status === 204) return null;
    if (res.status === 401) {
      throw new Error("Sessão expirada. Faça login novamente.");
    }
    if (res.status === 403) {
      throw new Error("Sem permissão para esta operação.");
    }
    return res.json().then(function(d) {
      if (!res.ok) throw new Error(JSON.stringify(d, null, 2));
      return d;
    });
  });
}

// Monta os botões de navegação
function montarNav() {
  var nav = document.getElementById("nav");
  nav.innerHTML = "";
  for (var k in R) {
    var btn = document.createElement("button");
    btn.textContent = R[k].label;
    if (k === cur) btn.className = "active";
    btn.setAttribute("data-key", k);
    btn.onclick = function() {
      cur = this.getAttribute("data-key");
      editId = null;
      render();
    };
    nav.appendChild(btn);
  }
}

// Monta o formulário de criação ou edição.
// Se "registro" for informado, os campos vêm preenchidos (modo edição).
function montarForm(registro) {
  var c = R[cur];
  var editando = registro && registro.id != null;
  document.getElementById("ttl").textContent = editando
    ? ("Editar " + c.label + " #" + registro.id)
    : ("Novo: " + c.label);
  var f = document.getElementById("form");
  f.innerHTML = "";

  for (var i = 0; i < c.fields.length; i++) {
    var name = c.fields[i][0];
    var label = c.fields[i][1];
    var type = c.fields[i][2] || "text";
    var from = c.fields[i][3];
    var valor = editando ? registro[name] : undefined;

    var div = document.createElement("div");
    div.className = "field";
    var lbl = document.createElement("label");
    lbl.textContent = label;
    div.appendChild(lbl);

    var el;
    if (type === "bool") {
      // Opção neutra primeiro: se não for tocada, o campo é omitido e o
      // backend aplica o default do model (evita marcar tudo como "Sim").
      el = document.createElement("select");
      el.innerHTML = "<option value=''>— (padrão) —</option><option value='true'>Sim</option><option value='false'>Não</option>";
      if (valor === true) el.value = "true";
      else if (valor === false) el.value = "false";
    } else if (type === "choice") {
      // Campo de escolha fixa (ex.: status, tipo) — opções vêm da definição.
      el = document.createElement("select");
      el.innerHTML = "<option value=''>— Selecione —</option>";
      for (var o = 0; o < from.length; o++) {
        var optC = document.createElement("option");
        optC.value = from[o][0];
        optC.textContent = from[o][1];
        el.appendChild(optC);
      }
      if (valor != null) el.value = valor;
    } else if (type === "m2m") {
      // ManyToMany: lista de checkboxes (permite marcar vários sem Ctrl+clique).
      el = document.createElement("div");
      el.className = "checkboxes";
      (function(container, rota, selecionados) {
        api(rota).then(function(d) {
          var lista = asList(d);
          if (lista.length === 0) {
            container.innerHTML = "<span class='vazio'>Nenhuma opção disponível.</span>";
            return;
          }
          for (var j = 0; j < lista.length; j++) {
            var lab = document.createElement("label");
            lab.className = "check";
            var cb = document.createElement("input");
            cb.type = "checkbox";
            cb.value = lista[j].id;
            if (selecionados && selecionados.indexOf(lista[j].id) !== -1) cb.checked = true;
            var sp = document.createElement("span");
            sp.textContent = rotuloOpcao(lista[j]);
            lab.appendChild(cb);
            lab.appendChild(sp);
            container.appendChild(lab);
          }
        }).catch(function() {});
      })(el, from, valor || []);
    } else if (type === "fk") {
      el = document.createElement("select");
      el.innerHTML = "<option value=''>— Selecione —</option>";
      // Carrega opções do servidor e, em edição, pré-seleciona o atual.
      (function(select, rota, selecionado) {
        api(rota).then(function(d) {
          var lista = asList(d);
          for (var j = 0; j < lista.length; j++) {
            var opt = document.createElement("option");
            opt.value = lista[j].id;
            opt.textContent = rotuloOpcao(lista[j]);
            select.appendChild(opt);
          }
          if (selecionado != null) select.value = String(selecionado);
        }).catch(function() {});
      })(el, from, valor);
    } else {
      el = document.createElement("input");
      if (type === "num") el.type = "number";
      else if (type === "date") el.type = "date";
      else if (type === "datetime") el.type = "datetime-local";
      else el.type = "text";
      if (valor != null) {
        if (type === "datetime") el.value = String(valor).slice(0, 16);
        else if (type === "date") el.value = String(valor).slice(0, 10);
        else el.value = valor;
      }
    }

    el.setAttribute("data-name", name);
    el.setAttribute("data-type", type);
    div.appendChild(el);
    f.appendChild(div);
  }

  var btn = document.createElement("button");
  btn.className = "add";
  btn.textContent = editando ? "Salvar alterações" : "Adicionar";
  btn.type = "submit";
  f.appendChild(btn);

  if (editando) {
    var btnCancel = document.createElement("button");
    btnCancel.className = "cancel";
    btnCancel.textContent = "Cancelar";
    btnCancel.type = "button";
    btnCancel.onclick = cancelarEdicao;
    f.appendChild(btnCancel);
  }

  f.onsubmit = salvar;
}

// Salva o registro: cria (POST) ou atualiza (PUT) conforme o modo.
function salvar(e) {
  e.preventDefault();
  var body = {};
  var campos = document.querySelectorAll("#form [data-name]");
  for (var i = 0; i < campos.length; i++) {
    var el = campos[i];
    var t = el.getAttribute("data-type");
    var n = el.getAttribute("data-name");
    if (t === "m2m") {
      var vals = [];
      var cbs = el.querySelectorAll("input[type=checkbox]");
      for (var j = 0; j < cbs.length; j++) {
        if (!cbs[j].checked) continue;
        var v = Number(cbs[j].value);
        if (v) vals.push(v);
      }
      // Envia sempre (lista vazia limpa o relacionamento).
      body[n] = vals;
    } else if (el.value !== "") {
      var val = el.value;
      if (t === "bool") val = val === "true";
      else if (t === "num" || t === "fk") val = Number(val);
      body[n] = val;
    }
  }

  var url = editId ? (R[cur].path + editId + "/") : R[cur].path;
  // PATCH na edição: só os campos enviados são alterados (não limpa o resto).
  var metodo = editId ? "PATCH" : "POST";
  var sucesso = editId ? "Atualizado com sucesso!" : "Criado com sucesso!";

  api(url, {
    method: metodo,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  }).then(function() {
    msg(sucesso, true);
    editId = null;
    render();
  }).catch(function(err) {
    msg("Erro: " + err.message, false);
  });
}

// Entra no modo edição: preenche o form com o registro selecionado.
function editar(id) {
  var registro = null;
  for (var i = 0; i < rowsCache.length; i++) {
    if (String(rowsCache[i].id) === String(id)) { registro = rowsCache[i]; break; }
  }
  if (!registro) return;
  editId = registro.id;
  montarForm(registro);
  window.scrollTo(0, 0);
}

// Cancela a edição e volta ao formulário de criação.
function cancelarEdicao() {
  editId = null;
  montarForm();
}

// Lista os registros na tabela
function listar() {
  var c = R[cur];
  var el = document.getElementById("table");
  el.innerHTML = "<p style='padding:15px;color:#999;'>Carregando...</p>";

  api(c.path).then(function(data) {
    var rows = asList(data);
    rowsCache = rows;
    if (rows.length === 0) {
      el.innerHTML = "<p class='empty'>Nenhum registro encontrado.</p>";
      return;
    }

    var html = "<table><thead><tr>";
    for (var i = 0; i < c.cols.length; i++) {
      html += "<th>" + c.cols[i] + "</th>";
    }
    html += "<th></th><th></th></tr></thead><tbody>";

    for (var j = 0; j < rows.length; j++) {
      html += "<tr>";
      for (var k = 0; k < c.cols.length; k++) {
        var v = rows[j][c.cols[k]];
        if (v === true) v = "Sim";
        else if (v === false) v = "Não";
        else if (v === null || v === undefined) v = "—";
        html += "<td>" + v + "</td>";
      }
      html += "<td class='editar' data-id='" + rows[j].id + "'>editar</td>";
      html += "<td class='del' data-id='" + rows[j].id + "'>excluir</td></tr>";
    }
    html += "</tbody></table>";
    el.innerHTML = html;

    // Eventos de editar
    var eds = el.querySelectorAll(".editar");
    for (var e2 = 0; e2 < eds.length; e2++) {
      eds[e2].onclick = function() {
        editar(this.getAttribute("data-id"));
      };
    }
    // Eventos de excluir
    var btns = el.querySelectorAll(".del");
    for (var b = 0; b < btns.length; b++) {
      btns[b].onclick = function() {
        excluir(this.getAttribute("data-id"));
      };
    }
  }).catch(function(err) {
    el.innerHTML = "<p class='empty'>Erro: " + err.message + "</p>";
  });
}

// Exclui um registro
function excluir(id) {
  if (!confirm("Excluir registro #" + id + "?")) return;
  api(R[cur].path + id + "/", { method: "DELETE" }).then(function() {
    msg("Registro #" + id + " excluído.", true);
    listar();
  }).catch(function(err) {
    msg("Erro: " + err.message, false);
  });
}

// Renderiza tudo
function render() {
  montarNav();
  montarForm();
  listar();
}

// Inicia
render();
