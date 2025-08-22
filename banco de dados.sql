create database bot;

use bot;

create table usuarios (
	id int auto_increment primary key,
    nome varchar(100) not null,
    email varchar(100) not null unique,
    senha varchar(255) not null,
    criado_em timestamp default current_timestamp
);

create table logs (
	id int auto_increment primary key,
    usuario_id int,
    pergunta text not null,
    resposta text not null,
    criado_em timestamp default current_timestamp,
	foreign key(usuario_id) references usuarios(id) on delete cascade
);