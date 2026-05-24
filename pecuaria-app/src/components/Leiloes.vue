<template>
  <div class="leiloes-page">
    <header class="top-bar">
      <p class="current-date">{{ dataFormatada }}</p>
    </header>

    <div v-if="mensagemFeedback" class="feedback-banner">
      <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
      {{ mensagemFeedback }}
    </div>

    <div v-if="telaAtual === 'lista'">
      <div class="page-header">
        <div class="title-section">
          <h1 class="page-title">LEILÕES</h1>
          <p class="page-subtitle">Gerencie os leilões e animais participantes</p>
        </div>
        <button class="btn-novo" @click="abrirFormulario()">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
          Novo Leilão
        </button>
      </div>

      <div class="cards-grid">
        <div v-if="listaLeiloes.length === 0" class="tabela-vazia">Nenhum leilão cadastrado.</div>
        
        <div 
          v-for="leilao in listaLeiloes" 
          :key="leilao.id_leilao" 
          :class="['leilao-card', leilao.status === 'Realizado' ? 'card-realizado' : 'card-agendado']"
        >
          <div class="card-header">
            <h3 class="card-name" :class="leilao.status === 'Realizado' ? 'text-green' : 'text-orange'">
              {{ leilao.nome_evento }}
            </h3>
            <span :class="leilao.status === 'Realizado' ? 'badge-realizado' : 'badge-agendado'">
              {{ leilao.status }}
            </span>
          </div>
          
          <div class="card-info">
            <p><svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg> {{ formatarDataBR(leilao.dt_leilao) }}</p>
            <p><svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg> {{ leilao.local || 'Local não informado' }}</p>
          </div>

          <div class="animais-vinculados">
            <p class="label-animais">Animais Participantes:</p>
            <div class="tags-container" v-if="leilao.animais.length > 0">
              <span class="animal-tag" v-for="animal in leilao.animais" :key="animal.id">{{ animal.nome }}</span>
            </div>
            <p v-else class="text-muted">Nenhum animal cadastrado</p>
          </div>

          <div class="card-footer">
            <button class="btn-editar-outline" @click="editarLeilao(leilao)">
              <svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
              Editar
            </button>
            <button class="btn-excluir-icon" @click="excluirLeilao(leilao.id_leilao)">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="telaAtual === 'formulario'">
      <div class="page-header header-form">
        <button class="btn-voltar" @click="voltarParaLista" title="Voltar">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
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
              <label class="checkbox-item" v-for="animal in listaAnimais" :key="animal.id">
                <input type="checkbox" :value="animal.id" v-model="form.animais_ids">
                <span class="checkbox-text">{{ animal.nome }} ({{ animal.raca }})</span>
              </label>
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
import { ref, reactive, onMounted } from 'vue';

const telaAtual = ref('lista'); 
const mensagemFeedback = ref(''); 
const editandoId = ref(null);

const listaLeiloes = ref([]);
const listaAnimais = ref([]); // Para preencher os checkboxes

// Configuração de Data da Tela (Cabeçalho)
const dataAtual = new Date();
const dataFormatada = ref(dataAtual.toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }));

const form = reactive({
  nome_evento: '', dt_leilao: '', local: '', custo_fixo: 0, animais_ids: []
});

const carregarDados = async () => {
  try {
    const resLeiloes = await fetch('http://127.0.0.1:8000/api/leiloes/');
    listaLeiloes.value = await resLeiloes.json();
    
    const resAnimais = await fetch('http://127.0.0.1:8000/api/animais/');
    listaAnimais.value = await resAnimais.json();
  } catch (error) {
    console.error("Erro ao carregar dados:", error);
  }
};

onMounted(carregarDados);

const formatarDataBR = (dataString) => {
  if (!dataString) return '';
  const [ano, mes, dia] = dataString.split('-');
  return `${dia}/${mes}/${ano}`;
};

const mostrarMensagem = (texto) => {
  mensagemFeedback.value = texto;
  setTimeout(() => { mensagemFeedback.value = ''; }, 3000);
};

const abrirFormulario = () => {
  form.nome_evento = ''; form.dt_leilao = ''; form.local = ''; form.custo_fixo = 0; form.animais_ids = [];
  editandoId.value = null;
  telaAtual.value = 'formulario';
};

const editarLeilao = (leilao) => {
  form.nome_evento = leilao.nome_evento;
  form.dt_leilao = leilao.dt_leilao;
  form.local = leilao.local;
  form.custo_fixo = leilao.custo_fixo;
  form.animais_ids = leilao.animais.map(a => a.id); // Extrai apenas os IDs para marcar os checkboxes
  editandoId.value = leilao.id_leilao;
  telaAtual.value = 'formulario';
};

const voltarParaLista = () => { telaAtual.value = 'lista'; };

const salvarLeilao = async () => {
  const url = editandoId.value ? `http://127.0.0.1:8000/api/leiloes/${editandoId.value}/` : 'http://127.0.0.1:8000/api/leiloes/';
  const metodo = editandoId.value ? 'PUT' : 'POST';

  try {
    const resposta = await fetch(url, {
      method: metodo,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });
    
    if (resposta.ok) {
      mostrarMensagem(editandoId.value ? 'Atualizado com sucesso!' : 'Cadastrado com sucesso!');
      await carregarDados();
      voltarParaLista();
    }
  } catch (error) { console.error(error); }
};

