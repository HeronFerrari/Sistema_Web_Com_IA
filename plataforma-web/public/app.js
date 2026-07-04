// ============================================================
// PROAGRO Smart — Front-end Application Logic
// Comunica com o back-end Node.js/Express em http://localhost:3000
// ============================================================

// app.js (Front-end)
const API_PROPOSTAS = 'http://localhost:3000/propostas';

// ============================================================
// STATE & NAVIGATION
// ============================================================
function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  const target = document.getElementById(id);
  if (target) {
    target.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'instant' });
  }
}

// ============================================================
// UTILS
// ============================================================
const Mask = {
  applyCpf(input) {
    if (!input) return;
    input.addEventListener('input', () => {
      let v = input.value.replace(/\D/g, '');
      if (v.length > 11) v = v.slice(0, 11);
      if (v.length > 9) v = v.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
      else if (v.length > 6) v = v.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
      else if (v.length > 3) v = v.replace(/(\d{3})(\d{1,3})/, '$1.$2');
      input.value = v;
    });
  },
  rawCpf(formatted) {
    return formatted.replace(/\D/g, '');
  },
  isValidCpf(formatted) {
    return this.rawCpf(formatted).length === 11;
  },
  formatCpf(raw) {
    const d = String(raw).replace(/\D/g, '').padStart(11, '0');
    return d.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
  },
  formatBRL(value) {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
  }
};

const UI = {
  showToast(message) {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = `⚠️  ${message}`;
    document.body.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.3s ease';
      setTimeout(() => toast.remove(), 320);
    }, 5000);
  },
  
  showLoading() {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.id = 'loading-overlay';
    overlay.innerHTML = `
      <div class="loading-spinner"></div>
      <div class="loading-title">🤖 Motor de IA processando...</div>
      <div class="loading-steps" id="ls-steps"></div>
    `;
    document.body.appendChild(overlay);

    const steps = [
      { icon: '📋', text: 'Verificando Regras MCR — Sistema Especialista...' },
      { icon: '🕸️', text: 'Analisando Rede de Grafos de Relacionamento...' },
      { icon: '🧠', text: 'Executando modelo Random Forest (Machine Learning)...' },
      { icon: '💾', text: 'Salvando resultado no PostgreSQL via Prisma...' },
    ];

    const container = overlay.querySelector('#ls-steps');
    steps.forEach((step, i) => {
      setTimeout(() => {
        if (!document.getElementById('loading-overlay')) return;
        const el = document.createElement('div');
        el.className = 'loading-step';
        el.innerHTML = `<span class="step-check">${step.icon}</span> ${step.text}`;
        container.appendChild(el);
      }, i * 750);
    });
  },

  hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
      overlay.style.opacity = '0';
      overlay.style.transition = 'opacity 0.3s ease';
      setTimeout(() => overlay.remove(), 320);
    }
  },

  setupToggle(checkboxId, labelId, onText, offText, isDanger) {
    const checkbox = document.getElementById(checkboxId);
    const label = document.getElementById(labelId);
    if (!checkbox || !label) return;

    const refresh = () => {
      if (checkbox.checked) {
        label.textContent = onText;
        label.style.color = isDanger ? 'var(--danger)' : 'var(--primary)';
      } else {
        label.textContent = offText;
        label.style.color = 'var(--txt-3)';
      }
    };
    checkbox.addEventListener('change', refresh);
    refresh(); // initial state
  },

  updateScore(val) {
    const display = document.getElementById('score-value');
    const tag = document.getElementById('score-tag');
    if (!display || !tag) return;

    display.textContent = val;
    if (val < 500) {
      display.style.color = 'var(--danger)';
      tag.textContent = 'Baixo';
      tag.className = 'tag tag-danger';
    } else if (val < 700) {
      display.style.color = 'var(--warning)';
      tag.textContent = 'Moderado';
      tag.className = 'tag tag-warning';
    } else {
      display.style.color = 'var(--success)';
      tag.textContent = 'Bom';
      tag.className = 'tag tag-success';
    }
  }
};

// ============================================================
// INITIALIZATION
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
  // Configura máscara
  Mask.applyCpf(document.getElementById('f-cpf'));

  // Configura Toggles
  UI.setupToggle('f-cpf-regular', 'lbl-cpf-regular', 'Sim — Regular', 'Não — Irregular', false);
  UI.setupToggle('f-car-regular', 'lbl-car-regular', 'Sim — Regular', 'Não — Irregular', false);
  UI.setupToggle('f-divergencia', 'lbl-divergencia', 'Sim — Divergente ⚠', 'Não — OK', true);
  UI.setupToggle('f-restricoes',  'lbl-restricoes',  'Sim — Há restrições ⚠', 'Não — Sem restrições', true);

  // Configura Slider de Score
  const scoreSlider = document.getElementById('f-score');
  if (scoreSlider) {
    scoreSlider.addEventListener('input', (e) => UI.updateScore(parseInt(e.target.value, 10)));
    UI.updateScore(parseInt(scoreSlider.value, 10)); // setup initial
  }

  // Configura Formulário
  const form = document.getElementById('form-proposta');
  if (form) {
    form.addEventListener('submit', handleFormSubmit);
  }

  // Configura Botão Nova Análise
  const btnNova = document.getElementById('btn-nova-analise');
  if (btnNova) {
    btnNova.addEventListener('click', () => {
      form.reset();
      if (scoreSlider) {
        scoreSlider.value = 600;
        UI.updateScore(600);
      }
      // Re-trigger toggle events to update labels
      ['f-cpf-regular', 'f-car-regular', 'f-divergencia', 'f-restricoes'].forEach(id => {
        const el = document.getElementById(id);
        if(el) el.dispatchEvent(new Event('change'));
      });
      showScreen('screen-form');
    });
  }
});


