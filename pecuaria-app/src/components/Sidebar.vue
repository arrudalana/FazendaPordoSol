<template>
  <div class="sidebar-container" :class="{ 'is-collapsed': !isExpanded }">
    
    <button 
      class="toggle-arrow" 
      @click="alternarMenu" 
      :title="isExpanded ? 'Recolher menu' : 'Expandir menu'"
      :aria-label="isExpanded ? 'Recolher menu' : 'Expandir menu'"
      :aria-expanded="isExpanded"
    >
      <svg 
        class="chevron-icon" 
        xmlns="http://www.w3.org/2000/svg" 
        viewBox="0 0 24 24" 
        fill="none" 
        stroke="currentColor" 
        stroke-width="2.5" 
        stroke-linecap="round" 
        stroke-linejoin="round"
      >
        <polyline points="15 18 9 12 15 6" />
      </svg>
    </button>

    <div class="sidebar-header">
      <div class="logo-box">
        <img src="../assets/logo_por_do_sol.png" alt="Logo Pôr do Sol" />
      </div>
      <div class="title-box" v-show="isExpanded">
        <h1 class="brand-title">PÔR DO SOL</h1>
        <p class="brand-subtitle">Gestão Pecuária</p>
      </div>
    </div>

    <div class="divider"></div>

    <nav class="sidebar-nav" role="navigation" aria-label="Navegação principal">
      <ul class="nav-list">
        <li 
          v-for="item in menuItems" 
          :key="item.id"
          class="nav-item" 
          :class="{ active: menuAtivo === item.id }" 
          @click="navegarPara(item.id)"
          :title="!isExpanded ? item.label : ''"
          role="menuitem"
          tabindex="0"
          @keydown.enter="navegarPara(item.id)"
        >
          <span class="icon" aria-hidden="true">
            <!-- Ícone SVG pode ser inserido aqui -->
          </span>
          <span class="nav-text" v-show="isExpanded">{{ item.label }}</span>
        </li>
      </ul>
    </nav>

    <div class="sidebar-footer">
      <div class="user-section">
        <div class="user-avatar" aria-hidden="true">{{ inicialLetra }}</div>
        <div class="user-info" v-show="isExpanded">
          <span class="user-role">{{ nomeUsuario }}</span>
          <span class="user-email">{{ usuarioLogin }}</span>
        </div>
      </div>
      <button class="btn-sair" @click="sairDoSistema" title="Sair do Sistema">
        <span class="icon" aria-hidden="true"></span>
        <span class="nav-text" v-show="isExpanded">Sair</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  nomeUsuario: { type: String, default: 'Usuário' },
  usuarioLogin: { type: String, default: 'usuario@email.com' }
});

const emit = defineEmits(['mudar-tela']);

const menuAtivo = ref('animais');
const isExpanded = ref(true);

const menuItems = ref([
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'animais', label: 'Animais' },
  { id: 'proprietarios', label: 'Proprietários' },
  { id: 'leiloes', label: 'Leilões' },
  { id: 'vendas', label: 'Vendas' },
  { id: 'medicamentos', label: 'Medicamentos' }
]);

const alternarMenu = () => {
  isExpanded.value = !isExpanded.value;
};

const navegarPara = (tela) => {
  menuAtivo.value = tela;
  emit('mudar-tela', tela);
  
  if (window.innerWidth <= 768) {
    isExpanded.value = false;
  }
};

const inicialLetra = computed(() => {
  return props.nomeUsuario.charAt(0).toUpperCase();
});

const sairDoSistema = () => {
  window.location.reload();
};

const checarTamanhoTela = () => {
  if (window.innerWidth <= 768) {
    isExpanded.value = false;
  } else {
    isExpanded.value = true;
  }
};

onMounted(() => {
  checarTamanhoTela();
  window.addEventListener('resize', checarTamanhoTela);
});

onUnmounted(() => {
  window.removeEventListener('resize', checarTamanhoTela);
});
</script>

<style scoped>
/* Container principal */
.sidebar-container {
  width: 260px;
  height: 100vh;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 20px rgba(0, 0, 0, 0.06);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  border-right: 3px solid #ff7322;
  overflow: hidden; /* evita que conteúdo estoure */
}

.is-collapsed {
  width: 80px;
}

/* Botão de toggle - agora com SVG */
.toggle-arrow {
  position: absolute;
  top: 40px;
  right: -16px;
  width: 32px;
  height: 32px;
  background: #ff7322;
  color: #ffffff;
  border: 2px solid #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 20;
  box-shadow: 0 2px 8px rgba(255, 115, 34, 0.3);
  transition: background-color 0.2s, box-shadow 0.2s, transform 0.3s ease;
  padding: 0;
}

.toggle-arrow:hover {
  background-color: #e65c00;
  box-shadow: 0 4px 12px rgba(230, 92, 0, 0.4);
}

