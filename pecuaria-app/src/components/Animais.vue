<template>
  <div class="animais-page">
    <header class="top-bar">
      <p class="current-date">{{ dataFormatada }}</p>
    </header>

    <div v-if="mensagemFeedback" class="feedback-banner">
      <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg>
      {{ mensagemFeedback }}
    </div>

    <div v-if="mostrarModal" class="modal-overlay">
      <div class="modal-content">
        <h2 class="modal-title">CONFIRMAR EXCLUSÃO</h2>
        <p class="modal-text">
          Tem certeza que deseja excluir o animal? Esta ação não pode ser desfeita.
        </p>
        <div class="modal-actions">
          <button class="btn-modal-excluir" @click="confirmarExclusao">Sim</button>
          <button class="btn-modal-cancelar" @click="fecharModal">Não</button>
        </div>
      </div>
    </div>

    <div v-if="telaAtual === 'lista'">
      <div class="page-header">
        <div class="title-section">
          <h1 class="page-title">ANIMAIS</h1>
          <p class="page-subtitle">Gerencie o rebanho e informações dos animais</p>
        </div>
        <button class="btn-novo" @click="abrirFormulario()">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          Novo Animal
        </button>
      </div>

      <div class="content-card">
        <!-- ============================================================ -->
        <!-- CONTÊINER ÚNICO: FILTRO E BUSCA LADO A LADO                   -->
        <!-- ============================================================ -->
        <div class="filtros-e-busca-container">

          <!-- DROPDOWN DE PROPRIETÁRIO -->
          <div class="custom-select-wrapper">
            <div class="custom-select-trigger">
              <div class="left-content">
                <svg class="icon-user" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z">
                  </path>
                </svg>
                <span>Proprietário</span>
              </div>
              <svg class="icon-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.5 8.25l-7.5 7.5-7.5-7.5">
                </path>
              </svg>
            </div>

            <select v-model="proprietarioSelecionado" class="hidden-select">
              <option value="">Proprietário</option>
              <option v-for="dono in proprietariosOrdenados" :key="dono.id_dono" :value="dono.id_dono">
                {{ dono.nome }}
              </option>
            </select>
          </div>

          <!-- CAMPO DE PESQUISA -->
          <div class="search-bar-container">
            <div class="search-bar">
              <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
              <input type="text" v-model="termoBusca" placeholder="Buscar por brinco, raça..." />
            </div>
          </div>

        </div>
        <!-- FIM DO CONTÊINER ÚNICO DE FILTRO E BUSCA -->

        <div class="table-container">
          <table class="animais-table">
            <thead>
              <tr>
                <th>Proprietário</th>
                <th>Brinco/Nome</th>
                <th>Raça</th>
                <th>Leilão</th>
                <th>Peso</th>
                <th>Status</th>
                <th>Causa Morte</th>
                <th class="text-right">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="animaisFiltrados.length === 0">
                <td colspan="8" class="tabela-vazia">Nenhum animal encontrado.</td>
              </tr>
              <tr v-for="animal in animaisFiltrados" :key="animal.id">
                <td>{{ animal.dono_nome }}</td>
                <td><strong>{{ animal.nome }}</strong></td>
                <td>{{ animal.raca }}</td>
                <td>
                  <span v-if="animal.leilao_nome !== 'Não vinculado'" class="badge-leilao">{{ animal.leilao_nome
                    }}</span>
                  <span v-else class="text-muted">Não vinculado</span>
                </td>
                <td>{{ animal.peso }} kg</td>
                <td>
                  <span :class="['status-badge', classeStatus(animal.status)]">
                    {{ animal.status === 'V' ? 'Vivo' : 'Morto' }}
                  </span>
                </td>
                <td>
                  <span v-if="animal.status === 'M'">
                    {{ animal.causa_morte === 'N' ? 'Morte natural' : (animal.causa_morte === 'O' ? 'Ataque de onça' :
                    'Não informado') }}
                  </span>
                  <span v-else>-</span>
                </td>
                <td class="acoes text-right">
                  <button class="btn-acao edit" title="Editar" @click="editarAnimal(animal)">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z">
                      </path>
                    </svg>
                  </button>
                  <button class="btn-acao delete" title="Excluir" @click="prepararExclusao(animal)">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
          <h1 class="page-title">{{ editandoId ? 'EDITAR ANIMAL' : 'NOVO ANIMAL' }}</h1>
        </div>
      </div>

      <div class="content-card form-card">
        <h3 class="section-title">INFORMAÇÕES DO ANIMAL</h3>

        <form @submit.prevent="salvarAnimal" class="form-animal">
          <div class="form-grid">
            <div class="input-group">
              <label>Número do Brinco / Nome</label>
              <input type="text" v-model="formAnimal.nome" placeholder="Ex: 1045" required>
            </div>
            <div class="input-group">
              <label>Raça</label>
              <input type="text" v-model="formAnimal.raca" placeholder="Ex: Nelore" required>
            </div>
            <div class="input-group">
              <label>Peso (kg)</label>
              <input type="number" step="0.01" v-model="formAnimal.peso" placeholder="0" min="0" required>
            </div>
            <div class="input-group">
              <label>Sexo</label>
              <div class="select-wrapper">
                <select v-model="formAnimal.sexo" required>
                  <option value="M">Macho</option>
                  <option value="F">Fêmea</option>
                </select>
              </div>
            </div>
            <div class="input-group">
              <label>Status</label>
              <div class="select-wrapper">
                <select v-model="formAnimal.status" required>
                  <option value="V">Vivo</option>
                  <option value="M">Morto</option>
                </select>
              </div>
            </div>

            <div class="input-group" v-if="formAnimal.status === 'M'">
              <label>Causa da Morte <span class="required-star">*</span></label>
              <div class="select-wrapper">
                <select v-model="formAnimal.causa_morte" required>
                  <option value="" disabled>Selecione a causa</option>
                  <option value="N">Morte natural</option>
                  <option value="O">Ataque de onça</option>
                </select>
              </div>
            </div>

            <div class="input-group">
              <label>Categoria</label>
              <div class="select-wrapper">
                <select v-model="formAnimal.id_categoria" required>
                  <option value="" disabled>Selecione a categoria</option>
                  <option v-for="cat in listaCategorias" :key="cat.id_categoria" :value="cat.id_categoria">
                    {{ cat.id_categoria }} - {{ cat.descricao }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <div class="input-group full-width" style="margin-top: 20px;">
            <label>Proprietário Vinculado</label>
            <div class="select-wrapper">
              <select v-model="formAnimal.id_dono" required>
                <option value="" disabled>Selecione um dono disponível</option>
                <option v-for="dono in proprietariosOrdenados" :key="dono.id_dono" :value="dono.id_dono">
                  {{ dono.nome }} (Usuário: {{ dono.usuario }})
                </option>
              </select>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-salvar">
              {{ editandoId ? 'Salvar Alterações' : 'Cadastrar Animal' }}
            </button>
            <button type="button" class="btn-cancelar" @click="voltarParaLista">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';

const telaAtual = ref('lista');
const mensagemFeedback = ref('');
const editandoId = ref(null);
const mostrarModal = ref(false);
const animalParaExcluir = ref(null);

const listaProprietarios = ref([]);
const listaCategorias = ref([]);
const animais = ref([]);
const termoBusca = ref('');

// Nova variável de filtro por proprietário
const proprietarioSelecionado = ref('');

const formAnimal = reactive({
  nome: '', raca: '', peso: '', status: 'V', sexo: 'M', id_categoria: '', id_dono: '', causa_morte: ''
});

const dataAtual = new Date();
const opcoesData = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
const dataFormatada = ref(dataAtual.toLocaleDateString('pt-BR', opcoesData));

// Ordena os proprietários alfabeticamente para exibição nos filtros
const proprietariosOrdenados = computed(() => {
  return [...listaProprietarios.value].sort((a, b) =>
    a.nome.localeCompare(b.nome, 'pt-BR')
  );
});

// Lógica que une Filtro (Dropdown) + Barra de Pesquisa
const animaisFiltrados = computed(() => {
  const termo = termoBusca.value.toLowerCase().trim();
  return animais.value.filter(a => {
    // 1. Verifica o texto de busca
    const bateTexto = !termo ||
      (a.nome && a.nome.toLowerCase().includes(termo)) ||
      (a.raca && a.raca.toLowerCase().includes(termo)) ||
      (a.dono_nome && a.dono_nome.toLowerCase().includes(termo));

    // 2. Verifica o proprietário selecionado no Dropdown (convertendo string para número)
    const idProprietarioFiltro = parseInt(proprietarioSelecionado.value);
    const bateDono = !proprietarioSelecionado.value || a.id_dono === idProprietarioFiltro;

    return bateTexto && bateDono;
  });
});

const carregarProprietarios = async () => {
  try {
    const resposta = await fetch('http://127.0.0.1:8000/api/proprietarios/');
    listaProprietarios.value = await resposta.json();
  } catch (error) { console.error(error); }
};

const carregarCategorias = async () => {
  try {
    const resposta = await fetch('http://127.0.0.1:8000/api/categorias/');
    listaCategorias.value = await resposta.json();
  } catch (error) { console.error(error); }
};

const carregarAnimais = async () => {
  try {
    const resposta = await fetch('http://127.0.0.1:8000/api/animais/');
    animais.value = await resposta.json();
  } catch (error) { console.error(error); }
};

onMounted(() => {
  carregarProprietarios();
  carregarCategorias();
  carregarAnimais();
});

const classeStatus = (status) => status === 'V' ? 'status-ativo' : 'status-doente';

const mostrarMensagem = (texto) => {
  mensagemFeedback.value = texto;
  setTimeout(() => { mensagemFeedback.value = ''; }, 3000);
};

const resetarFormulario = () => {
  formAnimal.nome = ''; formAnimal.raca = ''; formAnimal.peso = '';
  formAnimal.status = 'V'; formAnimal.sexo = 'M'; formAnimal.id_categoria = ''; formAnimal.id_dono = ''; formAnimal.causa_morte = '';
  editandoId.value = null;
};

const abrirFormulario = () => { resetarFormulario(); telaAtual.value = 'formulario'; };

const editarAnimal = (animal) => {
  editandoId.value = animal.id;
  formAnimal.nome = animal.nome;
  formAnimal.raca = animal.raca;
  formAnimal.peso = animal.peso;
  formAnimal.status = animal.status;
  formAnimal.sexo = animal.sexo;
  formAnimal.id_categoria = animal.id_categoria || '';
  formAnimal.id_dono = animal.id_dono || '';
  formAnimal.causa_morte = animal.causa_morte || '';
  telaAtual.value = 'formulario';
};

const voltarParaLista = () => { telaAtual.value = 'lista'; resetarFormulario(); };
const prepararExclusao = (animal) => { animalParaExcluir.value = animal; mostrarModal.value = true; };
const fecharModal = () => { mostrarModal.value = false; animalParaExcluir.value = null; };

const confirmarExclusao = async () => {
  if (animalParaExcluir.value) {
    try {
      const resposta = await fetch(`http://127.0.0.1:8000/api/animais/${animalParaExcluir.value.id}/`, { method: 'DELETE' });
      if (resposta.ok) {
        mostrarMensagem('Animal removido com sucesso!');
        await carregarAnimais();
      }
    } catch (error) { mostrarMensagem('Erro de conexão.'); }
    fecharModal();
  }
};

const salvarAnimal = async () => {
  if (formAnimal.status === 'M' && !formAnimal.causa_morte) {
    mostrarMensagem('Por favor, selecione a causa da morte.');
    return;
  }
  const url = editandoId.value ? `http://127.0.0.1:8000/api/animais/${editandoId.value}/` : 'http://127.0.0.1:8000/api/animais/';
  const metodo = editandoId.value ? 'PUT' : 'POST';
  try {
    const resposta = await fetch(url, {
      method: metodo,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nome: formAnimal.nome, raca: formAnimal.raca, peso: formAnimal.peso, status: formAnimal.status,
        sexo: formAnimal.sexo, dt_nasc: '2024-05-19', id_categoria: formAnimal.id_categoria, id_dono: formAnimal.id_dono,
        causa_morte: formAnimal.status === 'M' ? formAnimal.causa_morte : null
      })
    });
    if (resposta.ok) {
      mostrarMensagem(editandoId.value ? 'Animal atualizado!' : 'Animal cadastrado!');
      await carregarAnimais();
      voltarParaLista();
    }
  } catch (error) { mostrarMensagem('Erro com o servidor.'); }
};
</script>

