<template>
  <div class="sidebar-container">
    <!-- Cabeçalho com Logo -->
    <div class="sidebar-header">
      <div class="logo-box">
        <!-- Verifique se o caminho da imagem abaixo está correto no seu projeto -->
        <img src="../assets/logo_por_do_sol.png" alt="Logo Pôr do Sol">
      </div>
      <div class="title-box">
        <h1 class="brand-title">PECUÁRIA PÔR DO SOL</h1>
        <p class="brand-subtitle">Sistema de Gestão</p>
      </div>
    </div>

    <div class="divider"></div>

    <!-- Menu de Navegação -->
    <nav class="sidebar-nav">
      <ul class="nav-list">
        <li class="nav-item" :class="{ active: menuAtivo === 'dashboard' }" @click="navegarPara('dashboard')">
          Dashboard
        </li>
        <li class="nav-item" :class="{ active: menuAtivo === 'animais' }" @click="navegarPara('animais')">
          Animais
        </li>
        <li class="nav-item" :class="{ active: menuAtivo === 'proprietarios' }" @click="navegarPara('proprietarios')">
          Proprietários
        </li>
        <li class="nav-item" :class="{ active: menuAtivo === 'leiloes' }" @click="navegarPara('leiloes')">
           Leilões
        </li>
        <li class="nav-item" :class="{ active: menuAtivo === 'vendas' }" @click="navegarPara('vendas')">
          Vendas
        </li>
        <li class="nav-item" :class="{ active: menuAtivo === 'medicamentos' }" @click="navegarPara('medicamentos')">
           Medicamentos
        </li>
      </ul>
    </nav>

    <!-- Rodapé com Usuário -->
    <div class="sidebar-footer">
      <div class="user-section">
        <div class="user-avatar">{{ inicialLetra }}</div>
        <div class="user-info">
          <span class="user-role">{{ nomeUsuario }}</span>
          <span class="user-email">administrador@pecuaria.com</span>
        </div>
      </div>
      <button class="btn-sair" @click="sairDoSistema">
        <span class="icon">⬅️</span> Sair
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  nomeUsuario: { type: String, default: 'Usuário' }
});

const emit = defineEmits(['mudar-tela']);
const menuAtivo = ref('animais'); // Define Animais como padrão ao carregar

const navegarPara = (tela) => {
  menuAtivo.value = tela;
  emit('mudar-tela', tela);
};

const inicialLetra = computed(() => {
  return props.nomeUsuario.charAt(0).toUpperCase();
});

const sairDoSistema = () => {
  window.location.reload();
};
</script>

<style scoped>
.sidebar-container {
  width: 260px;
  height: 100vh;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 15px rgba(0,0,0,0.05);
}

.sidebar-header {
  display: flex;
  align-items: center;
  padding: 25px 20px;
  gap: 15px;
}

.logo-box img { width: 45px; height: auto; }

.brand-title {
  font-family: "Anton SC", sans-serif; 
  font-size: 18px;
  color: #ff7322;
  margin: 0;
  line-height: 1.1;
}

.brand-subtitle { font-size: 11px; color: #64748b; margin: 4px 0 0 0; }

.divider { height: 1px; background-color: rgba(255, 115, 34, 0.1); margin: 0 20px; }

.sidebar-nav { padding: 20px 10px; flex-grow: 1; }

.nav-list { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 5px; }

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 15px;
  color: #ff7322; /* Cor padrão laranja */
  transition: 0.2s;
}

/* ITEM ATIVO: Laranja sólido com texto branco conforme a imagem */
.nav-item.active {
  background-color: #ff7322; 
  color: #ffffff;
  font-weight: 600;
}

.nav-item:hover:not(.active) {
  background-color: rgba(255, 115, 34, 0.05);
}

.icon { margin-right: 15px; font-size: 18px; }

.sidebar-footer { padding-bottom: 20px; border-top: 1px solid #f1f5f9; }

.user-section { display: flex; align-items: center; padding: 20px; gap: 12px; }

.user-avatar {
  width: 40px;
  height: 40px;
  background-color: #ff7322;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 20px;
}

.user-info { display: flex; flex-direction: column; overflow: hidden; }
.user-role { font-weight: bold; font-size: 14px; color: #1e293b; }
.user-email { font-size: 11px; color: #64748b; }

.btn-sair {
  background: transparent;
  border: none;
  color: #ff7322;
  padding: 10px 25px;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 14px;
  font-weight: 500;
}
</style>