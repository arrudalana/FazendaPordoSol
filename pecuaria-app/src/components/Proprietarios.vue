<template>
  <div class="prop-page">
    <header class="top-bar">
      <p class="current-date">{{ dataFormatada }}</p>
    </header>

    <div v-if="mensagemFeedback" class="feedback-banner">
      <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
      {{ mensagemFeedback }}
    </div>

    <div v-if="mostrarModalDelete" class="modal-overlay">
      <div class="modal-content">
        <h2 class="modal-title">CONFIRMAR EXCLUSÃO</h2>
        <p class="modal-text">
          Tem certeza que deseja excluir o proprietário <strong>{{ donoParaExcluir?.nome }}</strong>? Esta ação não pode ser desfeita.
        </p>
        <div class="modal-actions">
          <button class="btn-modal-cancelar" @click="fecharModalDelete">Cancelar</button>
          <button class="btn-modal-excluir" @click="confirmarExclusao">Excluir</button>
        </div>
      </div>
    </div>

    <div v-if="telaAtual === 'lista'">
      <div class="page-header">
        <div class="title-section">
          <h1 class="page-title">PROPRIETÁRIOS</h1>
          <p class="page-subtitle">Gerencie os proprietários e suas informações</p>
        </div>
        <button class="btn-novo" @click="abrirFormulario()">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
          Novo Proprietário
        </button>
      </div>

      <div class="content-card">
        <div class="search-bar">
          <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
          <input type="text" v-model="termoBusca" placeholder="Buscar por nome ou usuário..." />
        </div>

        <div class="cards-grid">
          <div v-if="proprietariosFiltrados.length === 0" class="tabela-vazia">
            Nenhum proprietário encontrado.
          </div>
          
          <div v-for="prop in proprietariosFiltrados" :key="prop.id_dono" class="prop-card">
            <div class="card-header">
              <h3 class="card-name">{{ prop.nome }}</h3>
              <span class="badge-perfil">{{ prop.perfil }}</span>
            </div>
            
            <p class="card-sub">{{ prop.status_dono === 'A' ? 'Status: Ativo' : 'Status: Inativo' }}</p>
            
            <div class="card-info">
              <p><svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg> Usuário: {{ prop.usuario }}</p>
              <p><svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg> {{ prop.telefone }}</p>
              <p><svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg> {{ prop.descricao_marca }}</p>
            </div>

            <div class="card-footer">
              <button class="btn-editar-outline" @click="editarProprietario(prop)">
                <svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                Editar
              </button>
              
              <button v-if="perfilUsuario === 'Admin'" class="btn-excluir-icon" title="Excluir" @click="prepararExclusao(prop)">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
              </button>
            </div>
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
          <h1 class="page-title">{{ editandoId ? 'EDITAR PROPRIETÁRIO' : 'NOVO PROPRIETÁRIO' }}</h1>
        </div>
      </div>

      <div class="content-card form-card"> 
        <form @submit.prevent="salvarProprietario" class="form-grid"> // Formulário para criar ou editar proprietário
          <div class="input-group">
            <label>Nome Completo</label>
            <input type="text" v-model="form.nome" required placeholder="Ex: Deivid Apoitia">
          </div>
          
          <div class="input-group">
            <label>Usuário de Acesso</label>
            <input type="text" v-model="form.usuario" required placeholder="Ex: deivid.ae">
          </div>

          <div class="input-group">
            <label>Senha ({{ editandoId ? 'Deixe em branco para manter' : 'Obrigatória' }})</label>
            <input type="password" v-model="form.senha" :required="!editandoId">
          </div>

          <div class="input-group">
            <label>Telefone</label>
            <input type="text" v-model="form.telefone" placeholder="(65) 99999-9999">
          </div>

          <div class="input-group">
            <label>Perfil de Acesso</label>
            <div class="select-wrapper">
              <select v-model="form.perfil" required>
                <option value="Admin">Administrador (Admin)</option>
                <option value="Dono">Comum (Dono)</option>
              </select>
            </div>
          </div>

          <div class="input-group">
            <label>Status</label>
            <div class="select-wrapper">
              <select v-model="form.status_dono" required>
                <option value="A">Ativo</option>
                <option value="I">Inativo</option>
              </select>
            </div>
          </div>

          <div class="input-group full-width">
            <label>Descrição da Fazenda/Marca</label>
            <input type="text" v-model="form.descricao_marca" placeholder="Ex: Fazenda Santa Rita, KM 12">
          </div>

          <div class="form-actions full-width">
            <button type="submit" class="btn-salvar">Salvar Proprietário</button>
            <button type="button" class="btn-cancelar" @click="voltarParaLista">Cancelar</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';

// Para checar se é Admin ou Dono
const props = defineProps({
  perfilUsuario: { type: String, default: 'Dono' }
});

const telaAtual = ref('lista'); 
const mensagemFeedback = ref(''); 
const editandoId = ref(null);
const mostrarModalDelete = ref(false);
const donoParaExcluir = ref(null);

