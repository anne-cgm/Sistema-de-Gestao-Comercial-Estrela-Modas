const storageKeys = {
  clientes: "clientes",
  compras: "compras",
  dividas: "dividas",
  movimentosCredito: "movimentosCredito",
}

function lerLista(chave) {
  if (typeof localStorage === "undefined") return []

  try {
    const valor = JSON.parse(localStorage.getItem(chave) || "[]")
    return Array.isArray(valor) ? valor : []
  } catch {
    return []
  }
}

function salvarLista(chave, valores) {
  if (typeof localStorage !== "undefined") {
    localStorage.setItem(chave, JSON.stringify(valores))
  }
}

export function normalizarValor(valor) {
  return Math.round((Number(valor) || 0) * 100) / 100
}

export function formatarMoeda(valor) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(Number(valor) || 0)
}

export function carregarClientes() {
  return lerLista(storageKeys.clientes)
}

export function salvarClientes(clientes) {
  salvarLista(storageKeys.clientes, clientes)
}

export function carregarCompras() {
  return lerLista(storageKeys.compras)
}

export function salvarCompras(compras) {
  salvarLista(storageKeys.compras, compras)
}

export function carregarDividas() {
  return lerLista(storageKeys.dividas)
}

export function salvarDividas(dividas) {
  salvarLista(storageKeys.dividas, dividas)
}

export function carregarMovimentosCredito() {
  return lerLista(storageKeys.movimentosCredito)
}

export function salvarMovimentosCredito(movimentos) {
  salvarLista(storageKeys.movimentosCredito, movimentos)
}

export function calcularSaldoCredito(movimentos, clienteId) {
  return normalizarValor(
    movimentos
      .filter((movimento) => Number(movimento.clienteId) === Number(clienteId))
      .reduce((saldo, movimento) => {
        if (movimento.tipo === "concedido") return saldo + Number(movimento.valor)
        if (movimento.tipo === "utilizado") return saldo - Number(movimento.valor)
        return saldo
      }, 0),
  )
}

export function registrarMovimentoCredito(movimentos, movimento) {
  const valor = normalizarValor(movimento.valor)
  if (valor <= 0) {
    return { sucesso: false, mensagem: "Informe um valor válido.", movimentos }
  }

  if (movimento.tipo === "utilizado") {
    const saldo = calcularSaldoCredito(movimentos, movimento.clienteId)
    if (valor > saldo) {
      return {
        sucesso: false,
        mensagem: "O valor informado excede o crédito disponível.",
        movimentos,
      }
    }
  }

  return {
    sucesso: true,
    mensagem: "Movimento registrado.",
    movimento: { ...movimento, id: Date.now(), valor },
    movimentos: [
      { ...movimento, id: Date.now(), valor },
      ...movimentos,
    ],
  }
}
