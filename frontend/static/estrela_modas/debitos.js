  // INTEGRAÇÃO COM DJANGO:
  // - A listagem de dívidas é renderizada pelo template Django.
  // - O total pendente e os saldos vêm da view.
  // - O formulário envia os dados por POST para a view.
  // - Os pagamentos recentes são carregados pelo Django.
  //
  // FUNCIONALIDADES FUTURAS:
  // - Implementar o uso de crédito da loja para quitar dívidas.
  //   Essa funcionalidade precisa ser integrada aos modelos,
  //   formulários e views do Django para registrar os movimentos
  //   de crédito no banco de dados.
  // - Caso necessário, implementar filtros e atualização dinâmica
  //   das informações sem recarregar a página.


import { iniciarTela } from './shared.js'

export default function iniciarDebitos() {
  // Marca a opção de clientes como ativa no menu.
  iniciarTela('clientes')

  // Os dados de dívidas, pagamentos e saldos são carregados
  // diretamente pelo Django no HTML.
  // O formulário de pagamento também é processado pela view.
}

if (typeof document !== 'undefined') iniciarDebitos()

