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
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
          Registrar Venda
        </button>
      </div>

      <div class="dashboard-cards">
        <div class="kpi-card">
          <div class="kpi-info">
            <span class="kpi-label">Total de Vendas</span>
            <span class="kpi-value">{{ totalVendas }}</span>
          </div>
          <div class="kpi-icon icon-orange">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-info">
            <span class="kpi-label">Valor Total</span>
            <span class="kpi-value">{{ formatarMoeda(valorTotal) }}</span>
          </div>
          <div class="kpi-icon icon-green">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-info">
            <span class="kpi-label">Ticket Médio</span>
            <span class="kpi-value">{{ formatarMoeda(ticketMedio) }}</span>
          </div>
          <div class="kpi-icon icon-yellow">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path></svg>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-info">
            <span class="kpi-label">Custo Fixo (Leilões)</span>
            <span class="kpi-value">{{ formatarMoeda(custoFixoTotal) }}</span>
          </div>
          <div class="kpi-icon icon-blue">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
          </div>
        </div>
      </div>

      <h3 class="section-title">HISTÓRICO DE VENDAS</h3>
      
      <div class="vendas-list">
        <div v-if="listaVendas.length === 0" class="card-vazio">Nenhuma venda registrada no sistema.</div>
        <div v-for="venda in listaVendas" :key="venda.id_venda" class="venda-card">
          <div class="venda-info-principal">
            <div class="venda-cabecalho">
              <h2 class="animal-nome">Brinco: {{ venda.animal_nome }}</h2>
              <span class="badge-vendido">Vendido</span>
              <span class="badge-leilao-tag">{{ venda.leilao_nome }}</span>
            </div>
            <div class="venda-detalhes">
              <span class="detalhe-item">
                <svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                {{ formatarDataBR(venda.dt_venda) }}
              </span>
              <span class="detalhe-item"><strong>Pagamento:</strong> {{ venda.tipo_pagamento }}</span>
              <span class="detalhe-item"><strong>De:</strong> {{ venda.vendedor }} — <strong>Para:</strong> {{ venda.comprador }}</span>
            </div>
            <p v-if="venda.justificativa_alteracao" class="text-justificativa">
              ⚠️ <strong>Histórico de Alteração:</strong> "{{ venda.justificativa_alteracao }}"
            </p>
          </div>
          
          <div class="venda-card-direita">
            <div class="venda-valor">{{ formatarMoeda(venda.valor) }}</div>
            <div class="venda-acoes">
              <button class="btn-acao-venda edit" title="Editar Informações" @click="prepararEdicao(venda)">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="18" height="18"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
              </button>
              <button v-if="perfilUsuario === 'Administrador'" class="btn-acao-venda delete" title="Excluir Venda" @click="removerVenda(venda.id_venda)">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="18" height="18"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TELA DE FORMULÁRIO -->
    <div v-else-if="telaAtual === 'formulario'">
      <div class="page-header header-form">
        <button class="btn-voltar" @click="voltarParaLista" title="Voltar">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
        </button>
        <div class="title-section">
          <h1 class="page-title">{{ editandoId ? 'ALTERAR DADOS DA VENDA' : 'REGISTRAR NOVO FATURAMENTO' }}</h1>
        </div>
      </div>

      <div v-if="!editandoId" class="tabs-container">
        <button :class="['tab-btn', { active: modoLancamento === 'direta' }]" @click="modoLancamento = 'direta'">Venda Individual Direta</button>
        <button :class="['tab-btn', { active: modoLancamento === 'leilao' }]" @click="modoLancamento = 'leilao'">Faturamento em Lote (Por Leilão)</button>
      </div>

      <div class="content-card form-card">
        <!-- FORMULÁRIO VENDA DIRETA -->
        <form v-if="modoLancamento === 'direta'" @submit.prevent="salvarVenda" class="form-grid">
          <div class="input-group full-width">
            <label>Selecione o Animal (Número do Brinco)</label>
            <div class="select-wrapper">
              <select v-model="formVenda.id_animal" required>
                <option value="" disabled>Escolha o brinco do animal...</option>
                <option v-for="animal in listaAnimais" :key="animal.id" :value="animal.id">
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
            <label>Vendedor</label>
            <input type="text" v-model="formVenda.vendedor" required>
          </div>

          <div class="input-group">
            <label>Comprador</label>
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
                <!-- Usa a lista completa aqui pois é opcional vincular vendas avulsas a um leilão -->
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

        <!-- FORMULÁRIO FATURAMENTO EM LOTE -->
        <form v-else @submit.prevent="salvarVendaLote" class="form-grid">
          <div class="input-group full-width">
            <label>Selecione o Leilão Realizado</label>
            <div class="select-wrapper">
              <select v-model="formLote.id_leilao" required>
                <option value="" disabled>Escolha o leilão para extrair os animais...</option>
                <!-- REQUISITO APLICADO: Filtra apenas leilões já finalizados e sem faturamento -->
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

          <div class="input-group">
            <label>Vendedor do Leilão</label>
            <input type="text" v-model="formLote.vendedor" required>
          </div>

          <div class="input-group">
            <label>Arrematante / Comprador</label>
            <input type="text" v-model="formLote.comprador" required>
          </div>

          <div class="input-group full-width">
            <label>Forma de Pagamento do Arremate</label>
            <div class="select-wrapper">
              <select v-model="formLote.tipo_pagamento" required>
                <option value="Pix">Pix</option>
                <option value="Boleto Bancário">Boleto Bancário</option>
                <option value="Dinheiro à Vista">Dinheiro à Vista</option>
              </select>
            </div>
          </div>

          <div class="form-actions full-width">
            <!-- Desativa o botão se não houver leilões disponíveis -->
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

