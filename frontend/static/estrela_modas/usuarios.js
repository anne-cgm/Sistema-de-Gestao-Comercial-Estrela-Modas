import { iniciarTela } from './shared.js'

// Inicializa a navegação e conecta o checklist de páginas à API do Django.
iniciarTela('mais')

const listaPermissoes = document.querySelector('[data-lista-permissoes-funcionarios]')
const botaoSalvar = document.querySelector('[data-salvar-permissoes-funcionarios]')
const feedback = document.querySelector('[data-feedback-permissoes]')
const formularioUsuario = document.querySelector('[data-formulario-usuario]')
const listaUsuarios = document.querySelector('[data-lista-usuarios]')
const mensagemUsuario = document.querySelector('[data-mensagem-usuario]')
const botaoNovoUsuario = document.querySelector('[data-novo-usuario]')
const botaoCancelarUsuario = document.querySelector('[data-cancelar-usuario]')
const botaoExcluirUsuario = document.querySelector('[data-excluir-usuario]')
const painelCodigo = document.querySelector('[data-painel-codigo]')
const statusCodigo = document.querySelector('[data-status-codigo]')
const botaoGerarCodigo = document.querySelector('[data-gerar-codigo]')
const resultadoCodigo = document.querySelector('[data-codigo-gerado]')
const campoCodigo = document.querySelector('[data-valor-codigo]')
const botaoCopiarCodigo = document.querySelector('[data-copiar-codigo]')
const tituloFormularioUsuario = document.querySelector('[data-titulo-perfil-usuario]')
let usuariosCarregados = []

if (listaPermissoes && botaoSalvar && feedback) {
  carregarPermissoes()
  botaoSalvar.addEventListener('click', salvarPermissoes)
}

if (formularioUsuario && listaUsuarios) {
  carregarUsuarios()
  botaoNovoUsuario?.addEventListener('click', abrirCadastroUsuario)
  botaoCancelarUsuario?.addEventListener('click', fecharFormularioUsuario)
  botaoExcluirUsuario?.addEventListener('click', excluirUsuario)
  botaoGerarCodigo?.addEventListener('click', gerarCodigoRecuperacao)
  botaoCopiarCodigo?.addEventListener('click', copiarCodigoRecuperacao)
  formularioUsuario.addEventListener('submit', salvarUsuario)
  listaUsuarios.addEventListener('click', interagirComUsuario)
}

// Busca os nomes, descrições e seleção atual definidos pelo backend.
async function carregarPermissoes() {
  listaPermissoes.setAttribute('aria-busy', 'true')

  try {
    const resposta = await fetch(listaPermissoes.dataset.url, {
      credentials: 'same-origin',
      headers: { Accept: 'application/json' },
    })
    const dados = await resposta.json()

    if (!resposta.ok) {
      throw new Error(dados.erro || 'Não foi possível carregar as permissões.')
    }

    desenharChecklist(dados.opcoes, dados.permissoes)
    mostrarFeedback('Marque as páginas que os funcionários poderão acessar.', 'info')
  } catch (erro) {
    mostrarFeedback(erro.message, 'erro')
  } finally {
    listaPermissoes.removeAttribute('aria-busy')
  }
}

// Cria inputs reais do tipo checkbox e marca os acessos já salvos.
function desenharChecklist(opcoes, permissoesSalvas) {
  const selecionadas = new Set(Array.isArray(permissoesSalvas) ? permissoesSalvas : [])
  listaPermissoes.replaceChildren()

  opcoes.forEach(opcao => {
    const identificador = `permissao-${opcao.chave}`
    const rotulo = document.createElement('label')
    rotulo.className = 'permission-option'
    rotulo.htmlFor = identificador

    const checkbox = document.createElement('input')
    checkbox.type = 'checkbox'
    checkbox.id = identificador
    checkbox.name = 'permissoes'
    checkbox.value = opcao.chave
    checkbox.checked = selecionadas.has(opcao.chave)

    const texto = document.createElement('span')
    texto.textContent = opcao.nome

    rotulo.append(checkbox, texto)
    listaPermissoes.append(rotulo)
  })
}

// Envia somente as permissões marcadas; o backend valida a lista permitida.
async function salvarPermissoes() {
  const tokenCsrf = document.querySelector('[name="csrfmiddlewaretoken"]')?.value
  const url = listaPermissoes.dataset.url
  const permissoes = [...listaPermissoes.querySelectorAll('input[name="permissoes"]:checked')]
    .map(checkbox => checkbox.value)

  botaoSalvar.disabled = true
  mostrarFeedback('Salvando permissões…', 'info')

  try {
    const resposta = await fetch(url, {
      method: 'PUT',
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': tokenCsrf,
      },
      body: JSON.stringify({ permissoes }),
    })
    const dados = await resposta.json()

    if (!resposta.ok) {
      throw new Error(dados.erro || 'Não foi possível salvar as permissões.')
    }

    mostrarFeedback('Permissões dos funcionários salvas com sucesso.', 'sucesso')
  } catch (erro) {
    mostrarFeedback(erro.message, 'erro')
  } finally {
    botaoSalvar.disabled = false
  }
}

