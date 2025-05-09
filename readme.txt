Use o comando abaixo para rodar a aplicação(tenha certeza de estar no diretório "Webscraping", não pode ser dentro da pasta app):

uvicorn app.main:app --reload


Use o comando abaixo para instalar todos os pacotes necessários (tenha certeza de estar no diretório "Webscraping")

python -m pip install -r requirements.txt





controllers/: Recebem requisições HTTP e delegam chamadas para os services.

database/: Contém a configuração da conexão com o banco de dados.

models/: Define as entidades mapeadas no banco (ORM), ou seja, são as tabelas.

repositories/: Realizam acesso direto ao banco (CRUD, queries), é quem o service vai chamar depois de ter feito as validações.

routes/: Agrupam e registram as rotas da aplicação.

schemas/: Definem os modelos de entrada/saída (Pydantic) para validação de dados. Ex: Para criar uma categoria você precisa receber "a" e "b", então é preciso criar um schema para essa requisição.

services/: Contêm as regras de negócio e lógica da aplicação. Toda validação é feita aqui, se o nome já existe, se a descrição ultrapassa ou não a quantidade de caracteres, tudo é feito ali, nada pode ser feito fora.

main.py: Ponto de entrada da aplicação FastAPI, onde a API é instanciada.




Caminho -> routes -> controller - (usando schema) -> service -> repository -> database -> 