const custoFixoTotal = computed(() => {
  return listaLeiloes.value.reduce((acc, leilao) => acc + (Number(leilao.custo_fixo) || 0), 0);
});

const props = defineProps({
  perfilUsuario: { type: String, default: 'Dono' }
});

const telaAtual = ref('lista');
const modoLancamento = ref('direta');
const editandoId = ref(null);

const mensagemFeedback = ref('');
const tipoFeedback = ref('sucesso'); 

const listaVendas = ref([]);
const listaAnimais = ref([]);
const listaLeiloes = ref([]);

// REQUISITO APLICADO: Filtra leilões NÃO faturados que já foram REALIZADOS (Data anterior a hoje)
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
      // Formata os dados de data vindo do backend
      const [ano, mes, dia] = leilao.dt_leilao.split('-');
      const dataLeilao = new Date(ano, mes - 1, dia);
      dataLeilao.setHours(0, 0, 0, 0);
      
      jaAconteceu = dataLeilao < hoje;
    }

    // Exibe apenas se atende ambas as condições
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
  } catch (error) { console.error(error); }
};

onMounted(carregarDadosDoSistema);

const abrirFormulario = () => {
  editandoId.value = null;
  modoLancamento.value = 'direta';
  formVenda.id_animal = ''; formVenda.valor = ''; formVenda.vendedor = ''; formVenda.comprador = ''; formVenda.id_leilao = null; formVenda.justificativa_alteracao = '';
  formVenda.data_venda = new Date().toISOString().split('T')[0];
  
  formLote.id_leilao = ''; formLote.valor_padrao = ''; formLote.vendedor = ''; formLote.comprador = '';
  telaAtual.value = 'formulario';
};

const prepararEdicao = (venda) => {
  editandoId.value = venda.id_venda;
  modoLancamento.value = 'direta';
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
    const resposta = await fetch(url, {
      method: metodo,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formVenda)
    });
    if (resposta.ok) {
      mostrarMensagem(editandoId.value ? 'Dados da venda alterados!' : 'Venda gravada com sucesso!', 'sucesso');
      await carregarDadosDoSistema();
      voltarParaLista();
    } else {
      const falha = await resposta.json();
      mostrarMensagem(falha.erro || 'Ocorreu um erro ao salvar.', 'erro');
    }
  } catch (error) { mostrarMensagem('Erro de conexão com o servidor.', 'erro'); }
};

