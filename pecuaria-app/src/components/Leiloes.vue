<template>
  <div class="leiloes-page">
    <header class="top-bar">
      <p class="current-date">{{ dataFormatada }}</p>
    </header>

    <div v-if="mensagemFeedback" class="feedback-banner">
      <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg>
      {{ mensagemFeedback }}
    </div>

    <!-- TELA DE LISTAGEM -->
    <div v-if="telaAtual === 'lista'">
      <div class="page-header">
        <div class="title-section">
          <h1 class="page-title">LEILÕES</h1>
          <p class="page-subtitle">Gerencie os leilões e animais participantes</p>
        </div>
        <button class="btn-novo" @click="abrirFormulario()">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          Novo Leilão
        </button>
      </div>

      <!-- BARRA DE FERRAMENTAS E FILTROS -->
      <div class="tools-bar">
        <div class="search-wrapper">
          <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          <input type="text" v-model="termoBusca" placeholder="Buscar por local..." />
        </div>

        <div class="status-filters">
          <button :class="['btn-filter-status', { active: filtroStatus === 'todos' }]"
            @click="filtroStatus = 'todos'">Todos</button>
          <button :class="['btn-filter-status', { active: filtroStatus === 'Agendado' }]"
            @click="filtroStatus = 'Agendado'">Agendado</button>
          <button :class="['btn-filter-status', { active: filtroStatus === 'Realizado' }]"
            @click="filtroStatus = 'Realizado'">Realizado</button>
        </div>

        <div class="custom-select-container">
          <div class="custom-select-trigger">
            <svg class="icon-filter" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4">
              </path>
            </svg>
            <span>Proprietário</span>
            <svg class="icon-arrow-down" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </div>
          <select v-model="filtroProprietario" class="hidden-select">
            <option value="">Todos</option>
            <option v-for="prop in listaProprietarios" :key="prop.id_dono" :value="prop.id_dono">{{ prop.nome }}
            </option>
          </select>
        </div>
      </div>

      <div class="table-wrapper">
        <table class="styled-table">
          <thead>
            <tr>
              <th style="width: 25%;">Data</th>
              <th style="width: 35%;">Local</th>
              <th style="width: 20%;">Status</th>
              <th style="width: 20%; text-align: center;">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="leiloesFiltrados.length === 0">
              <td colspan="4" class="tabela-vazia">Nenhum leilão encontrado com esses filtros.</td>
            </tr>
            <tr v-for="leilao in leiloesFiltrados" :key="leilao.id_leilao">
              <td class="col-date">
                <span class="icon-text-group">
                  <svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  {{ formatarDataExtenso(leilao.dt_leilao) }}
                </span>
              </td>
              <td class="col-local">
                <span class="icon-text-group">
                  <svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                  {{ leilao.local || 'Local não informado' }}
                </span>
              </td>
              <td class="col-status">
                <!-- ETIQUETAS DE STATUS CORRIGIDAS -->
                <span class="status-badge" :class="leilao.badgeClass">{{ leilao.badgeText }}</span>
              </td>
              <td class="col-actions">
                <button class="btn-action btn-view" @click="abrirModalDetalhes(leilao.id_leilao)" title="Detalhes">
                  <svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z">
                    </path>
                  </svg>
                </button>

                <button class="btn-action btn-edit" @click="editarLeilao(leilao)" title="Editar">
                  <svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z">
                    </path>
                  </svg>
                </button>

                <button class="btn-action btn-delete" @click="excluirLeilao(leilao.id_leilao)" title="Excluir">
                  <svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16">
                    </path>
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL DE DETALHES (VALORES REMOVIDOS) -->
    <div v-if="mostrarModalDetalhes" class="modal-overlay">
      <div class="modal-detalhes-wrapper">
        <div class="modal-header-detalhes">
          <button class="btn-close-modal" @click="fecharModalDetalhes">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
          <h2 class="detalhes-titulo">{{ detalhesLeilao.nome_evento || 'Carregando...' }}</h2>
          <div class="detalhes-sub-header">
            <span class="icon-text-group" v-if="detalhesLeilao.dt_leilao">
              <svg class="icon-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
              {{ formatarDataExtenso(detalhesLeilao.dt_leilao) }}
            </span>
            <span class="status-badge"
              :class="detalhesLeilao.status_text === 'Realizado' ? 'badge-verde' : 'badge-amarelo'"
              v-if="detalhesLeilao.status_text">
              {{ detalhesLeilao.status_text }}
            </span>
          </div>
        </div>

        <div class="modal-body-detalhes">

          <div v-if="detalhesLeilao.erro" class="erro-detalhes">
            <h3>Erro ao carregar detalhes!</h3>
            <p>{{ detalhesLeilao.erro }}</p>
          </div>

          <div v-else-if="!detalhesLeilao.erro">
            <!-- Blocos de Resumo (Apenas Animais e Proprietários) -->
            <div class="summary-blocks">
              <div class="summary-item">
                <div class="icon-box"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253">
                    </path>
                  </svg></div>
                <span class="summary-value">{{ detalhesLeilao.qtd_animais || 0 }}</span>
                <span class="summary-label">animais</span>
              </div>
              <div class="summary-item">
                <div class="icon-box"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z">
                    </path>
                  </svg></div>
                <span class="summary-value">{{ detalhesLeilao.qtd_proprietarios || 0 }}</span>
                <span class="summary-label">proprietário{{ detalhesLeilao.qtd_proprietarios > 1 ? 's' : '' }}</span>
              </div>
            </div>

            <!-- Métricas -->
            <div class="metrics-row">
              <div class="metric-card">
                <div class="metric-icon"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                  </svg></div>
                <span class="metric-label">PESO TOTAL</span>
                <span class="metric-value">{{ (detalhesLeilao.peso_total || 0).toFixed(1).replace('.', ',') }}
                  <small>kg</small></span>
              </div>
              <div class="metric-card">
                <div class="metric-icon"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3">
                    </path>
                  </svg></div>
                <span class="metric-label">PESO MÉDIO</span>
                <span class="metric-value">{{ (detalhesLeilao.peso_medio || 0).toFixed(1).replace('.', ',') }}
                  <small>kg</small></span>
              </div>
            </div>

            <!-- Categorias -->
            <div class="section-block">
              <h4 class="section-subtitle">CATEGORIAS</h4>
              <div class="categories-list">
                <div v-for="cat in detalhesLeilao.categorias" :key="cat.id_categoria" class="category-tag">
                  <span>{{ cat.descricao }}</span>
                  <span class="category-count">{{ cat.total }}</span>
                </div>
                <div v-if="!detalhesLeilao.categorias || detalhesLeilao.categorias.length === 0" class="text-muted">
                  Nenhuma categoria definida para este lote.
                </div>
              </div>
            </div>

            <!-- Distribuição por Proprietário -->
            <div class="section-block">
              <h4 class="section-subtitle">DISTRIBUIÇÃO POR PROPRIETÁRIO</h4>
              <div class="owners-list">
                <div v-for="prop in detalhesLeilao.distribuicao_proprietarios" :key="prop.id_dono" class="owner-item">
                  <div class="owner-avatar">{{ prop.nome.charAt(0) }}</div>
                  <div class="owner-info">
                    <div class="owner-name">{{ prop.nome }}</div>
                    <div class="owner-stats">{{ prop.total_animais }} animais - {{ prop.porcentagem }}% do lote</div>
                    <div class="progress-bar-container">
                      <div class="progress-bar-fill" :style="{ width: prop.porcentagem + '%' }"></div>
                    </div>
                  </div>
                </div>
                <div
                  v-if="!detalhesLeilao.distribuicao_proprietarios || detalhesLeilao.distribuicao_proprietarios.length === 0"
                  class="text-muted">
                  Nenhum proprietário vinculado a este lote.
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- TELA DE FORMULÁRIO -->
    <div v-else-if="telaAtual === 'formulario'">
      <div class="page-header header-form">
        <button class="btn-voltar" @click="voltarParaLista" title="Voltar">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18">
            </path>
          </svg>
        </button>
        <div class="title-section">
          <h1 class="page-title">{{ editandoId ? 'EDITAR LEILÃO' : 'NOVO LEILÃO' }}</h1>
        </div>
      </div>

      <div class="content-card form-card">
        <form @submit.prevent="salvarLeilao" class="form-grid">
          <div class="input-group">
            <label>Nome do Evento (Ex: Leilão #1)</label>
            <input type="text" v-model="form.nome_evento" required>
          </div>
          <div class="input-group">
            <label>Data do Leilão</label>
            <input type="date" v-model="form.dt_leilao" required>
          </div>
          <div class="input-group">
            <label>Local do Evento</label>
            <input type="text" v-model="form.local" placeholder="Ex: Parque de Exposições">
          </div>
          <div class="input-group">
            <label>Custo Fixo Previsto (R$)</label>
            <input type="number" step="0.01" v-model="form.custo_fixo" required>
          </div>

          <div class="input-group full-width" style="margin-top: 15px;">
            <label>Selecione os Animais Participantes</label>
            <div class="checkbox-grid">
              <label class="checkbox-item" v-for="animal in animaisDisponiveis" :key="animal.id">
                <input type="checkbox" :value="animal.id" v-model="form.animais_ids">
                <span class="checkbox-text">{{ animal.nome }} ({{ animal.raca }})</span>
              </label>
              <div v-if="animaisDisponiveis.length === 0" class="sem-animais-aviso">
                Nenhum animal livre no momento.
              </div>
            </div>
          </div>

          <div class="form-actions full-width">
            <button type="submit" class="btn-salvar">Salvar Leilão</button>
            <button type="button" class="btn-cancelar" @click="voltarParaLista">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';

const telaAtual = ref('lista');
const mensagemFeedback = ref('');
const editandoId = ref(null);

// Dados
const listaLeiloes = ref([]);
const listaAnimais = ref([]);
const listaProprietarios = ref([]);

// Filtros
const termoBusca = ref('');
const filtroStatus = ref('todos');
const filtroProprietario = ref('');

// Modal de Detalhes
const mostrarModalDetalhes = ref(false);
const detalhesLeilao = ref({});

// Formulário
const form = reactive({
  nome_evento: '',
  dt_leilao: '',
  local: '',
  custo_fixo: 0,
  animais_ids: []
});

// Data atual formatada
const dataAtual = new Date();
const dataFormatada = ref(
  dataAtual.toLocaleDateString('pt-BR', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
);

// Computed: animais disponíveis para vincular
const animaisDisponiveis = computed(() => {
  const idsOcupados = new Set();
  listaLeiloes.value.forEach(leilao => {
    if (leilao.id_leilao !== editandoId.value) {
      (leilao.animais || []).forEach(animal => idsOcupados.add(animal.id));
    }
  });
  return listaAnimais.value.filter(animal => !idsOcupados.has(animal.id));
});

/* ==============================================================
   LÓGICA DE ESTILOS E ETIQUETAS (CORRIGIDO)
   ============================================================== */
const leiloesComEstilo = computed(() => {
  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);

  return listaLeiloes.value.map(leilao => {
    let dataLeilao = null;
    if (leilao.dt_leilao) {
      // Converte string 'YYYY-MM-DD' para objeto Date de forma segura
      const partes = leilao.dt_leilao.split('-');
      if (partes.length === 3) {
        dataLeilao = new Date(parseInt(partes[0]), parseInt(partes[1]) - 1, parseInt(partes[2]));
      } else {
        dataLeilao = new Date(leilao.dt_leilao + 'T00:00:00');
      }
      dataLeilao.setHours(0, 0, 0, 0);
    }

    let badgeClass = 'badge-amarelo';
    let badgeText = 'Agendado';

    if (dataLeilao && dataLeilao < hoje) {
      badgeClass = 'badge-verde';
      badgeText = 'Realizado';
    }

    return {
      ...leilao,
      badgeClass,
      badgeText
    };
  });
});

/* ==============================================================
   LÓGICA DE FILTRAGEM (AQUI ESTAVA O ERRO ANTES)
   ============================================================== */
const leiloesFiltrados = computed(() => {
  return leiloesComEstilo.value.filter(leilao => {
    const termo = termoBusca.value.toLowerCase().trim();
    const bateLocal = !termo || (leilao.local && leilao.local.toLowerCase().includes(termo));
    const bateStatus = filtroStatus.value === 'todos' || leilao.badgeText === filtroStatus.value;

    let bateProprietario = true;
    if (filtroProprietario.value) {
      const idProp = parseInt(filtroProprietario.value);
      const temAnimalDoProp = leilao.animais.some(a => a.id_dono === idProp);
      bateProprietario = temAnimalDoProp;
    }

    return bateLocal && bateStatus && bateProprietario;
  });
});

// ----------------------------------------------------------------------
// Carregar dados da API
// ----------------------------------------------------------------------
const carregarDados = async () => {
  try {
    const resLeiloes = await fetch('http://127.0.0.1:8000/api/leiloes/');
    listaLeiloes.value = await resLeiloes.json();

    const resAnimais = await fetch('http://127.0.0.1:8000/api/animais/');
    listaAnimais.value = await resAnimais.json();

    const resProprietarios = await fetch('http://127.0.0.1:8000/api/proprietarios/');
    listaProprietarios.value = await resProprietarios.json();
  } catch (error) {
    console.error('Erro ao carregar dados:', error);
    mostrarMensagem('Erro ao conectar com o servidor.');
  }
};

onMounted(carregarDados);

// ----------------------------------------------------------------------
// Helpers
// ----------------------------------------------------------------------
const formatarDataExtenso = (dataString) => {
  if (!dataString) return '';
  const data = new Date(dataString + 'T00:00:00');
  return data.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' });
};

const mostrarMensagem = (texto) => {
  mensagemFeedback.value = texto;
  setTimeout(() => {
    mensagemFeedback.value = '';
  }, 3000);
};

// ----------------------------------------------------------------------
// Ações da listagem
// ----------------------------------------------------------------------
const abrirFormulario = () => {
  form.nome_evento = '';
  form.dt_leilao = '';
  form.local = '';
  form.custo_fixo = 0;
  form.animais_ids = [];
  editandoId.value = null;
  telaAtual.value = 'formulario';
};

const editarLeilao = (leilao) => {
  form.nome_evento = leilao.nome_evento;
  form.dt_leilao = leilao.dt_leilao;
  form.local = leilao.local || '';
  form.custo_fixo = leilao.custo_fixo;
  form.animais_ids = (leilao.animais || []).map(a => a.id);
  editandoId.value = leilao.id_leilao;
  telaAtual.value = 'formulario';
};

const voltarParaLista = () => {
  telaAtual.value = 'lista';
};

const excluirLeilao = async (id) => {
  if (!confirm('Tem certeza que deseja excluir este leilão?')) return;
  try {
    const resposta = await fetch(`http://127.0.0.1:8000/api/leiloes/${id}/`, {
      method: 'DELETE'
    });
    if (resposta.ok) {
      mostrarMensagem('Leilão removido com sucesso!');
      await carregarDados();
    } else {
      mostrarMensagem('Erro ao excluir o leilão.');
    }
  } catch (error) {
    console.error(error);
    mostrarMensagem('Erro de conexão.');
  }
};

/* ==============================================================
   AÇÃO DO OLHINHO
   ============================================================== */
const abrirModalDetalhes = async (id_leilao) => {
  mostrarModalDetalhes.value = true;
  detalhesLeilao.value = { carregando: true };

  try {
    const resposta = await fetch(`http://127.0.0.1:8000/api/leiloes/${id_leilao}/detalhes/`);
    if (resposta.ok) {
      detalhesLeilao.value = await resposta.json();
    } else {
      detalhesLeilao.value = {
        erro: `Erro ${resposta.status}: Não foi possível carregar as informações.`
      };
    }
  } catch (error) {
    console.error(error);
    detalhesLeilao.value = {
      erro: 'Erro de conexão com o servidor. Verifique sua rede.'
    };
  }
};

const fecharModalDetalhes = () => {
  mostrarModalDetalhes.value = false;
  detalhesLeilao.value = {};
};

// ----------------------------------------------------------------------
// Salvar (criação/edição)
// ----------------------------------------------------------------------
const salvarLeilao = async () => {
  const url = editandoId.value
    ? `http://127.0.0.1:8000/api/leiloes/${editandoId.value}/`
    : 'http://127.0.0.1:8000/api/leiloes/';
  const metodo = editandoId.value ? 'PUT' : 'POST';

  try {
    const resposta = await fetch(url, {
      method: metodo,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });

    if (resposta.ok) {
      mostrarMensagem(editandoId.value ? 'Leilão atualizado com sucesso!' : 'Leilão cadastrado com sucesso!');
      await carregarDados();
      voltarParaLista();
    } else {
      const erro = await resposta.json();
      mostrarMensagem(erro.erro || 'Erro ao salvar leilão.');
    }
  } catch (error) {
    console.error(error);
    mostrarMensagem('Erro de conexão com o servidor.');
  }
};
</script>

<style scoped>
/* ===== ESTILOS GERAIS ===== */
.leiloes-page {
  padding: 20px 40px;
  background-color: #f9f2ec;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, sans-serif;
}

.top-bar {
  border-bottom: 1px solid #ebdcd1;
  padding-bottom: 10px;
  margin-bottom: 25px;
}

.current-date {
  color: #8a7b72;
  font-size: 14px;
  margin: 0;
  text-transform: lowercase;
}

.feedback-banner {
  position: fixed;
  top: 30px;
  right: 30px;
  z-index: 9999;
  width: fit-content;
  max-width: 400px;
  background-color: #eafbee;
  color: #0b9e15;
  border: 1px solid #b7f0c1;
  padding: 15px 25px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
  font-size: 14px;
  box-shadow: 0 10px 25px rgba(11, 158, 21, 0.15);
  animation: deslizarParaEsquerda 0.3s ease-out forwards;
}

@keyframes deslizarParaEsquerda {
  from {
    transform: translateX(100%);
    opacity: 0;
  }

  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 30px;
}

.page-title {
  font-family: "Anton SC", sans-serif;
  font-size: 32px;
  color: #1e293b;
  margin: 0;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.page-subtitle {
  color: #64748b;
  font-size: 15px;
  margin: 5px 0 0 0;
}

.btn-novo {
  background-color: #0b9e15;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: 0.2s;
}

.btn-novo:hover {
  background-color: #098011;
}

/* ===========================================================
   BARRA DE FERRAMENTAS E FILTROS
   =========================================================== */
.tools-bar {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  flex-wrap: wrap;
}

.search-wrapper {
  display: flex;
  align-items: center;
  background-color: #ffffff;
  border: 1.5px solid #f0e6de;
  border-radius: 8px;
  padding: 8px 16px;
  flex: 1;
  max-width: 400px;
  height: 44px;
  transition: border-color 0.2s;
}

.search-wrapper:focus-within {
  border-color: #ff7322;
}

.search-wrapper input {
  border: none;
  background: transparent;
  outline: none;
  width: 100%;
  font-size: 14px;
  color: #334155;
}

.search-icon {
  width: 20px;
  height: 20px;
  color: #94a3b8;
  margin-right: 10px;
}

.status-filters {
  display: flex;
  gap: 8px;
}

.btn-filter-status {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  color: #64748b;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-filter-status:hover {
  border-color: #ff7322;
  color: #ff7322;
}

.btn-filter-status.active {
  background-color: #ff7322;
  border-color: #ff7322;
  color: #ffffff;
}

.custom-select-container {
  position: relative;
  width: 200px;
  height: 44px;
}

.custom-select-trigger {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border: 1.5px solid #ff7322;
  border-radius: 8px;
  background-color: #ffffff;
  color: #ff7322;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  box-sizing: border-box;
  pointer-events: none;
}

.custom-select-trigger .icon-filter,
.custom-select-trigger .icon-arrow-down {
  width: 20px;
  height: 20px;
  stroke: #ff7322;
}

.hidden-select {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  z-index: 2;
}

/* ===========================================================
   TABELA
   =========================================================== */
.table-wrapper {
  background: #ffffff;
  border-radius: 10px;
  padding: 20px;
  border: 1px solid #f0e6de;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.styled-table thead tr {
  border-bottom: 2px solid #f1f3f5;
}

.styled-table thead th {
  text-align: left;
  padding: 12px 16px;
  font-weight: 600;
  color: #475569;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.styled-table tbody tr {
  border-bottom: 1px solid #f1f3f5;
  transition: background 0.2s;
}

.styled-table tbody tr:hover {
  background-color: #faf8f6;
}

.styled-table tbody td {
  padding: 16px 16px;
  color: #1e293b;
  vertical-align: middle;
}

.icon-sm {
  width: 16px;
  height: 16px;
  color: #94a3b8;
  flex-shrink: 0;
}

.icon-text-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.text-muted {
  font-size: 13px;
  color: #94a3b8;
  font-style: italic;
}

/* ===== BADGES DE STATUS ===== */
.status-badge {
  padding: 4px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  display: inline-block;
}

.badge-verde {
  background-color: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.badge-amarelo {
  background-color: #fef3c7;
  color: #92400e;
  border: 1px solid #fde68a;
}

/* ===== AÇÕES DA TABELA ===== */
.col-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.btn-action {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 6px;
  border-radius: 4px;
  transition: background 0.2s, color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-action .icon-sm {
  width: 20px;
  height: 20px;
}

.btn-view {
  color: #ff7322;
}

.btn-view:hover {
  background-color: #fff7ed;
}

.btn-edit {
  color: #f97316;
}

.btn-edit:hover {
  background-color: #fff7ed;
}

.btn-delete {
  color: #ef4444;
}

.btn-delete:hover {
  background-color: #fef2f2;
}

.tabela-vazia {
  text-align: center;
  color: #94a3b8;
  padding: 40px;
  font-style: italic;
}

/* ===========================================================
   MODAL DE DETALHES (SEM VALORES FINANCEIROS)
   =========================================================== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-detalhes-wrapper {
  background-color: #ffffff;
  width: 100%;
  max-width: 650px;
  max-height: 90vh;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.modal-header-detalhes {
  background-color: #ff6b00;
  color: #ffffff;
  padding: 25px 30px;
  position: relative;
}

.btn-close-modal {
  position: absolute;
  top: 15px;
  right: 15px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #ffffff;
  transition: 0.2s;
}

.btn-close-modal:hover {
  background: rgba(255, 255, 255, 0.4);
}

.btn-close-modal svg {
  width: 18px;
  height: 18px;
  stroke-width: 2.5px;
}

.detalhes-titulo {
  font-family: "Anton SC", sans-serif;
  font-size: 26px;
  margin: 0 0 10px 0;
  text-transform: uppercase;
}

.detalhes-sub-header {
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 14px;
  font-weight: 500;
}

.detalhes-sub-header .icon-white {
  width: 18px;
  height: 18px;
  stroke: #ffffff;
}

.modal-body-detalhes {
  padding: 25px 30px 30px 30px;
  overflow-y: auto;
  background-color: #f9f2ec;
}

.erro-detalhes {
  background-color: #fee2e2;
  border: 1px solid #fecaca;
  padding: 20px;
  border-radius: 8px;
  color: #991b1b;
  text-align: center;
  margin-bottom: 20px;
}

.summary-blocks {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 25px;
}

.summary-item {
  background: #ffffff;
  border-radius: 8px;
  flex: 1;
  padding: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.summary-item .icon-box svg {
  width: 22px;
  height: 22px;
  color: #ff7322;
  margin-bottom: 6px;
}

.summary-value {
  font-weight: 800;
  font-size: 15px;
  color: #1e293b;
}

.summary-label {
  font-size: 11px;
  color: #94a3b8;
  font-weight: 500;
  text-transform: lowercase;
}

.metrics-row {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
}

.metric-card {
  flex: 1;
  background: #ffffff;
  border-radius: 8px;
  padding: 15px 20px;
  display: flex;
  flex-direction: column;
  border: 1px solid #f0e6de;
}

.metric-icon svg {
  width: 24px;
  height: 24px;
  color: #ff7322;
  margin-bottom: 8px;
}

.metric-label {
  font-size: 11px;
  color: #64748b;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.metric-value {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

.metric-value small {
  font-size: 12px;
  font-weight: 400;
  color: #94a3b8;
}

.section-block {
  margin-bottom: 20px;
}

.section-subtitle {
  font-size: 12px;
  color: #64748b;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}

.categories-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.category-tag {
  background: #fffaf7;
  border: 1px solid #ffede3;
  padding: 6px 14px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #1e293b;
}

.category-count {
  background: #ff7322;
  color: #ffffff;
  font-weight: 700;
  font-size: 12px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.owners-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.owner-item {
  background: #ffffff;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 15px;
  border-bottom: 3px solid #ff7322;
}

.owner-avatar {
  background: #ff7322;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  flex-shrink: 0;
}

.owner-info {
  flex: 1;
}

.owner-name {
  font-weight: 600;
  color: #1e293b;
  font-size: 15px;
}

.owner-stats {
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 8px;
}

.progress-bar-container {
  width: 100%;
  height: 4px;
  background-color: #f1f5f9;
  border-radius: 4px;
}

.progress-bar-fill {
  height: 100%;
  background-color: #ff7322;
  border-radius: 4px;
}

/* ===== FORMULÁRIO ===== */
.header-form {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 20px;
}

.btn-voltar {
  background: none;
  border: none;
  color: #ff7322;
  cursor: pointer;
  display: flex;
  padding: 5px;
}

.btn-voltar svg {
  width: 26px;
  height: 26px;
}

.content-card {
  background: #ffffff;
  border-radius: 10px;
  padding: 30px;
  border: 1px solid #ff7322;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px 40px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  font-size: 13px;
  font-weight: 500;
  color: #ff7322;
}

.input-group input {
  width: 100%;
  padding: 10px 0;
  border: none;
  border-bottom: 1px solid transparent;
  background-color: transparent;
  font-size: 14px;
  color: #ff7322;
  outline: none;
}

.input-group input:focus {
  border-bottom: 1px solid #ff7322;
}

.full-width {
  grid-column: span 2;
}

.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
  background: #fffaf7;
  padding: 15px;
  border-radius: 6px;
  border: 1px solid #ffede3;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.checkbox-item input[type="checkbox"] {
  width: auto;
  accent-color: #ff7322;
  transform: scale(1.2);
}

.checkbox-text {
  font-size: 14px;
  color: #475569;
}

.sem-animais-aviso {
  color: #ea580c;
  font-size: 14px;
  font-style: italic;
  width: 100%;
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.btn-salvar {
  background-color: #0b9e15;
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}

.btn-cancelar {
  background-color: transparent;
  color: #ff7322;
  border: 1px solid #ffede3;
  padding: 12px 25px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}

@media (max-width: 768px) {
  .leiloes-page {
    padding: 15px;
  }

  .tools-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-wrapper {
    max-width: 100%;
  }

  .status-filters {
    justify-content: space-between;
  }

  .custom-select-container {
    width: 100%;
  }

  .summary-blocks {
    flex-wrap: wrap;
  }

  .summary-item {
    min-width: 45%;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .full-width {
    grid-column: span 1;
  }
}
</style>