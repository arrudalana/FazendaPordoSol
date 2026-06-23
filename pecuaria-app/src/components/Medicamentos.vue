<template>
  <div class="medicamentos-page">
    <header class="top-bar">
      <p class="current-date">{{ dataFormatada }}</p>
    </header>

    <div v-if="mensagemFeedback" :class="['feedback-banner', tipoFeedback]">
      <svg v-if="tipoFeedback === 'sucesso'" class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg>
      <svg v-else class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
      </svg>
      {{ mensagemFeedback }}
    </div>

    <div v-if="telaAtual === 'lista'">
      <div class="page-header">
        <div class="title-section">
          <h1 class="page-title">MEDICAMENTOS E APLICAÇÕES</h1>
          <p class="page-subtitle">Controle sanitário do rebanho — vacinas, antiparasitários e tratamentos</p>
        </div>
        <button class="btn-novo" @click="abrirFormulario()">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          Nova Aplicação
        </button>
      </div>

      <div class="dashboard-cards">
        <div class="kpi-card">
          <div class="kpi-info">
            <span class="kpi-label">Total de Aplicações</span>
            <span class="kpi-value">{{ listaAplicacoes.length }}</span>
          </div>
          <div class="kpi-icon icon-orange">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
          </div>
        </div>
        <div class="kpi-card">
          <div class="kpi-info">
            <span class="kpi-label">Medicamentos Registrados</span>
            <span class="kpi-value">{{ listaMedicamentos.length }}</span>
          </div>
          <div class="kpi-icon icon-blue">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
          </div>
        </div>
      </div>

      <div class="content-card">
        <div class="filtros-bar">
          <div class="search-bar">
            <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            <input type="text" v-model="termoBusca" placeholder="Buscar por brinco ou medicamento..." />
          </div>

          <div class="filtro-proprietario-custom">
            <svg class="icon-user" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
            <select v-model="donoSelecionado">
              <option :value="null">Proprietário</option>
              <option v-for="dono in proprietariosOrdenados" :key="dono.id_dono" :value="dono.id_dono">
                {{ dono.nome }}
              </option>
            </select>
            <svg class="icon-seta" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </div>
        </div>

        <h3 class="section-title">HISTÓRICO DE APLICAÇÕES</h3>
        <div class="table-container">
          <table class="dados-table">
            <thead>
              <tr>
                <th>Animal</th>
                <th>Medicamento</th>
                <th>Lote / INDEA</th>
                <th>Data</th>
                <th class="text-right">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="aplicacoesFiltradas.length === 0">
                <td colspan="5" class="tabela-vazia">Nenhuma aplicação registrada no sistema.</td>
              </tr>
              <tr v-for="app in aplicacoesFiltradas" :key="app.id_animal + '-' + app.id_medicamento">
                <td>
                  <div class="animal-cell">
                    <div class="seringa-icon-bg">
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                    </div>
                    <strong>Brinco: {{ app.animal_nome }}</strong>
                  </div>
                </td>
                <td>
                  <span class="med-nome">{{ app.medicamento_nome }}</span>
                  <span :class="['badge-med', getBadgeClass(app.tp_medicamento)]">
                    {{ getMedTypeName(app.tp_medicamento) }}
                  </span>
                </td>
                <td>
                  <span class="lote-text">Lote: {{ app.lote || '---' }}</span>
                  <span :class="['badge-indea', app.informado_indea === 'S' ? 'indea-ok' : 'indea-pendente']">
                    {{ app.informado_indea === 'S' ? 'Declarado INDEA' : 'Pendente INDEA' }}
                  </span>
                </td>
                <td class="col-date">
                  <span class="icon-text-group">
                    <svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                    {{ formatarDataBR(app.dt_aplicacao) }}
                  </span>
                </td>
                <td class="acoes text-right">
                  <button class="btn-acao delete" title="Remover Registro" @click="removerAplicacao(app.id_animal, app.id_medicamento)">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-else-if="telaAtual === 'formulario'">
      <div class="page-header header-form">
        <button class="btn-voltar" @click="voltarParaLista" title="Voltar">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
        </button>
        <div class="title-section">
          <h1 class="page-title form-title-orange">REGISTRAR APLICAÇÃO DE MEDICAMENTO</h1>
        </div>
      </div>

      <div class="tabs-container">
        <button :class="['tab-btn', { active: abaAtual === 'aplicar' }]" @click="abaAtual = 'aplicar'">Lançar Aplicação</button>
        <button :class="['tab-btn', { active: abaAtual === 'novo_med' }]" @click="abaAtual = 'novo_med'">Novo Medicamento/Vacina no Catálogo</button>
      </div>

      <div class="content-card form-card">
        
        <form v-if="abaAtual === 'aplicar'" @submit.prevent="salvarAplicacao" class="form-layout-clean">
          
          <div class="form-grid-3">
            <div class="input-col">
              <label>Animal</label>
              <div class="select-box">
                <select v-model="formAplicacao.id_animal" required>
                  <option value="" disabled>Selecione o animal</option>
                  <option v-for="animal in listaAnimais" :key="animal.id" :value="animal.id">
                    {{ animal.nome }} ({{ animal.raca }})
                  </option>
                </select>
              </div>
            </div>

            <div class="input-col">
              <label>Medicamento</label>
              <div class="select-box">
                <select v-model="formAplicacao.id_medicamento" required>
                  <option value="" disabled>Selecione o medicamento</option>
                  <option v-for="med in listaMedicamentos" :key="med.id_medicamento" :value="med.id_medicamento">
                    {{ med.nome }}
                  </option>
                </select>
              </div>
            </div>

            <div class="input-col">
              <label>Data da Aplicação</label>
              <input type="date" v-model="formAplicacao.dt_aplicacao" required>
            </div>
          </div>

          <div class="form-grid-3 mt-20">
            <div class="input-col">
              <label>Lote do Medicamento</label>
              <input type="text" v-model="formAplicacao.lote" placeholder="Ex: L-001/24">
            </div>

            <div class="input-col">
              <label>Status INDEA</label>
              <div class="select-box">
                <select v-model="formAplicacao.informado_indea" required>
                  <option value="S">Informado ao INDEA (Sim)</option>
                  <option value="N">Não informado (Pendente)</option>
                </select>
              </div>
            </div>
          </div>

          <div class="form-actions-right">
            <button type="button" class="btn-cancelar" @click="voltarParaLista">Cancelar</button>
            <button type="submit" class="btn-salvar">Confirmar Aplicação</button>
          </div>
        </form>

        <form v-else @submit.prevent="salvarMedicamento" class="form-layout-clean">
          <div class="form-grid-3">
            <div class="input-col">
              <label>Nome Comercial do Remédio</label>
              <input type="text" v-model="formMedicamento.nome" required placeholder="Ex: Oxitetraciclina">
            </div>

            <div class="input-col">
              <label>Tipo de Medicamento</label>
              <div class="select-box">
                <select v-model="formMedicamento.tp_medicamento" required>
                  <option value="VAC">Vacina</option>
                  <option value="ANT">Antibiótico</option>
                  <option value="PAR">Antiparasitário</option>
                  <option value="OUT">Outros</option>
                </select>
              </div>
            </div>
          </div>

          <div class="form-actions-right">
            <button type="button" class="btn-cancelar" @click="voltarParaLista">Cancelar</button>
            <button type="submit" class="btn-salvar">Adicionar ao Catálogo</button>
          </div>
        </form>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';

