<template>
  <div class="vendas-page">
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
          <h1 class="page-title">VENDAS</h1>
          <p class="page-subtitle">Histórico e análise de vendas realizadas</p>
        </div>
        <button class="btn-novo" @click="abrirFormulario()">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          + Nova Venda
        </button>
      </div>

      <div class="dashboard-cards">
        <div class="kpi-card">
          <div class="kpi-info">
            <span class="kpi-label">Total de Vendas</span>
            <span class="kpi-value">{{ totalVendas }}</span>
          </div>
          <div class="kpi-icon icon-orange">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6">
              </path>
            </svg>
          </div>
        </div>
        <div class="kpi-card">
          <div class="kpi-info">
            <span class="kpi-label">Valor Total</span>
            <span class="kpi-value">{{ formatarMoeda(valorTotal) }}</span>
          </div>
          <div class="kpi-icon icon-green">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z">
              </path>
            </svg>
          </div>
        </div>
        <div class="kpi-card">
          <div class="kpi-info">
            <span class="kpi-label">Ticket Médio</span>
            <span class="kpi-value">{{ formatarMoeda(ticketMedio) }}</span>
          </div>
          <div class="kpi-icon icon-yellow">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path>
            </svg>
          </div>
        </div>
        <div class="kpi-card">
          <div class="kpi-info">
            <span class="kpi-label">Custo Fixo (Leilões)</span>
            <span class="kpi-value">{{ formatarMoeda(custoFixoTotal) }}</span>
          </div>
          <div class="kpi-icon icon-blue">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z">
              </path>
            </svg>
          </div>
        </div>
      </div>

      <div class="content-card">
        <div class="filtros-bar">
          <div class="search-bar">
            <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            <input type="text" v-model="termoBusca" placeholder="Buscar por brinco, evento ou comprador..." />
          </div>

          <div class="filtro-proprietario-custom">
            <svg class="icon-user" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            <select v-model="donoSelecionado">
              <option :value="null">Todas as Vendas</option>
              <option v-for="dono in proprietariosOrdenados" :key="dono.id_dono" :value="dono.id_dono">
                {{ dono.nome }}
              </option>
            </select>
            <svg class="icon-seta" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </div>
        </div>

        <div class="table-container">
          <table class="dados-table">
            <thead>
              <tr>
                <th>Data</th>
                <th>Brinco</th>
                <th>Leilão Origem</th>
                <th>Vendedor</th>
                <th>Comprador</th>
                <th>Pagamento</th>
                <th>Valor</th>
                <th class="text-right">Ações</th>
              </tr>
            </thead>

            <tbody v-if="vendasFiltradas.length === 0">
              <tr>
                <td colspan="8" class="tabela-vazia">Nenhuma venda encontrada.</td>
              </tr>
            </tbody>

            <tbody v-for="venda in vendasFiltradas" :key="venda.id_venda">
              <tr>
                <td>{{ formatarDataBR(venda.dt_venda) }}</td>
                <td class="destaque-texto">{{ venda.animal_nome }}</td>
                <td>
                  <span v-if="venda.leilao_nome !== 'Venda Direta'" class="badge-leilao-tag">{{ venda.leilao_nome
                  }}</span>
                  <span v-else class="badge-direta">Direta</span>
                </td>
                <td>{{ venda.vendedor }}</td>
                <td>{{ venda.comprador }}</td>
                <td>{{ venda.tipo_pagamento }}</td>
                <td class="td-valor">{{ formatarMoeda(venda.valor) }}</td>
                <td class="acoes text-right">
                  <button class="btn-acao edit" title="Editar" @click="prepararEdicao(venda)">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z">
                      </path>
                    </svg>
                  </button>
                  <button v-if="perfilUsuario === 'Administrador'" class="btn-acao delete" title="Excluir"
                    @click="removerVenda(venda.id_venda)">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16">
                      </path>
                    </svg>
                  </button>
                </td>
              </tr>
              <tr v-if="venda.justificativa_alteracao" class="row-justificativa">
                <td colspan="8">
                  <div class="text-justificativa">
                    <svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z">
                      </path>
                    </svg>
                    <strong>Histórico de Alteração:</strong> "{{ venda.justificativa_alteracao }}"
                  </div>
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
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18">
            </path>
          </svg>
        </button>
        <div class="title-section">
          <h1 class="page-title">{{ editandoId ? 'ALTERAR DADOS DA VENDA' : 'REGISTRAR NOVO FATURAMENTO' }}</h1>
        </div>
      </div>

      <div v-if="!editandoId" class="tabs-container">
        <button :class="['tab-btn', { active: modoLancamento === 'direta' }]" @click="modoLancamento = 'direta'">Venda
          Individual Direta</button>
        <button :class="['tab-btn', { active: modoLancamento === 'leilao' }]"
          @click="modoLancamento = 'leilao'">Faturamento em Lote (Por Leilão)</button>
      </div>

      <div class="content-card form-card">
        <form v-if="modoLancamento === 'direta'" @submit.prevent="salvarVenda" class="form-grid">

          <div class="input-group">
            <label>Selecione o Proprietário do Gado</label>
            <div class="select-wrapper">
              <select v-model="donoFormCadastro">
                <option :value="null">Todos os Proprietários</option>
                <option v-for="dono in proprietariosOrdenados" :key="dono.id_dono" :value="dono.id_dono">
                  {{ dono.nome }}
                </option>
              </select>
            </div>
          </div>

          <div class="input-group">
            <label>Selecione o Animal (Número do Brinco)</label>
            <div class="select-wrapper">
              <select v-model="formVenda.id_animal" required @change="vincularVendedorAutomatico">
                <option value="" disabled>Escolha o brinco do animal...</option>
                <option v-for="animal in animaisFiltradosPorDonoForm" :key="animal.id" :value="animal.id">
                  Brinco: {{ animal.nome }} — {{ animal.raca }} (Dono: {{ animal.dono_nome }})
                </option>
              </select>
            </div>
          </div>

          <div class="input-group">
            <label>Valor da Venda (R$)</label>
            <input type="number" step="0.01" v-model="formVenda.valor" required>
          </div>

          <div class="input-group">
            <label>Data da Venda</label>
            <input type="date" v-model="formVenda.data_venda" required>
          </div>

          <div class="input-group">
            <label>Vendedor (Proprietário Vinculado)</label>
            <div class="select-wrapper">
              <select v-model="formVenda.vendedor" required>
                <option value="" disabled>Selecione o proprietário vendedor...</option>
                <option v-for="dono in proprietariosOrdenados" :key="dono.id_dono" :value="dono.nome">
                  {{ dono.nome }}
                </option>
              </select>
            </div>
          </div>

          <div class="input-group">
            <label>Comprador / Destino</label>
            <input type="text" v-model="formVenda.comprador" required>
          </div>

          <div class="input-group">
            <label>Forma de Pagamento</label>
            <div class="select-wrapper">
              <select v-model="formVenda.tipo_pagamento" required>
                <option value="Pix">Pix</option>
                <option value="Boleto Bancário">Boleto Bancário</option>
                <option value="Dinheiro à Vista">Dinheiro à Vista</option>
                <option value="Cartão de Crédito">Cartão de Crédito</option>
              </select>
            </div>
          </div>

          <div class="input-group">
            <label>Vincular a um Leilão (Opcional)</label>
            <div class="select-wrapper">
              <select v-model="formVenda.id_leilao">
                <option :value="null">Nenhum (Venda Direta)</option>
                <option v-for="l in listaLeiloes" :key="l.id_leilao" :value="l.id_leilao">{{ l.nome_evento }}</option>
              </select>
            </div>
          </div>

          <div class="input-group full-width section-alert" v-if="editandoId">
            <label class="alert-label">Justificativa para alteração dos dados cadastrais (Obrigatório)</label>
            <input type="text" v-model="formVenda.justificativa_alteracao" required>
          </div>

          <div class="form-actions full-width">
            <button type="submit" class="btn-salvar">Gravar Registro</button>
            <button type="button" class="btn-cancelar" @click="voltarParaLista">Cancelar</button>
          </div>
        </form>

        <form v-else @submit.prevent="salvarVendaLote" class="form-grid">
          <div class="input-group full-width">
            <label>Selecione o Leilão Realizado</label>
            <div class="select-wrapper">
              <select v-model="formLote.id_leilao" required>
                <option value="" disabled>Escolha o leilão para extrair os animais...</option>
                <option v-for="l in leiloesDisponiveisLote" :key="l.id_leilao" :value="l.id_leilao">
                  {{ l.nome_evento }} ({{ formatarDataBR(l.dt_leilao) }})
                </option>
              </select>
            </div>
            <span v-if="leiloesDisponiveisLote.length === 0" class="alerta-lista-vazia">
              Não há leilões realizados disponíveis para faturamento.
            </span>
          </div>

          <div class="input-group">
            <label>Valor Padrão por Animal (R$)</label>
            <input type="number" step="0.01" v-model="formLote.valor_padrao" required>
          </div>

          <div class="input-group">
            <label>Data de Fechamento</label>
            <input type="date" v-model="formLote.data_venda" required>
          </div>

          <div class="input-group full-width">
            <label>Vendedor do Leilão</label>
            <div class="select-wrapper">
              <select v-model="formLote.vendedor" required>
                <option value="" disabled>Selecione o proprietário remetente...</option>
                <option v-for="dono in proprietariosOrdenados" :key="dono.id_dono" :value="dono.nome">
                  {{ dono.nome }}
                </option>
              </select>
            </div>
          </div>

          <div class="input-group">
            <label>Arrematante / Comprador</label>
            <input type="text" v-model="formLote.comprador" required>
          </div>

          <div class="input-group">
            <label>Forma de Pagamento do Arremate</label>
            <div class="select-wrapper">
              <select v-model="formLote.tipo_pagamento" required>
                <option value="Pix">Pix</option>
                <option value="Boleto Bancário">Boleto Bancário</option>
                <option value="Dinheiro à Vista">Dinheiro à Vista</option>
              </select>
            </div>
          </div>

          <div class="input-group full-width section-demonstrativo"
            v-if="formLote.id_leilao && formLote.valor_padrao > 0">
            <h4 class="demonstrativo-title">Divisão Bruta de Receita do Leilão</h4>
            <div class="demonstrativo-grid">
              <div v-for="item in divisaoReceitaLote" :key="item.nome" class="demonstrativo-row">
                <span class="owner-lbl">🤠 {{ item.nome }}</span>
                <span class="owner-calc">{{ item.quantidade }} cabeça(s) × {{ formatarMoeda(formLote.valor_padrao) }}
                  =</span>
                <span class="owner-total">{{ formatarMoeda(item.totalProprietario) }}</span>
              </div>
            </div>
          </div>

          <div class="form-actions full-width">
            <button type="submit" class="btn-salvar btn-lote-color" :disabled="leiloesDisponiveisLote.length === 0">
              Processar Gados do Leilão
            </button>
            <button type="button" class="btn-cancelar" @click="voltarParaLista">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, defineProps } from 'vue';