// Mantém a mensagem acessível por leitores de tela e visível após o salvamento.
function mostrarFeedback(mensagem, tipo) {
  feedback.textContent = mensagem
  feedback.dataset.tipo = tipo === 'erro' ? 'erro' : 'info'
  feedback.hidden = false
}

// Busca os perfis de usuário já persistidos para preencher a lista e os totais.
async function carregarUsuarios() {
  try {
    const resposta = await fetch(listaUsuarios.dataset.url, {
      credentials: 'same-origin',
      headers: { Accept: 'application/json' },
    })
    const dados = await resposta.json()

    if (!resposta.ok) {
      throw new Error(dados.erro || 'Não foi possível carregar os usuários.')
    }

    usuariosCarregados = dados.usuarios
    desenharUsuarios(usuariosCarregados)
  } catch (erro) {
    listaUsuarios.replaceChildren()
    const aviso = document.createElement('p')
    aviso.className = 'card users-empty'
    aviso.textContent = erro.message
    listaUsuarios.append(aviso)
  }
}

// Mostra apenas o login na lista; os outros dados ficam no painel recolhido.
function desenharUsuarios(usuarios) {
  listaUsuarios.replaceChildren()
  document.querySelector('[data-total-usuarios]').textContent = usuarios.length
  document.querySelector('[data-total-administradores]').textContent =
    usuarios.filter(usuario => usuario.perfil === 'administrador').length

  if (!usuarios.length) {
    const aviso = document.createElement('p')
    aviso.className = 'card users-empty'
    aviso.textContent = 'Nenhum usuário cadastrado.'
    listaUsuarios.append(aviso)
    return
  }

  usuarios.forEach(usuario => {
    const cartao = document.createElement('article')
    cartao.className = 'card user-card'

    const botao = document.createElement('button')
    botao.type = 'button'
    botao.className = 'user-profile-trigger'
    botao.dataset.toggleUsuario = String(usuario.id)
    botao.setAttribute('aria-expanded', 'false')

    const login = document.createElement('span')
    login.className = 'row-title'
    login.textContent = usuario.login

    const seta = document.createElement('span')
    seta.className = 'chevron'
    seta.textContent = '›'

    botao.append(login, seta)

    const detalhes = document.createElement('div')
    detalhes.className = 'user-profile-details'
    detalhes.hidden = true
    detalhes.append(
      criarLinhaDetalhe('Login', usuario.login),
      criarLinhaDetalhe('Nome', usuario.nome),
      criarLinhaDetalhe('E-mail', usuario.email || 'Não informado'),
      criarLinhaDetalhe('Perfil', usuario.perfil === 'administrador' ? 'Administrador' : 'Funcionário'),
      criarLinhaDetalhe('Status', usuario.ativo ? 'Ativo' : 'Inativo'),
    )

    const botaoEditar = document.createElement('button')
    botaoEditar.type = 'button'
    botaoEditar.className = 'button button--small'
    botaoEditar.dataset.editarUsuario = String(usuario.id)
    botaoEditar.textContent = 'Editar perfil'
    detalhes.append(botaoEditar)

    cartao.append(botao, detalhes)
    listaUsuarios.append(cartao)
  })
}

// Organiza cada dado em uma linha com o rótulo pedido pela administradora.
function criarLinhaDetalhe(rotulo, valor) {
  const linha = document.createElement('div')
  linha.className = 'user-detail-row'
  const nomeCampo = document.createElement('span')
  nomeCampo.className = 'user-detail-label'
  nomeCampo.textContent = `${rotulo}:`
  const valorCampo = document.createElement('span')
  valorCampo.className = 'user-detail-value'
  valorCampo.textContent = valor
  linha.append(nomeCampo, valorCampo)
  return linha
}

// Abre um formulário limpo; senha é obrigatória somente ao criar uma conta.
function abrirCadastroUsuario() {
  formularioUsuario.reset()
  delete formularioUsuario.dataset.userId
  tituloFormularioUsuario.textContent = 'Novo usuário'
  formularioUsuario.querySelector('[data-nova-senha]').required = true
  formularioUsuario.elements.login.disabled = false
  botaoExcluirUsuario.hidden = true
  painelCodigo.hidden = true
  formularioUsuario.hidden = false
  formularioUsuario.scrollIntoView({ behavior: 'smooth', block: 'start' })
  formularioUsuario.elements.nome.focus()
}