<style scoped>
.animais-page {
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
}

.feedback-banner .icon {
  width: 22px;
  height: 22px;
}

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
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 12px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.modal-title {
  font-family: "Anton SC", sans-serif;
  color: #ff7322;
  margin: 0 0 15px 0;
  font-size: 24px;
  text-transform: uppercase;
}

.modal-text {
  color: #ffb68c;
  font-size: 15px;
  line-height: 1.5;
  margin-bottom: 25px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

.btn-modal-cancelar {
  background-color: white;
  color: #ff7322;
  border: 1px solid #ff7322;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}

.btn-modal-excluir {
  background-color: #e60000;
  color: white;
  border: none;
  padding: 10px 25px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
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
}

.content-card {
  background: #ffffff;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
  border: 1px solid #f0e6de;
}

.form-card {
  border: 1px solid #ff7322;
}

/* ===========================================================
   ALTERAÇÕES DE LAYOUT: ALINHANDO FILTRO E BUSCA
   =========================================================== */
.filtros-e-busca-container {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 25px;
  flex-wrap: wrap;
  /* Garante que quebre linha se a tela for pequena */
}

/* 1. Ajustes do Dropdown (Filtro de Proprietário) */
.custom-select-wrapper {
  position: relative;
  width: 220px;
  /* Largura um pouco maior para acomodar o texto */
  height: 44px;
  /* Altura fixa padrão para inputs */
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
  /* Borda Laranja */
  border-radius: 8px;
  background-color: #ffffff;
  color: #ff7322;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.custom-select-trigger .left-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.custom-select-trigger .icon-user,
.custom-select-trigger .icon-arrow {
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

/* 2. Ajustes da Barra de Busca */
.search-bar-container {
  flex: 1;
  max-width: 450px;
  /* Limita largura máxima */
  height: 44px;
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: #ffffff;
  border: 1.5px solid #ff7322;
  /* Borda Laranja aplicada aqui também */
  border-radius: 8px;
  padding: 0 16px;
  height: 100%;
  box-sizing: border-box;
  width: 100%;
}

.search-bar input {
  border: none;
  background: transparent;
  width: 100%;
  outline: none;
  font-size: 14px;
  color: #334155;
  padding-left: 8px;
}

.search-icon {
  width: 20px;
  height: 20px;
  color: #ff7322;
  /* Ícone de busca também na cor laranja */
  flex-shrink: 0;
}

/* ===========================================================
   FIM DAS ALTERAÇÕES DE LAYOUT
   =========================================================== */

.table-container {
  overflow-x: auto;
}

.animais-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  color: #1e293b;
}

.animais-table th {
  text-align: left;
  padding: 15px 10px;
  color: #1e293b;
  font-weight: 600;
  border-bottom: 2px solid #f1f5f9;
}

.animais-table td {
  padding: 15px 10px;
  border-bottom: 1px solid #f1f5f9;
}

.tabela-vazia {
  text-align: center !important;
  color: #94a3b8;
  padding: 30px !important;
  font-style: italic;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-ativo {
  background-color: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.status-doente {
  background-color: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.badge-leilao {
  background-color: #fffaf7;
  color: #ea580c;
  border: 1px solid #ffede3;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
}

.text-muted {
  color: #94a3b8;
  font-style: italic;
  font-size: 13px;
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
  color: #ff7322;
  border-radius: 4px;
  padding: 4px;
}

.btn-acao svg {
  width: 18px;
  height: 18px;
}

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
  align-items: center;
}

.btn-voltar svg {
  width: 24px;
  height: 24px;
}

.section-title {
  font-size: 14px;
  font-weight: 900;
  color: #ff7322;
  text-transform: uppercase;
  margin-bottom: 25px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px 40px;
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

.required-star {
  color: #e60000;
  margin-left: 4px;
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

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 40px;
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
}

@media (max-width: 768px) {
  .animais-page {
    padding: 15px;
  }

  .filtros-e-busca-container {
    flex-direction: column;
    align-items: stretch;
  }

  .custom-select-wrapper {
    width: 100%;
  }

  .search-bar-container {
    max-width: 100%;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .full-width {
    grid-column: span 1;
  }
}
</style>