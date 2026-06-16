<template>
  <div class="login-wrapper">
    <div class="header">
      <img src="../assets/logo_por_do_sol.png" alt="Logo Pecuária Pôr do Sol" class="logo" />
      <h1 class="title">PECUÁRIA PÔR DO SOL</h1>
      <p class="subtitle">Sistema de Gestão de Gado</p>
    </div>

    <div class="login-card">
      <h2>ENTRAR NO SISTEMA</h2>
      
      <form @submit.prevent="realizarLogin">
        <div class="input-group">
          <label for="usuario">Usuário</label>
          <div class="input-field">
            <span class="icon">👤</span>
            <input 
              type="text" 
              id="usuario" 
              v-model="form.usuario" 
              placeholder="Digite seu usuário" 
              required 
              :disabled="carregando"
            />
          </div>
        </div>

        <div class="input-group">
          <label for="senha">Senha</label>
          <div class="input-field">
            <span class="icon">🔒</span>
            <input 
              type="password" 
              id="senha" 
              v-model="form.senha" 
              placeholder="••••••••" 
              required 
              :disabled="carregando"
            />
          </div>
        </div>

        <div v-if="mensagemErro" class="erro-alerta"> <!--Exibe mensagens de erro vindas do backend, como "Usuário não encontrado" ou "Senha incorreta"-->
          {{ mensagemErro }}
        </div>

        <button type="submit" class="btn-entrar" :disabled="carregando"> 
          {{ carregando ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';

const emit = defineEmits(['login-sucesso']); // Define o evento que será emitido para o componente pai (App.vue) quando o login for bem-sucedido, passando o nome do usuário logado e o perfil como parâmetros

const form = reactive({  // Objeto reativo para armazenar os dados do formulário de login
  usuario: '',
  senha: ''
});

const mensagemErro = ref(''); // Variável reativa para armazenar mensagens de erro que serão exibidas para o usuário
const carregando = ref(false); 

const realizarLogin = async () => {
  mensagemErro.value = ''; // Limpa mensagens anteriores
  carregando.value = true; // Inicia o estado de carregamento

  try { 
    // Envia os dados do formulário para a API de login
    const resposta = await fetch('http://127.0.0.1:8000/api/login/', { 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: form.usuario, 
        senha: form.senha
      })
    });

    const dados = await resposta.json(); // Converte a resposta da API para JSON

    if (dados.sucesso) {
      // Repassa o nome e também o perfil para o componente pai (App.vue)
      emit('login-sucesso', dados.nome_usuario, dados.perfil); 
    } else {
      // Exibe "Usuário não encontrado" ou "Senha incorreta" vindo do Django
      mensagemErro.value = dados.mensagem; 
    }
    
  } catch (erro) {
    console.error("Erro ao conectar com a API:", erro);
    mensagemErro.value = 'Erro ao tentar conectar com o servidor do banco de dados.';
  } finally {
    carregando.value = false; // Finaliza o carregamento, independentemente de sucesso ou erro
  }
};
</script>

<style scoped>
.login-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #fafafa;
  font-family: 'Arial', sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  width: 130px; 
  height: auto;
  margin-bottom: 15px;
}

.title {
  font-family: "Anton SC", sans-serif;
  font-size: 36px; 
  font-weight: 400; 
  color: #1a202c;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 1px; 
}

.subtitle {
  font-size: 16px;
  color: #718096;
  margin-top: 5px;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.login-card h2 {
  font-family: "Anton SC", sans-serif;
  font-size: 22px;
  font-weight: 400;
  color: #1a202c;
  margin-bottom: 30px;
  text-transform: uppercase;
}

.input-group {
  text-align: left;
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  font-size: 14px;
  color: #4a5568;
  margin-bottom: 8px;
}

.input-field {
  display: flex;
  align-items: center;
  background-color: #f7fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 10px 15px;
  transition: border-color 0.2s;
}

.input-field:focus-within {
  border-color: #ff7322;
}

.input-field .icon {
  margin-right: 10px;
  font-size: 18px;
}

.input-field input {
  border: none;
  background: transparent;
  width: 100%;
  font-size: 15px;
  color: #2d3748;
  outline: none;
}

.input-field input:disabled {
  color: #a0aec0;
}

/* Estilo do Alerta de Erro */
.erro-alerta {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 15px;
  font-size: 14px;
  text-align: center;
  border: 1px solid #f87171;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

.btn-entrar {
  width: 100%;
  background-color: #ff7322; 
  color: white;
  font-weight: bold;
  font-size: 16px;
  padding: 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.3s, opacity 0.3s;
}

.btn-entrar:hover:not(:disabled) {
  background-color: orange;
}

.btn-entrar:disabled {
  background-color: #ffb68c;
  cursor: not-allowed;
}
</style>