// Abre os detalhes ao clicar no cartão ou leva ao formulário ao escolher editar.
function interagirComUsuario(evento) {
  const botao = evento.target.closest('[data-editar-usuario]')
  if (botao) {
    abrirEdicaoUsuario(botao.dataset.editarUsuario)
    return
  }

  const acionador = evento.target.closest('[data-toggle-usuario]')
  if (!acionador) return

  const detalhes = acionador.parentElement.querySelector('.user-profile-details')
  detalhes.hidden = !detalhes.hidden
  acionador.setAttribute('aria-expanded', String(!detalhes.hidden))
}

// Preenche o formulário de edição com os dados do perfil escolhido.
function abrirEdicaoUsuario(idUsuario) {

  const usuario = usuariosCarregados.find(item => String(item.id) === String(idUsuario))
  if (!usuario) return

  formularioUsuario.reset()
  formularioUsuario.dataset.userId = usuario.id
  formularioUsuario.elements.login.value = usuario.login
  formularioUsuario.elements.login.disabled = false
  formularioUsuario.elements.nome.value = usuario.nome
  formularioUsuario.elements.email.value = usuario.email
  formularioUsuario.elements.perfil.value = usuario.perfil
  formularioUsuario.elements.ativo.value = usuario.ativo ? 'sim' : 'nao'
  formularioUsuario.querySelector('[data-nova-senha]').required = false
  tituloFormularioUsuario.textContent = `Editar perfil: ${usuario.nome}`
  const loginAtual = document.querySelector('[data-login-perfil]')?.dataset.loginPerfil
  botaoExcluirUsuario.hidden = usuario.login === loginAtual
  painelCodigo.hidden = false
  resultadoCodigo.hidden = true
  campoCodigo.value = ''
  botaoGerarCodigo.textContent = usuario.codigo_recuperacao_configurado
    ? 'Gerar novo código'
    : 'Gerar código'
  botaoGerarCodigo.disabled = !usuario.ativo
  statusCodigo.textContent = !usuario.ativo
    ? 'Ative este usuário antes de gerar um código.'
    : usuario.codigo_recuperacao_configurado
      ? `Há um código ativo até ${formatarDataHora(usuario.codigo_recuperacao_expira_em)}. O texto não pode ser consultado novamente.`
      : 'Nenhum código ativo. Gere um código para esta pessoa.'
  formularioUsuario.hidden = false
  formularioUsuario.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

// Envia novos perfis por POST e salva alterações dos existentes por PATCH.
async function salvarUsuario(evento) {
  evento.preventDefault()

  const idUsuario = formularioUsuario.dataset.userId
  const urlBase = listaUsuarios.dataset.url
  const dadosUsuario = {
    login: formularioUsuario.elements.login.value,
    nome: formularioUsuario.elements.nome.value,
    email: formularioUsuario.elements.email.value,
    perfil: formularioUsuario.elements.perfil.value,
    ativo: formularioUsuario.elements.ativo.value,
    novaSenha: formularioUsuario.elements.novaSenha.value,
    confirmarSenha: formularioUsuario.elements.confirmarSenha.value,
  }
  const botaoEnviar = formularioUsuario.querySelector('[type="submit"]')

  botaoEnviar.disabled = true
  mostrarMensagemUsuario(idUsuario ? 'Salvando alterações…' : 'Salvando usuário…', 'info')

  try {
    const resposta = await fetch(idUsuario ? `${urlBase}${idUsuario}/` : urlBase, {
      method: idUsuario ? 'PATCH' : 'POST',
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': formularioUsuario.querySelector('[name="csrfmiddlewaretoken"]').value,
      },
      body: JSON.stringify(dadosUsuario),
    })
    const dados = await resposta.json()

    if (!resposta.ok) {
      const erros = dados.erros
        ? Object.values(dados.erros).flat().join(' ')
        : dados.erro
      throw new Error(erros || 'Não foi possível salvar o perfil.')
    }

    fecharFormularioUsuario()
    await carregarUsuarios()

    if (!idUsuario && dados.codigo_recuperacao) {
      // Ao cadastrar uma conta ativa, abre o perfil e mostra o código gerado uma única vez.
      abrirEdicaoUsuario(dados.usuario.id)
      mostrarCodigoGerado(dados.codigo_recuperacao, dados.expira_em)
      mostrarMensagemUsuario('Usuário criado. Copie e entregue o código de recuperação.', 'sucesso')
    } else {
      mostrarMensagemUsuario('Perfil salvo com sucesso.', 'sucesso')
    }
  } catch (erro) {
    mostrarMensagemUsuario(erro.message, 'erro')
  } finally {
    botaoEnviar.disabled = false
  }
}

