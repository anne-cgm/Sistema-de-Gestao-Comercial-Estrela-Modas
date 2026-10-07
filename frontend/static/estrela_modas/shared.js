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
}

export function navegarParaTela(tela) {
  const caminho = caminhosDasTelas[tela]
  if (caminho) window.location.href = caminho
}

export function iniciarTela(abaAtiva) {
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

export function exibirMensagem(mensagem) {
  document.querySelector('.toast')?.remove()
  const aviso = document.createElement('div')
  aviso.className = 'toast'
  aviso.textContent = mensagem
  document.body.append(aviso)
  window.setTimeout(() => aviso.remove(), 2200)
}
