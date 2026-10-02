import { exibirMensagem, iniciarTela } from './shared.js'

export default function iniciarNovoProduto() {
  iniciarTela('produtos')
  document.querySelector('[data-product-form]')?.addEventListener('submit', evento => {
    evento.preventDefault()
  })
  document.querySelector('[data-save-product]')?.addEventListener('click', () => {
    exibirMensagem('Produto salvo com sucesso.')
  })
}

if (typeof document !== 'undefined') iniciarNovoProduto()
