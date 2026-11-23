import { iniciarTela } from "./shared.js"

export default function iniciarNovoCliente() {
  iniciarTela("novo_cliente")
}

if (typeof document !== "undefined") iniciarNovoCliente()
