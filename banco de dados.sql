create database if not exists bot;

use bot;

create table if not exists usuarios (
	id int auto_increment primary key,
    nome varchar(100) not null,
    email varchar(100) unique,
    senha varchar(220) not null,
    criado_em timestamp default current_timestamp
);

create table if not exists logs (
	id int auto_increment primary key,
    usuario_id int,
    pergunta text not null,
    resposta text not null,
    criado_em timestamp default current_timestamp,
    foreign key(usuario_id) references usuarios(id) on delete cascade
);

create index idx_logs_usuarios_id on logs(usuario_id);
