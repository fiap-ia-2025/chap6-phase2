# FIAP - Faculdade de Informática e Administração Paulista

<img alt="Soja" src="./assets/logo-fiap.png" />   

## Sistema controlador de temperatura e irrigação com alerta por tempo sem chuva para produtores rurais

## Nome do Grupo: Grupo 61

## 👩 Integrantes:

- Ana Gabriela Soares Santos
- Nayana Mehta Miazaki
- Bianca Nascimento de Santa Cruz Oliveira
- Milena Pereira dos Santos Silva
- Amanda Vieira Pires

## 👨 Professores:

### Tutor: Lucas Gomes Moreira
### Coordenador: André Godoi

## 📜 Descrição

O sistema controlador de temperatura e irrigação tem dois objetivos. O primeiro, é dar informações sobre o clima (temperatura, temperatura mínima, temperatura máxima, sensação térmica e umidade) de sua cidade/estado ao produtor rural. O segundo, é alertar ao produtor se suas plantações necessitam de irrigação dependendo da quantidade de dias sem chuvas e do tipo de cultura plantada.

## 📁 Estrutura de pastas
Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- assets: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- document: aqui estão todos os arquivos utilizados pelo programa.

- scripts: aqui estão os scripts de banco de dados, DDL e DML.

- src: Todo o código fonte criado para o desenvolvimento do projeto.

- README.md: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

- .github: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

## 🔧 Como executar o código

1. Instale as seguentes dependências:

   1. pip install requests
   2. pip install meteostat
   3. pip install geopy
   4. pip install datetime
   5. pip install pandas
   6. pip install oracledb

2. Import o projeto em uma IDE de sua preferência (ex: PyCharm)
3. Abra o arquivo [database_connection.py](src/database_connection.py), e na linha 10, substitua as informações de banco de dados pelas suas.
4. Execute o arquivo main.py dentro de /src que contém a função main


## 📜 Referêncicias

1. Como irrigar uma plantacao de café: https://www.picturethisai.com/pt/care/water/Coffea_arabica.html
2. Como irrigar uma plantação de soja: https://agrosmart.com.br/blog/o-uso-da-agua-na-cultura-de-soja/
4. Como irrigar uma plantação de cana de cana de açucar: https://www.embrapa.br/agencia-de-informacao-tecnologica/cultivos/cana/producao/manejo/irrigacao#:~:text=A%20aplicação%20é%20feita%20em,e%20desenvolvimento%20(Figura%201).&text=irrigação%20para%20a%20cana%2Dde%2Daçúcar.

