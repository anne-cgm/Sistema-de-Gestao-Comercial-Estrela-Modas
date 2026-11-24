import { iniciarTela } from './shared.js'

// FUTURO: os dados dos períodos deverão vir da view do Django.
// A estrutura abaixo serve como referência para a implementação
// dos filtros de hoje, últimos 7 dias e mês.

// Calcula o percentual de uma meta comercial.
// Esta função poderá ser utilizada quando os dados reais
// de faturamento e meta estiverem disponíveis.
export function calcularPercentualMeta(valorRealizado, metaPeriodo) {
  if (!metaPeriodo || metaPeriodo <= 0) return 0

  const percentual = Math.round((valorRealizado / metaPeriodo) * 100)

  return Math.min(100, Math.max(0, percentual))
}

// FUTURO: receber os dados reais do Django para cada período.
// Não inserir valores fictícios nesta função.

// FUTURO: renderizar gráfico com os valores reais de vendas.
// A estrutura visual já está preparada no HTML.
function renderizarBarrasVendas(gradeBarras, serieVendas) {
  if (!gradeBarras || !serieVendas) return

  const maiorValor = Math.max(
    ...serieVendas.map((item) => item.valor),
    1,
  )

  gradeBarras.style.setProperty(
    '--colunas-grafico',
    String(serieVendas.length),
  )

  gradeBarras.innerHTML = serieVendas
    .map((item) => {
      const altura = Math.max(
        16,
        Math.round((item.valor / maiorValor) * 100),
      )

      const classeDestaque = item.destaque ? ' is-peak' : ''

      return `
        <div class="chart-col${classeDestaque}">
          <span class="chart-amount">${item.valorCurto}</span>
          <div class="chart-track">
            <div class="chart-bar" style="height: ${altura}%"></div>
          </div>
          <span class="chart-label">${item.rotulo}</span>
        </div>
      `
    })
    .join('')
}

// FUTURO: renderizar os meios de pagamento com os dados
// reais das vendas e dos recebimentos.
function renderizarMeiosPagamento(listaPagamentos, meiosPagamento) {
  if (!listaPagamentos || !meiosPagamento) return

  listaPagamentos.innerHTML = meiosPagamento
    .map(
      (item) => `
        <div class="meter-item">
          <div class="meter-head">
            <span class="meter-name">${item.metodo}</span>
            <span class="meter-values">
              <strong>${item.valor}</strong> · ${item.percentual}%
            </span>
          </div>

          <div class="meter-track">
            <div class="meter-fill" style="width: ${item.percentual}%"></div>
          </div>
        </div>
      `,
    )
    .join('')
}

// FUTURO: atualizar os indicadores, gráfico e meios de pagamento
// conforme o período selecionado, utilizando dados reais do Django.
function atualizarPainelPeriodo(periodo, dados) {
  if (!dados) return

  const percentualMeta = calcularPercentualMeta(
    dados.valorRealizado,
    dados.metaPeriodo,
  )

  const definirTexto = (seletor, texto) => {
    const elemento = document.querySelector(seletor)

    if (elemento) elemento.textContent = texto
  }

  definirTexto('[data-kpi-faturamento]', dados.faturamento)
  definirTexto('[data-kpi-faturamento-detalhe]', dados.faturamentoDetalhe)
  definirTexto('[data-kpi-lucro]', dados.lucro)
  definirTexto('[data-kpi-lucro-detalhe]', dados.lucroDetalhe)
  definirTexto('[data-kpi-ticket]', dados.ticketMedio)
  definirTexto('[data-kpi-ticket-detalhe]', dados.ticketDetalhe)
  definirTexto('[data-grafico-pico]', dados.picoResumo)
  definirTexto('[data-meta-percentual]', `${percentualMeta}% atingida`)
  definirTexto('[data-meta-resumo]', dados.resumoMeta)

  const barraMeta = document.querySelector('[data-meta-barra]')

  if (barraMeta) {
    barraMeta.style.width = `${percentualMeta}%`
  }

  renderizarBarrasVendas(
    document.querySelector('[data-grafico-barras]'),
    dados.serieVendas,
  )

  renderizarMeiosPagamento(
    document.querySelector('[data-lista-pagamentos]'),
    dados.meiosPagamento,
  )

  document.querySelectorAll('[data-periodo-painel]').forEach((botao) => {
    const ativo = botao.dataset.periodoPainel === periodo

    botao.classList.toggle('is-active', ativo)
    botao.setAttribute('aria-pressed', String(ativo))
  })
}

// Inicialização do dashboard
export default function iniciarDashboard() {
  iniciarTela('inicio')

  // Os filtros permanecem preparados visualmente,
  // mas ainda não alteram os dados apresentados.
  // A integração será feita quando as consultas por período
  // estiverem implementadas na view do Django.
}

if (typeof document !== 'undefined') iniciarDashboard()
