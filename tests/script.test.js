import assert from 'node:assert/strict'
import test from 'node:test'

import { calcularNovoEstoque, calcularValorCompra } from '../frontend/static/estrela_modas/compras.js'
import { produtoComEstoqueBaixo } from '../frontend/static/estrela_modas/estoque.js'
import iniciarLogin, { validarLogin } from '../frontend/static/estrela_modas/login.js'
import { calcularTotalVenda, formatarMoeda } from '../frontend/static/estrela_modas/nova_venda.js'
import { buscarProduto } from '../frontend/static/estrela_modas/produtos.js'
import { iniciarValidacaoObrigatoriaEmPortugues } from '../frontend/static/estrela_modas/shared.js'
import iniciarDetalhesCliente from '../frontend/static/estrela_modas/cliente-detalhes.js'

test('validarLogin aceita usuário e senha preenchidos', () => {
  assert.equal(validarLogin('kamila', '123456'), true)
})

test('validarLogin rejeita campos vazios', () => {
  assert.equal(validarLogin('   ', '123456'), false)
  assert.equal(validarLogin('kamila', '   '), false)
  assert.equal(validarLogin('', ''), false)
})

test('mensagens nativas de campos obrigatórios aparecem em português', () => {
  const listeners = {}
  const documentoAnterior = globalThis.document
  globalThis.document = {
    addEventListener(tipo, manipulador) {
      listeners[tipo] = manipulador
    },
  }

  try {
    iniciarValidacaoObrigatoriaEmPortugues()
    const campo = {
      dataset: {},
      validity: { valueMissing: true },
      matches: () => true,
      setCustomValidity(mensagem) {
        this.mensagem = mensagem
      },
    }

    listeners.invalid({ target: campo })
    assert.equal(campo.mensagem, 'Este campo é obrigatório.')
    assert.equal(campo.dataset.mensagemObrigatoria, 'sim')

    listeners.input({ target: campo })
    assert.equal(campo.mensagem, '')
    assert.equal(campo.dataset.mensagemObrigatoria, undefined)
  } finally {
    if (documentoAnterior === undefined) {
      delete globalThis.document
    } else {
      globalThis.document = documentoAnterior
    }
  }
})

test('diálogo de exclusão do cliente abre e pode ser cancelado', () => {
  const criarBotao = () => ({
    manipuladores: {},
    addEventListener(tipo, manipulador) {
      this.manipuladores[tipo] = manipulador
    },
    click() {
      this.manipuladores.click()
    },
  })
  const botaoAbrir = criarBotao()
  const botaoCancelar = criarBotao()
  const dialogo = {
    aberto: false,
    showModal() {
      this.aberto = true
    },
    close() {
      this.aberto = false
    },
    querySelector() {
      return botaoCancelar
    },
  }
  const documentoAnterior = globalThis.document
  globalThis.document = {
    querySelector() {
      return null
    },
    querySelectorAll() {
      return []
    },
  }
  globalThis.document.querySelector = seletor => ({
    '[data-dialogo-excluir]': dialogo,
    '[data-abrir-dialogo-excluir]': botaoAbrir,
  })[seletor] ?? null

  try {
    iniciarDetalhesCliente()
    botaoAbrir.click()
    assert.equal(dialogo.aberto, true)

    botaoCancelar.click()
    assert.equal(dialogo.aberto, false)
  } finally {
    if (documentoAnterior === undefined) {
      delete globalThis.document
    } else {
      globalThis.document = documentoAnterior
    }
  }
})

test('o diálogo avança entre etapas e rejeita senhas diferentes', () => {
  const criarBotao = (dataset = {}) => ({
    dataset,
    addEventListener(evento, manipulador) {
      this.manipuladores ??= {}
      this.manipuladores[evento] = manipulador
    },
    click() {
      this.manipuladores.click()
    },
  })
  const criarFormulario = campos => ({
    elements: campos,
    addEventListener(evento, manipulador) {
      this.manipulador = manipulador
    },
    reset() {
      Object.values(this.elements).forEach(campo => {
        campo.value = ''
      })
    },
    submit() {
      this.manipulador({ preventDefault() {} })
    },
  })
  const criarEtapa = () => ({
    hidden: true,
    querySelector() {
      return { focus() {} }
    },
  })
  const botaoAbrir = criarBotao()
  const botaoFechar = criarBotao()
  const botaoVoltarEmail = criarBotao({ voltarEtapaRecuperacao: 'email' })
  const botaoVoltarCodigo = criarBotao({ voltarEtapaRecuperacao: 'codigo' })
  const formulario = { addEventListener() {} }
  const campoEmail = { value: 'teste@example.com' }
  const campoCodigo = { value: '123456' }
  const campoNovaSenha = { value: 'Senha123' }
  const campoConfirmacao = { value: 'SenhaDiferente' }
  const formularioEmail = criarFormulario({ email: campoEmail })
  const formularioCodigo = criarFormulario({ codigo: campoCodigo })
  const formularioSenha = criarFormulario({
    novaSenha: campoNovaSenha,
    confirmarSenha: campoConfirmacao,
  })
  const etapaEmail = criarEtapa()
  const etapaCodigo = criarEtapa()
  const etapaSenha = criarEtapa()
  const resultado = { hidden: true, textContent: '' }
  const elementosDialogo = {
    '[data-fechar-recuperacao]': botaoFechar,
    '[data-etapa-email-recuperacao]': etapaEmail,
    '[data-etapa-codigo-recuperacao]': etapaCodigo,
    '[data-etapa-senha-recuperacao]': etapaSenha,
    '[data-resultado-recuperacao]': resultado,
    '[data-formulario-email-recuperacao]': formularioEmail,
    '[data-formulario-codigo-recuperacao]': formularioCodigo,
    '[data-formulario-senha-recuperacao]': formularioSenha,
  }
  const dialogo = {
    open: false,
    addEventListener(evento, manipulador) {
      this.manipuladores ??= {}
      this.manipuladores[evento] = manipulador
    },
    showModal() {
      this.open = true
    },
    close() {
      this.open = false
      this.manipuladores.close()
    },
    querySelector(seletor) {
      return elementosDialogo[seletor] ?? null
    },
    querySelectorAll() {
      return [botaoVoltarEmail, botaoVoltarCodigo]
    },
  }
  const elementos = {
    '[data-login-form]': formulario,
    '[data-abrir-recuperacao]': botaoAbrir,
    '[data-recuperar-senha]': dialogo,
  }
  const documentoAnterior = globalThis.document

  globalThis.document = {
    querySelector(seletor) {
      return elementos[seletor] ?? null
    },
  }

  try {
    iniciarLogin()
    botaoAbrir.click()

    assert.equal(dialogo.open, true)
    assert.equal(etapaEmail.hidden, false)

    campoEmail.value = 'teste@example.com'
    formularioEmail.submit()
    assert.equal(etapaCodigo.hidden, false)
    assert.match(resultado.textContent, /código de recuperação/)

    campoCodigo.value = '123456'
    formularioCodigo.submit()
    assert.equal(etapaSenha.hidden, false)
    assert.match(resultado.textContent, /nova senha/)

    campoNovaSenha.value = 'Senha123'
    campoConfirmacao.value = 'SenhaDiferente'
    formularioSenha.submit()
    assert.match(resultado.textContent, /não são iguais/)

    botaoFechar.click()
    assert.equal(dialogo.open, false)
    assert.equal(etapaEmail.hidden, false)
  } finally {
    if (documentoAnterior === undefined) {
      delete globalThis.document
    } else {
      globalThis.document = documentoAnterior
    }
  }
})

