import { iniciarTela } from "./shared.js"

// Inicia a tela de detalhes do cliente, chamando a função iniciarTela com o parâmetro "clientes" para configurar a interface e funcionalidades específicas para a seção de clientes.
export default function iniciarDetalhesCliente() {
  iniciarTela("clientes")

  const dialogoExclusao = document.querySelector("[data-dialogo-excluir]")
  document
    .querySelector("[data-abrir-dialogo-excluir]")
    ?.addEventListener("click", () => dialogoExclusao?.showModal())
  dialogoExclusao
    ?.querySelector("[data-cancelar-exclusao]")
    ?.addEventListener("click", () => dialogoExclusao.close())
}

// Verifica se o código está sendo executado em um ambiente de navegador (onde o objeto document está definido) e, em caso afirmativo, chama a função iniciarDetalhesCliente para iniciar a tela de detalhes do cliente.
if (typeof document !== "undefined") iniciarDetalhesCliente()
