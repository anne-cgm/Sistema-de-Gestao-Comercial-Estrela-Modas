import { iniciarTela } from './shared.js'

export default function iniciarDebitos() {
  iniciarTela('clientes')
}

if (typeof document !== 'undefined') iniciarDebitos()
