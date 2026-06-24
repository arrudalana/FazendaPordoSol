<template>
    <div class="dashboard-page">
        <header class="top-bar">
            <p class="current-date">{{ dataFormatada }}</p>
        </header>

        <div class="page-header">
            <div class="title-section">
                <h1 class="page-title">DASHBOARD</h1>
                <p class="page-subtitle">Visão geral do sistema de gestão de gado</p>
            </div>

            <div class="filtro-proprietario-custom">
                <svg class="icon-user" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
                <select v-model="donoSelecionado"> <!-- Dropdown para selecionar o proprietário, vinculado à variável reativa donoSelecionado -->
                    <option :value="null">Todos os proprietários</option>
                    <option v-for="dono in listaProprietarios" :key="dono.id_dono" :value="dono.id_dono">
                        {{ dono.nome }}
                    </option>
                </select>
                <svg class="icon-seta" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
            </div>
        </div>

        <div class="dashboard-grid top-kpis">
            <div class="kpi-card border-green">
                <div class="kpi-content">
                    <span class="kpi-title">TOTAL DE ANIMAIS</span>
                    <span class="kpi-value">{{ totalAnimaisVivos }}</span>
                </div>
                <div class="kpi-icon bg-green">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z">
                        </path>
                    </svg>
                </div>
            </div>

            <div class="kpi-card border-orange">
                <div class="kpi-content">
                    <span class="kpi-title">PROPRIETÁRIOS</span>
                    <span class="kpi-value">{{ totalProprietarios }}</span>
                </div>
                <div class="kpi-icon bg-orange">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z">
                        </path>
                    </svg>
                </div>
            </div>

            <div class="kpi-card border-yellow">
                <div class="kpi-content">
                    <span class="kpi-title">LEILÕES</span>
                    <span class="kpi-value">{{ totalLeiloes }}</span>
                </div>
                <div class="kpi-icon bg-yellow">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z">
                        </path>
                    </svg>
                </div>
            </div>

            <div class="kpi-card border-green">
                <div class="kpi-content">
                    <span class="kpi-title">VENDAS</span>
                    <span class="kpi-value">{{ totalVendas }}</span>
                </div>
                <div class="kpi-icon bg-green">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                    </svg>
                </div>
            </div>
        </div>

        <div class="dashboard-grid middle-section">
            <div class="finance-card border-red">
                <div class="finance-header">
                    <div class="finance-main">
                        <span class="finance-title">LUCRO DA FAZENDA</span>
                        <span :class="['finance-value', lucroLiquido >= 0 ? 'text-green' : 'text-red']">
                            {{ formatarMoeda(lucroLiquido) }}
                        </span>
                    </div>
                    <div :class="['finance-icon', lucroLiquido >= 0 ? 'bg-green' : 'bg-red']">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z">
                            </path>
                        </svg>
                    </div>
                </div>
                <div class="finance-details">
                    <div class="detail-col">
                        <span class="detail-label">RECEITA</span>
                        <span class="detail-val text-green">{{ formatarMoeda(receitaTotal) }}</span>
                    </div>
                    <div class="detail-col">
                        <span class="detail-label">CUSTOS</span>
                        <span class="detail-val text-red">− {{ formatarMoeda(custosTotais) }}</span>
                    </div>
                    <div class="detail-col">
                        <span class="detail-label">PERDA (ONÇA)</span>
                        <span class="detail-val text-red">− {{ formatarMoeda(perdaOncaValor) }}</span>
                    </div>
                    <div class="detail-col">
                        <span class="detail-label">PERDA (NATURAL)</span>
                        <span class="detail-val text-red">− {{ formatarMoeda(perdaNaturalValor) }}</span>
                    </div>
                </div>
            </div>

            <div class="deaths-card border-orange-light">
                <div class="deaths-header">
                    <div class="deaths-main">
                        <span class="deaths-title">REGISTRO DE MORTES</span>
                        <span class="deaths-value">{{ mortesList.length }}</span>
                    </div>
                    <div class="deaths-icon bg-orange-light">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                </div>
                <div class="deaths-list">
                    <div v-for="morte in mortesList.slice(0, 4)" :key="morte.id" class="death-row">
                        <span class="death-name">
                            {{ morte.nome || 'Sem brinco' }}
                            <span class="causa-badge">{{ morte.causa_morte === 'O' ? 'Onça' : 'Natural' }}</span>
                        </span>
                        <span class="death-date">{{ formatarDataCurta(morte.dt_morte || morte.dt_nasc) }}</span>
                    </div>
                    <div v-if="mortesList.length === 0" class="empty-list">Nenhum registro de mortalidade.</div>
                </div>
            </div>
        </div>

        <div class="alert-box">
            <div class="alert-header">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>ANIMAIS COM PROBLEMAS DE SAÚDE</span>
            </div>
            <div class="alert-list">
                <div v-for="doente in animaisDoentesList" :key="doente.id_animal" class="alert-item">
                    - {{ doente.animal_nome }} — Tratamento: {{ doente.medicamento_nome }}
                </div>
                <div v-if="animaisDoentesList.length === 0" class="alert-item success-msg">
                    Nenhum animal em tratamento médico no momento. Rebanho saudável!
                </div>
            </div>
        </div>

        <div class="dashboard-grid charts-section">
            <div class="chart-card">
                <h3 class="chart-title">STATUS DO REBANHO</h3>
                <div class="pie-chart-container">
                    <div class="pie-chart" :style="pieChartStyle"></div>
                    <div class="pie-legends">
                        <div class="legend-item"><span class="dot bg-green"></span> Ativo: {{ statusData.ativo }}</div>
                        <div class="legend-item"><span class="dot bg-orange"></span> Leilão: {{ statusData.leilao }}
                        </div>
                        <div class="legend-item"><span class="dot bg-yellow"></span> Doente: {{ statusData.doente }}
                        </div>
                    </div>
                </div>
            </div>

            <div class="chart-card">
                <h3 class="chart-title">ANIMAIS POR RAÇA</h3>
                <div class="bar-chart-container">
                    <div class="y-axis">
                        <span>{{ maxRacaCount }}</span>
                        <span>{{ Math.ceil(maxRacaCount / 2) }}</span>
                        <span>0</span>
                    </div>
                    <div class="bars-area">
                        <div v-for="raca in racaData" :key="raca.nome" class="bar-group">
                            <div class="bar-fill" :style="{ height: raca.percent + '%' }">
                                <span class="bar-tooltip">{{ raca.count }}</span>
                            </div>
                            <span class="bar-label">{{ raca.nome }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="chart-card">
                <h3 class="chart-title">ANIMAIS POR CATEGORIA</h3>
                <div class="bar-chart-container">
                    <div class="y-axis">
                        <span>{{ maxCategoriaCount }}</span>
                        <span>{{ Math.ceil(maxCategoriaCount / 2) }}</span>
                        <span>0</span>
                    </div>
                    <div class="bars-area">
                        <div v-for="cat in categoriaData" :key="cat.nome" class="bar-group">
                            <div class="bar-fill bg-blue" :style="{ height: cat.percent + '%' }">
                                <span class="bar-tooltip text-blue">{{ cat.count }}</span>
                            </div>
                            <span class="bar-label">{{ cat.nome }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const donoSelecionado = ref(null);

const listaAnimais = ref([]);
const listaProprietarios = ref([]);
const listaLeiloes = ref([]);
const listaVendas = ref([]);
const listaAplicacoes = ref([]);

const dataAtual = new Date();
const dataFormatada = ref(dataAtual.toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }));

