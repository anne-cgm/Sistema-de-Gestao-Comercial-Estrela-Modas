
export default function iniciarLogin() {
  // FORMULÁRIO DE LOGIN
  const formulario = document.querySelector('[data-login-form]')

  formulario?.addEventListener('submit', fazerLogin)

}

// Verifica se os campos obrigatórios do login foram preenchidos.
export function validarLogin(usuario, senha) {
  return usuario.trim() !== '' && senha.trim() !== ''
}

// Processa a validação inicial do formulário de login.
function fazerLogin(evento) {
  const formulario = evento.currentTarget
  const usuario = formulario.elements.usuario.value
  const senha = formulario.elements.senha.value

  // Impede o envio somente quando os campos estão inválidos.
  if (!validarLogin(usuario, senha)) {
    evento.preventDefault()
    exibirErroLogin(
      formulario,
      'Preencha usuário e senha para continuar.',
    )
  }

  // Se os campos estiverem preenchidos, o formulário segue
  // normalmente por POST para a view Django.
}

// Exibe mensagens de erro no formulário de login.
function exibirErroLogin(formulario, mensagem) {
  const erro = formulario.querySelector('[data-erro-login]')

  if (!erro) return

  erro.textContent = mensagem
  erro.hidden = false
}

if (typeof document !== 'undefined') iniciarLogin()