const excluirLeilao = async (id) => {
  if(confirm("Tem certeza que deseja excluir este leilão?")) {
    await fetch(`http://127.0.0.1:8000/api/leiloes/${id}/`, { method: 'DELETE' });
    mostrarMensagem('Leilão removido!');
    await carregarDados();
  }
};
</script>

<style scoped>
/* CORES E FUNDO PADRÃO */
.leiloes-page { padding: 20px 40px; background-color: #f9f2ec; min-height: 100vh; font-family: 'Segoe UI', Tahoma, sans-serif; }
.top-bar { border-bottom: 1px solid #ebdcd1; padding-bottom: 10px; margin-bottom: 25px; }
.current-date { color: #8a7b72; font-size: 14px; margin: 0; text-transform: lowercase; }

.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 30px; }
.page-title { font-family: "Anton SC", sans-serif; font-size: 32px; color: #1e293b; margin: 0; letter-spacing: 0.5px; text-transform: uppercase; }
.page-subtitle { color: #64748b; font-size: 15px; margin: 5px 0 0 0; }
.btn-novo { background-color: #0b9e15; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: 0.2s; }
.btn-novo:hover { background-color: #098011; }

/* ======== LÓGICA DE CORES DOS CARDS ======== */
.cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 20px; }
.leilao-card { border-radius: 10px; padding: 25px; display: flex; flex-direction: column; transition: transform 0.2s; }
.leilao-card:hover { transform: translateY(-3px); }

/* Card Verde - Realizado */
.card-realizado { background-color: #ffffff; border: 1px solid #d1fae5; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.05); }
.badge-realizado { background-color: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.text-green { color: #ea580c; } /* Mantém título laranja mesmo no verde para harmonia */

/* Card Amarelo - Agendado */
.card-agendado { background-color: #fefce8; border: 1px solid #fef08a; box-shadow: 0 4px 15px rgba(234, 179, 8, 0.05); }
.badge-agendado { background-color: #fef3c7; color: #d97706; border: 1px solid #fde68a; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.text-orange { color: #ea580c; }

/* Estrutura Interna do Card */
.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px; }
.card-name { font-family: "Anton SC", sans-serif; font-size: 24px; margin: 0; text-transform: uppercase; }
.card-info { margin-bottom: 20px; }
.card-info p { display: flex; align-items: center; gap: 10px; font-size: 14px; color: #475569; margin: 10px 0; }
.icon-sm { width: 18px; height: 18px; color: #64748b; }

.animais-vinculados { flex-grow: 1; border-top: 1px solid rgba(0,0,0,0.05); padding-top: 15px; }
.label-animais { font-size: 13px; color: #64748b; margin: 0 0 10px 0; }
.tags-container { display: flex; flex-wrap: wrap; gap: 8px; }
.animal-tag { background: white; border: 1px solid #ffede3; color: #ff7322; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 500; }
.text-muted { font-size: 13px; color: #94a3b8; font-style: italic; margin: 0; }

.card-footer { display: flex; gap: 10px; margin-top: 20px; }
.btn-editar-outline { flex-grow: 1; background: white; border: 1px solid #ffede3; color: #ff7322; padding: 8px; border-radius: 6px; font-weight: 600; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 5px; transition: 0.2s;}
.btn-editar-outline:hover { background-color: #fffaf7; }
.btn-excluir-icon { background: white; border: 1px solid #fee2e2; color: #ef4444; width: 40px; border-radius: 6px; cursor: pointer; display: flex; justify-content: center; align-items: center; transition: 0.2s; }
.btn-excluir-icon:hover { background-color: #fef2f2; }
.btn-excluir-icon svg { width: 20px; height: 20px; }
.tabela-vazia { grid-column: 1 / -1; text-align: center; color: #94a3b8; padding: 40px; font-style: italic; }

/* ======== FORMULÁRIO DE LEILÕES ======== */
.header-form { display: flex; align-items: center; justify-content: flex-start; gap: 20px; }
.btn-voltar { background: none; border: none; color: #ff7322; cursor: pointer; display: flex; padding: 5px; }
.btn-voltar svg { width: 26px; height: 26px; }
.content-card { background: #ffffff; border-radius: 10px; padding: 30px; border: 1px solid #ff7322; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px 40px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 13px; font-weight: 500; color: #ff7322; }
.input-group input { width: 100%; padding: 10px 0; border: none; border-bottom: 1px solid transparent; background-color: transparent; font-size: 14px; color: #ff7322; outline: none; }
.input-group input:focus { border-bottom: 1px solid #ff7322; }
.full-width { grid-column: span 2; }
.form-actions { display: flex; gap: 15px; margin-top: 20px; }
.btn-salvar { background-color: #0b9e15; color: white; border: none; padding: 12px 25px; border-radius: 6px; font-weight: 600; cursor: pointer; }
.btn-cancelar { background-color: transparent; color: #ff7322; border: 1px solid #ffede3; padding: 12px 25px; border-radius: 6px; font-weight: 600; cursor: pointer; }

/* Estilo dos Checkboxes de Animais */
.checkbox-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; background: #fffaf7; padding: 15px; border-radius: 6px; border: 1px solid #ffede3;}
.checkbox-item { display: flex; align-items: center; gap: 10px; cursor: pointer; }
.checkbox-item input[type="checkbox"] { width: auto; accent-color: #ff7322; transform: scale(1.2); }
.checkbox-text { font-size: 14px; color: #475569; }

.feedback-banner { background-color: #eafbee; color: #0b9e15; border: 1px solid #b7f0c1; padding: 12px 20px; border-radius: 6px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; font-weight: 600; font-size: 14px; }
</style>