const props = defineProps({ perfilUsuario: { type: String, default: 'Dono' } });

const telaAtual = ref('lista');
const modoLancamento = ref('direta');
const editandoId = ref(null);
const mensagemFeedback = ref('');
const tipoFeedback = ref('sucesso');
const termoBusca = ref('');
const donoSelecionado = ref(null);
const donoFormCadastro = ref(null);

const listaVendas = ref([]);
const listaAnimais = ref([]);
const listaLeiloes = ref([]);
const listaProprietarios = ref([]);

const proprietariosOrdenados = computed(() => {
  return [...listaProprietarios.value].sort((a, b) => a.nome.localeCompare(b.nome, 'pt-BR'));
});

const animaisFiltradosPorDonoForm = computed(() => {
  if (!donoFormCadastro.value) return listaAnimais.value;
  return listaAnimais.value.filter(a => Number(a.id_dono) === Number(donoFormCadastro.value));
});

const vincularVendedorAutomatico = () => {
  const animal = listaAnimais.value.find(a => a.id === formVenda.id_animal);
  if (animal) {
    formVenda.vendedor = animal.dono_nome;
  }
};

const divisaoReceitaLote = computed(() => {
  if (!formLote.id_leilao || !formLote.valor_padrao) return [];
  const leilaoSelecionado = listaLeiloes.value.find(l => Number(l.id_leilao) === Number(formLote.id_leilao));
  if (!leilaoSelecionado || !leilaoSelecionado.animais) return [];

  const contagem = {};
  leilaoSelecionado.animais.forEach(animal => {
    const dono = listaProprietarios.value.find(p => Number(p.id_dono) === Number(animal.id_dono));
    const nomeDono = dono ? dono.nome : 'Desconhecido';
    contagem[nomeDono] = (contagem[nomeDono] || 0) + 1;
  });

  return Object.keys(contagem).map(nome => ({
    nome,
    quantidade: contagem[nome],
    totalProprietario: contagem[nome] * Number(formLote.valor_padrao)
  }));
});

