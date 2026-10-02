const test = require('node:test');
const assert = require('node:assert/strict');

const {
  validarLogin,
  calcularTotalVenda,
  produtoComEstoqueBaixo,
  buscarProduto,
  mostrarTela,
  inicializarApp
} = require('../script.js');

const originalDocument = global.document;

test.afterEach(() => {
  if (typeof originalDocument === 'undefined') {
    delete global.document;
    return;
  }

  global.document = originalDocument;
});

test('validarLogin aceita usuário e senha preenchidos', () => {
  assert.equal(validarLogin('kamila', '123456'), true);
});

test('validarLogin rejeita campos vazios', () => {
  assert.equal(validarLogin('   ', '123456'), false);
  assert.equal(validarLogin('kamila', '   '), false);
  assert.equal(validarLogin('', ''), false);
});

test('calcularTotalVenda aplica desconto corretamente', () => {
  const produtos = [
    { preco: 100, quantidade: 2 },
    { preco: 50, quantidade: 1 }
  ];

  assert.equal(calcularTotalVenda(produtos, 10), 225);
});

test('calcularTotalVenda retorna valor sem desconto quando desconto é zero', () => {
  const produtos = [
    { preco: 79.9, quantidade: 2 },
    { preco: 119.9, quantidade: 1 }
  ];

  assert.equal(calcularTotalVenda(produtos, 0), 279.7);
});

test('produtoComEstoqueBaixo identifica itens com estoque crítico', () => {
  assert.equal(produtoComEstoqueBaixo(1), true);
  assert.equal(produtoComEstoqueBaixo(0), true);
  assert.equal(produtoComEstoqueBaixo(2), false);
});

test('buscarProduto filtra produtos por nome sem diferenciar maiúsculas/minúsculas', () => {
  const produtos = [
    { nome: 'Camiseta Básica' },
    { nome: 'Calça Wide Leg' },
    { nome: 'Bolsa Mini' }
  ];

  const resultado = buscarProduto(produtos, 'calça');

  assert.deepEqual(resultado.map(p => p.nome), ['Calça Wide Leg']);
});

test('buscarProduto retorna lista vazia quando termo não existe', () => {
  const produtos = [
    { nome: 'Camiseta Básica' },
    { nome: 'Vestido Floral' }
  ];

  assert.deepEqual(buscarProduto(produtos, 'sapato'), []);
});

test('mostrarTela ativa a tela correta quando existe DOM', () => {
  const { JSDOM } = require('jsdom');
  const dom = new JSDOM(`
    <div id="login-screen" class="screen active"></div>
    <div id="dashboard-screen" class="screen"></div>
  `);

  global.document = dom.window.document;

  mostrarTela('dashboard-screen');

  const login = document.getElementById('login-screen');
  const dashboard = document.getElementById('dashboard-screen');

  assert.equal(login.classList.contains('active'), false);
  assert.equal(dashboard.classList.contains('active'), true);
});

test('inicializarApp não quebra quando o formulário não existe', () => {
  global.document = {
    getElementById: () => null
  };

  assert.doesNotThrow(() => inicializarApp());
});