const carregarDadosDoSistema = async () => {
    try {
        const [resAn, resProp, resLei, resVen, resApp] = await Promise.all([
            fetch('http://127.0.0.1:8000/api/animais/'),
            fetch('http://127.0.0.1:8000/api/proprietarios/'),
            fetch('http://127.0.0.1:8000/api/leiloes/'),
            fetch('http://127.0.0.1:8000/api/vendas/'),
            fetch('http://127.0.0.1:8000/api/aplicacoes/')
        ]);

        if (resAn.ok) listaAnimais.value = await resAn.json();
        if (resProp.ok) listaProprietarios.value = await resProp.json();
        if (resLei.ok) listaLeiloes.value = await resLei.json();
        if (resVen.ok) listaVendas.value = await resVen.json();
        if (resApp.ok) listaAplicacoes.value = await resApp.json();
    } catch (error) { console.error("Erro na comunicação com a API"); }
};

onMounted(carregarDadosDoSistema); //montar a tela

/*  FILTRAGEM REATIVA */
const animaisFiltrados = computed(() => {
    if (!donoSelecionado.value) return listaAnimais.value;
    return listaAnimais.value.filter(a => Number(a.id_dono) === Number(donoSelecionado.value));
});

const vendasFiltradas = computed(() => {
    if (!donoSelecionado.value) return listaVendas.value;
    return listaVendas.value.filter(v => Number(v.id_dono) === Number(donoSelecionado.value));
});