const vendasFiltradas = computed(() => {
  const termo = (termoBusca.value || '').toLowerCase();

  return listaVendas.value.filter(venda => {
    let bateTexto = true;
    if (termo) {
      const animalNomeStr = String(venda.animal_nome || '').toLowerCase();
      const compradorStr = String(venda.comprador || '').toLowerCase();
      const leilaoNomeStr = String(venda.leilao_nome || '').toLowerCase();
      const vendedorStr = String(venda.vendedor || '').toLowerCase();

      bateTexto = animalNomeStr.includes(termo) ||
        compradorStr.includes(termo) ||
        leilaoNomeStr.includes(termo) ||
        vendedorStr.includes(termo);
    }
    const bateDono = !donoSelecionado.value || String(venda.id_dono) === String(donoSelecionado.value);

    return bateTexto && bateDono;
  });
});

const custoFixoTotal = computed(() => {
  return listaLeiloes.value.reduce((acc, leilao) => acc + (Number(leilao.custo_fixo) || 0), 0);
});

const valorTotal = computed(() => listaVendas.value.reduce((acc, v) => acc + Number(v.valor), 0));
const totalVendas = computed(() => listaVendas.value.length);
const ticketMedio = computed(() => totalVendas.value === 0 ? 0 : valorTotal.value / totalVendas.value);

