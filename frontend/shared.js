const caminhosDasTelas = {
  login: './login.html',
  dashboard: './dashboard.html',
  produtos: './produtos.html',
  'novo-produto': './novo-produto.html',
  estoque: './estoque.html',
  'nova-venda': './nova-venda.html',
  clientes: './clientes.html',
  debitos: './debitos.html',
  mais: './mais.html',
  relatorios: './relatorios.html',
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
