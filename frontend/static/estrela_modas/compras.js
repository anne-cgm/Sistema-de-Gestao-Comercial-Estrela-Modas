
import { iniciarTela } from './shared.js'

export default function iniciarCompras() {
  // Inicializa a navegação e identifica a aba ativa.
  iniciarTela('mais')

  const formularioCompra = document.querySelector('[data-formulario-compra]')
  const seletorProduto = document.querySelector('[data-seletor-produto]')

  // Atualiza o resumo conforme os campos do formulário são preenchidos.
  formularioCompra?.addEventListener('input', atualizarResumoCompra)

  // Valida o formulário antes do envio.
  // Se estiver válido, o Django recebe os dados normalmente.
  formularioCompra?.addEventListener('submit', registrarCompra)

  // Atualiza o preço quando outro produto é selecionado.
  seletorProduto?.addEventListener('change', selecionarProduto)

  atualizarResumoCompra()
}

// Preenche automaticamente o preço de custo do produto selecionado.
function selecionarProduto(evento) {
  const produtoSelecionado = evento.currentTarget.selectedOptions[0]
  const campoPrecoCusto = document.querySelector('[name="preco_custo_unitario"]')

  if (campoPrecoCusto) {
    campoPrecoCusto.value = produtoSelecionado.dataset.precoCusto ?? ''
  }

  atualizarResumoCompra()
}

// Atualiza os valores apresentados no resumo da compra.
function atualizarResumoCompra() {
  const produtoSelecionado = obterProdutoSelecionado()

  const precoCusto = lerNumeroDoCampo('[name="preco_custo_unitario"]')
  const quantidadeRecebida = lerNumeroDoCampo('[name="quantidade"]')

  const quantidadeEstoque = Number(
    produtoSelecionado?.dataset.quantidadeEstoque ?? 0
  )

  const valorTotal = calcularValorCompra(precoCusto, quantidadeRecebida)
  const novoEstoque = calcularNovoEstoque(quantidadeEstoque, quantidadeRecebida)

  const elementoValorTotal = document.querySelector('[data-valor-total-compra]')
  const elementoEstoqueAtual = document.querySelector('[data-estoque-atual]')
  const elementoNovoEstoque = document.querySelector('[data-novo-estoque]')
  const elementoNomeProduto = document.querySelector('[data-nome-produto-selecionado]')

  if (elementoValorTotal) {
    elementoValorTotal.textContent = formatarMoeda(valorTotal)
  }

  if (elementoEstoqueAtual) {
    elementoEstoqueAtual.textContent = quantidadeEstoque
  }

  if (elementoNovoEstoque) {
    elementoNovoEstoque.textContent = novoEstoque
  }

  if (elementoNomeProduto) {
    elementoNomeProduto.textContent =
      produtoSelecionado?.dataset.nomeProduto ?? 'Nenhum produto selecionado'
  }
}

// Impede o envio somente quando o formulário apresenta campos inválidos.
// Não impede o envio quando está válido, pois o Django precisa processá-lo.
function registrarCompra(evento) {
  const formularioCompra = evento.currentTarget

  if (!formularioCompra.checkValidity()) {
    evento.preventDefault()
    formularioCompra.reportValidity()
  }
}

// Recupera o produto atualmente selecionado.
function obterProdutoSelecionado() {
  const seletorProduto = document.querySelector('[data-seletor-produto]')
  const produtoSelecionado = seletorProduto?.selectedOptions[0]

  return produtoSelecionado?.value ? produtoSelecionado : null
}

// Lê um campo numérico do formulário.
function lerNumeroDoCampo(seletor) {
  const valor = document.querySelector(seletor)?.value ?? '0'
  return Number(valor) || 0
}

// Calcula o valor total da compra.
export function calcularValorCompra(precoCusto, quantidadeRecebida) {
  return Number((precoCusto * quantidadeRecebida).toFixed(2))
}

// Calcula a previsão de estoque após a entrada.
export function calcularNovoEstoque(quantidadeEstoque, quantidadeRecebida) {
  return quantidadeEstoque + quantidadeRecebida
}

// Formata valores monetários para o padrão brasileiro.
function formatarMoeda(valor) {
  return valor.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })
}

// Executa a inicialização somente quando existe um documento HTML.
if (typeof document !== 'undefined') iniciarCompras()

