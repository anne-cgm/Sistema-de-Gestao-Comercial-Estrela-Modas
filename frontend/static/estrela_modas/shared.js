const caminhosDasTelas = {
  login: '/login/',
  dashboard: '/dashboard/',
  produtos: '/produtos/',
  'novo-produto': '/produtos/novo/',
  estoque: '/estoque/',
  'nova-venda': '/vendas/nova/',
  clientes: '/clientes/',
  debitos: '/debitos/',
  mais: '/mais/',
  relatorios: '/relatorios/',
  compras: '/compras/',
  despesas: '/despesas/',
  trocas: '/trocas/',
}

export function navegarParaTela(tela) {
  const caminho = caminhosDasTelas[tela]
  if (caminho) window.location.href = caminho
}

export function iniciarTela(abaAtiva) {
  iniciarMenuLateral()

  document.querySelectorAll('[data-screen]').forEach(elemento => {
    elemento.addEventListener('click', evento => {
      evento.preventDefault()
      navegarParaTela(elemento.dataset.screen)
    })
  })

  if (abaAtiva) {
    document.querySelector(`[data-tab="${abaAtiva}"]`)?.classList.add('is-active')
  }
}

export function iniciarMenuLateral() {
  const menu = document.querySelector('[data-menu]')
  if (!menu) return

  const fundo = document.querySelector('[data-fundo-menu]')
  const alternar = document.querySelector('[data-alternar-menu]')
  const fechar = document.querySelector('[data-fechar-menu]')

  const fecharMenu = () => {
    menu.classList.remove('is-open')
    if (fundo) fundo.hidden = true
    document.body.classList.remove('menu-sobreposto')
    alternar?.setAttribute('aria-expanded', 'false')
  }

  alternar?.addEventListener('click', () => {
    menu.classList.add('is-open')
    if (fundo) fundo.hidden = false
    document.body.classList.add('menu-sobreposto')
    alternar.setAttribute('aria-expanded', 'true')
  })
  fechar?.addEventListener('click', fecharMenu)
  fundo?.addEventListener('click', fecharMenu)
  document.addEventListener('keydown', evento => {
    if (evento.key === 'Escape') fecharMenu()
  })
}

export function exibirMensagem(mensagem) {
  document.querySelector('.toast')?.remove()
  const aviso = document.createElement('div')
  aviso.className = 'toast'
  aviso.textContent = mensagem
  document.body.append(aviso)
  window.setTimeout(() => aviso.remove(), 2200)
}
