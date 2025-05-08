README DO CHESS BRAWL DE GABRIEL BRUNO OLIVEIRA FERNANDES
---------------------------------------------------------

REQUISITOS PARA ACESSAR O PROGRAMA:

* Windows 11
* Python Versão 3.13.3 
* MySQL Versão 8.0.42
* Configurações do Banco de Dados MySQL
* Instalação Python + Módulos

--------------------TUTORIAIS----------------------------

     [ TUTORIAL DE INSTALAÇÃO PYTHON ]
  .  Disponível em: https://www.python.org/downloads/

  -   Adicione-o às variáveis de ambiente

     1.   Clique em "Pesquisar" na barra de tarefas
          Digite Python 
          Aperte com o botão direito em cima do programa
          Clique em "Abrir local do arquivo"
          (Isto lhe levará ao diretório onde se localiza o atalho do Python, queremos o executável)
          Com o mouse em cima do atalho destacado, pressione o botão direito novamente.
          Clique em "Abrir local do arquivo"
          Copie o endereço do diretório, se encontra na parte superior da tela se parecerá com algo assim:
           C:\Users\Seu_Nome\AppData\Local\Programs\Python\Python313

     2.   Clique em "Pesquisar" na barra de tarefas
          Digite Variáveis e clique em "Editar as Variáveis de Ambiente do Sistema"
          Na tela que surgiu aperte o botão Variáveis de Ambiente.
          Na lista "Variáveis de Ambiente de Seu_Nome" selecione "PATH" e aperte em "EDITAR", mais abaixo.
          Selecione "NOVO" e cole ali o endereço que você copiou anteriormente.
          
     3.   Retorne à pasta do Python
          Entre na pasta scripts clicando duas vezes sobre ela
          Copie seu diretório, se parece com:
           C:\Users\Seu_Nome\AppData\Local\Programs\Python\Python313\Scripts
          Abra de novo as Variáveis de Ambiente no mesmo lugar que você estava editando o PATH
          Selecione "NOVO" e cole ali o endereço que você copiou anteriormente.
          Dê Ok em todas as janelas que permitirem esse comando.


       [ TUTORIAL DE INSTALAÇÃO RECURSOS PYTHON ]
  

     4.   Pressione Windows + R ou clique em "Pesquisar" na barra de tarefas
          digite Powershell e aperte "Enter", insira os comandos:

          pip install pygame
          pip install mysql-connector-python





     [ TUTORIAL DE INSTALAÇÃO MySQL ]
  .  Disponível em: https://dev.mysql.com/downloads/windows/
    
         Selecione a opção de 353.7M (ou a de número maior)
         
         IMPORTANTE - NÃO PERCA A SENHA DO ROOT DO MOMENTO DA INSTALAÇÃO
         Siga os passos neste vídeo: https://youtu.be/oi3UHWXLxLs?t=101
       
  -   Adicione-o às variáveis de ambiente

     1.   Clique em "Pesquisar" na barra de tarefas
          Digite MySQL 
          Aperte com o botão direito em cima do programa
          Clique em "Abrir local do arquivo"
          Selecione a pasta "MySQL Server 8.0"
          Clique com o botão direito em cima de "MySQL 8.0 Command Line Client" e abra o local do arquivo
          Copie o endereço do diretório, se encontra na parte superior da tela se parecerá com algo assim:
            C:\ProgramData\Microsoft\Windows\Start Menu\Programs\MySQL\MySQL Server 8.0\bin

     2.   Clique em "Pesquisar" na barra de tarefas
          Digite Variáveis e clique em "Editar as Variáveis de Ambiente do Sistema"
          Na tela que surgiu aperte o botão Variáveis de Ambiente.
          Na lista "Variáveis de Ambiente de Seu_Nome" selecione "PATH" e aperte em "EDITAR", mais abaixo.
          Selecione "NOVO" e cole ali o endereço que você copiou anteriormente.
          Dê Ok em todas as janelas que permitirem esse comando.



    
      [ TUTORIAL Configurações do Banco de Dados MySQL ]
  
     1.   Comandos no CMD

          Pressione Windows + R ou clique em "Pesquisar" na barra de tarefas
          digite CMD e aperte "Enter" 
          
          mysql -u root -p
          (insira a senha que você fez na instalação)

     2.  Criando banco de dados chess_brawl e usuário
         
          CREATE DATABASE `chess_brawl`;

          CREATE USER `chess.brawl`@`%` IDENTIFIED BY 'S@Nha123!@';

          GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, PROCESS, INDEX, ALTER, SUPER, TRIGGER ON *.* TO `chess.brawl`@`%`;
          (este comando acima serve para dar ao usuário chess.brawl todas permissões para evitar falhas de inserção.)

          USE DATABASE chess_brawl;

     3.  Criando tables (copie e cole estes dois grandes blocos)
         
CREATE TABLE partida_estatisticas (id INT NOT NULL AUTO_INCREMENT, jogador_1 VARCHAR(100) DEFAULT NULL, jogador_2 VARCHAR(100) DEFAULT NULL, vencedor VARCHAR(100) DEFAULT NULL, numero_de_movimentos INT DEFAULT NULL, duracao_segundos INT DEFAULT NULL, data_partida DATETIME DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE jogadores (nick VARCHAR(100) NOT NULL, nome VARCHAR(100) DEFAULT NULL, partidas INT DEFAULT 0, vitorias INT DEFAULT 0, derrotas INT DEFAULT 0, empates INT DEFAULT 0, pontuacao_total INT DEFAULT 0, ranking INT DEFAULT 0, PRIMARY KEY (nick)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


     4.   PARA CONSULTAR O BANCO DE DADOS (CMD) / Após uma partida ou torneio completo (sem ter limpado o banco de dados)
          feche o CMD, abra-o de novo

          mysql -u chess.brawl -p 
          S@Nha123!@
          use chess_brawl;
          SELECT * from jogadores;
          SELECT * from partida_estatisticas;
       




  -   Database: chess_brawl
  -   Usuário: chess.brawl 
  -   Host: %
  -   Senha: S@Nha123!@