// ============================================================
// FORM SUBMISSION
// ============================================================
async function handleFormSubmit(e) {
  e.preventDefault();

  const nome = document.getElementById('f-nome').value.trim();
  const cpf = document.getElementById('f-cpf').value.trim();
  const car = document.getElementById('f-car').value.trim();
  const valor = parseFloat(document.getElementById('f-valor').value);
  const operacoes = parseFloat(document.getElementById('f-operacoes').value) || 0;
  
  const score = parseInt(document.getElementById('f-score').value, 10);
  const recusadas = parseInt(document.getElementById('f-recusadas').value, 10) || 0;
  const inadimplencia = parseFloat(document.getElementById('f-inadimplencia').value) || 0.05;

  const cpfRegular = document.getElementById('f-cpf-regular').checked;
  const carRegular = document.getElementById('f-car-regular').checked;
  const divergencia = document.getElementById('f-divergencia').checked ? 1 : 0;
  const restricoes = document.getElementById('f-restricoes').checked ? 1 : 0;

  // Validações
  if (!nome) return UI.showToast('Preencha o nome do produtor.');
  if (!Mask.isValidCpf(cpf)) return UI.showToast('CPF do produtor inválido.');
  if (!car) return UI.showToast('Preencha o Código do CAR.');
  if (!valor || valor <= 0) return UI.showToast('Informe um valor solicitado válido.');

  const payload = {
    nome_produtor: nome,
    cpf_produtor: Mask.rawCpf(cpf),
    car_propriedade: car,
    valor_solicitado: valor,
    operacoes_ativas_valor: operacoes,
    cpf_regular: cpfRegular,
    car_regular: carRegular,
    score_credito: score,
    solicitacoes_recusadas: recusadas,
    divergencia_area_car: divergencia,
    historico_restricoes: restricoes,
    indice_inadimplencia_regiao: inadimplencia
  };

  const btnAnalisar = document.getElementById('btn-analisar');
  const btnText = btnAnalisar.querySelector('.btn-text');
  const btnLoader = btnAnalisar.querySelector('.btn-loading');

  btnText.classList.add('hidden');
  btnLoader.classList.remove('hidden');
  btnAnalisar.disabled = true;
  
  UI.showLoading();

  try {
    const response = await fetch(API_PROPOSTAS, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    UI.hideLoading();

    if (!response.ok) {
      throw new Error(data.erro || `Erro ${response.status} ao processar.`);
    }

    renderDashboard(data, payload);

  } catch (err) {
    UI.hideLoading();
    UI.showToast(err.message || 'Falha na comunicação com o servidor.');
  } finally {
    btnText.classList.remove('hidden');
    btnLoader.classList.add('hidden');
    btnAnalisar.disabled = false;
  }
}

// ============================================================
// RESULT RENDERER
// ============================================================
function renderDashboard(data, input) {
  const isApproved = (data.status_analise ?? data.status) === 'Aprovado';
  const statusClass = isApproved ? 'approved' : 'blocked';
  const tecnica = data.tecnica_bloqueio || 'Nenhuma';
  const justificativas = Array.isArray(data.justificativas) ? data.justificativas : [];

  // 1. Atualizar Background e Card
  document.getElementById('result-bg').className = `result-bg ${statusClass}`;
  document.getElementById('result-card').className = `result-card ${statusClass}`;

  // 2. Veredito Header
  document.getElementById('veredito-icon').textContent = isApproved ? '✅' : '🚫';
  
  const titulo = document.getElementById('veredito-titulo');
  titulo.textContent = isApproved ? 'CRÉDITO APROVADO' : 'CRÉDITO BLOQUEADO';
  titulo.className = `veredito-titulo ${statusClass}`;

  const badge = document.getElementById('veredito-badge');
  badge.textContent = isApproved ? '✓ Aprovado em todos os critérios' : '⚠️ Bloqueado pela análise de IA';
  badge.className = `veredito-badge ${statusClass}`;

  // 3. Técnica
  document.getElementById('tecnica-usada').innerHTML = `<span class="tecnica-chip">Técnica: ${tecnica}</span>`;

  // 4. Justificativas
  const list = document.getElementById('justificativas-list');
  list.className = `justificativas-list ${statusClass}`;
  list.innerHTML = justificativas.map(j => `<li><span class="bullet"></span><span>${j}</span></li>`).join('');

  // 5. Chips Resumo
  document.getElementById('proposta-chips').innerHTML = `
    <div class="chip"><strong>${input.nome_produtor}</strong><span>Produtor</span></div>
    <div class="chip"><strong>${Mask.formatCpf(input.cpf_produtor)}</strong><span>CPF</span></div>
    <div class="chip"><strong>${input.car_propriedade}</strong><span>CAR</span></div>
    <div class="chip"><strong>${Mask.formatBRL(input.valor_solicitado)}</strong><span>Solicitado</span></div>
    <div class="chip"><strong>${input.score_credito} pts</strong><span>Score</span></div>
  `;

  // 6. Timestamp
  document.getElementById('result-timestamp').textContent = `Análise realizada em ${new Date().toLocaleString('pt-BR')}`;

  showScreen('screen-result');
}
