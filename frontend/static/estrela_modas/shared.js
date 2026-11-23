const caminhosDasTelas = {
  login: "./login.html",
  dashboard: "./dashboard.html",
  produtos: "./produtos.html",
  "novo_produto": "./novo_produto.html",
  estoque: "./estoque.html",
  "nova-venda": "./nova-venda.html",
  clientes: "./clientes.html",
  debitos: "./debitos.html",
  mais: "./mais.html",
  relatorios: "./relatorios.html",
  compras: "./compras.html",
  usuarios: "./usuarios.html",
  "novo-cliente": "./novo-cliente.html",
  "cliente-detalhes": "./cliente-detalhes.html",
  trocas: "./trocas.html",
}

const permissaoPorTela = {
  dashboard: "dashboard",
  produtos: "produtos",
  "novo_produto": "produtos",
  estoque: "estoque",
  compras: "estoque",
  "nova-venda": "vendas",
  clientes: "clientes",
  "novo-cliente": "clientes",
  "cliente-detalhes": "clientes",
  debitos: "clientes",
  trocas: "clientes",
  relatorios: "relatorios",
  usuarios: "usuarios",
}

export function podeAcessarTela(tela, sessao) {
  if (!tela || tela === "login" || tela === "mais") return true
  if (sessao?.perfil === "administrador") return true
  const permissao = permissaoPorTela[tela]
  return !permissao || Boolean(sessao?.permissoes?.includes(permissao))
}

export function obterSessaoAcesso(armazenamento = globalThis.sessionStorage) {
  try {
    const perfil = armazenamento?.getItem("estrelaPerfil") || "administrador"
    const permissoes = JSON.parse(
      armazenamento?.getItem("estrelaPermissoes") || "[]",
    )
    return {
      perfil,
      permissoes: Array.isArray(permissoes) ? permissoes : [],
    }
  } catch {
    return { perfil: "administrador", permissoes: [] }
  }
}

export function navegarParaTela(tela) {
  const caminho = caminhosDasTelas[tela]
  if (!caminho) return
  if (!podeAcessarTela(tela, obterSessaoAcesso())) {
    window.location.href = caminhosDasTelas.dashboard
    return
  }
  window.location.href = caminho
}

export function iniciarTela(abaAtiva) {
  const sessao = obterSessaoAcesso()
  const arquivoAtual = window.location.pathname.split("/").at(-1)
  const telaAtual = Object.entries(caminhosDasTelas).find(
    ([, caminho]) => caminho.replace("./", "") === arquivoAtual,
  )?.[0]
  if (!podeAcessarTela(telaAtual, sessao)) {
    window.location.replace(caminhosDasTelas.dashboard)
    return
  }

  atualizarPerfil()
  iniciarMenu()

  document.querySelectorAll("[data-screen]").forEach((elemento) => {
    if (!podeAcessarTela(elemento.dataset.screen, sessao)) {
      elemento.remove()
      return
    }
    elemento.addEventListener("click", (evento) => {
      evento.preventDefault()
      navegarParaTela(elemento.dataset.screen)
    })
  })

  if (abaAtiva) {
    document
      .querySelector(`[data-tab="${abaAtiva}"]`)
      ?.classList.add("is-active")
  }

  document.querySelector("[data-sair]")?.addEventListener("click", () => {
    try {
      window.sessionStorage.removeItem("estrelaNomePerfil")
      window.sessionStorage.removeItem("estrelaPerfil")
      window.sessionStorage.removeItem("estrelaPermissoes")
    } catch {
      // O login também pode ser aberto quando o armazenamento estiver bloqueado.
    }
  })
}

export function formatarNomePerfil(usuario) {
  return usuario
    .trim()
    .split("@")[0]
    .replace(/[._-]+/g, " ")
    .split(/\s+/)
    .filter(Boolean)
    .map(
      (parte) =>
        parte.charAt(0).toLocaleUpperCase("pt-BR") +
        parte.slice(1).toLocaleLowerCase("pt-BR"),
    )
    .join(" ")
}

export function obterInicialPerfil(usuario) {
  const nomeFormatado = formatarNomePerfil(usuario)
  return nomeFormatado
    ? nomeFormatado.charAt(0).toLocaleUpperCase("pt-BR")
    : "P"
}

