import { existsSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const diretorioRaiz = path.dirname(fileURLToPath(import.meta.url))

const arquivosObrigatorios = [
  'index.html',
  'vite.config.ts',
  'src/screens/login.html',
  'src/screens/login.js',
  'src/screens/dashboard.html',
  'src/screens/dashboard.js',
  'src/screens/produtos.html',
  'src/screens/produtos.js',
  'src/screens/novo-produto.html',
  'src/screens/novo-produto.js',
  'src/screens/estoque.html',
  'src/screens/estoque.js',
  'src/screens/nova-venda.html',
  'src/screens/nova-venda.js',
  'src/screens/clientes.html',
  'src/screens/clientes.js',
  'src/screens/debitos.html',
  'src/screens/debitos.js',
  'src/screens/mais.html',
  'src/screens/mais.js',
  'src/screens/relatorios.html',
  'src/screens/relatorios.js',
  'src/screens/shared.js',
]

const arquivosAusentes = arquivosObrigatorios.filter(arquivo => {
  return !existsSync(path.join(diretorioRaiz, arquivo))
})

if (arquivosAusentes.length > 0) {
  throw new Error(`Arquivos obrigatórios ausentes:\n- ${arquivosAusentes.join('\n- ')}`)
}

console.log(`Verificação OK: ${arquivosObrigatorios.length} arquivos encontrados.`)
