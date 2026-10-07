import { iniciarTela } from './shared.js'

export default function iniciarEstoque() {
  iniciarTela('mais')

  document.querySelectorAll('[data-item-estoque]').forEach(itemEstoque => {
    const quantidadeEstoque = Number(itemEstoque.dataset.quantidadeEstoque)
    itemEstoque.classList.toggle('card--alert', produtoComEstoqueBaixo(quantidadeEstoque))
  })
}

export function produtoComEstoqueBaixo(quantidadeEstoque, estoqueMinimo = 1) {
  return quantidadeEstoque <= estoqueMinimo
}

if (typeof document !== 'undefined') iniciarEstoque()
