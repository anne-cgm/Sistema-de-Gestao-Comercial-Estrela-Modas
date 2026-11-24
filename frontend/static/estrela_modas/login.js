
export default function iniciarLogin() {
  // FORMULÁRIO DE LOGIN
  const formulario = document.querySelector('[data-login-form]')

  formulario?.addEventListener('submit', fazerLogin)

  // ELEMENTOS DA RECUPERAÇÃO DE SENHA
  const dialogo = document.querySelector('[data-recuperar-senha]')
  const formularioRecuperacao = document.querySelector(
    '[data-formulario-recuperacao]',
  )
  const resultadoRecuperacao = document.querySelector(
    '[data-resultado-recuperacao]',
  )

  // Abre a janela de recuperação de senha.
  document
    .querySelector('[data-abrir-recuperacao]')
    ?.addEventListener('click', () => {
      formularioRecuperacao?.reset()

      if (resultadoRecuperacao) {
        resultadoRecuperacao.hidden = true
      }

      dialogo?.showModal()
      formularioRecuperacao?.elements.email?.focus()
    })

  // Fecha a janela pelo botão cancelar.
  document
    .querySelector('[data-fechar-recuperacao]')
    ?.addEventListener('click', () => {
      dialogo?.close()
    })

  // Permite fechar a janela clicando fora dela.
  dialogo?.addEventListener('click', evento => {
    if (evento.target !== dialogo) return

    const limites = dialogo.getBoundingClientRect()

    if (
      evento.clientX < limites.left ||
      evento.clientX > limites.right ||
      evento.clientY < limites.top ||
      evento.clientY > limites.bottom
    ) {
      dialogo.close()
    }
  })

  // RECUPERAÇÃO DE SENHA - FUNCIONALIDADE FUTURA
  // Impede o envio do formulário enquanto não existir uma view
  // Django responsável por processar a recuperação.
  formularioRecuperacao?.addEventListener('submit', evento => {
    evento.preventDefault()

    exibirResultadoRecuperacao(
      resultadoRecuperacao,
      'A recuperação de senha ainda não está disponível. Consulte um administrador da loja.',
      'aviso',
    )
  })

  // FUTURO: integrar a recuperação de senha ao Django.
  // Será necessário implementar a consulta do usuário, verificar
  // as permissões do perfil e criar o fluxo de redefinição da senha.
}

// Exibe uma mensagem na janela de recuperação de senha.
function exibirResultadoRecuperacao(elemento, mensagem, tipo) {
  if (!elemento) return

  elemento.textContent = mensagem
  elemento.dataset.tipo = tipo
  elemento.style.borderLeftColor =
    tipo === 'erro' ? 'var(--pink)' : 'var(--gold)'
  elemento.hidden = false
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

