import { exibirMensagem, iniciarTela } from './shared.js'

export default function iniciarNovaVenda() {
  iniciarTela('venda')
  atualizarTotalVenda()

  document.querySelectorAll('[data-forma-pagamento]').forEach(botaoFormaPagamento => {
    botaoFormaPagamento.addEventListener('click', () => {
      selecionarFormaDePagamento(botaoFormaPagamento)
    })
  })

  document.querySelector('[data-finish-sale]')?.addEventListener('click', () => {
    finalizarVenda()
  })
}

function selecionarFormaDePagamento(botaoFormaPagamento) {
  document.querySelector('.payment.is-active')?.classList.remove('is-active')
  botaoFormaPagamento.classList.add('is-active')
}

function finalizarVenda() {
  exibirMensagem('Venda finalizada com sucesso.')
}

function atualizarTotalVenda() {
  const itensVenda = [...document.querySelectorAll('[data-item-venda]')].map(itemVenda => ({
    precoVenda: Number(itemVenda.dataset.precoVenda),
    quantidade: Number(itemVenda.dataset.quantidade),
  }))
  const descontoAplicado = Number(
    document.querySelector('[data-desconto-aplicado]')?.dataset.descontoAplicado ?? 0,
  )
  const valorTotal = calcularTotalVenda(itensVenda, descontoAplicado)
  const elementoValorTotal = document.querySelector('[data-valor-total]')

  if (elementoValorTotal) elementoValorTotal.textContent = formatarMoeda(valorTotal)
}

export function calcularTotalVenda(itensVenda, descontoAplicado = 0) {
  const subtotal = itensVenda.reduce((valorAcumulado, itemVenda) => {
    return valorAcumulado + itemVenda.precoVenda * itemVenda.quantidade
  }, 0)

  const percentualDesconto = Math.min(Math.max(descontoAplicado, 0), 100)
  return Number((subtotal - (subtotal * percentualDesconto) / 100).toFixed(2))
}

export function formatarMoeda(valor) {
  return valor.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })
}

if (typeof document !== 'undefined') iniciarNovaVenda()
