  // INTEGRAÇÃO COM DJANGO:
  // - A listagem de dívidas é renderizada pelo template Django.
  // - O total pendente e os saldos vêm da view.
  // - O formulário envia os dados por POST para a view.
  // - Os pagamentos recentes são carregados pelo Django.
  //
  // FUNCIONALIDADES FUTURAS:
  // - Implementar o uso de crédito da loja para quitar dívidas.
  //   Essa funcionalidade precisa ser integrada aos modelos,
  //   formulários e views do Django para registrar os movimentos
  //   de crédito no banco de dados.
  // - Caso necessário, implementar filtros e atualização dinâmica
  //   das informações sem recarregar a página.


import { iniciarTela } from './shared.js'

export default function iniciarDebitos() {
  // Marca a opção de clientes como ativa no menu.
  iniciarTela('clientes')

  // Elementos responsáveis pelo menu lateral.
  const menu = document.querySelector('[data-menu]')
  const fundo = document.querySelector('[data-fundo-menu]')
  const alternar = document.querySelector('[data-alternar-menu]')
  const fechar = document.querySelector('[data-fechar-menu]')

  // Fecha o menu e restaura o estado da página.
  function fecharMenu() {
    menu?.classList.remove('is-open')

    if (fundo) fundo.hidden = true

    document.body.classList.remove('menu-sobreposto')
    alternar?.setAttribute('aria-expanded', 'false')
  }

  // Abre o menu lateral.
  alternar?.addEventListener('click', () => {
    menu?.classList.add('is-open')

    if (fundo) fundo.hidden = false

    document.body.classList.add('menu-sobreposto')
    alternar.setAttribute('aria-expanded', 'true')
  })

  // Fecha o menu pelo botão ou pelo fundo escuro.
  fechar?.addEventListener('click', fecharMenu)
  fundo?.addEventListener('click', fecharMenu)

  // Também permite fechar o menu pressionando Esc.
  document.addEventListener('keydown', evento => {
    if (evento.key === 'Escape') fecharMenu()
  })

  // Os dados de dívidas, pagamentos e saldos são carregados
  // diretamente pelo Django no HTML.
  // O formulário de pagamento também é processado pela view.
}

if (typeof document !== 'undefined') iniciarDebitos()