const leiloesDisponiveisLote = computed(() => {
  const leiloesJaFaturados = new Set(
    listaVendas.value.filter(venda => venda.id_leilao != null).map(venda => venda.id_leilao)
  );
  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);

  return listaLeiloes.value.filter(leilao => {
    const naoFoiFaturado = !leiloesJaFaturados.has(leilao.id_leilao);
    let jaAconteceu = false;
    if (leilao.dt_leilao) {
      const [ano, mes, dia] = leilao.dt_leilao.split('-');
      const dataLeilao = new Date(ano, mes - 1, dia);
      dataLeilao.setHours(0, 0, 0, 0);
      jaAconteceu = dataLeilao <= hoje;
    }
    return naoFoiFaturado && jaAconteceu;
  });
});

const formVenda = reactive({
  id_animal: '', valor: '', data_venda: '', vendedor: '', comprador: '', tipo_pagamento: 'Pix', id_leilao: null, justificativa_alteracao: ''
});

const formLote = reactive({
  id_leilao: '', valor_padrao: '', data_venda: '', vendedor: '', comprador: '', tipo_pagamento: 'Boleto Bancário'
});

const dataAtual = new Date();
const dataFormatada = ref(dataAtual.toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }));

const carregarDadosDoSistema = async () => {
  try {
    const resVendas = await fetch('http://127.0.0.1:8000/api/vendas/');
    listaVendas.value = await resVendas.json();
    const resAnimais = await fetch('http://127.0.0.1:8000/api/animais/');
    listaAnimais.value = await resAnimais.json();
    const resLeiloes = await fetch('http://127.0.0.1:8000/api/leiloes/');
    listaLeiloes.value = await resLeiloes.json();
    const resProprietarios = await fetch('http://127.0.0.1:8000/api/proprietarios/');
    listaProprietarios.value = await resProprietarios.json();
  } catch (error) { console.error(error); }
};