// Exclui somente após confirmação e envia a operação protegida ao backend.
async function excluirUsuario() {
  const idUsuario = formularioUsuario.dataset.userId
  const usuario = usuariosCarregados.find(item => String(item.id) === String(idUsuario))
  if (!usuario) return

  const confirmar = window.confirm(`Deseja excluir o usuário "${usuario.login}"? Esta ação não pode ser desfeita.`)
  if (!confirmar) return

  botaoExcluirUsuario.disabled = true

  try {
    const resposta = await fetch(`${listaUsuarios.dataset.url}${idUsuario}/`, {
      method: 'DELETE',
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json',
        'X-CSRFToken': formularioUsuario.querySelector('[name="csrfmiddlewaretoken"]').value,
      },
    })
    const dados = await resposta.json()

    if (!resposta.ok) {
      throw new Error(dados.erro || 'Não foi possível excluir este usuário.')
    }

    fecharFormularioUsuario()
    await carregarUsuarios()
    mostrarMensagemUsuario(`Usuário "${dados.login}" excluído.`, 'sucesso')
  } catch (erro) {
    mostrarMensagemUsuario(erro.message, 'erro')
  } finally {
    botaoExcluirUsuario.disabled = false
  }
}

// Cria ou substitui o código e exibe o texto puro apenas nesta resposta.
async function gerarCodigoRecuperacao() {
  const idUsuario = formularioUsuario.dataset.userId
  const usuario = usuariosCarregados.find(item => String(item.id) === String(idUsuario))
  if (!usuario) return

  if (usuario.codigo_recuperacao_configurado) {
    const confirmar = window.confirm('O código atual será invalidado. Gerar um código novo?')
    if (!confirmar) return
  }

  botaoGerarCodigo.disabled = true
  statusCodigo.textContent = 'Gerando código…'

  try {
    const resposta = await fetch(`${listaUsuarios.dataset.url}${idUsuario}/codigo-recuperacao/`, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json',
        'X-CSRFToken': formularioUsuario.querySelector('[name="csrfmiddlewaretoken"]').value,
      },
    })
    const dados = await resposta.json()

    if (!resposta.ok) {
      throw new Error(dados.erro || 'Não foi possível gerar o código.')
    }

    mostrarCodigoGerado(dados.codigo, dados.expira_em)
    usuario.codigo_recuperacao_configurado = true
    usuario.codigo_recuperacao_expira_em = dados.expira_em
    botaoGerarCodigo.textContent = 'Gerar novo código'
  } catch (erro) {
    statusCodigo.textContent = erro.message
  } finally {
    botaoGerarCodigo.disabled = false
  }
}

// Exibe o texto puro apenas no momento da geração para que possa ser compartilhado.
function mostrarCodigoGerado(codigo, expiracao) {
  campoCodigo.value = codigo
  resultadoCodigo.hidden = false
  statusCodigo.textContent = `Código válido até ${formatarDataHora(expiracao)}. Copie e entregue à pessoa agora.`
}

// Copia o código recém-gerado para que o administrador possa compartilhá-lo.
async function copiarCodigoRecuperacao() {
  try {
    await navigator.clipboard.writeText(campoCodigo.value)
    statusCodigo.textContent = 'Código copiado. Compartilhe-o com o usuário.'
  } catch {
    campoCodigo.select()
    document.execCommand('copy')
    statusCodigo.textContent = 'Código selecionado para cópia.'
  }
}

// Apresenta a expiração no fuso e formato local do navegador.
function formatarDataHora(valor) {
  return new Date(valor).toLocaleString('pt-BR', {
    dateStyle: 'short',
    timeStyle: 'short',
  })
}

// Esconde e limpa o formulário após cancelar ou salvar.
function fecharFormularioUsuario() {
  formularioUsuario.reset()
  delete formularioUsuario.dataset.userId
  formularioUsuario.hidden = true
  formularioUsuario.querySelector('[data-nova-senha]').required = false
  botaoExcluirUsuario.hidden = true
  painelCodigo.hidden = true
  resultadoCodigo.hidden = true
  campoCodigo.value = ''
}

// Exibe o resultado das operações sem recarregar a página.
function mostrarMensagemUsuario(mensagem, tipo) {
  if (!mensagemUsuario) return
  mensagemUsuario.textContent = mensagem
  mensagemUsuario.dataset.tipo = tipo
  mensagemUsuario.hidden = false
}
