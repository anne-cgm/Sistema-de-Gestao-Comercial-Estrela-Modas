import { iniciarTela } from './shared.js'

export default function iniciarRelatorios() {
  iniciarTela('mais')
  configurarExportacaoRelatorio()
}

function configurarExportacaoRelatorio() {
  const botaoCsv = document.querySelector('[data-export="csv"]')
  const botaoImprimir = document.querySelector('[data-print-report]')

  if (botaoCsv) {
    botaoCsv.addEventListener('click', () => {
      const titulo = document.querySelector('.title')?.textContent?.trim() || 'Relatórios'
      const vendas = document.querySelector('.report-value')?.textContent?.trim() || 'R$ 0,00'
      const quantidade = document.querySelector('.row-sub')?.textContent?.trim() || '0 vendas registradas no mês'
      const produtos = [...document.querySelectorAll('.row-title')].map((item) => item.textContent.trim())

      const linhas = [
        ['Relatório', titulo],
        ['Vendas no período', vendas],
        ['Quantidade de vendas', quantidade],
        [],
        ['Produto', 'Detalhe'],
      ]

      produtos.forEach((produto) => {
        linhas.push([produto, 'Produto mais vendido'])
      })

      const csv = linhas.map((linha) => linha.map((celula) => `"${String(celula ?? '').replace(/"/g, '""')}"`).join(';')).join('\r\n')
      const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'relatorios-estrela-modas.csv'
      document.body.appendChild(link)
      link.click()
      link.remove()
      URL.revokeObjectURL(url)
    })
  }

  if (botaoImprimir) {
    botaoImprimir.addEventListener('click', () => {
      window.print()
    })
  }
}

if (typeof document !== 'undefined') iniciarRelatorios()