onMounted(carregarDadosDoSistema);

const abrirFormulario = () => {
  editandoId.value = null;
  modoLancamento.value = 'direta';
  donoFormCadastro.value = null;
  formVenda.id_animal = ''; formVenda.valor = ''; formVenda.vendedor = ''; formVenda.comprador = ''; formVenda.id_leilao = null; formVenda.justificativa_alteracao = '';
  formVenda.data_venda = new Date().toISOString().split('T')[0];
  formLote.id_leilao = ''; formLote.valor_padrao = ''; formLote.vendedor = 'Faturamento Lote'; formLote.comprador = '';
  telaAtual.value = 'formulario';
};

const prepararEdicao = (venda) => {
  editandoId.value = venda.id_venda;
  modoLancamento.value = 'direta';
  donoFormCadastro.value = venda.id_dono;
  formVenda.id_animal = venda.id_animal;
  formVenda.valor = venda.valor;
  formVenda.data_venda = venda.dt_venda;
  formVenda.vendedor = venda.vendedor;
  formVenda.comprador = venda.comprador;
  formVenda.tipo_pagamento = venda.tipo_pagamento;
  formVenda.id_leilao = venda.id_leilao;
  formVenda.justificativa_alteracao = '';
  telaAtual.value = 'formulario';
};

const voltarParaLista = () => { telaAtual.value = 'lista'; };

const mostrarMensagem = (texto, tipo = 'sucesso') => {
  mensagemFeedback.value = texto;
  tipoFeedback.value = tipo;
  setTimeout(() => { mensagemFeedback.value = ''; }, 3500);
};

const salvarVenda = async () => {
  const url = editandoId.value ? `http://127.0.0.1:8000/api/vendas/${editandoId.value}/` : 'http://127.0.0.1:8000/api/vendas/';
  const metodo = editandoId.value ? 'PUT' : 'POST';
  try {
    const resposta = await fetch(url, { method: metodo, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formVenda) });
    if (resposta.ok) {
      mostrarMensagem(editandoId.value ? 'Dados da venda alterados!' : 'Venda gravada com sucesso!', 'sucesso');
      await carregarDadosDoSistema(); voltarParaLista();
    } else {
      const falha = await resposta.json(); mostrarMensagem(falha.erro || 'Ocorreu um erro ao salvar.', 'erro');
    }
  } catch (error) { mostrarMensagem('Erro de conexão com o servidor.', 'erro'); }
};

const salvarVendaLote = async () => {
  try {
    const resposta = await fetch('http://127.0.0.1:8000/api/vendas/importar-leilao/', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...formLote, id_leilao: Number(formLote.id_leilao) })
    });
    const resultado = await resposta.json();
    if (resposta.ok && resultado.sucesso !== false) {
      mostrarMensagem('Lote de faturamentos gravado com sucesso!', 'sucesso');
      await carregarDadosDoSistema(); voltarParaLista();
    } else {
      mostrarMensagem(resultado.erro || 'Erro ao processar o faturamento do lote.', 'erro');
    }
  } catch (error) { mostrarMensagem('Erro técnico ao conectar com o banco.', 'erro'); }
};