/*CÁLCULO DOS KPIS */
const totalAnimaisVivos = computed(() => animaisFiltrados.value.filter(a => a.status === 'V').length);
const totalProprietarios = computed(() => donoSelecionado.value ? 1 : listaProprietarios.value.length);
const totalLeiloes = computed(() => listaLeiloes.value.length);
const totalVendas = computed(() => vendasFiltradas.value.length);

/*CÁLCULO FINANCEIRO */
const receitaTotal = computed(() => vendasFiltradas.value.reduce((acc, v) => acc + Number(v.valor), 0));
const custosTotais = computed(() => listaLeiloes.value.reduce((acc, l) => acc + (Number(l.custo_fixo) || 0), 0));

const PRECO_KG_ESTIMADO = 20;

const perdaOncaValor = computed(() => {
    const mortosOnca = animaisFiltrados.value.filter(a => a.status === 'M' && a.causa_morte === 'O');
    return mortosOnca.reduce((acc, a) => acc + (Number(a.peso || 0) * PRECO_KG_ESTIMADO), 0);
});

// NOVA MÉTRICA ADICIONADA
const perdaNaturalValor = computed(() => {
    const mortosNat = animaisFiltrados.value.filter(a => a.status === 'M' && a.causa_morte === 'N');
    return mortosNat.reduce((acc, a) => acc + (Number(a.peso || 0) * PRECO_KG_ESTIMADO), 0);
});

// O Lucro Líquido agora abate todos os tipos de perdas
const lucroLiquido = computed(() => receitaTotal.value - custosTotais.value - perdaOncaValor.value - perdaNaturalValor.value);

/* =========================================
   LISTAS DE ALERTAS E MORTALIDADE
   ========================================= */
// Unifica todas as mortes para exibição no card
const mortesList = computed(() => animaisFiltrados.value.filter(a => a.status === 'M'));

const animaisDoentesList = computed(() => {
    const aplicacoesFiltro = listaAplicacoes.value.filter(app => app.tp_medicamento === 'ANT' || app.tp_medicamento === 'PAR');
    const doentesMap = new Map();

    aplicacoesFiltro.forEach(app => {
        if (!donoSelecionado.value || Number(app.id_dono) === Number(donoSelecionado.value)) {
            if (!doentesMap.has(app.id_animal)) {
                doentesMap.set(app.id_animal, app);
            }
        }
    });
    return Array.from(doentesMap.values()).slice(0, 5);
});

/* =========================================
   GRÁFICOS E ESTATÍSTICAS
   ========================================= */
const statusData = computed(() => {
    let ativo = 0, leilao = 0, doente = animaisDoentesList.value.length;
    animaisFiltrados.value.forEach(a => {
        if (a.status === 'V') {
            if (a.leilao_nome !== 'Não vinculado') leilao++;
            else ativo++;
        }
    });
    ativo = Math.max(0, ativo - doente);
    return { ativo, leilao, doente };
});

const pieChartStyle = computed(() => {
    const { ativo, leilao, doente } = statusData.value;
    const total = ativo + leilao + doente;
    if (total === 0) return 'background: #f1f5f9;';

    const pAtivo = (ativo / total) * 100;
    const pLeilao = (leilao / total) * 100;
    return `background: conic-gradient(#0b9e15 0% ${pAtivo}%, #ff7322 ${pAtivo}% ${pAtivo + pLeilao}%, #eab308 ${pAtivo + pLeilao}% 100%);`;
});

const racaData = computed(() => {
    const contagem = {};
    animaisFiltrados.value.forEach(a => {
        if (a.status === 'V' && a.raca) {
            const raca = a.raca.trim();
            contagem[raca] = (contagem[raca] || 0) + 1;
        }
    });
    const arr = Object.keys(contagem).map(key => ({ nome: key, count: contagem[key] })).sort((a, b) => b.count - a.count).slice(0, 4);
    const max = Math.max(...arr.map(d => d.count), 1);
    return arr.map(item => ({ ...item, percent: (item.count / max) * 100 }));
});
const maxRacaCount = computed(() => racaData.value.length === 0 ? 10 : Math.max(...racaData.value.map(d => d.count)));

