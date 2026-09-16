function validarLogin(usuario, senha) {
    return usuario.trim() !== "" && senha.trim() !== "";
}

function calcularTotalVenda(produtos, desconto) {
    const subtotal = produtos.reduce((total, produto) => {
        return total + produto.preco * produto.quantidade;
    }, 0);

    return Number((subtotal - subtotal * desconto / 100).toFixed(2));
}

function produtoComEstoqueBaixo(quantidade) {
    return quantidade <= 1;
}

function buscarProduto(produtos, termo) {
    const busca = termo.toLowerCase().trim();

    return produtos.filter(produto =>
        produto.nome.toLowerCase().includes(busca)
    );
}

function mostrarTela(telaId) {
    if (typeof document === 'undefined') {
        return;
    }

    const telas = document.querySelectorAll('.screen');
    telas.forEach(tela => {
        tela.classList.toggle('active', tela.id === telaId);
    });
}

function inicializarApp() {
    if (typeof document === 'undefined') {
        return;
    }

    const usuarioInput = document.getElementById('usuario');
    const senhaInput = document.getElementById('senha');
    const btnEntrar = document.getElementById('btnEntrar');

    if (!btnEntrar || !usuarioInput || !senhaInput) {
        return;
    }

    btnEntrar.addEventListener('click', () => {
        const usuario = usuarioInput.value;
        const senha = senhaInput.value;

        if (!validarLogin(usuario, senha)) {
            alert('Preencha usuário e senha para continuar.');
            return;
        }

        mostrarTela('dashboard-screen');
    });

    usuarioInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            btnEntrar.click();
        }
    });

    senhaInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            btnEntrar.click();
        }
    });
}

if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', inicializarApp);
}

if (typeof module !== 'undefined') {
    module.exports = {
        validarLogin,
        calcularTotalVenda,
        produtoComEstoqueBaixo,
        buscarProduto,
        mostrarTela,
        inicializarApp
    };
}