.toggle-arrow:focus-visible {
  outline: 2px solid #ff7322;
  outline-offset: 3px;
}

/* Ícone do chevron */
.chevron-icon {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
}

/* Quando colapsado, gira a seta para apontar para direita */
.is-collapsed .chevron-icon {
  transform: rotate(180deg);
}

/* Cabeçalho */
.sidebar-header {
  display: flex;
  align-items: center;
  padding: 25px 20px;
  gap: 15px;
  min-height: 85px;
  overflow: hidden;
}

.is-collapsed .sidebar-header {
  padding: 25px 10px;
  justify-content: center;
}

.logo-box img {
  width: 45px;
  height: auto;
  transition: width 0.3s;
}

.is-collapsed .logo-box img {
  width: 35px;
}

.title-box {
  white-space: nowrap;
  overflow: hidden;
  transition: opacity 0.25s ease, max-width 0.25s ease;
  opacity: 1;
  max-width: 200px;
}

.is-collapsed .title-box {
  opacity: 0;
  max-width: 0;
  visibility: hidden;
}

.brand-title {
  font-family: "Anton SC", sans-serif;
  font-size: 18px;
  color: #ff7322;
  margin: 0;
  line-height: 1.1;
}

.brand-subtitle {
  font-size: 11px;
  color: #64748b;
  margin: 4px 0 0 0;
}

/* Divisor */
.divider {
  height: 1px;
  background-color: rgba(255, 115, 34, 0.12);
  margin: 0 20px;
  transition: margin 0.3s;
}

.is-collapsed .divider {
  margin: 0 10px;
}

/* Navegação */
.sidebar-nav {
  padding: 20px 10px;
  flex: 1;
  overflow-x: hidden;
}

.nav-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 18px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 15px;
  color: #ff7322;
  transition: background-color 0.2s, color 0.2s, padding 0.3s;
  white-space: nowrap;
  outline: none;
}

.nav-item:focus-visible {
  outline: 2px solid #ff7322;
  outline-offset: -2px;
  background-color: rgba(255, 115, 34, 0.08);
}

.is-collapsed .nav-item {
  justify-content: center;
  padding: 12px 0;
}

.nav-item.active {
  background-color: #ff7322;
  color: #ffffff;
  font-weight: 600;
  box-shadow: 0 4px 10px rgba(255, 115, 34, 0.2);
}

.nav-item:hover:not(.active) {
  background-color: rgba(255, 115, 34, 0.06);
}

/* Ícones placeholder */
.icon {
  width: 24px;
  height: 24px;
  margin-right: 15px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: margin 0.3s;
  color: currentColor;
  opacity: 0.8;
}

.nav-item.active .icon {
  opacity: 1;
}

.is-collapsed .icon {
  margin-right: 0;
}

/* Texto da navegação com transição */
.nav-text {
  display: inline-block;
  overflow: hidden;
  white-space: nowrap;
  transition: opacity 0.25s ease, max-width 0.25s ease, visibility 0.25s;
  opacity: 1;
  max-width: 150px;
}

.is-collapsed .nav-text {
  opacity: 0;
  max-width: 0;
  visibility: hidden;
}

/* Rodapé */
.sidebar-footer {
  padding-bottom: 20px;
  border-top: 1px solid #f1f5f9;
  overflow: hidden;
}

.user-section {
  display: flex;
  align-items: center;
  padding: 20px;
  gap: 12px;
  white-space: nowrap;
}

.is-collapsed .user-section {
  padding: 20px 0;
  justify-content: center;
}

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
  flex-shrink: 0;
}

.user-info {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: opacity 0.25s ease, max-width 0.25s ease, visibility 0.25s;
  opacity: 1;
  max-width: 120px;
}

.is-collapsed .user-info {
  opacity: 0;
  max-width: 0;
  visibility: hidden;
}

.user-role {
  font-weight: bold;
  font-size: 14px;
  color: #1e293b;
}

.user-email {
  font-size: 11px;
  color: #64748b;
}

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
  width: 100%;
  white-space: nowrap;
  transition: background-color 0.2s, padding 0.3s;
}

.is-collapsed .btn-sair {
  justify-content: center;
  padding: 10px 0;
}

.btn-sair:hover {
  background-color: rgba(255, 115, 34, 0.05);
}

.btn-sair:focus-visible {
  outline: 2px solid #ff7322;
  outline-offset: -2px;
}

/* Responsivo */
@media (max-width: 768px) {
  .sidebar-container {
    position: absolute;
    z-index: 1000;
    height: 100%;
  }
  
  .toggle-arrow {
    top: 20px;
    right: -14px;
    width: 28px;
    height: 28px;
  }
  
  .chevron-icon {
    width: 16px;
    height: 16px;
  }
}
</style>