const telaAtual = ref('lista');
const abaAtual = ref('aplicar'); 
const mensagemFeedback = ref('');
const tipoFeedback = ref('sucesso'); 
const termoBusca = ref('');
const donoSelecionado = ref(null); 

const listaAplicacoes = ref([]);
const listaAnimais = ref([]);
const listaMedicamentos = ref([]);
const listaProprietarios = ref([]);

const proprietariosOrdenados = computed(() => {
  return [...listaProprietarios.value].sort((a, b) => a.nome.localeCompare(b.nome, 'pt-BR'));
});

const aplicacoesFiltradas = computed(() => {
  const termo = termoBusca.value.toLowerCase();
  return listaAplicacoes.value.filter(app => {
    const animalNome = String(app.animal_nome || '').toLowerCase();
    const medNome = String(app.medicamento_nome || '').toLowerCase();
    
    const bateTexto = animalNome.includes(termo) || medNome.includes(termo);
    const bateDono = !donoSelecionado.value || Number(app.id_dono) === Number(donoSelecionado.value);
    
    return bateTexto && bateDono;
  });
});

const formAplicacao = reactive({
  id_animal: '', id_medicamento: '', dt_aplicacao: '', lote: '', informado_indea: 'N'
});

const formMedicamento = reactive({
  nome: '', tp_medicamento: 'VAC'
});

