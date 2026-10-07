import { iniciarTela } from './shared.js'

export default function iniciarNovaVenda() {
  iniciarTela('venda')
  atualizarTotalVenda()
  document.querySelector('[data-form-venda]')?.addEventListener('input', atualizarTotalVenda)
  document.querySelector('[data-form-venda]')?.addEventListener('change', atualizarTotalVenda)
}

function atualizarTotalVenda() {
  const subtotal = [...document.querySelectorAll('[data-produto-venda]')].reduce((total, seletor) => {
    const produto = seletor.selectedOptions[0]
    const campoQuantidade = document.querySelector(`[name="${seletor.name.replace(/produto$/, 'quantidade')}"]`)
    return total + Number(produto?.dataset.precoVenda ?? 0) * Number(campoQuantidade?.value ?? 0)
  }, 0)
  const desconto = Number(document.querySelector('[name="desconto_aplicado"]')?.value ?? 0)
  const valorTotal = Math.max(0, subtotal - desconto)
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
