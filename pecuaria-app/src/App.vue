<script setup>
import { ref } from 'vue';
import Login from './components/Login.vue';
import Sidebar from './components/Sidebar.vue';
import Animais from './components/Animais.vue'; 
import Proprietarios from './components/Proprietarios.vue';
import Leiloes from './components/Leiloes.vue';

const usuarioLogado = ref(false);
const nomeDono = ref(''); 
const telaAtual = ref('animais'); 

const acessarSistema = (nome) => { // Função que é chamada quando o login é bem-sucedido, recebe o nome do usuário logado como parâmetro
  usuarioLogado.value = true;
  nomeDono.value = nome; 
};
</script>

<template>
  <!-- O componente de Login é renderizado se não houver usuário logado-->
  <Login v-if="!usuarioLogado" @login-sucesso="acessarSistema" />
  
  
  <div class="layout-sistema" v-else>
    <!-- Sidebar recebe o nome do dono via props e emite evento para mudar tela-->
    <Sidebar :nome-usuario="nomeDono" @mudar-tela="(tela) => telaAtual = tela" />
    
    <main class="conteudo-principal">
      <!-- Alternância entre as telas-->
      <Animais v-if="telaAtual === 'animais'" />
      <Proprietarios v-else-if="telaAtual === 'proprietarios'" />
      <Leiloes v-else-if="telaAtual === 'leiloes'" />
      <!-- Mensagem para módulos que ainda serão desenvolvidos-->
      <div v-else class="tela-placeholder">
        <h2 class="anton-sc-regular">Módulo: {{ telaAtual.toUpperCase() }}</h2>
        <p>(Telas não desenvolvidas)</p>
      </div>
    </main>
  </div>
</template>

<style>
/* Configuração global de fontes profissionais conforme solicitado */
html, body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  background-color: #f8fafc;
  font-family: 'Figtree', sans-serif; /* Fonte profissional para leitura principal */
}

/* Classe utilitária para títulos com a fonte Anton SC */
.anton-sc-regular {
  font-family: "Anton SC", sans-serif;
  font-weight: 400;
  font-style: normal;
}

.layout-sistema {
  display: flex; /* Mantém Sidebar na esquerda e Conteúdo na direita[cite: 2] */
  height: 100vh;
  width: 100%;
  overflow: hidden; 
}

.conteudo-principal {
  flex-grow: 1; 
  overflow-y: auto; 
  background-color: #f9f2ec; /* Fundo creme/bege das telas internas */
}

.tela-placeholder {
  padding: 80px 40px;
  text-align: center;
  color: #ff7322;
}

.tela-placeholder h2 {
  font-size: 32px;
  margin-bottom: 10px;
  letter-spacing: 1px;
}

.tela-placeholder p {
  font-size: 16px;
  color: #64748b;
  font-weight: 500;
}
</style>