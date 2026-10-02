import { exibirMensagem, iniciarTela } from './shared.js'

export default function iniciarCompras() {
  iniciarTela('mais')

  const formularioCompra = document.querySelector('[data-formulario-compra]')
  const seletorProduto = document.querySelector('[data-seletor-produto]')
  formularioCompra?.addEventListener('input', atualizarResumoCompra)
  formularioCompra?.addEventListener('submit', registrarCompra)
  seletorProduto?.addEventListener('change', selecionarProduto)

  atualizarResumoCompra()
}

function selecionarProduto(evento) {
  const produtoSelecionado = evento.currentTarget.selectedOptions[0]
  const campoPrecoCusto = document.querySelector('[name="precoCusto"]')

  if (campoPrecoCusto) campoPrecoCusto.value = produtoSelecionado.dataset.precoCusto ?? ''
  atualizarResumoCompra()
}

function atualizarResumoCompra() {
  const produtoSelecionado = obterProdutoSelecionado()
  const precoCusto = lerNumeroDoCampo('[name="precoCusto"]')
  const quantidadeRecebida = lerNumeroDoCampo('[name="quantidadeRecebida"]')
  const quantidadeEstoque = Number(produtoSelecionado?.dataset.quantidadeEstoque ?? 0)
  const valorTotal = calcularValorCompra(precoCusto, quantidadeRecebida)
  const novoEstoque = calcularNovoEstoque(quantidadeEstoque, quantidadeRecebida)
  const elementoValorTotal = document.querySelector('[data-valor-total-compra]')
  const elementoEstoqueAtual = document.querySelector('[data-estoque-atual]')
  const elementoNovoEstoque = document.querySelector('[data-novo-estoque]')
  const elementoNomeProduto = document.querySelector('[data-nome-produto-selecionado]')

  if (elementoValorTotal) elementoValorTotal.textContent = formatarMoeda(valorTotal)
  if (elementoEstoqueAtual) elementoEstoqueAtual.textContent = quantidadeEstoque
  if (elementoNovoEstoque) elementoNovoEstoque.textContent = novoEstoque
  if (elementoNomeProduto) {
    elementoNomeProduto.textContent =
      produtoSelecionado?.dataset.nomeProduto ?? 'Nenhum produto selecionado'
  }
}

function registrarCompra(evento) {
  evento.preventDefault()
  const formularioCompra = evento.currentTarget

  if (!formularioCompra.checkValidity()) {
    formularioCompra.reportValidity()
    return
  }

  const produtoSelecionado = obterProdutoSelecionado()
  const quantidadeEstoque = Number(produtoSelecionado.dataset.quantidadeEstoque)
  const quantidadeRecebida = lerNumeroDoCampo('[name="quantidadeRecebida"]')
  produtoSelecionado.dataset.quantidadeEstoque = calcularNovoEstoque(
    quantidadeEstoque,
    quantidadeRecebida,
  )
  atualizarResumoCompra()
  exibirMensagem('Compra registrada e estoque atualizado.')
}

function obterProdutoSelecionado() {
  const seletorProduto = document.querySelector('[data-seletor-produto]')
  const produtoSelecionado = seletorProduto?.selectedOptions[0]

  return produtoSelecionado?.value ? produtoSelecionado : null
}

function lerNumeroDoCampo(seletor) {
  const valor = document.querySelector(seletor)?.value ?? '0'
  return Number(valor) || 0
}

export function calcularValorCompra(precoCusto, quantidadeRecebida) {
  return Number((precoCusto * quantidadeRecebida).toFixed(2))
}

export function calcularNovoEstoque(quantidadeEstoque, quantidadeRecebida) {
  return quantidadeEstoque + quantidadeRecebida
}

function formatarMoeda(valor) {
  return valor.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })
}

if (typeof document !== 'undefined') iniciarCompras()
