-- DDL

create table fazenda(
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    estado VARCHAR2(5) NOT NULL,
    cidade VARCHAR2(200) NOT NULL,
    dt_inclusao timestamp with local time zone default sysdate
);

create table tipo_plantacao (
    id NUMBER PRIMARY KEY,
    nome VARCHAR2(50) NOT NULL
);

create table plantacao(
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_tipo_plantacao NUMBER NOT NULL,
    id_fazenda NUMBER NOT NULL,
    dt_inclusao timestamp with local time zone default sysdate,
    constraint id_fazenda_fk FOREIGN KEY (id_fazenda) REFERENCES fazenda(id),
    constraint id_tipo_plantacao_fk FOREIGN KEY (id_tipo_plantacao) REFERENCES tipo_plantacao(id)
);

drop table plantacao;
drop table tipo_plantacao;
drop table fazenda;

-- DML

INSERT INTO tipo_plantacao(id, nome) values (1, 'Soja');
INSERT INTO tipo_plantacao(id, nome) values (2, 'Cana de açucar');
INSERT INTO tipo_plantacao(id, nome) values (3, 'Café');

select * from tipo_plantacao;
select * from fazenda order by id desc;

select * from fazenda order by id desc fetch first 1 rows only;

INSERT INTO plantacao (id_tipo_plantacao, id_fazenda) VALUES (1, 14);