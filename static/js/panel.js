// Token CSRF — vem do template Django
// const CSRF_TOKEN é definido no HTML

var API = "/api";

// Recurso selecionado atualmente
var cur = "unidades";

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
    fields: [["paciente","Paciente","fk","/pessoas/pacientes/"],["grupo_risco","Grupo de risco"],["gestante","Gestante","bool"],["alergias","Alergias"],["observacoes","Observações"]],
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
    fields: [["paciente","Paciente","fk","/pessoas/pacientes/"],["unidade_saude","Unidade","fk","/unidades/"],["profissional","Profissional","fk","/pessoas/profissionais/"],["data_atendimento","Data","date"],["status","Status"],["observacao","Observação"]],
    cols: ["id","paciente_nome","unidade_saude_nome","profissional_nome","data_atendimento","status"]
  },
  doses: {
    label: "Doses",
    path: "/atendimentos/doses/",
    fields: [["atendimento","Atendimento (id)","num"],["vacina","Vacina","fk","/vacinas/"],["lote","Lote","fk","/vacinas/lotes/"],["ordem_dose","Ordem da dose","num"],["observacao","Observação"]],
    cols: ["id","atendimento","vacina_nome","lote_numero","ordem_dose"]
  },
  registros: {
    label: "Registros",
    path: "/registros/",
    fields: [["paciente","Paciente","fk","/pessoas/pacientes/"],["vacina","Vacina","fk","/vacinas/"],["lote","Lote","fk","/vacinas/lotes/"],["profissional","Profissional","fk","/pessoas/profissionais/"],["unidade_saude","Unidade","fk","/unidades/"],["atendimento","Atendimento (id)","num"],["data_aplicacao","Data aplicação","date"],["dose","Dose"],["observacao","Observação"]],
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
    fields: [["paciente","Paciente","fk","/pessoas/pacientes/"],["titulo","Título"],["mensagem","Mensagem"],["data_envio","Data envio","date"],["tipo","Tipo"],["lida","Lida","bool"]],
    cols: ["id","paciente_nome","titulo","tipo","data_envio","lida"]
  },
  situacao: {
    label: "Situação Vacinal",
    path: "/situacao/",
    fields: [["paciente","Paciente","fk","/pessoas/pacientes/"],["vacina","Vacina","fk","/vacinas/"],["calendario_vacinal","Calendário (id)","num"],["status","Status"],["data_verificacao","Data verificação","date"],["observacao","Observação"]],
    cols: ["id","paciente_nome","vacina_nome","status","data_verificacao"]
  }
};

// Converte resposta da API em lista
function asList(d) {
  if (Array.isArray(d)) return d;
  if (d && d.results) return d.results;
  return [];
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
  // Adiciona token CSRF em POST, PUT, DELETE
  if (opts.method && opts.method !== "GET") {
    if (!opts.headers) opts.headers = {};
    opts.headers["X-CSRFToken"] = CSRF_TOKEN;
  }
  return fetch(API + path, opts).then(function(res) {
    if (res.status === 204) return null;
    if (res.status === 401 || res.status === 403) {
      window.location.reload();
      return null;
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
      render();
    };
    nav.appendChild(btn);
  }
}

// Monta o formulário de criação
function montarForm() {
  var c = R[cur];
  document.getElementById("ttl").textContent = "Novo: " + c.label;
  var f = document.getElementById("form");
  f.innerHTML = "";

  for (var i = 0; i < c.fields.length; i++) {
    var name = c.fields[i][0];
    var label = c.fields[i][1];
    var type = c.fields[i][2] || "text";
    var from = c.fields[i][3];

    var div = document.createElement("div");
    div.className = "field";
    var lbl = document.createElement("label");
    lbl.textContent = label;
    div.appendChild(lbl);

    var el;
    if (type === "bool") {
      el = document.createElement("select");
      el.innerHTML = "<option value='true'>Sim</option><option value='false'>Não</option>";
    } else if (type === "fk" || type === "m2m") {
      el = document.createElement("select");
      if (type === "m2m") el.multiple = true;
      el.innerHTML = "<option value=''>— Selecione —</option>";
      // Carrega opções do servidor
      (function(select, rota) {
        api(rota).then(function(d) {
          var lista = asList(d);
          for (var j = 0; j < lista.length; j++) {
            var opt = document.createElement("option");
            opt.value = lista[j].id;
            opt.textContent = lista[j].nome || lista[j].titulo || lista[j].numero_lote || ("#" + lista[j].id);
            select.appendChild(opt);
          }
        }).catch(function() {});
      })(el, from);
    } else {
      el = document.createElement("input");
      if (type === "num") el.type = "number";
      else if (type === "date") el.type = "date";
      else el.type = "text";
    }

    el.setAttribute("data-name", name);
    el.setAttribute("data-type", type);
    div.appendChild(el);
    f.appendChild(div);
  }

  var btn = document.createElement("button");
  btn.className = "add";
  btn.textContent = "Adicionar";
  btn.type = "submit";
  f.appendChild(btn);

  f.onsubmit = salvar;
}

// Salva novo registro
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
      for (var j = 0; j < el.selectedOptions.length; j++) {
        var v = Number(el.selectedOptions[j].value);
        if (v) vals.push(v);
      }
      if (vals.length) body[n] = vals;
    } else if (el.value !== "") {
      var val = el.value;
      if (t === "bool") val = val === "true";
      else if (t === "num" || t === "fk") val = Number(val);
      body[n] = val;
    }
  }

  api(R[cur].path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  }).then(function() {
    msg("Criado com sucesso!", true);
    render();
  }).catch(function(err) {
    msg("Erro: " + err.message, false);
  });
}

// Lista os registros na tabela
function listar() {
  var c = R[cur];
  var el = document.getElementById("table");
  el.innerHTML = "<p style='padding:15px;color:#999;'>Carregando...</p>";

  api(c.path).then(function(data) {
    var rows = asList(data);
    if (rows.length === 0) {
      el.innerHTML = "<p class='empty'>Nenhum registro encontrado.</p>";
      return;
    }

    var html = "<table><thead><tr>";
    for (var i = 0; i < c.cols.length; i++) {
      html += "<th>" + c.cols[i] + "</th>";
    }
    html += "<th></th></tr></thead><tbody>";

    for (var j = 0; j < rows.length; j++) {
      html += "<tr>";
      for (var k = 0; k < c.cols.length; k++) {
        var v = rows[j][c.cols[k]];
        if (v === true) v = "Sim";
        else if (v === false) v = "Não";
        else if (v === null || v === undefined) v = "—";
        html += "<td>" + v + "</td>";
      }
      html += "<td class='del' data-id='" + rows[j].id + "'>excluir</td></tr>";
    }
    html += "</tbody></table>";
    el.innerHTML = html;

    // Adiciona evento de excluir
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
