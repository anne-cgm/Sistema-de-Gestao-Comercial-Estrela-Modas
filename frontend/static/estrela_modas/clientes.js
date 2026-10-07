import { exibirMensagem, iniciarTela } from './shared.js'

export default function iniciarClientes() {
  iniciarTela('clientes')
  document.querySelector('[data-new-client]')?.addEventListener('click', () => {
    exibirMensagem('Cadastro de cliente pronto para preenchimento.')
  })
}

if (typeof document !== 'undefined') iniciarClientes()