const removerVenda = async (id) => {
  if (confirm("Deseja realmente deletar esta venda do histórico?")) {
    try {
      const resposta = await fetch(`http://127.0.0.1:8000/api/vendas/${id}/?perfil=${props.perfilUsuario}`, { method: 'DELETE' });
      if (resposta.ok) {
        mostrarMensagem('Venda deletada permanentemente!', 'sucesso'); await carregarDadosDoSistema();
      } else {
        const falha = await resposta.json(); mostrarMensagem(falha.erro, 'erro');
      }
    } catch (error) { mostrarMensagem('Erro na conexão.', 'erro'); }
  }
};

const formatarDataBR = (dataString) => {
  if (!dataString) return '';
  const [ano, mes, dia] = dataString.split('-');
  return `${dia}/${mes}/${ano}`;
};
const formatarMoeda = (valor) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);
</script>

<style scoped>
/* Reset e base */
*,
*::before,
*::after {
  box-sizing: border-box;
}

.vendas-page {
  padding: 20px 40px;
  background-color: #f9f2ec;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, sans-serif;
}

@media (max-width: 768px) {
  .vendas-page {
    padding: 15px 20px;
  }
}

@media (max-width: 480px) {
  .vendas-page {
    padding: 10px 12px;
  }
}

/* Barra superior com data */
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

/* Banner de feedback */
.feedback-banner {
  position: fixed;
  top: 25px;
  right: 25px;
  padding: 15px 25px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
  font-size: 14px;
  z-index: 9999;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  max-width: calc(100% - 40px);
  word-break: break-word;
}

@media (max-width: 768px) {
  .feedback-banner {
    left: 20px;
    right: 20px;
    top: 15px;
    width: auto;
    max-width: none;
  }
}

.feedback-banner.sucesso {
  background-color: #eafbee;
  color: #0b9e15;
  border: 1px solid #b7f0c1;
}

.feedback-banner.erro {
  background-color: #fef2f2;
  color: #b91c1c;
  border: 1px solid #fecaca;
}

.feedback-banner .icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

/* Header da página */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 30px;
  gap: 20px;
  flex-wrap: wrap;
}

@media (max-width: 600px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
}

.title-section {
  flex: 1;
}

.page-title {
  font-family: "Anton SC", sans-serif;
  font-size: 32px;
  color: #1e293b;
  margin: 0;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  word-break: break-word;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 20px;
  }
}

.page-subtitle {
  color: #64748b;
  font-size: 15px;
  margin: 5px 0 0 0;
}

/* Botão "Registrar Venda" */
.btn-novo {
  background-color: #ff7322;
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
  white-space: nowrap;
}

@media (max-width: 600px) {
  .btn-novo {
    width: auto;
    /* tamanho natural, sem esticar */
    align-self: flex-start;
  }
}

/* Cards KPI */
.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.kpi-card {
  background: #ffffff;
  border: 1px solid #ffede3;
  border-radius: 12px;
  padding: 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-width: 0;
}

@media (max-width: 480px) {
  .kpi-card {
    padding: 15px;
  }
}

.kpi-info {
  display: flex;
  flex-grow: 1;
  flex-direction: column;
  gap: 5px;
}

