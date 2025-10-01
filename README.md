💰 Bot de Finanças Pessoais - Java

https://img.shields.io/badge/Java-11%252B-blue
https://img.shields.io/badge/Telegram-Bot_API-green
https://img.shields.io/badge/Database-SQLite-lightgrey

Um bot do Telegram para controle financeiro pessoal desenvolvido em Java, permitindo registrar receitas, despesas e acompanhar seu saldo em tempo real.
✨ Funcionalidades

    💳 Adicionar Créditos: Registre entradas de dinheiro (salário, vendas, etc.)

    💸 Registrar Débitos: Controle suas despesas (aluguel, alimentação, etc.)

    📊 Saldo Atual: Consulte seu saldo em tempo real

    📋 Extrato Completo: Veja o histórico de todas as transações

    💾 Armazenamento Local: Dados salvos em banco SQLite

    ⌨️ Interface Intuitiva: Menu com teclado personalizado

🛠️ Tecnologias Utilizadas

    Java 11+ - Linguagem de programação

    Telegram Bot API - Integração com Telegram

    SQLite JDBC - Banco de dados embutido

    Maven - Gerenciamento de dependências

📋 Pré-requisitos

Antes de executar o bot, certifique-se de ter instalado:

    Java JDK 11 ou superior

    Maven 3.6+

    Conta no Telegram

    Token do Bot do Telegram (obtido com @BotFather)

🚀 Configuração e Execução
Passo 1: Obter Token do Bot no Telegram

    Abra o Telegram e busque por @BotFather

    Envie /newbot e siga as instruções:

        Digite um nome para o bot (ex: "Meu Bot Financeiro")

        Escolha um username único (ex: "meu_bot_financeiro")

    Anote o token fornecido pelo BotFather (algo como 123456789:ABCdefGHIjklMNOpqrsTUVwxyz)

Passo 2: Clonar/Configurar o Projeto
bash

# Criar diretório do projeto
mkdir finance-bot
cd finance-bot

# Criar estrutura de diretórios
mkdir -p src/main/java/com/financebot

Passo 3: Configurar os Arquivos do Projeto

1. Criar pom.xml (na raiz do projeto):
xml

<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.financebot</groupId>
    <artifactId>finance-bot</artifactId>
    <version>1.0.0</version>
    
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
    
    <dependencies>
        <!-- Telegram Bot API -->
        <dependency>
            <groupId>org.telegram</groupId>
            <artifactId>telegrambots</artifactId>
            <version>6.8.0</version>
        </dependency>
        
        <!-- SQLite JDBC Driver -->
        <dependency>
            <groupId>org.xerial</groupId>
            <artifactId>sqlite-jdbc</artifactId>
            <version>3.42.0.0</version>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>11</source>
                    <target>11</target>
                </configuration>
            </plugin>
            
            <!-- Plugin para executar o aplicativo -->
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>exec-maven-plugin</artifactId>
                <version>3.1.0</version>
                <configuration>
                    <mainClass>com.financebot.Main</mainClass>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>

2. Criar src/main/java/com/financebot/Config.java:
java

package com.financebot;

public class Config {
    // SUBSTITUA PELO SEU TOKEN REAL
    public static final String BOT_TOKEN = "SEU_TOKEN_AQUI";
    public static final String BOT_USERNAME = "SeuBotFinanceiro";
}

3. Criar os outros arquivos conforme fornecido anteriormente:

    Database.java

    FinanceBot.java

    Main.java

Passo 4: Configurar o Token

Edite o arquivo Config.java e substitua:
java

public static final String BOT_TOKEN = "SEU_TOKEN_AQUI";

Pelo token real que você obteve do BotFather.
Passo 5: Compilar e Executar
bash

# Compilar o projeto
mvn clean compile

# Executar o bot
mvn exec:java -Dexec.mainClass="com.financebot.Main"

Execução em Background (Produção)
bash

# Compilar JAR executável
mvn clean package

