import {
  calcularSaldoCredito,
  carregarClientes,
  carregarCompras,
  carregarDividas,
  carregarMovimentosCredito,
  formatarMoeda as formatarMoedaBase,
  normalizarValor,
  registrarMovimentoCredito,
  salvarCompras,
  salvarDividas,
  salvarMovimentosCredito,
} from "./clientes-data.js"
import { exibirMensagem, iniciarTela } from "./shared.js"

export function calcularTotalVenda(itensVenda, descontoAplicado = 0) {
  const subtotal = itensVenda.reduce(
    (total, item) => total + item.precoVenda * item.quantidade,
    0,
  )
  const desconto = Math.min(Math.max(descontoAplicado, 0), 100)
  return normalizarValor(subtotal - (subtotal * desconto) / 100)
}

export function calcularUsoCredito(
  totalVenda,
  creditoSolicitado,
  saldoCredito,
) {
  const credito = Math.max(0, Number(creditoSolicitado) || 0)
  const limite = Math.min(
    Math.max(0, Number(totalVenda) || 0),
    Math.max(0, Number(saldoCredito) || 0),
  )
  const creditoUtilizado = normalizarValor(Math.min(credito, limite))
  return {
    creditoUtilizado,
    restante: normalizarValor(Number(totalVenda) - creditoUtilizado),
  }
}

export function formatarMoedaVenda(valor) {
  return formatarMoedaBase(valor)
}

export const formatarMoeda = formatarMoedaVenda

export function vendaExigeCliente(formaPagamento, creditoUtilizado = 0) {
  return (
    String(formaPagamento).trim().toLocaleLowerCase("pt-BR") === "fiado" ||
    Number(creditoUtilizado) > 0
  )
}

export default function iniciarNovaVenda() {
  iniciarTela("venda")

  const clientes = carregarClientes()
  let movimentosCredito = carregarMovimentosCredito()
  const seletorCliente = document.querySelector("[data-cliente-venda]")
  const campoCredito = document.querySelector("[data-valor-credito]")
  const painelCredito = document.querySelector("[data-painel-credito]")
  let totalVenda = calcularTotalAtual()
  let saldoCredito = 0

  clientes.forEach((cliente) => {
    const opcao = document.createElement("option")
    opcao.value = cliente.id
    opcao.textContent = cliente.nomeCliente
    seletorCliente?.append(opcao)
  })

  const clienteInicial = new URLSearchParams(window.location.search).get(
    "cliente",
  )
  if (clienteInicial && seletorCliente) seletorCliente.value = clienteInicial

  function atualizarCreditoCliente() {
    const clienteId = Number(seletorCliente?.value)
    saldoCredito = clienteId
      ? calcularSaldoCredito(movimentosCredito, clienteId)
      : 0
    painelCredito.hidden = !clienteId || saldoCredito <= 0
    document.querySelector("[data-saldo-credito-venda]").textContent =
      formatarMoeda(saldoCredito)
    campoCredito.max = String(Math.min(saldoCredito, totalVenda))
    if (!clienteId || saldoCredito <= 0) campoCredito.value = "0"
    atualizarResumoVenda()
  }

  function atualizarResumoVenda() {
    const resultado = calcularUsoCredito(
      totalVenda,
      campoCredito?.value,
      saldoCredito,
    )
    document.querySelector("[data-valor-total]").textContent =
      formatarMoeda(totalVenda)
    document.querySelector("[data-valor-restante]").textContent = formatarMoeda(
      resultado.restante,
    )
    document.querySelector("[data-credito-utilizado]").textContent =
      `− ${formatarMoeda(resultado.creditoUtilizado)}`
    document.querySelector("[data-linha-credito]").hidden =
      resultado.creditoUtilizado <= 0
    return resultado
  }

  seletorCliente?.addEventListener("change", atualizarCreditoCliente)
  campoCredito?.addEventListener("input", atualizarResumoVenda)
  document
    .querySelector("[data-usar-credito-total]")
    ?.addEventListener("click", () => {
      campoCredito.value = String(Math.min(saldoCredito, totalVenda))
      atualizarResumoVenda()
    })

  document
    .querySelectorAll("[data-forma-pagamento]")
    .forEach((botaoFormaPagamento) => {
      botaoFormaPagamento.addEventListener("click", () => {
        document
          .querySelector(".payment.is-active")
          ?.classList.remove("is-active")
        botaoFormaPagamento.classList.add("is-active")
      })
    })

  document
    .querySelector("[data-finish-sale]")
    ?.addEventListener("click", () => {
      const clienteId = Number(seletorCliente?.value)
      const resultado = atualizarResumoVenda()
      const formaPagamento =
        document.querySelector(".payment.is-active")?.textContent.trim() ||
        "Não informado"

      if (
        !clienteId &&
        vendaExigeCliente(formaPagamento, resultado.creditoUtilizado)
      ) {
        exibirMensagem(
          formaPagamento === "Fiado"
            ? "Selecione ou cadastre um cliente para registrar a venda fiada."
            : "Selecione um cliente para utilizar crédito.",
        )
        return
      }

      if (resultado.creditoUtilizado > 0) {
        const movimento = registrarMovimentoCredito(movimentosCredito, {
          clienteId,
          tipo: "utilizado",
          valor: resultado.creditoUtilizado,
          descricao: "Crédito utilizado em nova venda",
        })
        if (!movimento.sucesso) {
          exibirMensagem(movimento.mensagem)
          return
        }
        movimentosCredito = movimento.movimentos
        salvarMovimentosCredito(movimentosCredito)
      }

      const vendaId = Date.now()
      salvarCompras([
        {
          id: vendaId,
          clienteId: clienteId || null,
          tipo: "venda",
          data: new Date().toISOString(),
          descricao: "Camiseta Básica e Bolsa Mini",
          valor: totalVenda,
          formaPagamento:
            resultado.creditoUtilizado > 0
              ? `Crédito + ${formaPagamento}`
              : formaPagamento,
        },
        ...carregarCompras(),
      ])

      if (clienteId) {
        if (formaPagamento === "Fiado" && resultado.restante > 0) {
          salvarDividas([
            {
              id: vendaId,
              clienteId,
              dataVenda: new Date().toISOString(),
              valorOriginal: resultado.restante,
              saldoDevedor: resultado.restante,
            },
            ...carregarDividas(),
          ])
        }
      }

      exibirMensagem("Venda finalizada com sucesso.")
      campoCredito.value = "0"
      movimentosCredito = carregarMovimentosCredito()
      atualizarCreditoCliente()
    })

  atualizarCreditoCliente()

  function calcularTotalAtual() {
    const itens = [...document.querySelectorAll("[data-item-venda]")].map(
      (item) => ({
        precoVenda: Number(item.dataset.precoVenda),
        quantidade: Number(item.dataset.quantidade),
      }),
    )
    const desconto = Number(
      document.querySelector("[data-desconto-aplicado]")?.dataset
        .descontoAplicado || 0,
    )
    return calcularTotalVenda(itens, desconto)
  }
}

if (typeof document !== "undefined") iniciarNovaVenda()