// NOVO CÁLCULO PARA O GRÁFICO DE CATEGORIA
const categoriaData = computed(() => {
    const contagem = {};
    animaisFiltrados.value.forEach(a => {
        if (a.status === 'V' && a.categoria_desc) {
            const cat = a.categoria_desc.trim();
            contagem[cat] = (contagem[cat] || 0) + 1;
        }
    });
    const arr = Object.keys(contagem).map(key => ({ nome: key, count: contagem[key] })).sort((a, b) => b.count - a.count).slice(0, 4);
    const max = Math.max(...arr.map(d => d.count), 1);
    return arr.map(item => ({ ...item, percent: (item.count / max) * 100 }));
});
const maxCategoriaCount = computed(() => categoriaData.value.length === 0 ? 10 : Math.max(...categoriaData.value.map(d => d.count)));


const formatarMoeda = (valor) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);
const formatarDataCurta = (dataString) => {
    if (!dataString) return '---';
    const data = new Date(dataString + 'T00:00:00');
    const dia = String(data.getDate()).padStart(2, '0');
    const mes = data.toLocaleString('pt-BR', { month: 'short' }).replace('.', '');
    return `${dia} de ${mes}.`;
};
</script>

<style scoped>
.dashboard-page {
    padding: 20px 40px;
    background-color: #f9f2ec;
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, sans-serif;
}

.top-bar {
    border-bottom: 1px solid #ebdcd1;
    padding-bottom: 10px;
    margin-bottom: 25px;
    display: block;
}