# Executar em background (Linux/Mac)
nohup java -cp target/finance-bot-1.0.0.jar:target/dependency/* com.financebot.Main > bot.log 2>&1 &

# Verificar se está rodando
tail -f bot.log

📱 Como Usar o Bot
Primeiros Passos:

    Iniciar o Bot: Envie /start para o bot no Telegram

    Configurar Nome: Digite como quer ser chamado

    Usar o Menu: Escolha entre as opções do teclado

Funcionalidades Disponíveis:
Comando	Descrição
➕ Saldo Inicial	Definir saldo inicial da conta
💳 Adicionar Crédito	Registrar entrada de dinheiro
💸 Adicionar Débito	Registrar despesa/saída de dinheiro
📊 Saldo Atual	Consultar saldo atual
📋 Extrato	Ver histórico de transações
Exemplo de Uso:
text

👤 Usuário: /start
🤖 Bot: "👋 Olá! Sou seu assistente financeiro pessoal. Como você gostaria de ser chamado?"

👤 Usuário: João
🤖 Bot: "🎉 Perfeito, João! Agora vamos gerenciar suas finanças..."

👤 Usuário: [Clica "➕ Saldo Inicial"]
🤖 Bot: "💰 Adicionar Saldo Inicial. Digite o valor:"

👤 Usuário: 1000
🤖 Bot: "✅ Saldo Inicial Registrado! Valor: R$ 1.000,00"

🗂️ Estrutura do Projeto
text

finance-bot/
├── pom.xml
├── finance.db (criado automaticamente)
└── src/
    └── main/
        └── java/
            └── com/
                └── financebot/
                    ├── Main.java          # Ponto de entrada
                    ├── Config.java        # Configurações do bot
                    ├── FinanceBot.java    # Lógica principal do bot
                    └── Database.java      # Operações com banco de dados

🗃️ Estrutura do Banco de Dados

O bot cria automaticamente duas tabelas:
Tabela users
Campo	Tipo	Descrição
user_id	INTEGER	ID único do usuário (chave primária)
nickname	TEXT	Apelido do usuário
Tabela transactions
Campo	Tipo	Descrição
id	INTEGER	ID auto-incrementável
user_id	INTEGER	ID do usuário
type	TEXT	'credit' ou 'debit'
amount	REAL	Valor da transação
description	TEXT	Descrição/origem
timestamp	DATETIME	Data/hora automática
🐛 Solução de Problemas
Erros Comuns:

Token inválido:
text

❌ Erro ao registrar bot: Invalid token

    Verifique se o token em Config.java está correto

    Confirme que não há espaços extras no token

Java não encontrado:
bash

java: command not found

    Instale o JDK 11+ e configure a variável de ambiente JAVA_HOME

Maven não encontrado:
bash

mvn: command not found  

    Instale o Maven e adicione ao PATH do sistema

Erro de dependências:
bash

[ERROR] Failed to resolve dependencies

    Execute: mvn clean dependency:resolve

Logs e Debug:

O bot gera logs no console com emojis para facilitar o monitoramento:

    ✅ Operações bem-sucedidas

    ❌ Erros e problemas

    🤖 Status do bot

    💾 Operações de banco de dados

🔧 Personalização
Adicionar Novas Funcionalidades:

    Novo Estado: Adicione constante em FinanceBot.java

    Novo Handler: Crie método privado para processar o estado

    Atualizar Roteamento: Adicione case no switch do onUpdateReceived

Modificar Mensagens:

Edite as strings nos métodos de envio de mensagem em FinanceBot.java:
java

private void handleStart(Long userId) {
    userStates.put(userId, GET_NAME);
    sendTextMessage(userId, "👋 SUA MENSAGEM PERSONALIZADA AQUI");
}

🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

    Fork o projeto

    Crie uma branch para sua feature (git checkout -b feature/nova-feature)

    Commit suas mudanças (git commit -m 'Adiciona nova feature')

    Push para a branch (git push origin feature/nova-feature)

    Abra um Pull Request


⭐️ Se este projeto foi útil, considere dar uma estrela no repositório!

Desenvolvido com ❤️ e ☕️