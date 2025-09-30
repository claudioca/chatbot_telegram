package com.financebot;

import org.telegram.telegrambots.meta.TelegramBotsApi;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.updatesreceivers.DefaultBotSession;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Main {
    public static void main(String[] args) {
        System.out.println("🚀 Inicializando Bot de Finanças Pessoais...");
        System.out.println("=".repeat(60));
        
        // Inicializa o banco de dados
        try {
            Database.initDB();
            System.out.println("✅ Banco de dados inicializado com sucesso!");
        } catch (Exception e) {
            System.out.println("❌ Erro ao inicializar banco de dados: " + e.getMessage());
            return;
        }

        // Cria e registra o bot
        try {
            TelegramBotsApi botsApi = new TelegramBotsApi(DefaultBotSession.class);
            FinanceBot bot = new FinanceBot();
            botsApi.registerBot(bot);
            System.out.println("✅ Bot registrado com sucesso!");
        } catch (TelegramApiException e) {
            System.out.println("❌ Erro ao registrar bot: " + e.getMessage());
            return;
        }

        // Mensagem de inicialização
        System.out.println("=".repeat(60));
        System.out.println("🤖 BOT DE FINANÇAS INICIADO COM SUCESSO!");
        System.out.println("⏰ Horário: " + LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss")));
        System.out.println("📍 Bot está rodando e aguardando mensagens...");
        System.out.println("📍 Pressione Ctrl+C para parar o bot");
        System.out.println("=".repeat(60));
        System.out.println();
    }
}