import { iniciarTela } from './shared.js'

export default function iniciarClientes() {
  iniciarTela('clientes')

  // DADOS DOS CLIENTES:
  // Atualmente, a listagem, a pesquisa e os dados financeiros
  // são fornecidos pelo Django através do template.
  //
  // Futuramente, a integração do saldo de crédito e dos movimentos
  // de crédito deverá utilizar os dados persistidos no banco de dados,
  // e não apenas informações armazenadas no navegador.
}

// Evita executar o código em ambientes de teste sem DOM.
if (typeof document !== 'undefined') iniciarClientes()

  
  
