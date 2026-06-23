<script setup>
import { ref } from 'vue';
import Login from './components/Login.vue';
import Sidebar from './components/Sidebar.vue';
import Animais from './components/Animais.vue';
import Proprietarios from './components/Proprietarios.vue';
import Leiloes from './components/Leiloes.vue';
import Vendas from './components/Vendas.vue';
import Medicamentos from './components/Medicamentos.vue';


const usuarioLogado = ref(false);
const nomeDono = ref('');
const usuarioLogin = ref('');     // guarda o email/login
const perfilLogado = ref('');     // guarda o perfil (Administrador ou Dono)
const telaAtual = ref('vendas');
const menuAberto = ref(false);

const acessarSistema = (nome, usuario, perfil) => {
  usuarioLogado.value = true;
  nomeDono.value = nome;
  usuarioLogin.value = usuario;
  perfilLogado.value = perfil;
};

const mudarTela = (tela) => {
  telaAtual.value = tela;
  menuAberto.value = false;
};
</script>

<template>
  <Login v-if="!usuarioLogado" @login-sucesso="acessarSistema" />

  <div class="layout-sistema" v-else>
    <header class="header-mobile">
      <button class="btn-menu" @click="menuAberto = true">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="28" height="28"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
      </button>
      <h2 class="anton-sc-regular title-mobile">Fazenda Pôr do Sol</h2> <!-- Título do cabeçalho móvel -->
    </header>

    <div v-if="menuAberto" class="overlay-mobile" @click="menuAberto = false"></div>

    <Sidebar
      :nome-usuario="nomeDono"
      :usuario-login="usuarioLogin"
      @mudar-tela="mudarTela"
      class="sidebar-componente"
      :class="{ 'sidebar-aberta': menuAberto }"
    />

    <main class="conteudo-principal">
      <Animais v-if="telaAtual === 'animais'" />
      <Proprietarios v-else-if="telaAtual === 'proprietarios'" />
      <Leiloes v-else-if="telaAtual === 'leiloes'" />
      <Vendas v-else-if="telaAtual === 'vendas'" :perfil-usuario="perfilLogado" />
      <Medicamentos v-else-if="telaAtual === 'medicamentos'" />
      <div v-else class="tela-placeholder">
        <h2 class="anton-sc-regular">Módulo: {{ telaAtual.toUpperCase() }}</h2>
        <p>(Telas não desenvolvidas)</p>
      </div>
    </main>
  </div>
</template>

<style>
html, body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  background-color: #f8fafc;
  font-family: 'Figtree', sans-serif;
}
.anton-sc-regular {
  font-family: "Anton SC", sans-serif;
  font-weight: 400;
  font-style: normal;
}
.layout-sistema {
  display: flex;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  position: relative;
}
.header-mobile { display: none; }
.overlay-mobile { display: none; }
.conteudo-principal {
  flex-grow: 1;
  overflow-y: auto;
  background-color: #f9f2ec;
}
.tela-placeholder { padding: 80px 40px; text-align: center; color: #ff7322; }
.tela-placeholder h2 { font-size: 32px; margin-bottom: 10px; letter-spacing: 1px; }
.tela-placeholder p { font-size: 16px; color: #64748b; font-weight: 500; }

@media (max-width: 768px) {
  .layout-sistema { flex-direction: column; }
  .header-mobile {
    display: flex;
    align-items: center;
    background-color: #ffffff;
    padding: 15px 20px;
    border-bottom: 1px solid #ebdcd1;
    z-index: 10;
  }
  .btn-menu {
    background: none;
    border: none;
    color: #ff7322;
    cursor: pointer;
    padding: 0;
    margin-right: 15px;
  }
  .title-mobile {
    margin: 0;
    color: #1e293b;
    font-size: 22px;
  }
  .sidebar-componente {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    z-index: 1000;
    transform: translateX(-100%);
    transition: transform 0.3s ease-in-out;
    box-shadow: 2px 0 15px rgba(0,0,0,0.1);
  }
  .sidebar-aberta { transform: translateX(0); }
  .overlay-mobile {
    display: block;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.4);
    z-index: 999;
  }
}
</style>