// Correção e Garantia da Data no Top Bar
const dataAtual = new Date();
const dataFormatada = ref(dataAtual.toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }));

const carregarDadosDoSistema = async () => {
  try {
    const [resApp, resAn, resMed, resProp] = await Promise.all([
      fetch('http://127.0.0.1:8000/api/aplicacoes/'),
      fetch('http://127.0.0.1:8000/api/animais/'),
      fetch('http://127.0.0.1:8000/api/medicamentos/'),
      fetch('http://127.0.0.1:8000/api/proprietarios/')
    ]);
    listaAplicacoes.value = await resApp.json();
    
    // Na hora de aplicar o remédio, só permite em gados vivos
    const animais = await resAn.json();
    listaAnimais.value = animais.filter(a => a.status === 'V'); 

    listaMedicamentos.value = await resMed.json();
    listaProprietarios.value = await resProp.json();
  } catch (error) { console.error("Erro na comunicação"); }
};

onMounted(carregarDadosDoSistema);

const abrirFormulario = () => {
  abaAtual.value = 'aplicar';
  formAplicacao.id_animal = ''; formAplicacao.id_medicamento = ''; formAplicacao.lote = ''; formAplicacao.informado_indea = 'N';
  formAplicacao.dt_aplicacao = new Date().toISOString().split('T')[0];
  formMedicamento.nome = ''; formMedicamento.tp_medicamento = 'VAC';
  telaAtual.value = 'formulario';
};

const voltarParaLista = () => { telaAtual.value = 'lista'; };

const mostrarMensagem = (texto, tipo = 'sucesso') => {
  mensagemFeedback.value = texto; tipoFeedback.value = tipo;
  setTimeout(() => { mensagemFeedback.value = ''; }, 4000);
};

const salvarAplicacao = async () => {
  try {
    const resposta = await fetch('http://127.0.0.1:8000/api/aplicacoes/', { 
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formAplicacao) 
    });
    const resultado = await resposta.json();
    if (resposta.ok && resultado.sucesso) {
      mostrarMensagem('Aplicação sanitária registrada com sucesso!', 'sucesso');
      await carregarDadosDoSistema(); voltarParaLista();
    } else {
      mostrarMensagem(resultado.erro || 'Erro ao registrar.', 'erro');
    }
  } catch (error) { mostrarMensagem('Erro de conexão.', 'erro'); }
};

const salvarMedicamento = async () => {
  try {
    const resposta = await fetch('http://127.0.0.1:8000/api/medicamentos/', { 
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formMedicamento) 
    });
    if (resposta.ok) {
      mostrarMensagem('Novo medicamento adicionado ao catálogo!', 'sucesso');
      await carregarDadosDoSistema(); abaAtual.value = 'aplicar';
    }
  } catch (error) { mostrarMensagem('Erro de conexão.', 'erro'); }
};

const removerAplicacao = async (id_animal, id_medicamento) => {
  if (confirm("Deletar este registro de aplicação?")) {
    try {
      const resposta = await fetch(`http://127.0.0.1:8000/api/aplicacoes/${id_animal}/${id_medicamento}/`, { method: 'DELETE' });
      if (resposta.ok) {
        mostrarMensagem('Registro deletado!', 'sucesso'); await carregarDadosDoSistema();
      }
    } catch (error) { mostrarMensagem('Erro na exclusão.', 'erro'); }
  }
};

const formatarDataBR = (dataString) => {
  if (!dataString) return '';
  const [ano, mes, dia] = dataString.split('-');
  return `${dia}/${mes}/${ano}`;
};

const getBadgeClass = (tipo) => {
  const map = { 'VAC': 'badge-blue', 'ANT': 'badge-red', 'PAR': 'badge-green', 'OUT': 'badge-gray' };
  return map[tipo] || 'badge-gray';
};

const getMedTypeName = (tipo) => {
  const map = { 'VAC': 'Vacina', 'ANT': 'Antibiótico', 'PAR': 'Antiparasitário', 'OUT': 'Outros' };
  return map[tipo] || tipo;
};
</script>