function atualizarPerfil() {
  let nomePerfil = ""
  try {
    nomePerfil = window.sessionStorage.getItem("estrelaNomePerfil") || ""
  } catch {
    // Sem armazenamento, exibe a inicial padrão.
  }

  const inicialPerfil = obterInicialPerfil(nomePerfil)
  document.querySelectorAll("[data-nome-perfil]").forEach((elemento) => {
    elemento.textContent = inicialPerfil
    elemento.setAttribute(
      "aria-label",
      nomePerfil ? `Perfil de ${nomePerfil}` : "Perfil",
    )
    if (nomePerfil) {
      elemento.setAttribute("title", nomePerfil)
    } else {
      elemento.removeAttribute("title")
    }
  })
  const saudacao = document.querySelector("[data-saudacao]")
  if (saudacao)
    saudacao.textContent = nomePerfil ? `Olá, ${nomePerfil}` : "Olá!"
}

function iniciarMenu() {
  const menu = document.querySelector("[data-menu]")
  const botaoMenu = document.querySelector("[data-alternar-menu]")
  const botaoFechar = document.querySelector("[data-fechar-menu]")
  const fundoMenu = document.querySelector("[data-fundo-menu]")
  if (!menu || !botaoMenu) return

  if (!menu.querySelector('[data-tab="trocas"]')) {
    const linkTrocas = document.createElement("a")
    linkTrocas.className = "nav-link"
    linkTrocas.href = "./trocas.html"
    linkTrocas.dataset.tab = "trocas"
    linkTrocas.innerHTML = '<span class="nav-icon">⇄</span>Trocas'
    menu.querySelector('[data-tab="mais"]')?.before(linkTrocas)
  }

  const telaLarga = window.matchMedia("(min-width: 1024px)")
  let menuAberto = telaLarga.matches
  try {
    if (telaLarga.matches)
      menuAberto = window.sessionStorage.getItem("estrelaMenuFechado") !== "sim"
  } catch {
    // A preferência de menu é opcional.
  }

  function atualizarMenu(devolverFoco = false) {
    menu.hidden = !menuAberto
    document
      .querySelector(".phone")
      ?.classList.toggle("menu-fechado", !menuAberto)
    document.body.classList.toggle(
      "menu-sobreposto",
      menuAberto && !telaLarga.matches,
    )
    const conteudo = document.querySelector(".screen")
    if (conteudo) conteudo.inert = menuAberto && !telaLarga.matches
    botaoMenu.setAttribute("aria-expanded", String(menuAberto))
    botaoMenu.setAttribute(
      "aria-label",
      menuAberto ? "Fechar menu" : "Abrir menu",
    )
    if (fundoMenu) fundoMenu.hidden = !menuAberto || telaLarga.matches
    if (devolverFoco) botaoMenu.focus()
  }

  function fecharMenu() {
    menuAberto = false
    guardarPreferencia()
    atualizarMenu(true)
  }

  function guardarPreferencia() {
    if (!telaLarga.matches) return
    try {
      window.sessionStorage.setItem(
        "estrelaMenuFechado",
        menuAberto ? "nao" : "sim",
      )
    } catch {
      // O menu permanece funcional sem salvar sua preferência.
    }
  }

  botaoMenu.addEventListener("click", () => {
    menuAberto = !menuAberto
    guardarPreferencia()
    atualizarMenu()
    if (menuAberto && !telaLarga.matches) botaoFechar?.focus()
  })
  botaoFechar?.addEventListener("click", fecharMenu)
  fundoMenu?.addEventListener("click", fecharMenu)
  document.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape" && menuAberto) fecharMenu()
    if (evento.key !== "Tab" || !menuAberto || telaLarga.matches) return
    const itens = [...menu.querySelectorAll("a, button")]
    const primeiro = itens[0]
    const ultimo = itens.at(-1)
    if (evento.shiftKey && document.activeElement === primeiro) {
      evento.preventDefault()
      ultimo?.focus()
    } else if (!evento.shiftKey && document.activeElement === ultimo) {
      evento.preventDefault()
      primeiro?.focus()
    }
  })
  telaLarga.addEventListener("change", () => {
    menuAberto = telaLarga.matches
    atualizarMenu()
  })
  atualizarMenu()
}

export function exibirMensagem(mensagem) {
  document.querySelector(".toast")?.remove()
  const aviso = document.createElement("div")
  aviso.className = "toast"
  aviso.textContent = mensagem
  document.body.append(aviso)
  window.setTimeout(() => aviso.remove(), 2200)
}
