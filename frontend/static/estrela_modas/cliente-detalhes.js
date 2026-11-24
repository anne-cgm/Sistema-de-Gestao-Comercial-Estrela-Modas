import {
  calcularSaldoCredito,
  calcularSaldoDevedorCliente,
  carregarClientes,
  carregarCompras,
  carregarDividas,
  carregarMovimentosCredito,
  formatarMoeda,
  obterCliente,
  salvarCadastroCliente,
  salvarClientes,
} from "./clientes-data.js"
import { iniciarTela } from "./shared.js"

function formatarData(data) {
  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(data))
}

function escaparHtml(valor) {
  const elemento = document.createElement("span")
  elemento.textContent = String(valor ?? "")
  return elemento.innerHTML
}

function renderizarLista(elemento, itens, criarItem, mensagemVazia) {
  if (!elemento) return
  elemento.innerHTML =
    itens.length > 0
      ? itens.map(criarItem).join("")
      : `<p class="card detail-empty">${mensagemVazia}</p>`
}

export default function iniciarDetalhesCliente() {
  iniciarTela("clientes")

  let clientes = carregarClientes()
  const clienteId = Number(
    new URLSearchParams(window.location.search).get("id"),
  )
  let cliente = obterCliente(clientes, clienteId)
  const formulario = document.querySelector("[data-formulario-detalhes]")

  if (!cliente) {
    document.querySelector("[data-nome-cliente]").textContent =
      "Cliente não encontrado"
    formulario?.remove()
    return
  }

  const dividas = carregarDividas()
  const movimentos = carregarMovimentosCredito()
  const compras = carregarCompras()
  const dividasCliente = dividas.filter(
    (divida) => Number(divida.clienteId) === clienteId,
  )
  const movimentosCliente = movimentos.filter(
    (movimento) => Number(movimento.clienteId) === clienteId,
  )
  const comprasCliente = compras.filter(
    (compra) => Number(compra.clienteId) === clienteId,
  )
  const saldoDevedor = calcularSaldoDevedorCliente(dividas, clienteId)
  const saldoCredito = calcularSaldoCredito(movimentos, clienteId)

  document.querySelector("[data-nome-cliente]").textContent =
    cliente.nomeCliente
  document.querySelector("[data-status-financeiro]").textContent =
    saldoDevedor > 0 ? "Com pendência" : "Em dia"
  document.querySelector("[data-saldo-devedor]").textContent =
    formatarMoeda(saldoDevedor)
  document.querySelector("[data-saldo-credito]").textContent =
    formatarMoeda(saldoCredito)
  formulario.elements.nomeCliente.value = cliente.nomeCliente
  formulario.elements.telefone.value = cliente.telefone || ""

  renderizarLista(
    document.querySelector("[data-historico-compras]"),
    comprasCliente,
    (compra) => `
      <article class="card row">
        <div class="row-main">
          <p class="row-title">${escaparHtml(compra.descricao)}</p>
          <p class="row-sub">${formatarData(compra.data)} · ${escaparHtml(compra.formaPagamento)}</p>
        </div>
        <p class="row-value">${formatarMoeda(compra.valor)}</p>
      </article>
    `,
    "Nenhuma compra registrada.",
  )

  renderizarLista(
    document.querySelector("[data-historico-creditos]"),
    movimentosCliente,
    (movimento) => `
      <article class="card row">
        <div class="row-main">
          <p class="row-title">${escaparHtml(movimento.descricao || "Movimentação de crédito")}</p>
          <p class="row-sub">${formatarData(movimento.data)} · ${
            movimento.tipo === "gerado" ? "Crédito gerado" : "Crédito utilizado"
          }</p>
        </div>
        <p class="row-value ${
          movimento.tipo === "gerado"
            ? "history-value--credit"
            : "history-value--debit"
        }">${
          movimento.tipo === "gerado" ? "+" : "−"
        } ${formatarMoeda(movimento.valor)}</p>
      </article>
    `,
    "Nenhuma movimentação de crédito.",
  )

  renderizarLista(
    document.querySelector("[data-historico-dividas]"),
    dividasCliente,
    (divida) => `
      <article class="card row">
        <div class="row-main">
          <p class="row-title">Venda #${divida.id}</p>
          <p class="row-sub">${formatarData(divida.dataVenda)} · Original: ${formatarMoeda(divida.valorOriginal)}</p>
        </div>
        <div>
          <p class="row-value">${formatarMoeda(divida.saldoDevedor)}</p>
          <p class="row-sub">${
            divida.saldoDevedor > 0 ? "Pendente" : "Quitada"
          }</p>
        </div>
      </article>
    `,
    "Nenhuma venda fiada registrada.",
  )

  formulario.addEventListener("submit", (evento) => {
    evento.preventDefault()
    const dados = new FormData(formulario)
    const resultado = salvarCadastroCliente(
      clientes,
      {
        nomeCliente: dados.get("nomeCliente"),
        telefone: dados.get("telefone"),
      },
      clienteId,
    )
    const erro = formulario.querySelector("[data-erro-detalhes]")
    if (!resultado.sucesso) {
      erro.textContent = resultado.mensagem
      erro.hidden = false
      return
    }
    clientes = resultado.clientes
    cliente = resultado.cliente
    salvarClientes(clientes)
    document.querySelector("[data-nome-cliente]").textContent =
      cliente.nomeCliente
    erro.textContent = "Dados salvos com sucesso."
    erro.style.color = "var(--wine)"
    erro.hidden = false
  })

  document
    .querySelector("[data-nova-venda-cliente]")
    ?.addEventListener("click", () => {
      window.location.href = `./nova-venda.html?cliente=${clienteId}`
    })
}

if (typeof document !== "undefined") iniciarDetalhesCliente()
