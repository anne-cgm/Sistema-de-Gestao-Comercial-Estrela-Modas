import { iniciarTela } from './shared.js'

// Os filtros de período são links GET; a view do Django consulta os dados e
// devolve a página com os indicadores e o gráfico do intervalo selecionado.
export default function iniciarDashboard() {
  // Ativa a navegação lateral e marca o Dashboard como a tela atual.
  iniciarTela('inicio')
}

if (typeof document !== 'undefined') iniciarDashboard()
