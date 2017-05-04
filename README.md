# RadarLivre

The RadarLivre system is a mixed software-hardware solution based in the ASD-B technology for monitoring the airspace. The main components are: 

* ADS-B receptor
* Software for interpreting the collected data
* Web server that receives the data and store them in a database
* Software for analising the collected information and detecting possible collision between the airplanes and geographical accidents
* Website that presents the data publicly.

## Getting Started

This paper will help you get a copy of the project(server-side) to run it in your local machine. If you are looking for the client-side for collecting the data of a ADS-B receptor, [this is the repository](https://github.com/FelipePinhoUFC/RadarLivreCollector). You need both to get the system running.

### Prerequisites

This project was designed to run in ubuntu.
You need to have these installed before installing the project.

```
* Python 2.7
* SQLite database
```

### Installing

Follow these steps to install, configure and run the server.

* Open the terminal and install Git (if you have already installed git and virtualenv, you may skip the first 2 steps)

```
sudo apt-get install git
```

* Install Virtualenv

```
sudo apt-get install python-virtualenv
```

* Clone this repository from github where you want to have your copy installed

```
git clone http://github.com/FelipePinhoUFC/RadarLivre.git
```

* With Virtualenv installed, use this command for creating a virtual python enviroment (with the name of venv, by default). For details, refer to [Virtualenv documentation](https://virtualenv.pypa.io/en/stable/).

```
virtualenv venv
```

* Activate the virtual enviroment. Make sure you are on the project directory. 

```
source venv/bin/activate
```

If you have done it right, you should notice a "(venv)" before your username. This indicates you have activated the virtual enviroment.

From now on, you need to follow the steps while the virtual enviroment is activated.

* Install the software dependencies listed in requirements.txt

```
pip install -r requirements.txt
```

* Now, to set up our database, use 

```
python manage.py makemigrations
```

* then

```
python manage.py migrate
```

* Now you can run your server

```
python manage.py runserver
```

Congratulations! Now that you have your running server, you can access it by going to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.

<!--
## Running the tests TODO

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```
-->

## Deployment

Once you have set up your server, you can aways access it by following these steps:

* Activate the virtual enviroment

```
source venv/bin/activate
```

* With the virtual enviroment activated, run the server

```
python manage.py runserver
```

* You can stop running the server by pressing CTRL+C.

* You can deactivate the virtual enviroment by using this command

```
deactivate
```

Access it by going to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.

## Built With

* [Python](https://www.python.org/)
* [Django](https://www.python.org/)
* [Markdown](https://daringfireball.net/projects/markdown/)
* [Pillow](https://python-pillow.org/)
* [SQLite](https://www.sqlite.org/)
* [Virtualenv](https://virtualenv.pypa.io/en/stable/)

## Versioning

We use [SemanticVersioning](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/FelipePinhoUFC/RadarLivre/tags).

## Changelog

You can refer to [CHANGELOG.md](https://github.com/FelipePinhoUFC/RadarLivre/blob/master/CHANGELOG.md) for details about the development and differences between versions.

<!-- Won't be displayed

<div style="text-align:center">
  <img src="https://raw.githubusercontent.com/FelipePinhoUFC/RadarLivre/master/radarlivre_website/static/website/img/icon.ico" width="256">
</div>

# O Sistema Radar Livre

O sistema de monitoramento aéreo Radar Livre é uma solução mista de hadware e software baseada na tecnologia ADS-B. Seus principais componentes são: um aparelho receptor de mensagens ADS-B, um software capaz de interpretar os dados coletados, um servidor web que recebe os dados e armazena em um banco de dados, um software capaz de analisar as informações coletadas e detectar possíveis conflitos entre trajetórias de aeronaves e entre aeronaves e acidentes geográficos, além de um site que disponibiliza os dados publicamente.

# Coleta de mensagens ADS-B

O aparelho coletor de mensagens ADS-B é um componente simples, que pode ser instalado e configurado facilmente. É composto por uma antena pequena e um receptor que pode ser conectado a uma porta USB de qualquer computador. Para o tratamento das mensagens recebidas é necessário um software específico. As aplicações disponíveis atualmente para o reconhecimento das mensagens ADS-B são em sua maioria privadas e para o sistema operacional Windows, o que gera uma dependência da plataforma e um alto custo de instalação. O sistema Radar livre conta com seu próprio software de coleta, uma aplicação de código fonte aberto implementada sobre a plataforma linux pela equipe do projeto na UFC. A aplicação interpreta as mensagens e extrai informações como identificação, posicionamento, velocidade e altitude, armazenando-os em um banco de dados local. Posteriormente, os dados são enviados a um servidor web.

# Servidor web e site

Após serem coletados, os dados são enviados a um servidor web, que armazena-os em um banco de dados que pode ser acessado para análise das informações obtidas das aeronaves. Esses dados serão disponibilisados em um site de acesso livre e gratuito, onde aeronaves serão representadas graficamente, mostrando sua posição e outras informações. Essa interface web também foi implementada pela equipe do projeto na UFC em Quixadá e resultou num Trabalho de Conclusão de Curso (TCC).

# Componentes em produção

Encontram-se em desenvolvimento a versão do software coletor para Android e o Software de Análise de Colisão. O software coletor para Android permitirá o uso de plataformas mais leves e baratas para a implantação das estações coletoras e está sendo desenvolvido também na forma de um Trabalho de Conclusão de Curso. Já o Software de Análise de Colisão está sendo implementado pelo autor deste artigo como projeto de Iniciação Científica.

# Software de Análise de Colisão

Uma das principais falhas do sistema de monitoramento aéreo atual é o atraso na atualização do posicionamento das aeronaves que gera um grande intervalo entre a identificação da possível colisão e o alerta aos pilotos das aeronaves envolvidas. Além disso, o sistema não prevê possíveis colisões contra acidentes geográficos. A Tecnologia ADS-B diminui substancialmente o tempo de atualização do posicionamento dos aviões, tornando o sistema bem mais seguro e confiável.

Com o objetivo de otimizar a prevensão contra colisões, o sistema Radar Livre disponibilizará um software que utiliza os dados coletados em tempo real para análise e verificação de possíveis conflitos entre rotas de aeronaves e entre rotas de aeronaves e acidentes geográficos. A aplicação, que está em fase de desenvolvimento, funcionará na plataforma linux e terá código fonte aberto. Portanto, poderá ser utilizada livremente, especialmente por torres de controle para auxiliar no monitoramento aéreo.

# Conclusão

O projeto Radar Livre, com seus componentes simples e acessíveis, permitirá que o sistema de monitoramento aéreo brasileiro acompanhe as melhorias que estão acontecendo nos sistemas norte americanos com a adoção do método de monitoramento ADS-B. Apesar de ainda estar em fase de desenvolvimento, o sistema já disponibiliza as funcionalidades de coleta, armazenamento e apresentação em funciomaneto, e prevê uma versão do Software Coletor para a plataforma Android e um Software de Análise de Colisão. O site está disponível em <a href="http://www.radarlivre.com">www.radarlivre.com</a>. Os softwares já produzidos estão neste repositório e podem ser baixados e configurados facilmente em qualquer máquina com plataforma linux. Para a instalação, consulte nosso manual em <a href="https://docs.google.com/document/d/1ipKDKALwp97XyFSJrwYT17DriH22y-IMSrwTwS7odJA/edit?usp=sharing">Manual de Instalação</a>.

-->