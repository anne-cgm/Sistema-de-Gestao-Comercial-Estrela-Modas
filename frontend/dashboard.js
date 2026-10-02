import { iniciarTela } from './shared.js'

export default function iniciarPainel() {
  iniciarTela('inicio')
}

if (typeof document !== 'undefined') iniciarPainel()