.current-date {
    color: #8a7b72;
    font-size: 14px;
    margin: 0;
    text-transform: lowercase;
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

.filtro-proprietario-custom {
    position: relative;
    display: flex;
    align-items: center;
    border: 1.5px solid #ff7322;
    border-radius: 6px;
    background-color: #ffffff;
    height: 42px;
    min-width: 240px;
    transition: box-shadow 0.2s;
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
    z-index: 1;
    pointer-events: none;
}

.icon-seta {
    width: 16px;
    height: 16px;
    color: #ff7322;
    position: absolute;
    right: 12px;
    z-index: 1;
    pointer-events: none;
}

.filtro-proprietario-custom select {
    position: relative;
    z-index: 10;
    width: 100%;
    height: 100%;
    padding: 0 35px 0 40px;
    border: none;
    background: transparent;
    color: #ff7322;
    font-weight: 500;
    font-size: 14px;
    appearance: none;
    -webkit-appearance: none;
    cursor: pointer;
    outline: none;
}

.filtro-proprietario-custom select option {
    color: #334155;
    background: white;
}

.dashboard-grid {
    display: flex;
    gap: 20px;
    margin-bottom: 25px;
}

/* ROW 1: KPIS */
.top-kpis .kpi-card {
    flex: 1;
    background: #ffffff;
    border-radius: 8px;
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
}

.border-green {
    border-left: 4px solid #0b9e15;
    border-top: 1px solid #f0e6de;
    border-right: 1px solid #f0e6de;
    border-bottom: 1px solid #f0e6de;
}

.border-orange {
    border-left: 4px solid #ff7322;
    border-top: 1px solid #f0e6de;
    border-right: 1px solid #f0e6de;
    border-bottom: 1px solid #f0e6de;
}

.border-yellow {
    border-left: 4px solid #eab308;
    border-top: 1px solid #f0e6de;
    border-right: 1px solid #f0e6de;
    border-bottom: 1px solid #f0e6de;
}

.kpi-content {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.kpi-title {
    font-size: 11px;
    color: #94a3b8;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.kpi-value {
    font-size: 26px;
    font-weight: 800;
    color: #1e293b;
    line-height: 1;
}

.kpi-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.kpi-icon svg {
    width: 20px;
    height: 20px;
}

.bg-green {
    background-color: #0b9e15;
}

.bg-orange {
    background-color: #ff7322;
}

.bg-yellow {
    background-color: #eab308;
}

.bg-red {
    background-color: #ef4444;
}

.text-green {
    color: #0b9e15;
}

.text-red {
    color: #ef4444;
}

/* ROW 2: FINANCEIRO E PERDAS */
.middle-section {
    align-items: stretch;
}

.finance-card {
    flex: 2;
    background: #ffffff;
    border-radius: 8px;
    padding: 25px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
    border-left: 4px solid #ef4444;
    border-top: 1px solid #f0e6de;
    border-right: 1px solid #f0e6de;
    border-bottom: 1px solid #f0e6de;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.finance-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 30px;
}

.finance-main {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.finance-title {
    font-size: 12px;
    color: #94a3b8;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.finance-value {
    font-family: "Anton SC", sans-serif;
    font-size: 38px;
    line-height: 1;
}

.finance-icon {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.finance-icon svg {
    width: 22px;
    height: 22px;
}

.finance-details {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    padding-top: 20px;
    border-top: 1px solid #f1f5f9;
}

.detail-col {
    display: flex;
    flex-direction: column;
    gap: 5px;
    min-width: 20%;
}

.detail-label {
    font-size: 10px;
    color: #94a3b8;
    font-weight: 700;
    text-transform: uppercase;
}

.detail-val {
    font-size: 16px;
    font-weight: 700;
}

.deaths-card {
    flex: 1;
    background: #ffffff;
    border-radius: 8px;
    padding: 25px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
    border-left: 4px solid #fdba74;
    border-top: 1px solid #f0e6de;
    border-right: 1px solid #f0e6de;
    border-bottom: 1px solid #f0e6de;
    display: flex;
    flex-direction: column;
}

.bg-orange-light {
    background-color: #ffedd5;
    color: #ea580c;
}

.deaths-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;
}

.deaths-main {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.deaths-title {
    font-size: 11px;
    color: #94a3b8;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.deaths-value {
    font-family: "Anton SC", sans-serif;
    font-size: 32px;
    color: #ea580c;
    line-height: 1;
}

.deaths-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.deaths-icon svg {
    width: 20px;
    height: 20px;
}

.deaths-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex-grow: 1;
}

.death-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    padding-bottom: 6px;
    border-bottom: 1px dashed #f1f5f9;
}

.death-name {
    color: #334155;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
}

.causa-badge {
    background-color: #f1f5f9;
    color: #64748b;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
}

.death-date {
    color: #94a3b8;
}

.empty-list {
    font-size: 12px;
    color: #94a3b8;
    font-style: italic;
}

/* ROW 3: ALERTA DE SAÚDE */
.alert-box {
    background-color: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 8px;
    padding: 15px 20px;
    margin-bottom: 25px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.alert-header {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #dc2626;
    font-weight: 700;
    font-size: 12px;
    letter-spacing: 0.5px;
}

.alert-header svg {
    width: 18px;
    height: 18px;
}

.alert-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding-left: 28px;
}

.alert-item {
    font-size: 13px;
    color: #b91c1c;
}

.success-msg {
    color: #15803d;
    font-style: italic;
}

/* ROW 4: GRÁFICOS (3 COLUNAS AGORA) */
.charts-section {
    flex-wrap: wrap;
}

.charts-section .chart-card {
    flex: 1;
    min-width: 30%;
    background: #ffffff;
    border-radius: 8px;
    padding: 25px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
    border: 1px solid #f0e6de;
}

.chart-title {
    font-family: "Anton SC", sans-serif;
    font-size: 18px;
    color: #ff7322;
    margin: 0 0 30px 0;
    text-transform: uppercase;
}

.pie-chart-container {
    display: flex;
    align-items: center;
    justify-content: space-around;
    padding: 10px;
}

.pie-chart {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    flex-shrink: 0;
}

.pie-legends {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    color: #ff7322;
    font-weight: 500;
}

.dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
}

.bar-chart-container {
    display: flex;
    height: 180px;
    gap: 10px;
    padding-top: 10px;
}

.y-axis {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    color: #94a3b8;
    font-size: 11px;
    padding-bottom: 25px;
    padding-right: 10px;
    border-right: 1px dashed #e2e8f0;
}

.bars-area {
    display: flex;
    flex-grow: 1;
    justify-content: space-around;
    align-items: flex-end;
    padding-bottom: 25px;
    position: relative;
}

.bar-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 40px;
    height: 100%;
    justify-content: flex-end;
    position: relative;
}

.bar-fill {
    width: 24px;
    background-color: #ff7322;
    border-radius: 4px 4px 0 0;
    position: relative;
    transition: height 0.5s;
    min-height: 2px;
}

.bar-fill.bg-blue {
    background-color: #3b82f6;
}

.bar-tooltip {
    position: absolute;
    top: -22px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 11px;
    font-weight: 700;
    color: #ff7322;
}

.bar-tooltip.text-blue {
    color: #3b82f6;
}

.bar-label {
    position: absolute;
    bottom: -25px;
    font-size: 10px;
    color: #64748b;
    text-align: center;
    width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

@media (max-width: 1100px) {
    .charts-section .chart-card {
        min-width: 100%;
    }
}

@media (max-width: 768px) {
    .dashboard-grid {
        flex-direction: column;
    }

    .page-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }

    .filtro-proprietario-custom {
        width: 100%;
    }

    .finance-details {
        flex-direction: column;
        gap: 10px;
    }
}
</style>