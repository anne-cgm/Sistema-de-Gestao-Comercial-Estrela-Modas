import { existsSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const diretorioTestes = path.dirname(fileURLToPath(import.meta.url))
const diretorioRaiz = path.resolve(diretorioTestes, '..')

const arquivosObrigatorios = [
  'manage.py',
  'requirements.txt',
  'config/settings.py',
  'config/urls.py',
  'estrela_modas/apps.py',
  'estrela_modas/urls.py',
  'estrela_modas/views.py',
  'estrela_modas/models.py',
  'estrela_modas/admin.py',
  'estrela_modas/tests.py',
  'estrela_modas/migrations/0001_initial.py',
  'frontend/templates/estrela_modas/index.html',
  'frontend/templates/estrela_modas/login.html',
  'frontend/templates/estrela_modas/dashboard.html',
  'frontend/templates/estrela_modas/produtos.html',
  'frontend/templates/estrela_modas/cadastro_produto.html',
  'frontend/templates/estrela_modas/estoque.html',
  'frontend/templates/estrela_modas/nova_venda.html',
  'frontend/templates/estrela_modas/clientes.html',
  'frontend/templates/estrela_modas/debitos.html',
  'frontend/templates/estrela_modas/mais_opcoes.html',
  'frontend/templates/estrela_modas/relatorios.html',
  'frontend/templates/estrela_modas/compras.html',
  'frontend/templates/estrela_modas/registro.html',
  'frontend/static/estrela_modas/login.js',
  'frontend/static/estrela_modas/dashboard.js',
  'frontend/static/estrela_modas/produtos.js',
  'frontend/static/estrela_modas/cadastro_produto.js',
  'frontend/static/estrela_modas/estoque.js',
  'frontend/static/estrela_modas/nova_venda.js',
  'frontend/static/estrela_modas/clientes.js',
  'frontend/static/estrela_modas/debitos.js',
  'frontend/static/estrela_modas/mais_opcoes.js',
  'frontend/static/estrela_modas/relatorios.js',
  'frontend/static/estrela_modas/compras.js',
  'frontend/static/estrela_modas/shared.js',
]

const arquivosAusentes = arquivosObrigatorios.filter(arquivo => {
  return !existsSync(path.join(diretorioRaiz, arquivo))
})

if (arquivosAusentes.length > 0) {
  throw new Error(`Arquivos obrigatórios ausentes:\n- ${arquivosAusentes.join('\n- ')}`)
}

console.log(`Verificação OK: ${arquivosObrigatorios.length} arquivos encontrados na raiz e em frontend/.`)
