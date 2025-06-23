# 💰 BR-MED – Sistema de Cotações de Moedas

Um sistema web simples para consultar e visualizar cotações do dólar em relação ao real, euro e iene, utilizando Django no backend, Highcharts no frontend e Docker para ambiente de produção.

<p align="center">
  <a href="#-tecnologias">Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-projeto">Projeto</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-funcionalidades">Funcionalidades</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-como-executar">Como executar</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
</p>

<br>

<a id="-tecnologias"></a>

## ✨ Tecnologias

Esse projeto foi desenvolvido com as seguintes tecnologias:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

---

<a id="-projeto"></a>

## 💻 Projeto

Este projeto foi desenvolvido como parte de um desafio técnico proposto pela empresa BR MED.

### 🧩 Enunciado do desafio

> Preciso de um sistema que guarde as cotações do dólar versus real, euro e iene (JPY) e que as exiba em um gráfico, respeitando as seguintes especificações:
>
> - Deve ser possível informar uma data de início e de fim para consultar qualquer período de tempo, contanto que o período informado seja de no máximo 5 dias úteis.
> - Deve ser possível variar as moedas (real, euro e iene).
>
> Restrições:
>
> - Os dados das cotações devem ser coletados utilizando a API do https://www.vatcomply.com/documentation (utilize o dólar como base).
> - O código deve ser desenvolvido utilizando um repositório git público (GitHub ou BitBucket).
>
> Tecnologias:
>
> - Backend: Python + Django.
> - Frontend: Highcharts para exibição dos dados.
>
> Não é necessário autenticação ou login. Apenas uma página com o gráfico é suficiente.
>
> **O que será avaliado:**
> - Clareza do código.
> - Uso de orientação a objetos.
> - Boas práticas como testes e controle de versão.
> - Conhecimento da stack utilizada.
>
> **Bônus:**
> - Deploy funcional.
> - API para leitura dos dados persistidos.

### ✅ Solução implementada

- Interface amigável para seleção de data e moeda.
- Validação de intervalo de datas (máximo 5 dias úteis).
- Visualização clara das cotações via Highcharts.
- Backend estruturado com Django, persistindo as cotações em PostgreSQL.
- API REST para leitura das cotações armazenadas.
- Deploy via Docker e Docker Compose.

---

<a id="-funcionalidades"></a>

## ✅ Funcionalidades

- [x] Consulta de cotações por data e moeda.
- [x] Visualização gráfica interativa com Highcharts.
- [x] Persistência dos dados em banco PostgreSQL.
- [x] API de leitura de cotações.
- [x] Deploy com Docker.

---

<a id="-como-executar"></a>

## 🚀 Como executar

### 💻 Pré-requisitos

Antes de começar, verifique se você possui instalado:

- Python 3.11+
- Git
- Docker (opcional para execução com contêiner)
- Editor de código ou IDE

---

### 🛠️ Instalação local (sem Docker)

Clone o repositório:

```bash
git clone https://github.com/Ricardo-Jackson-Ferrari/BR-MED.git
cd BR-MED
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate   # Unix/macOS
.venv\Scripts\activate.bat  # Windows
```

Instale as dependências:

```bash
pip install -r requirements.dev.txt
```

Crie o arquivo `.env` com base no exemplo:

```bash
cp env_example .env
```

Caso não utilize PostgreSQL localmente, altere no `.env`:

```env
DATABASE_URL=sqlite:///db.sqlite3
```

Aplique as migrações e inicie o servidor:

```bash
python manage.py migrate
python manage.py runserver
```

Acesse: [http://localhost:8000](http://localhost:8000)

---

### 🐳 Execução com Docker (produção simplificada)

Suba a aplicação com:

```bash
docker-compose up -V -d
```

Acesse: [http://localhost:8000](http://localhost:8000)

Para derrubar os contêineres:

```bash
docker-compose down
```

---

### 🌐 Deploy online (opcional)

Caso o projeto esteja publicado, você pode testá-lo aqui:

[https://br-med.onrender.com](https://br-med.onrender.com)

---


Desenvolvido por Ricardo Jackson Ferrari