<style scoped>
.medicamentos-page { padding: 20px 40px; background-color: #f9f2ec; min-height: 100vh; font-family: 'Segoe UI', Tahoma, sans-serif; }
.top-bar { border-bottom: 1px solid #ebdcd1; padding-bottom: 10px; margin-bottom: 25px; display: block; }
.current-date { color: #8a7b72; font-size: 14px; margin: 0; text-transform: lowercase; }

.feedback-banner { position: fixed; top: 25px; right: 25px; padding: 15px 25px; border-radius: 8px; display: flex; align-items: center; gap: 12px; font-weight: 600; font-size: 14px; z-index: 9999; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
.feedback-banner.sucesso { background-color: #eafbee; color: #0b9e15; border: 1px solid #b7f0c1; }
.feedback-banner.erro { background-color: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.feedback-banner .icon { width: 20px; height: 20px; }

.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 30px; }
.page-title { font-family: "Anton SC", sans-serif; font-size: 32px; color: #1e293b; margin: 0; letter-spacing: 0.5px; text-transform: uppercase; }
.page-subtitle { color: #64748b; font-size: 15px; margin: 5px 0 0 0; }
.btn-novo { background-color: #ff7322; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: opacity 0.2s; }
.btn-novo:hover { opacity: 0.9; }

.dashboard-cards { display: flex; gap: 20px; margin-bottom: 40px; }
.kpi-card { flex: 1; background: #ffffff; border: 1px solid #ffede3; border-radius: 12px; padding: 25px; display: flex; justify-content: space-between; align-items: center; }
.kpi-info { display: flex; flex-direction: column; gap: 5px; }
.kpi-label { font-size: 14px; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
.kpi-value { font-size: 32px; font-weight: 700; color: #1e293b; }
.kpi-icon { width: 45px; height: 45px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; }
.kpi-icon svg { width: 24px; height: 24px; }
.icon-orange { background-color: #ff7322; }
.icon-blue { background-color: #3b82f6; }

.content-card { background: #ffffff; border-radius: 10px; padding: 30px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03); border: 1px solid #f0e6de; }
.section-title { font-family: "Anton SC", sans-serif; font-size: 20px; color: #1e293b; margin-bottom: 25px; text-transform: uppercase; }

/* BARRA DE FILTROS */
.filtros-bar { display: flex; gap: 15px; margin-bottom: 25px; align-items: center; flex-wrap: wrap; }
.search-bar { display: flex; align-items: center; background-color: #ffffff; border: 1px solid #ff7322; border-radius: 6px; padding: 10px 15px; flex: 1; max-width: 400px; transition: box-shadow 0.2s; }
.search-bar:focus-within { box-shadow: 0 0 0 1px #ff7322; }
.search-bar input { border: none; background: transparent; width: 100%; outline: none; font-size: 14px; color: #334155; }
.search-icon { width: 20px; height: 20px; color: #ff7322; margin-right: 10px; }

/* DROPDOWN DE PROPRIETÁRIO (CLICÁVEL) */
.filtro-proprietario-custom { position: relative; display: flex; align-items: center; border: 1px solid #ff7322; border-radius: 6px; background-color: #ffffff; height: 42px; min-width: 220px; transition: box-shadow 0.2s; }
.filtro-proprietario-custom:focus-within { box-shadow: 0 0 0 1px #ff7322; }
.icon-user { width: 18px; height: 18px; color: #ff7322; position: absolute; left: 12px; z-index: 1; pointer-events: none; }
.icon-seta { width: 16px; height: 16px; color: #ff7322; position: absolute; right: 12px; z-index: 1; pointer-events: none; }
.filtro-proprietario-custom select { position: relative; z-index: 10; width: 100%; height: 100%; padding: 0 35px 0 40px; border: none; background: transparent; color: #ff7322; font-weight: 500; font-size: 14px; appearance: none; -webkit-appearance: none; cursor: pointer; outline: none; }
.filtro-proprietario-custom select option { color: #334155; background: white; }

/* TABELA DATA GRID */
.table-container { overflow-x: auto; }
.dados-table { width: 100%; border-collapse: collapse; font-size: 14px; color: #1e293b; }
.dados-table th { text-align: left; padding: 15px 10px; color: #ff7322; font-weight: 600; background-color: #fdf6f0; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }
.dados-table th:first-child { border-top-left-radius: 8px; border-bottom-left-radius: 8px; }
.dados-table th:last-child { border-top-right-radius: 8px; border-bottom-right-radius: 8px; }
.dados-table td { padding: 18px 10px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
.tabela-vazia { text-align: center !important; color: #94a3b8; padding: 40px !important; font-style: italic; }

.animal-cell { display: flex; align-items: center; gap: 12px; }
.seringa-icon-bg { background-color: #fff4ed; color: #ff7322; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.seringa-icon-bg svg { width: 18px; height: 18px; }

.med-nome { font-weight: 600; color: #1e293b; margin-right: 10px; }
.badge-med { padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; display: inline-block; white-space: nowrap; }
.badge-blue { background-color: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
.badge-red { background-color: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
.badge-green { background-color: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
.badge-gray { background-color: #f8fafc; color: #64748b; border: 1px solid #e2e8f0; }

.lote-text { font-size: 13px; color: #475569; display: block; margin-bottom: 4px; }
.badge-indea { font-size: 11px; font-weight: 600; padding: 2px 6px; border-radius: 4px; }
.indea-ok { background-color: #dcfce7; color: #166534; }
.indea-pendente { background-color: #fef3c7; color: #92400e; }

/* CORREÇÃO DO DISPLAY DA DATA */
.col-date { min-width: 130px; }
.icon-text-group { display: inline-flex; align-items: center; gap: 8px; color: #64748b; font-weight: 500; }
.icon-sm { width: 18px; height: 18px; color: #94a3b8; flex-shrink: 0;}

.acoes { text-align: right; }
.btn-acao { background: transparent; border: none; cursor: pointer; border-radius: 4px; padding: 6px; display: inline-flex; align-items: center; justify-content: center; transition: 0.2s;}
.btn-acao.delete { color: #ef4444; }
.btn-acao:hover { background-color: #fef2f2; }
.btn-acao svg { width: 18px; height: 18px; }

/* TABS */
.tabs-container { display: flex; gap: 10px; margin-bottom: 20px; }
.tab-btn { background: #ffffff; border: 1px solid #ffede3; color: #ff7322; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer; transition: 0.2s;}
.tab-btn.active { background: #ff7322; color: white; border-color: #ff7322; }

.header-form { justify-content: flex-start; gap: 20px; }
.btn-voltar { background: none; border: none; color: #ff7322; cursor: pointer; display: flex; align-items: center; }
.btn-voltar svg { width: 24px; height: 24px; }

/* TÍTULO E LAYOUT DO FORMULÁRIO IGUAL À IMAGEM */
.form-title-orange { font-family: "Anton SC", sans-serif; color: #ff7322; margin: 0; }
.form-card { border: 1px solid #ff7322; padding: 30px; }
.form-layout-clean { display: flex; flex-direction: column; gap: 25px; }
.form-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; }
.mt-20 { margin-top: 10px; }

.input-col { display: flex; flex-direction: column; gap: 8px; }
.input-col label { color: #ff7322; font-size: 13px; font-weight: 500; }
.input-col input, .input-col select { width: 100%; border: none; border-bottom: 1px solid #ffede3; padding: 10px 0; font-size: 14px; color: #ff7322; background: transparent; outline: none; cursor: pointer; }
.input-col input:focus, .input-col select:focus { border-bottom: 1px solid #ff7322; }

.select-box { position: relative; }
.select-box::after { content: '▼'; font-size: 10px; color: #ff7322; position: absolute; right: 0; top: 50%; transform: translateY(-50%); pointer-events: none; }
.select-box select { appearance: none; -webkit-appearance: none; padding-right: 20px; }

.form-actions-right { display: flex; justify-content: flex-end; gap: 15px; margin-top: 30px; border-top: 1px dashed #f0e6de; padding-top: 25px; }
.btn-salvar { background-color: #0b9e15; color: white; border: none; padding: 12px 30px; border-radius: 6px; font-weight: 600; font-size: 14px; cursor: pointer; }
.btn-cancelar { background-color: transparent; color: #ff7322; border: 1px solid #ffede3; padding: 12px 30px; border-radius: 6px; font-weight: 600; font-size: 14px; cursor: pointer; }

@media (max-width: 768px) {
  .form-grid-3 { grid-template-columns: 1fr; gap: 15px; }
  .filtros-bar { flex-direction: column; align-items: stretch; }
  .search-bar, .filtro-proprietario-custom { max-width: 100%; }
}
</style>