const listaProprietarios = ref([]);
const termoBusca = ref('');

// Configuração de Data da Tela
const dataAtual = new Date();
const opcoesData = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
const dataFormatada = ref(dataAtual.toLocaleDateString('pt-BR', opcoesData));

const form = reactive({
  nome: '', usuario: '', senha: '', telefone: '', perfil: 'Dono', status_dono: 'A', descricao_marca: '', cor_brinco: ''
});

// Busca na API
const carregarProprietarios = async () => {
  try {
    const resposta = await fetch('http://127.0.0.1:8000/api/proprietarios/');
    listaProprietarios.value = await resposta.json();
  } catch (error) {
    mostrarMensagem('Erro ao carregar os dados.');
  }
};

onMounted(carregarProprietarios);

// Filtro da barra de pesquisa
const proprietariosFiltrados = computed(() => {
  const termo = termoBusca.value.toLowerCase();
  return listaProprietarios.value.filter(p => 
    p.nome.toLowerCase().includes(termo) || 
    p.usuario.toLowerCase().includes(termo)
  );
});

// Ações de Tela
const mostrarMensagem = (texto) => {
  mensagemFeedback.value = texto;
  setTimeout(() => { mensagemFeedback.value = ''; }, 3000);
};

const abrirFormulario = () => {
  form.nome = ''; form.usuario = ''; form.senha = ''; form.telefone = ''; 
  form.perfil = 'Dono'; form.status_dono = 'A'; form.descricao_marca = '';
  editandoId.value = null;
  telaAtual.value = 'formulario';
};

const editarProprietario = (prop) => {
  form.nome = prop.nome;
  form.usuario = prop.usuario;
  form.senha = ''; // Não trazemos a senha por segurança
  form.telefone = prop.telefone;
  form.perfil = prop.perfil;
  form.status_dono = prop.status_dono;
  form.descricao_marca = prop.descricao_marca;
  editandoId.value = prop.id_dono;
  telaAtual.value = 'formulario';
};

const voltarParaLista = () => {
  telaAtual.value = 'lista';
};

// CRUD - Salvar (Create / Update)
const salvarProprietario = async () => {
  const url = editandoId.value 
    ? `http://127.0.0.1:8000/api/proprietarios/${editandoId.value}/` 
    : 'http://127.0.0.1:8000/api/proprietarios/';
    
  const metodo = editandoId.value ? 'PUT' : 'POST';

  try {
    const resposta = await fetch(url, {
      method: metodo,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });
    
    if (resposta.ok) {
      mostrarMensagem(editandoId.value ? 'Atualizado com sucesso!' : 'Cadastrado com sucesso!');
      await carregarProprietarios();
      voltarParaLista();
    } else {
      mostrarMensagem('Erro ao salvar os dados.');
    }
  } catch (error) {
    mostrarMensagem('Erro de conexão com o servidor.');
  }
};

// CRUD - Excluir
const prepararExclusao = (prop) => {
  donoParaExcluir.value = prop; 
  mostrarModalDelete.value = true;        
};

const fecharModalDelete = () => {
  mostrarModalDelete.value = false;
  donoParaExcluir.value = null;
};

const confirmarExclusao = async () => {
  if (donoParaExcluir.value) {
    try {
      const resposta = await fetch(`http://127.0.0.1:8000/api/proprietarios/${donoParaExcluir.value.id_dono}/`, {
        method: 'DELETE'
      });
      if (resposta.ok) {
        mostrarMensagem('Proprietário removido com sucesso!');
        await carregarProprietarios();
      } else {
        mostrarMensagem('Erro ao tentar excluir.');
      }
    } catch (error) {
      mostrarMensagem('Erro de conexão com o servidor.');
    }
    fecharModalDelete();
  }
};
</script>

<style scoped>
/* CORES E FUNDO PADRÃO DO SISTEMA */
.prop-page { 
  padding: 20px 40px; 
  background-color: #f9f2ec; 
  min-height: 100vh; 
  font-family: 'Segoe UI', Tahoma, sans-serif; 
}

