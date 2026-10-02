import { existsSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const diretorioTestes = path.dirname(fileURLToPath(import.meta.url))
const diretorioRaiz = path.resolve(diretorioTestes, '..')

const arquivosObrigatorios = [
  'frontend/index.html',
  'frontend/cadastro_produto.html',
  'frontend/cadastro_produto.js',
  'frontend/clientes.html',
  'frontend/clientes.js',
  'frontend/dashboard.html',
  'frontend/dashboard.js',
  'frontend/debitos.html',
  'frontend/debitos.js',
  'frontend/estoque.html',
  'frontend/estoque.js',
  'frontend/login.html',
  'frontend/login.js',
  'frontend/mais_opcoes.html',
  'frontend/mais_opcoes.js',
  'frontend/nova_venda.html',
  'frontend/nova_venda.js',
  'frontend/produtos.html',
  'frontend/produtos.js',
  'frontend/relatorios.html',
  'frontend/relatorios.js',
  'frontend/shared.js',
]

const arquivosAusentes = arquivosObrigatorios.filter(arquivo => {
  return !existsSync(path.join(diretorioRaiz, arquivo))
})

if (arquivosAusentes.length > 0) {
  throw new Error(`Arquivos obrigatórios ausentes:\n- ${arquivosAusentes.join('\n- ')}`)
}

console.log(`Verificação OK: ${arquivosObrigatorios.length} arquivos encontrados.`)