.kpi-label {
  font-size: 14px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.kpi-value {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  word-break: break-word;
}

@media (max-width: 768px) {
  .kpi-value {
    font-size: 22px;
  }
}

.kpi-icon {
  width: 45px;
  height: 45px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.kpi-icon svg {
  width: 24px;
  height: 24px;
}

.icon-orange {
  background-color: #ff7322;
}

.icon-green {
  background-color: #0b9e15;
}

.icon-yellow {
  background-color: #eab308;
}

.icon-blue {
  background-color: #3b82f6;
}

/* Content card */
.content-card {
  background: #ffffff;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
  border: 1px solid #f0e6de;
}

@media (max-width: 480px) {
  .content-card {
    padding: 15px;
  }
}

/* Barra de filtros */
.filtros-bar {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  align-items: center;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .filtros-bar {
    flex-direction: column;
    align-items: stretch;
  }
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: #ffffff;
  border: 1px solid #ff7322;
  border-radius: 6px;
  padding: 10px 15px;
  flex: 1;
  max-width: 400px;
  transition: box-shadow 0.2s;
  min-width: 200px;
}

@media (max-width: 768px) {
  .search-bar {
    max-width: 100%;
  }
}

.search-bar:focus-within {
  box-shadow: 0 0 0 1px #ff7322;
}

.search-bar input {
  border: none;
  background: transparent;
  width: 100%;
  outline: none;
  font-size: 14px;
  color: #334155;
}

.search-icon {
  width: 20px;
  height: 20px;
  color: #ff7322;
  margin-right: 10px;
  flex-shrink: 0;
}

.filtro-proprietario-custom {
  position: relative;
  display: flex;
  align-items: center;
  border: 1px solid #ff7322;
  border-radius: 6px;
  background-color: #ffffff;
  height: 42px;
  min-width: 220px;
  transition: box-shadow 0.2s;
}

@media (max-width: 768px) {
  .filtro-proprietario-custom {
    min-width: 0;
    width: 100%;
  }
}

.filtro-proprietario-custom:focus-within {
  box-shadow: 0 0 0 1px #ff7322;
}

.icon-user {
  width: 18px;
  height: 18px;
  color: #ff7322;
  position: absolute;
  left: 12px;
  pointer-events: none;
}

.icon-seta {
  width: 16px;
  height: 16px;
  color: #ff7322;
  position: absolute;
  right: 12px;
  pointer-events: none;
}

.filtro-proprietario-custom select {
  width: 100%;
  height: 100%;
  padding: 0 35px 0 40px;
  border: none;
  background: transparent;
  color: #ff7322;
  font-weight: 500;
  font-size: 14px;
  appearance: none;
  cursor: pointer;
  outline: none;
}

.filtro-proprietario-custom select option {
  color: #334155;
  background: white;
}

/* Tabela */
.table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin: 0 -5px;
  padding: 0 5px;
}

.dados-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  color: #1e293b;
  min-width: 700px;
}

@media (max-width: 768px) {
  .dados-table {
    font-size: 13px;
  }
}

.dados-table th {
  text-align: left;
  padding: 15px 10px;
  color: #475569;
  font-weight: 600;
  border-bottom: 2px solid #f1f5f9;
  background-color: #ffffff;
  font-size: 13px;
  text-transform: uppercase;
  white-space: nowrap;
}

.dados-table td {
  padding: 15px 10px;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
  white-space: nowrap;
}

.row-justificativa td {
  white-space: normal;
}

.tabela-vazia {
  text-align: center !important;
  color: #94a3b8;
  padding: 40px !important;
  font-style: italic;
}

.destaque-texto {
  font-family: "Anton SC", sans-serif;
  font-size: 18px;
  color: #1e293b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.td-valor {
  font-weight: 700;
  color: #0b9e15;
  font-size: 16px;
}

.badge-leilao-tag {
  background-color: #fffaf7;
  color: #ea580c;
  border: 1px solid #ffede3;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
  white-space: nowrap;
}

.badge-direta {
  background-color: #f1f5f9;
  color: #475569;
  border: 1px solid #cbd5e1;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
}

.text-justificativa {
  font-size: 13px;
  color: #b91c1c;
  background-color: #fef2f2;
  padding: 6px 12px;
  border-radius: 6px;
  margin-bottom: 10px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border-left: 3px solid #ef4444;
  word-break: break-word;
}

