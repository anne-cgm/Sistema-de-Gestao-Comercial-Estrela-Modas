const caminhosDasTelas = {
  login: "/login/",
  dashboard: "/dashboard/",
  produtos: "/produtos/",
  novo_produto: "/produtos/novo/",
  estoque: "/estoque/",
  "nova-venda": "/vendas/nova/",
  clientes: "/clientes/",
  debitos: "/debitos/",
  mais: "/mais/",
  relatorios: "/relatorios/",
  compras: "/compras/",
  despesas: "/despesas/",
  usuarios: "/usuarios/",
  novo_cliente: "/clientes/novo/",
  "cliente-detalhes": "/clientes/",
  trocas: "/trocas/",
}

const permissaoPorTela = {
  dashboard: "dashboard",
  produtos: "produtos",
  "novo_produto": "produtos",
  estoque: "estoque",
  compras: "estoque",
  "nova-venda": "vendas",
  clientes: "clientes",
  novo_cliente: "clientes",
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
  window.location.href = caminho
}

export function iniciarTela(abaAtiva) {
  atualizarPerfil()
  iniciarMenu()

  document.querySelectorAll("[data-screen]").forEach((elemento) => {
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
    // O nome do usuário autenticado ainda pode vir renderizado pelo Django.
  }
  nomePerfil =
    document.querySelector("[data-login-perfil]")?.dataset.loginPerfil ||
    nomePerfil

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
  if (menu.dataset.menuInicializado === "sim") return
  menu.dataset.menuInicializado = "sim"

  if (!document.querySelector("#menu-padrao-estrela")) {
    const estiloMenu = document.createElement("style")
    estiloMenu.id = "menu-padrao-estrela"
    estiloMenu.textContent = `
      .nav-brand {
        display: block !important;
        width: 170px !important;
        max-width: 170px !important;
        height: auto !important;
        margin: 0 auto 28px !important;
        border-radius: 8px !important;
      }
      .nav-top {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
      }
      .menu-close {
        display: inline-grid !important;
        place-items: center !important;
        min-width: 36px !important;
      }
      .menu-toggle {
        display: inline-grid !important;
      }
      @media (max-width: 1023px) {
        .nav {
          transform: translateX(-100%) !important;
        }
        .nav.is-open {
          transform: translateX(0) !important;
        }
        .menu-backdrop {
          display: block !important;
        }
        .menu-backdrop[hidden] {
          display: none !important;
        }
      }
      @media (min-width: 1024px) {
        .nav {
          transform: none !important;
        }
        .nav[hidden] {
          display: none !important;
        }
        .menu-backdrop {
          display: none !important;
        }
      }
    `
    document.head.append(estiloMenu)
  }

  if (!menu.querySelector(".nav-brand")) {
    const logo = document.createElement("img")
    logo.className = "nav-brand"
    logo.src = "/static/imagens/icon_da_loja.jpg"
    logo.alt = "Estrela Modas"
    logo.width = 1254
    logo.height = 1254
    logo.style.display = "block"
    logo.style.width = "170px"
    logo.style.height = "auto"
    logo.style.margin = "0 auto 28px"
    menu.querySelector(".nav-top")?.after(logo)
  }

  if (botaoFechar) {
    botaoFechar.textContent = "×"
    botaoFechar.setAttribute("aria-label", "Fechar menu")
  }

  if (!menu.querySelector('[data-tab="trocas"]')) {
    const linkTrocas = document.createElement("a")
    linkTrocas.className = "nav-link"
    linkTrocas.href = "/trocas/"
    linkTrocas.dataset.tab = "trocas"
    linkTrocas.innerHTML = '<span class="nav-icon">⇄</span>Trocas'
    const linkMais = menu.querySelector('[data-tab="mais"]')
    if (linkMais) linkMais.before(linkTrocas)
    else menu.append(linkTrocas)
  }

  const telaLarga = window.matchMedia("(min-width: 1024px)")
  let menuAberto = telaLarga.matches

  function atualizarMenu(devolverFoco = false) {
    if (telaLarga.matches) {
      menu.hidden = !menuAberto
      menu.classList.toggle("is-open", menuAberto)
    } else {
      menu.hidden = false
      menu.classList.toggle("is-open", menuAberto)
    }
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
    // O estado do menu não atravessa módulos e é recalculado por breakpoint.
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

export function iniciarMenuLateral() {
  const menu = document.querySelector('[data-menu]')
  if (!menu) return

  const fundo = document.querySelector('[data-fundo-menu]')
  const alternar = document.querySelector('[data-alternar-menu]')
  const fechar = document.querySelector('[data-fechar-menu]')

  const fecharMenu = () => {
    menu.classList.remove('is-open')
    if (fundo) fundo.hidden = true
    document.body.classList.remove('menu-sobreposto')
    alternar?.setAttribute('aria-expanded', 'false')
  }

  alternar?.addEventListener('click', () => {
    menu.classList.add('is-open')
    if (fundo) fundo.hidden = false
    document.body.classList.add('menu-sobreposto')
    alternar.setAttribute('aria-expanded', 'true')
  })
  fechar?.addEventListener('click', fecharMenu)
  fundo?.addEventListener('click', fecharMenu)
  document.addEventListener('keydown', evento => {
    if (evento.key === 'Escape') fecharMenu()
  })
}

export function exibirMensagem(mensagem) {
  document.querySelector(".toast")?.remove()
  const aviso = document.createElement("div")
  aviso.className = "toast"
  aviso.textContent = mensagem
  document.body.append(aviso)
  window.setTimeout(() => aviso.remove(), 2200)
}

if (typeof document !== "undefined") {
  const iniciarMenusPadrao = () => {
    const menu = document.querySelector("[data-menu]")
    if (menu) iniciarMenu()
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciarMenusPadrao, {
      once: true,
    })
  } else {
    iniciarMenusPadrao()
  }
}
