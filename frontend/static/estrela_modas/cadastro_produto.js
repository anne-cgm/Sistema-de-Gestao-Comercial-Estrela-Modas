import { iniciarTela } from './shared.js'

export default function iniciarNovoProduto() {
  iniciarTela('produtos')
}

if (typeof document !== 'undefined') iniciarNovoProduto()