const salvarVendaLote = async () => {
  try {
    const resposta = await fetch('http://127.0.0.1:8000/api/vendas/importar-leilao/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formLote)
    });
    
    const resultado = await resposta.json();
    
    if (resposta.ok && resultado.sucesso !== false) {
      mostrarMensagem('Lote de vendas gravado com sucesso!', 'sucesso');
      await carregarDadosDoSistema();
      voltarParaLista();
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
        mostrarMensagem('Venda deletada permanentemente!', 'sucesso');
        await carregarDadosDoSistema();
      } else {
        const falha = await resposta.json();
        mostrarMensagem(falha.erro, 'erro');
      }
    } catch (error) { mostrarMensagem('Erro na conexão.', 'erro'); }
  }
};

const formatarDataBR = (dataString) => {
  if (!dataString) return '';
  const [ano, mes, dia] = dataString.split('-');
  return `${dia}/${mes}/${ano}`;
};

const formatarMoeda = (valor) => {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);
};

const totalVendas = computed(() => listaVendas.value.length);
const valorTotal = computed(() => listaVendas.value.reduce((acc, v) => acc + Number(v.valor), 0));
const ticketMedio = computed(() => totalVendas.value === 0 ? 0 : valorTotal.value / totalVendas.value);
</script>

<style scoped>
.vendas-page { padding: 20px 40px; background-color: #f9f2ec; min-height: 100vh; font-family: 'Segoe UI', Tahoma, sans-serif; }
.top-bar { border-bottom: 1px solid #ebdcd1; padding-bottom: 10px; margin-bottom: 25px; }
.current-date { color: #8a7b72; font-size: 14px; margin: 0; text-transform: lowercase; }

/* ESTILOS DO BANNER DINÂMICO */
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
  box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
}
.feedback-banner.sucesso { background-color: #eafbee; color: #0b9e15; border: 1px solid #b7f0c1; }
.feedback-banner.erro { background-color: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.feedback-banner .icon { width: 20px; height: 20px; }

.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 30px; }
.page-title { font-family: "Anton SC", sans-serif; font-size: 32px; color: #1e293b; margin: 0; letter-spacing: 0.5px; text-transform: uppercase; }
.page-subtitle { color: #64748b; font-size: 15px; margin: 5px 0 0 0; }
.btn-novo { background-color: #ff7322; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 8px; }

.dashboard-cards { display: flex; gap: 20px; margin-bottom: 40px; }
.kpi-card { flex: 1; background: #ffffff; border: 1px solid #ffede3; border-radius: 12px; padding: 25px; display: flex; justify-content: space-between; align-items: center; }
.kpi-info { display: flex; flex-direction: column; gap: 5px; }
.kpi-label { font-size: 14px; color: #94a3b8; font-weight: 500; }
.kpi-value { font-size: 32px; font-weight: 700; color: #1e293b; }
.kpi-icon { width: 45px; height: 45px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; }
.kpi-icon svg { width: 24px; height: 24px; }
.icon-orange { background-color: #ff7322; }
.icon-green { background-color: #0b9e15; }
.icon-yellow { background-color: #eab308; }
.icon-blue { background-color: #3b82f6; }

.tabs-container { display: flex; gap: 10px; margin-bottom: 20px; }
.tab-btn { background: #ffffff; border: 1px solid #ffede3; color: #ff7322; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer; }
.tab-btn.active { background: #ff7322; color: white; border-color: #ff7322; }

.section-title { font-family: "Anton SC", sans-serif; color: #ff7322; font-size: 20px; margin-bottom: 20px; text-transform: uppercase; }
.vendas-list { display: flex; flex-direction: column; gap: 15px; }
.venda-card { background: #ffffff; border: 1px solid #f0e6de; border-radius: 10px; padding: 20px 25px; display: flex; justify-content: space-between; align-items: center; }
.venda-info-principal { display: flex; flex-direction: column; gap: 10px; flex-grow: 1; }
.venda-cabecalho { display: flex; align-items: center; gap: 15px; }
.animal-nome { font-family: "Anton SC", sans-serif; font-size: 22px; color: #1e293b; margin: 0; text-transform: uppercase; }
.badge-vendido { background-color: #dcfce7; color: #166534; border: 1px solid #bbf7d0; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.badge-leilao-tag { background-color: #fffaf7; color: #ea580c; border: 1px solid #ffede3; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.venda-detalhes { display: flex; gap: 20px; color: #64748b; font-size: 14px; align-items: center; }
.text-justificativa { font-size: 13px; color: #b91c1c; background-color: #fef2f2; padding: 6px 12px; border-radius: 6px; margin: 5px 0 0 0; display: inline-block; border-left: 3px solid #ef4444; }

.venda-card-direita { display: flex; flex-direction: column; align-items: flex-end; gap: 10px; }
.venda-valor { font-size: 24px; font-weight: 700; color: #0b9e15; }
.venda-acoes { display: flex; gap: 8px; }
.btn-acao-venda { background: none; border: 1px solid #ffede3; padding: 6px; border-radius: 6px; cursor: pointer; display: flex; align-items: center; justify-content: center; color: #ff7322; }
.btn-acao-venda.delete { border-color: #fee2e2; color: #ef4444; }
.btn-acao-venda.delete:hover { background-color: #fef2f2; }
.btn-acao-venda.edit:hover { background-color: #fffaf7; }

.card-vazio { text-align: center; color: #94a3b8; padding: 40px; background: white; border-radius: 10px; border: 1px solid #f0e6de; font-style: italic; }

.header-form { justify-content: flex-start; gap: 20px; }
.btn-voltar { background: none; border: none; color: #ff7322; cursor: pointer; display: flex; align-items: center; }
.btn-voltar svg { width: 24px; height: 24px; }
.content-card { background: #ffffff; border-radius: 10px; padding: 30px; }
.form-card { border: 1px solid #ff7322; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 25px 40px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 13px; font-weight: 500; color: #ff7322; }
.input-group input, .select-wrapper select { width: 100%; padding: 12px 0; border: none; border-bottom: 1px solid transparent; background-color: transparent; font-size: 14px; color: #ff7322; outline: none; }
.input-group input:focus, .select-wrapper select:focus { border-bottom: 1px solid #ff7322; }
.select-wrapper { position: relative; }
.select-wrapper select { appearance: none; cursor: pointer; color: #ffb68c; }
.select-wrapper select:focus, .select-wrapper select:not(:invalid) { color: #ff7322; }
.select-wrapper::after { content: '▼'; font-size: 10px; color: #ffb68c; position: absolute; right: 5px; top: 50%; transform: translateY(-50%); pointer-events: none; }
.full-width { grid-column: span 2; }

.section-alert { background-color: #fff7ed; padding: 15px; border-radius: 6px; border: 1px dashed #ff7322; }
.alert-label { color: #b45309 !important; font-weight: 700 !important; }

.alerta-lista-vazia { font-size: 13px; color: #ea580c; font-style: italic; margin-top: 5px; }

.form-actions { display: flex; gap: 15px; margin-top: 40px; }
.btn-salvar { background-color: #0b9e15; color: white; border: none; padding: 12px 25px; border-radius: 6px; font-weight: 600; font-size: 14px; cursor: pointer; transition: opacity 0.2s;}
.btn-salvar:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-lote-color { background-color: #eab308; }
.btn-cancelar { background-color: transparent; color: #ff7322; border: 1px solid #ffede3; padding: 12px 25px; border-radius: 6px; font-weight: 600; font-size: 14px; cursor: pointer; }
</style>