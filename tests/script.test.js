import assert from 'node:assert/strict'
import test from 'node:test'

import { produtoComEstoqueBaixo } from '../src/screens/estoque.js'
import { validarLogin } from '../src/screens/login.js'
import { calcularTotalVenda, formatarMoeda } from '../src/screens/nova-venda.js'
import { buscarProduto } from '../src/screens/produtos.js'

test('validarLogin aceita usuário e senha preenchidos', () => {
  assert.equal(validarLogin('kamila', '123456'), true)
})

test('validarLogin rejeita campos vazios', () => {
  assert.equal(validarLogin('   ', '123456'), false)
  assert.equal(validarLogin('kamila', '   '), false)
  assert.equal(validarLogin('', ''), false)
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
    '../src/screens/clientes.js',
    '../src/screens/dashboard.js',
    '../src/screens/debitos.js',
    '../src/screens/mais.js',
    '../src/screens/novo-produto.js',
    '../src/screens/relatorios.js',
    '../src/screens/shared.js',
  ]

  await assert.doesNotReject(() => Promise.all(modulos.map(modulo => import(modulo))))
})
