import { iniciarTela } from './shared.js'

// Os filtros de período são links GET processados pela view do Django.
export default function iniciarDashboard() {
  iniciarTela('inicio')
}

if (typeof document !== 'undefined') iniciarDashboard()