.icon-sm {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.acoes {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn-acao {
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-acao.edit {
  color: #ff7322;
}

.btn-acao.delete {
  color: #ef4444;
}

.btn-acao:hover {
  background-color: #f8fafc;
}

.btn-acao svg {
  width: 18px;
  height: 18px;
}

/* Formulários */
.header-form {
  justify-content: flex-start;
  gap: 20px;
}

.btn-voltar {
  background: none;
  border: none;
  color: #ff7322;
  cursor: pointer;
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.btn-voltar svg {
  width: 24px;
  height: 24px;
}

.form-card {
  border: 1px solid #ff7322;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px 40px;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
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

.input-group input,
.select-wrapper select {
  width: 100%;
  padding: 12px 0;
  border: none;
  border-bottom: 1px solid transparent;
  background-color: transparent;
  font-size: 14px;
  color: #ff7322;
  outline: none;
}

.input-group input:focus,
.select-wrapper select:focus {
  border-bottom: 1px solid #ff7322;
}

.select-wrapper {
  position: relative;
}

.select-wrapper select {
  appearance: none;
  cursor: pointer;
  color: #ffb68c;
  padding-right: 20px;
}

.select-wrapper select:focus,
.select-wrapper select:not(:invalid) {
  color: #ff7322;
}

.select-wrapper::after {
  content: '▼';
  font-size: 10px;
  color: #ffb68c;
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
}

.full-width {
  grid-column: span 2;
}

@media (max-width: 768px) {
  .full-width {
    grid-column: span 1;
  }
}

.section-alert {
  background-color: #fff7ed;
  padding: 15px;
  border-radius: 6px;
  border: 1px dashed #ff7322;
}

.alert-label {
  color: #b45309 !important;
  font-weight: 700 !important;
}

.alerta-lista-vazia {
  font-size: 13px;
  color: #ea580c;
  font-style: italic;
  margin-top: 5px;
}

/* Abas */
.tabs-container {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.tab-btn {
  background: #ffffff;
  border: 1px solid #ffede3;
  color: #ff7322;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  flex: 1 0 auto;
  text-align: center;
}

@media (max-width: 480px) {
  .tab-btn {
    font-size: 13px;
    padding: 10px;
  }
}

.tab-btn.active {
  background: #ff7322;
  color: white;
  border-color: #ff7322;
}

/* Seção demonstrativo */
.section-demonstrativo {
  background-color: #fffaf7;
  border: 1px dashed #ff7322;
  padding: 20px;
  border-radius: 8px;
  margin-top: 10px;
}

.demonstrativo-title {
  font-size: 14px;
  font-weight: 700;
  color: #ff7322;
  text-transform: uppercase;
  margin: 0 0 15px 0;
  letter-spacing: 0.5px;
}

.demonstrativo-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.demonstrativo-row {
  display: grid;
  grid-template-columns: 2fr 3fr 1fr;
  align-items: center;
  font-size: 14px;
  padding-bottom: 8px;
  border-bottom: 1px solid #ffede3;
}

@media (max-width: 600px) {
  .demonstrativo-row {
    grid-template-columns: 1fr;
    gap: 5px;
    text-align: left;
  }
}

.owner-lbl {
  font-weight: 600;
  color: #1e293b;
}

.owner-calc {
  color: #64748b;
  text-align: right;
  padding-right: 15px;
}

.owner-total {
  font-weight: 700;
  color: #0b9e15;
  text-align: right;
}

@media (max-width: 600px) {

  .owner-calc,
  .owner-total {
    text-align: left;
    padding-right: 0;
  }
}

/* Ações do formulário */
.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 40px;
  flex-wrap: wrap;
}

.btn-salvar {
  background-color: #0b9e15;
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: opacity 0.2s;
  white-space: nowrap;
}

.btn-salvar:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-lote-color {
  background-color: #eab308;
}

.btn-cancelar {
  background-color: transparent;
  color: #ff7322;
  border: 1px solid #ffede3;
  padding: 12px 25px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
}

@media (max-width: 480px) {

  .btn-salvar,
  .btn-cancelar {
    width: auto;
    min-width: 120px;
  }
}
</style>