.top-bar { border-bottom: 1px solid #ebdcd1; padding-bottom: 10px; margin-bottom: 25px; }
.current-date { color: #8a7b72; font-size: 14px; margin: 0; text-transform: lowercase; }

.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 30px; }
.page-title { font-family: "Anton SC", sans-serif; font-size: 32px; color: #1e293b; margin: 0; letter-spacing: 0.5px; text-transform: uppercase; }
.page-subtitle { color: #64748b; font-size: 15px; margin: 5px 0 0 0; }

.btn-novo { background-color: #ff7322; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: background-color 0.2s; }
.btn-novo:hover { background-color: #e66014; }

.content-card { background: #ffffff; border-radius: 10px; padding: 30px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03); border: 1px solid #f0e6de; }
.search-bar { display: flex; align-items: center; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 15px; margin-bottom: 30px; max-width: 400px; }
.search-bar input { border: none; background: transparent; width: 100%; outline: none; font-size: 14px; color: #334155; }
.search-icon { width: 20px; height: 20px; color: #94a3b8; margin-right: 10px; }

/* ======== GRID DE CARDS ======== */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.prop-card {
  border: 1px solid #ffede3;
  border-radius: 8px;
  padding: 20px;
  background-color: #ffffff;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
}
.prop-card:hover {
  box-shadow: 0 6px 12px rgba(255, 115, 34, 0.08);
  transform: translateY(-2px);
}

.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 5px; }
.card-name { font-family: "Anton SC", sans-serif; font-size: 22px; color: #1e293b; margin: 0; text-transform: uppercase; }
.badge-perfil { background-color: #ffede3; color: #ff7322; padding: 4px 10px; border-radius: 15px; font-size: 12px; font-weight: bold; }

.card-sub { font-size: 13px; color: #94a3b8; margin: 0 0 20px 0; }

.card-info { flex-grow: 1; }
.card-info p { display: flex; align-items: center; gap: 10px; font-size: 14px; color: #475569; margin: 10px 0; }
.icon-sm { width: 18px; height: 18px; color: #64748b; }

.card-footer { display: flex; gap: 10px; margin-top: 25px; pt: 15px; border-top: 1px solid #f1f5f9; padding-top: 15px; }
.btn-editar-outline { flex-grow: 1; background: transparent; border: 1px solid #ffede3; color: #ff7322; padding: 8px; border-radius: 6px; font-weight: 600; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 5px; transition: 0.2s;}
.btn-editar-outline:hover { background-color: #fffaf7; border-color: #ffb68c; }
.btn-excluir-icon { background: transparent; border: 1px solid #fee2e2; color: #ef4444; width: 40px; border-radius: 6px; cursor: pointer; display: flex; justify-content: center; align-items: center; transition: 0.2s; }
.btn-excluir-icon:hover { background-color: #fef2f2; }
.btn-excluir-icon svg { width: 20px; height: 20px; }

.tabela-vazia { grid-column: 1 / -1; text-align: center; color: #94a3b8; padding: 40px; font-style: italic; }

/* ======== FORMULÁRIO (Igual a Animais) ======== */
.header-form { display: flex; align-items: center; justify-content: flex-start; gap: 20px; }
.btn-voltar { background: none; border: none; color: #ff7322; cursor: pointer; display: flex; align-items: center; padding: 5px; }
.btn-voltar svg { width: 26px; height: 26px; }
.form-card { border: 1px solid #ff7322; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px 40px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 13px; font-weight: 500; color: #ff7322; }
.input-group input, .select-wrapper select { width: 100%; padding: 10px 0; border: none; border-bottom: 1px solid transparent; background-color: transparent; font-size: 14px; color: #ff7322; outline: none; }
.input-group input:focus, .select-wrapper select:focus { border-bottom: 1px solid #ff7322; }
.input-group input::placeholder { color: #ffb68c; }
.select-wrapper { position: relative; }
.select-wrapper select { appearance: none; cursor: pointer; color: #ffb68c; }
.select-wrapper select:focus, .select-wrapper select:not(:invalid) { color: #ff7322; }
.select-wrapper::after { content: '▼'; font-size: 10px; color: #ffb68c; position: absolute; right: 5px; top: 50%; transform: translateY(-50%); pointer-events: none; }
.full-width { grid-column: span 2; }
.form-actions { display: flex; gap: 15px; margin-top: 20px; }
.btn-salvar { background-color: #0b9e15; color: white; border: none; padding: 12px 25px; border-radius: 6px; font-weight: 600; cursor: pointer; }
.btn-salvar:hover { background-color: #098011; }
.btn-cancelar { background-color: transparent; color: #ff7322; border: 1px solid #ffede3; padding: 12px 25px; border-radius: 6px; font-weight: 600; cursor: pointer; }
.btn-cancelar:hover { background-color: #fffaf7; }

/* ======== FEEDBACK E MODAIS ======== */
.feedback-banner { background-color: #eafbee; color: #0b9e15; border: 1px solid #b7f0c1; padding: 12px 20px; border-radius: 6px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; font-weight: 600; font-size: 14px; }
.feedback-banner .icon { width: 20px; height: 20px; }
.modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: rgba(0, 0, 0, 0.4); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-content { background-color: white; padding: 30px; border-radius: 12px; width: 100%; max-width: 450px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
.modal-title { font-family: "Anton SC", sans-serif; color: #ff7322; margin: 0 0 15px 0; font-size: 24px; text-transform: uppercase; }
.modal-text { color: #ffb68c; font-size: 15px; line-height: 1.5; margin-bottom: 25px; }
.modal-actions { display: flex; justify-content: flex-end; gap: 15px; }
.btn-modal-cancelar { background-color: white; color: #ff7322; border: 1px solid #ff7322; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer; }
.btn-modal-excluir { background-color: #e60000; color: white; border: none; padding: 10px 25px; border-radius: 6px; font-weight: 600; cursor: pointer; }
</style>