import { exibirMensagem, iniciarTela } from './shared.js'

export default function iniciarMais() {
  iniciarTela('mais')
  document.querySelectorAll('[data-module]').forEach(botao => {
    botao.addEventListener('click', () => exibirMensagem(`${botao.dataset.module} em breve.`))
  })
}

if (typeof document !== 'undefined') iniciarMais()