test('calcularTotalVenda aplica desconto corretamente', () => {
  const itensVenda = [
    { precoVenda: 100, quantidade: 2 },
    { precoVenda: 50, quantidade: 1 },
  ]

  assert.equal(calcularTotalVenda(itensVenda, 10), 225)
})

test('calcularTotalVenda retorna o valor sem desconto quando ele é zero', () => {
  const itensVenda = [
    { precoVenda: 79.9, quantidade: 2 },
    { precoVenda: 119.9, quantidade: 1 },
  ]

  assert.equal(calcularTotalVenda(itensVenda, 0), 279.7)
})

test('calcularTotalVenda limita descontos inválidos', () => {
  const itensVenda = [{ precoVenda: 100, quantidade: 1 }]

  assert.equal(calcularTotalVenda(itensVenda, -10), 100)
  assert.equal(calcularTotalVenda(itensVenda, 150), 0)
})

test('produtoComEstoqueBaixo identifica itens com estoque crítico', () => {
  assert.equal(produtoComEstoqueBaixo(1), true)
  assert.equal(produtoComEstoqueBaixo(0), true)
  assert.equal(produtoComEstoqueBaixo(2), false)
  assert.equal(produtoComEstoqueBaixo(3, 3), true)
})

test('calcularValorCompra multiplica custo e quantidade recebida', () => {
  assert.equal(calcularValorCompra(48.5, 10), 485)
  assert.equal(calcularValorCompra(19.99, 3), 59.97)
})

test('calcularNovoEstoque soma a quantidade recebida ao estoque atual', () => {
  assert.equal(calcularNovoEstoque(12, 8), 20)
  assert.equal(calcularNovoEstoque(0, 5), 5)
})

test('buscarProduto ignora diferenças entre maiúsculas e minúsculas', () => {
  const produtos = [
    { nomeProduto: 'Camiseta Básica' },
    { nomeProduto: 'Calça Wide Leg' },
    { nomeProduto: 'Bolsa Mini' },
  ]

  const resultado = buscarProduto(produtos, 'calça')

  assert.deepEqual(
    resultado.map(produto => produto.nomeProduto),
    ['Calça Wide Leg'],
  )
})

test('buscarProduto retorna lista vazia quando o termo não existe', () => {
  const produtos = [
    { nomeProduto: 'Camiseta Básica' },
    { nomeProduto: 'Vestido Floral' },
  ]

  assert.deepEqual(buscarProduto(produtos, 'sapato'), [])
})

test('formatarMoeda usa o padrão brasileiro', () => {
  const valorFormatado = formatarMoeda(189.81)

  assert.match(valorFormatado, /189,81/)
  assert.match(valorFormatado, /R\$/)
})

test('módulos das telas podem ser importados sem um DOM', async () => {
  const modulos = [
    '../frontend/static/estrela_modas/clientes.js',
    '../frontend/static/estrela_modas/clientes-data.js',
    '../frontend/static/estrela_modas/compras.js',
    '../frontend/static/estrela_modas/dashboard.js',
    '../frontend/static/estrela_modas/debitos.js',
    '../frontend/static/estrela_modas/estoque.js',
    '../frontend/static/estrela_modas/mais_opcoes.js',
    '../frontend/static/estrela_modas/nova_venda.js',
    '../frontend/static/estrela_modas/novo_cliente.js',
    '../frontend/static/estrela_modas/novo_produto.js',
    '../frontend/static/estrela_modas/produtos.js',
    '../frontend/static/estrela_modas/relatorios.js',
    '../frontend/static/estrela_modas/shared.js',
  ]

  await assert.doesNotReject(() => Promise.all(modulos.map(modulo => import(modulo))))
})
