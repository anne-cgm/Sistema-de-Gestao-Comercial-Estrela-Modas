import { existsSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const diretorioTestes = path.dirname(fileURLToPath(import.meta.url))
const diretorioRaiz = path.resolve(diretorioTestes, '..')

const arquivosObrigatorios = [
  'manage.py',
  'requirements.txt',
  'backend/config/settings.py',
  'backend/config/urls.py',
  'backend/apps/__init__.py',
  'backend/apps/usuarios/apps.py',
  'backend/apps/usuarios/api.py',
  'backend/apps/usuarios/models.py',
  'backend/apps/usuarios/migrations/0001_initial.py',
  'backend/apps/core/apps.py',
  'backend/apps/core/urls.py',
  'backend/apps/core/views.py',
  'backend/apps/core/migrations/0001_initial.py',
  'backend/apps/dashboard/apps.py',
  'backend/apps/dashboard/urls.py',
  'backend/apps/dashboard/views.py',
  'backend/apps/produtos/apps.py',
  'backend/apps/produtos/models.py',
  'backend/apps/produtos/forms.py',
  'backend/apps/produtos/views.py',
  'backend/apps/clientes/apps.py',
  'backend/apps/clientes/models.py',
  'backend/apps/clientes/forms.py',
  'backend/apps/clientes/views.py',
  'backend/apps/vendas/apps.py',
  'backend/apps/vendas/models.py',
  'backend/apps/vendas/forms.py',
  'backend/apps/vendas/views.py',
  'backend/apps/estoque/apps.py',
  'backend/apps/estoque/models.py',
  'backend/apps/estoque/forms.py',
  'backend/apps/estoque/views.py',
  'backend/apps/core/forms.py',
  'backend/apps/trocas/apps.py',
  'backend/apps/trocas/models.py',
  'backend/apps/trocas/forms.py',
  'backend/apps/trocas/views.py',
  'frontend/templates/estrela_modas/login.html',
  'frontend/templates/estrela_modas/dashboard.html',
  'frontend/templates/estrela_modas/produtos.html',
  'frontend/templates/estrela_modas/novo_produto.html',
  'frontend/templates/estrela_modas/estoque.html',
  'frontend/templates/estrela_modas/nova_venda.html',
  'frontend/templates/estrela_modas/clientes.html',
  'frontend/templates/estrela_modas/cliente-detalhes.html',
  'frontend/templates/estrela_modas/novo_cliente.html',
  'frontend/templates/estrela_modas/debitos.html',
  'frontend/templates/estrela_modas/mais_opcoes.html',
  'frontend/templates/estrela_modas/relatorios.html',
  'frontend/templates/estrela_modas/compras.html',
  'frontend/templates/estrela_modas/registro.html',
  'frontend/templates/estrela_modas/trocas.html',
  'frontend/templates/estrela_modas/usuarios.html',
  'frontend/static/estrela_modas/login.js',
  'frontend/static/estrela_modas/dashboard.js',
  'frontend/static/estrela_modas/produtos.js',
  'frontend/static/estrela_modas/novo_produto.js',
  'frontend/static/estrela_modas/estoque.js',
  'frontend/static/estrela_modas/nova_venda.js',
  'frontend/static/estrela_modas/clientes.js',
  'frontend/static/estrela_modas/cliente-detalhes.js',
  'frontend/static/estrela_modas/novo_cliente.js',
  'frontend/static/estrela_modas/debitos.js',
  'frontend/static/estrela_modas/mais_opcoes.js',
  'frontend/static/estrela_modas/relatorios.js',
  'frontend/static/estrela_modas/compras.js',
  'frontend/static/estrela_modas/shared.js',
  'frontend/static/estrela_modas/clientes-data.js',
]

const arquivosAusentes = arquivosObrigatorios.filter(arquivo => {
  return !existsSync(path.join(diretorioRaiz, arquivo))
})

if (arquivosAusentes.length > 0) {
  throw new Error(`Arquivos obrigatórios ausentes:\n- ${arquivosAusentes.join('\n- ')}`)
}

console.log(`Verificação OK: ${arquivosObrigatorios.length} arquivos encontrados na raiz e em frontend/.`)
