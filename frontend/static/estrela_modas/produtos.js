import { iniciarTela } from './shared.js'

export default function iniciarProdutos() {
  iniciarTela('produtos')

  const campoBusca = document.querySelector('[data-busca-produto]')
  const produtos = [...document.querySelectorAll('[data-produto]')].map(elemento => ({
    nomeProduto: elemento.dataset.nomeProduto,
    elemento,
  }))

  campoBusca?.addEventListener('input', () => {
    filtrarProdutos(produtos, campoBusca.value)
  })
}

function filtrarProdutos(produtos, termoBusca) {
  const resultados = new Set(buscarProduto(produtos, termoBusca))
  produtos.forEach(produto => {
    produto.elemento.hidden = !resultados.has(produto)
  })
}

export function buscarProduto(produtos, termoBusca) {
  const buscaNormalizada = termoBusca.toLocaleLowerCase('pt-BR').trim()

  return produtos.filter(produto => {
    return produto.nomeProduto.toLocaleLowerCase('pt-BR').includes(buscaNormalizada)
  })
}

if (typeof document !== 'undefined') iniciarProdutos()
