create database estrela_modas;

use estrela_modas;

create table if not exists usuario (
	id int auto_increment primary key,
    nome varchar(255) not null,
    senha varchar(255) not null,
    login varchar(100) not null unique,
    ativo boolean not null default TRUE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    
create table if not exists categoria (
	id int auto_increment primary key,
    nome varchar(100) not null,
    descricao text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table if not exists produto (
	id int auto_increment primary key,
    sku_pai varchar(50) not null unique,
    nome varchar(255) not null,
    descricao text,
    material varchar(100),
    estampa varchar(100),
    composicao varchar(100),
    preco_custo decimal(10,2) not null,
    preco_venda decimal(10,2) not null,
    status boolean not null default TRUE,
    categoria_id int not null,
    
		constraint fk_produto_categoria
			foreign key (cateogria_id)
            references categoria(id)
            on delete restrict
            on update cascade
		) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table if not exists variacao_produto (
	id int auto_increment primary key,
    sku varchar(50) not null unique,
    tamanho varchar(20) not null,
    cor varchar(50) not null,
    codigo_qr varchar(255),
    produto_id int not null,
    
		constraint fk_variacao_produto
			foreign key (produto_id)
            references produto(id)
            on delete cascade
            on update cascade
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    
create table if not exists estoque (
	id int auto_increment primary key,
    quantidade int not null default 0,
    minimo int not null default 0,
    variacao_produto_id int not null unique,
    
		constraint fk_estoque_varicao
        foreign key (variacao_produto_id)
        references variacao_produto(id)
        on delete cascade
        on update cascade
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    
create table if not exists movimentacao_estoque (
	id int auto_increment primary key,
    tipo varchar(50) not null,
    quantidade int not null,
    data_hora datetime not null default current_timestamp,
    estoque_id int not null,
    
	constraint fk_movimentacao_estoque
		foreign key (estoque_id)
        references estoque(id)
        on delete cascade
        on update cascade
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    
create table if not exists cliente (
	id int auto_increment primary key,
    nome varchar(255) not null,
    telefone varchar(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table if not exists despesa (
	id int auto_increment primary key,
    descricao varchar(255) not null,
    valor decimal(10,2) not null,
    data date not null,
    categoria varchar(100),
    usuario_id int not null,
    
    constraint fk_despesa_usuario
		foreign key (usuario_id)
        references usuario(id)
        on delete cascade
        on update cascade
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table if not exists compra (
	id int auto_increment primary key,
    data date not null,
    valorTotal decimal(10,2) not null default 0.00,
    usuario_id int not null,
    
    constraint fk_compra_usuario
		foreign key (usuario_id)
        references usuario(id)
        on delete cascade
        on update cascade
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        
create table if not exists item_compra (
	id int auto_increment primary key,
    quantidade int not null,
    valor_unitario decimal(10,2) not null,
    subtotal decimal(10,2) not null,
    compra_id int not null,
    variacao_produto_id int not null,
    
    constraint fk_item_compra_compra
		foreign key (compra_id) 
		references compra(id)
		on delete cascade
		on update cascade,
	constraint fk_item_compra_variacao
		foreign key (variacao_produto_id)
        references variacao_produto(id)
        on delete restrict
        on update cascade
		) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        
    
create table if not exists venda (
	id int auto_increment primary key,
	data_hora datetime not null,
	subtotal decimal(10,2),
	desconto decimal(10,2),
	valor_total decimal(10,2),
	forma_pagamento varchar(5),
	usuario_id int not null,
    cliente_id int null,
        
	constraint fk_venda_usuario
		foreign key (usuario_id)
		references usuario(id)
		on delete cascade
		on update cascade,
	constraint fk_venda_cliente
		foreign key (cliente_id)
        references cliente(id)
        on delete set null
        on update cascade
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
	
create table if not exists item_venda (
	id int auto_increment primary key,
    quantidade int not null,
    preco_unitario decimal(10,2) not null,
    subtotal decimal(10,2) not null,
    tipo varchar(50) not null,
    venda_id int not null,
    variacao_produto_id int not null,
    
		constraint fk_item_venda_venda
			foreign key (venda_id)
            references venda(id)
            on delete cascade
            on update cascade,
            
		constraint fk_item_venda_variacao
			foreign key (variacao_produto_id)
            references variacao_produto(id)
            on delete restrict
            on update cascade
		) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    
create table if not exists troca (
	id int auto_increment primary key,
	data date not null,
	diferenca_preco decimal(10,2),
	possui_etiqueta boolean default TRUE, 
	esta_manchado_ou_lavado boolean default false, -- mudar nome da variável?
    venda_id int not null,
        
	constraint fk_troca_venda
		foreign key (venda_id)
		references venda(id)
		on delete cascade
		on update cascade
		) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table if not exists item_troca (
	id int auto_increment primary key,
    quantidade int not null,
    troca_id int not null,
    variacao_produto_id int not null,
    
    constraint fk_item_troca_troca
		foreign key (troca_id)
        references troca(id)
        on delete cascade
        on update cascade,
	constraint fk_item_troca_variacao
		foreign key (variacao_produto_id)
        references variacao_produto(id)
        on delete restrict
        on update cascade
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    
create table if not exists debito (
	id int auto_increment primary key,
    valor decimal(10,2) not null,
    status varchar(50) not null,
    saldo_pendente decimal(10,2) not null,
    venda_id int not null,
    cliente_id int not null,
    
    constraint fk_debito_venda
		foreign key (venda_id)
        references venda(id)
        on delete cascade
        on update cascade,
	constraint fk_debito_cliente
		foreign key (cliente_id)
        references cliente(id)
        on delete restrict
        on update cascade
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    
create table if not exists pagamento (
	id int auto_increment primary key,
    valor decimal(10,2) not null,
    data_hora datetime not null default current_timestamp,
    debito_id int not null,
    
    constraint fk_pagamento_debito
		foreign key (debito_id)
        references debito(id)
        on delete cascade
        on update cascade
	)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;