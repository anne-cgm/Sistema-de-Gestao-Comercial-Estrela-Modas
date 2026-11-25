
import "./shared.js"

export default function iniciarLogin() {
  // FORMULÁRIO DE LOGIN
  const formulario = document.querySelector('[data-login-form]')

  formulario?.addEventListener('submit', fazerLogin)

  const botaoAbrirRecuperacao = document.querySelector('[data-abrir-recuperacao]')
  const dialogoRecuperacao = document.querySelector('[data-recuperar-senha]')
  const botaoFecharRecuperacao = dialogoRecuperacao?.querySelector('[data-fechar-recuperacao]')
  const etapaEmail = dialogoRecuperacao?.querySelector('[data-etapa-email-recuperacao]')
  const etapaCodigo = dialogoRecuperacao?.querySelector('[data-etapa-codigo-recuperacao]')
  const etapaSenha = dialogoRecuperacao?.querySelector('[data-etapa-senha-recuperacao]')
  const resultadoRecuperacao = dialogoRecuperacao?.querySelector('[data-resultado-recuperacao]')
  const formularioEmail = dialogoRecuperacao?.querySelector('[data-formulario-email-recuperacao]')
  const formularioCodigo = dialogoRecuperacao?.querySelector('[data-formulario-codigo-recuperacao]')
  const formularioSenha = dialogoRecuperacao?.querySelector('[data-formulario-senha-recuperacao]')

  function exibirEtapa(etapa) {
    if (!etapaEmail || !etapaCodigo || !etapaSenha) return

    etapaEmail.hidden = etapa !== etapaEmail
    etapaCodigo.hidden = etapa !== etapaCodigo
    etapaSenha.hidden = etapa !== etapaSenha
    etapa.querySelector('input')?.focus()
  }

  function exibirResultado(mensagem) {
    if (!resultadoRecuperacao) return
    resultadoRecuperacao.textContent = mensagem
    resultadoRecuperacao.hidden = false
  }

  function reiniciarRecuperacao() {
    formularioEmail?.reset()
    formularioCodigo?.reset()
    formularioSenha?.reset()
    if (resultadoRecuperacao) {
      resultadoRecuperacao.textContent = ''
      resultadoRecuperacao.hidden = true
    }
    if (etapaEmail) exibirEtapa(etapaEmail)
  }

  botaoAbrirRecuperacao?.addEventListener('click', () => {
    if (dialogoRecuperacao && !dialogoRecuperacao.open) {
      reiniciarRecuperacao()
      dialogoRecuperacao.showModal()
    }
  })

  botaoFecharRecuperacao?.addEventListener('click', () => {
    dialogoRecuperacao.close()
  })

  dialogoRecuperacao?.addEventListener('close', reiniciarRecuperacao)

  formularioEmail?.addEventListener('submit', evento => {
    evento.preventDefault()
    exibirResultado('A existência deste e-mail ainda não foi consultada. A próxima etapa é apenas uma prévia.')
    if (etapaCodigo) exibirEtapa(etapaCodigo)
  })

  formularioCodigo?.addEventListener('submit', evento => {
    evento.preventDefault()
    exibirResultado('Este código não foi validado. A próxima etapa é apenas uma prévia.')
    if (etapaSenha) exibirEtapa(etapaSenha)
  })

  formularioSenha?.addEventListener('submit', evento => {
    evento.preventDefault()
    const senha = formularioSenha.elements.novaSenha.value
    const confirmacao = formularioSenha.elements.confirmarSenha.value

    if (senha !== confirmacao) {
      exibirResultado('As senhas informadas não são iguais.')
      return
    }

    exibirResultado('Prévia concluída. A senha não foi alterada; esta etapa ainda não está conectada ao servidor.')
  })

  dialogoRecuperacao?.querySelectorAll('[data-voltar-etapa-recuperacao]').forEach(botao => {
    botao.addEventListener('click', () => {
      const etapaAnterior = {
        email: etapaEmail,
        codigo: etapaCodigo,
      }[botao.dataset.voltarEtapaRecuperacao]

      if (etapaAnterior) exibirEtapa(etapaAnterior)
    })
  })

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
