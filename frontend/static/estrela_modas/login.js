export default function iniciarLogin() {
  const formulario = document.querySelector('[data-login-form]')
  formulario?.addEventListener('submit', fazerLogin)
}

function fazerLogin(evento) {
  const formulario = evento.currentTarget
  const usuario = formulario.elements.usuario.value
  const senha = formulario.elements.senha.value

  if (!validarLogin(usuario, senha)) {
    evento.preventDefault()
    exibirErroLogin(formulario, 'Preencha usuário e senha para continuar.')
  }
}

export function validarLogin(usuario, senha) {
  return usuario.trim() !== '' && senha.trim() !== ''
}

function exibirErroLogin(formulario, mensagem) {
  const erro = formulario.querySelector('[data-erro-login]')
  if (!erro) return

  erro.textContent = mensagem
  erro.hidden = false
}

if (typeof document !== 'undefined') iniciarLogin()
