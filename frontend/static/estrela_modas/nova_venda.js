import { iniciarTela } from './shared.js'

export default function iniciarNovaVenda() {
  iniciarTela('venda')
  atualizarTotalVenda()
  document.querySelector('[data-form-venda]')?.addEventListener('input', atualizarTotalVenda)
  document.querySelector('[data-form-venda]')?.addEventListener('change', atualizarTotalVenda)
  configurarLeitorQr()
}

function atualizarTotalVenda() {
  const subtotal = [...document.querySelectorAll('[data-produto-venda]')].reduce((total, seletor) => {
    const produto = seletor.selectedOptions[0]
    const campoQuantidade = document.querySelector(`[name="${seletor.name.replace(/produto$/, 'quantidade')}"]`)
    return total + Number(produto?.dataset.precoVenda ?? 0) * Number(campoQuantidade?.value ?? 0)
  }, 0)
  const desconto = Number(document.querySelector('[name="desconto_aplicado"]')?.value ?? 0)
  const valorTotal = Math.max(0, subtotal - desconto)
  const elementoValorTotal = document.querySelector('[data-valor-total]')

  if (elementoValorTotal) elementoValorTotal.textContent = formatarMoeda(valorTotal)
}

function configurarLeitorQr() {
  const campoQr = document.getElementById('qr-input')
  const status = document.getElementById('qr-status')
  const botaoBuscar = document.querySelector('[data-qr-search]')
  const botaoCamera = document.querySelector('[data-qr-camera]')
  const botaoLimpar = document.querySelector('[data-qr-reset]')
  const video = document.getElementById('qr-video')

  if (!campoQr || !botaoBuscar || !botaoCamera || !botaoLimpar || !video || !status) return

  const localizarProduto = (valorCodigo) => {
    const codigo = (valorCodigo || '').trim()
    if (!codigo) return false

    const selects = [...document.querySelectorAll('[data-produto-venda]')]
    for (const select of selects) {
      const opcoes = [...select.options].filter((option) => option.value)
      const produto = opcoes.find((option) => {
        const texto = (option.dataset.nome || option.textContent || '').toLowerCase()
        const sku = (option.dataset.sku || '').toLowerCase()
        const valor = codigo.toLowerCase()
        return texto.includes(valor) || sku.includes(valor) || option.value === codigo
      })

      if (produto) {
        select.value = produto.value
        status.textContent = `Produto localizado: ${produto.dataset.nome || produto.textContent.trim()}`
        exibirMensagem('Produto localizado pelo QR/SKU.')
        return true
      }
    }

    status.textContent = 'Código não encontrado. Tente outro QR/SKU ou selecione o produto manualmente.'
    exibirMensagem('Código não encontrado.')
    return false
  }

  botaoBuscar.addEventListener('click', () => localizarProduto(campoQr.value))
  campoQr.addEventListener('keydown', (evento) => {
    if (evento.key === 'Enter') {
      evento.preventDefault()
      localizarProduto(campoQr.value)
    }
  })

  botaoLimpar.addEventListener('click', () => {
    campoQr.value = ''
    status.textContent = 'Digite o código do QR/SKU ou abra a câmera do celular para escanear.'
    if (video.srcObject) {
      video.srcObject.getTracks().forEach((track) => track.stop())
      video.srcObject = null
    }
    video.style.display = 'none'
  })

  botaoCamera.addEventListener('click', async () => {
    if (!('mediaDevices' in navigator) || !navigator.mediaDevices?.getUserMedia) {
      status.textContent = 'Câmera não disponível neste navegador. Digite o código do QR/SKU.'
      return
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
      video.srcObject = stream
      video.style.display = 'block'
      status.textContent = 'Câmera ativa. Aponte para o QR da peça.'

      if (!('BarcodeDetector' in window)) {
        status.textContent = 'Câmera ativa. O navegador não suporta leitura de QR nativa; digite o código do QR/SKU.'
        return
      }

      const detector = new window.BarcodeDetector({ formats: ['qr_code'] })
      const escanear = async () => {
        try {
          const resultados = await detector.detect(video)
          if (!resultados.length) {
            requestAnimationFrame(escanear)
            return
          }

          const codigo = resultados[0].rawValue
          if (localizarProduto(codigo)) {
            stream.getTracks().forEach((track) => track.stop())
            video.srcObject = null
            video.style.display = 'none'
          }
        } catch (erro) {
          requestAnimationFrame(escanear)
        }
      }

      video.addEventListener('loadedmetadata', () => {
        video.play().catch(() => {})
        escanear()
      }, { once: true })
    } catch (erro) {
      status.textContent = 'Não foi possível acessar a câmera. Digite o código do QR/SKU.'
    }
  })
}

export function calcularTotalVenda(itensVenda, descontoAplicado = 0) {
  const subtotal = itensVenda.reduce((valorAcumulado, itemVenda) => {
    return valorAcumulado + itemVenda.precoVenda * itemVenda.quantidade
  }, 0)

  const percentualDesconto = Math.min(Math.max(descontoAplicado, 0), 100)
  return Number((subtotal - (subtotal * percentualDesconto) / 100).toFixed(2))
}

export function formatarMoeda(valor) {
  return valor.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })
}

function exibirMensagem(mensagem) {
  const existente = document.querySelector('.toast')
  if (existente) existente.remove()

  const aviso = document.createElement('div')
  aviso.className = 'toast'
  aviso.textContent = mensagem
  document.body.append(aviso)
  window.setTimeout(() => aviso.remove(), 2200)
}

if (typeof document !== 'undefined') iniciarNovaVenda()
