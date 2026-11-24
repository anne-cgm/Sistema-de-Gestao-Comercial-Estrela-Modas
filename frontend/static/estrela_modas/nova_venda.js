import { iniciarTela } from "./shared.js"

export function formatarMoeda(valor) {
  return Number(valor || 0).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  })
}

export function calcularTotalVenda(itensVenda, descontoAplicado = 0) {
  const subtotal = itensVenda.reduce(
    (total, item) =>
      total +
      (Number(item.precoVenda) || 0) * (Number(item.quantidade) || 0),
    0,
  )
  const desconto = Math.min(
    Math.max(Number(descontoAplicado) || 0, 0),
    100,
  )
  return Number((subtotal - subtotal * (desconto / 100)).toFixed(2))
}

function atualizarTotal() {
  let subtotal = 0

  document.querySelectorAll("[data-produto-venda]").forEach((seletor) => {
    const opcao = seletor.selectedOptions[0]
    if (!opcao || !opcao.value) return

    const preco = Number(opcao.dataset.precoVenda || 0)
    const nomeQuantidade = seletor.name.replace("produto", "quantidade")
    const quantidade = Number(
      document.querySelector(`[name="${nomeQuantidade}"]`)?.value || 0,
    )
    subtotal += preco * quantidade
  })

  const desconto = Number(
    document.querySelector('[name="desconto_aplicado"]')?.value || 0,
  )
  const total = Math.max(subtotal - desconto, 0)
  const elementoTotal = document.querySelector("[data-valor-total]")
  if (elementoTotal) elementoTotal.textContent = formatarMoeda(total)
}

export default function iniciarNovaVenda() {
  iniciarTela("nova-venda")

  const formulario = document.querySelector("[data-form-venda]")
  formulario?.addEventListener("input", atualizarTotal)
  formulario?.addEventListener("change", atualizarTotal)
  atualizarTotal()
}

if (typeof document !== "undefined") iniciarNovaVenda()
