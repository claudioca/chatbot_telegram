package com.financebot;

import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Message;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.ReplyKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.KeyboardRow;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

import java.text.NumberFormat;
import java.text.ParseException;
import java.util.*;

public class FinanceBot extends TelegramLongPollingBot {
    
    // Estados da conversa
    private static final int GET_NAME = 0;
    private static final int MAIN_MENU = 1;
    private static final int GET_INITIAL = 2;
    private static final int GET_CREDIT = 3;
    private static final int GET_CREDIT_DESC = 4;
    private static final int GET_DEBIT = 5;
    private static final int GET_DEBIT_DESC = 6;
    
    // Mapa para guardar o estado de cada usuário
    private Map<Long, Integer> userStates = new HashMap<>();
    // Mapa para dados temporários
    private Map<Long, Double> tempAmounts = new HashMap<>();
    
    @Override
    public String getBotUsername() {
        return Config.BOT_USERNAME;
    }
    
    @Override
    public String getBotToken() {
        return Config.BOT_TOKEN;
    }
    
    @Override
    public void onUpdateReceived(Update update) {
        if (update.hasMessage() && update.getMessage().hasText()) {
            Message message = update.getMessage();
            String text = message.getText();
            Long userId = message.getFrom().getId();
            int currentState = userStates.getOrDefault(userId, GET_NAME);
            
            switch (currentState) {
                case GET_NAME:
                    handleGetName(userId, text);
                    break;
                case MAIN_MENU:
                    handleMainMenu(userId, text);
                    break;
                case GET_INITIAL:
                    handleGetInitial(userId, text);
                    break;
                case GET_CREDIT:
                    handleGetCredit(userId, text);
                    break;
                case GET_CREDIT_DESC:
                    handleGetCreditDesc(userId, text);
                    break;
                case GET_DEBIT:
                    handleGetDebit(userId, text);
                    break;
                case GET_DEBIT_DESC:
                    handleGetDebitDesc(userId, text);
                    break;
            }
        }
    }
    
    private void handleGetName(Long userId, String text) {
        if (text.trim().isEmpty()) {
            sendTextMessage(userId, "❌ Por favor, digite um nome válido.");
            return;
        }
        
        Database.addUser(userId, text.trim());
        userStates.put(userId, MAIN_MENU);
        
        sendMainMenu(userId, "🎉 Perfeito, " + text.trim() + "! Agora vamos gerenciar suas finanças.\n\n" +
                "Use o menu abaixo para controlar seus gastos e ganhos:");
    }
    
    private void handleMainMenu(Long userId, String text) {
        switch (text) {
            case "➕ Saldo Inicial":
                userStates.put(userId, GET_INITIAL);
                sendTextMessage(userId, "💰 **Adicionar Saldo Inicial**\n\n" +
                        "Digite o valor do seu saldo inicial:\n" +
                        "Ex: 1000 ou 1500,50");
                break;
                
            case "💳 Adicionar Crédito":
                userStates.put(userId, GET_CREDIT);
                sendTextMessage(userId, "💳 **Adicionar Crédito**\n\n" +
                        "Digite o valor do crédito:\n" +
                        "Ex: 500 ou 750,25");
                break;
                
            case "💸 Adicionar Débito":
                userStates.put(userId, GET_DEBIT);
                sendTextMessage(userId, "💸 **Adicionar Débito**\n\n" +
                        "Digite o valor do débito:\n" +
                        "Ex: 150 ou 89,90");
                break;
                
            case "📊 Saldo Atual":
                showBalance(userId);
                break;
                
            case "📋 Extrato":
                showStatement(userId);
                break;
                
            default:
                sendTextMessage(userId, "❌ Opção inválida. Use o menu.");
                break;
        }
    }
    
    private void handleGetInitial(Long userId, String text) {
        try {
            double amount = parseAmount(text);
            if (amount <= 0) {
                sendTextMessage(userId, "❌ O valor deve ser maior que zero. Tente novamente:");
                return;
            }
            
            Database.addTransaction(userId, "credit", amount, "Saldo inicial");
            userStates.put(userId, MAIN_MENU);
            
            sendMainMenu(userId, "✅ **Saldo Inicial Registrado!**\n\n" +
                    "💰 Valor: R$ " + formatCurrency(amount) + "\n\n" +
                    "Agora você pode adicionar créditos e débitos usando o menu abaixo:");
                    
        } catch (ParseException e) {
            sendTextMessage(userId, "❌ **Valor inválido!**\n\n" +
                    "Por favor, digite um valor numérico válido:\n" +
                    "Ex: 1000 ou 1500,50");
        }
    }
    
    private void handleGetCredit(Long userId, String text) {
        try {
            double amount = parseAmount(text);
            if (amount <= 0) {
                sendTextMessage(userId, "❌ O valor deve ser maior que zero. Tente novamente:");
                return;
            }
            
            tempAmounts.put(userId, amount);
            userStates.put(userId, GET_CREDIT_DESC);
            
            sendTextMessage(userId, "📝 **Origem do Crédito**\n\n" +
                    "Digite a origem deste valor:\n" +
                    "Ex: Salário, Freelance, Vendas, etc.");
                    
        } catch (ParseException e) {
            sendTextMessage(userId, "❌ **Valor inválido!**\n\n" +
                    "Por favor, digite um valor numérico válido:\n" +
                    "Ex: 500 ou 750,25");
        }
    }
    
    private void handleGetCreditDesc(Long userId, String text) {
        if (text.trim().isEmpty()) {
            sendTextMessage(userId, "❌ Por favor, digite uma descrição válida:");
            return;
        }
        
        Double amount = tempAmounts.remove(userId);
        if (amount != null) {
            Database.addTransaction(userId, "credit", amount, text.trim());
            userStates.put(userId, MAIN_MENU);
            
            sendMainMenu(userId, "✅ **Crédito Adicionado!**\n\n" +
                    "💰 Valor: R$ " + formatCurrency(amount) + "\n" +
                    "📝 Origem: " + text.trim() + "\n\n" +
                    "Seu saldo foi atualizado com sucesso!");
        } else {
            sendMainMenu(userId, "❌ Ocorreu um erro. Por favor, comece novamente.");
        }
    }
    
    private void handleGetDebit(Long userId, String text) {
        try {
            double amount = parseAmount(text);
            if (amount <= 0) {
                sendTextMessage(userId, "❌ O valor deve ser maior que zero. Tente novamente:");
                return;
            }
            
            tempAmounts.put(userId, amount);
            userStates.put(userId, GET_DEBIT_DESC);
            
            sendTextMessage(userId, "📝 **Descrição do Débito**\n\n" +
                    "Digite a descrição desta despesa:\n" +
                    "Ex: Aluguel, Supermercado, Transporte, etc.");
                    
        } catch (ParseException e) {
            sendTextMessage(userId, "❌ **Valor inválido!**\n\n" +
                    "Por favor, digite um valor numérico válido:\n" +
                    "Ex: 150 ou 89,90");
        }
    }
    
    private void handleGetDebitDesc(Long userId, String text) {
        if (text.trim().isEmpty()) {
            sendTextMessage(userId, "❌ Por favor, digite uma descrição válida:");
            return;
        }
        
        Double amount = tempAmounts.remove(userId);
        if (amount != null) {
            Database.addTransaction(userId, "debit", amount, text.trim());
            userStates.put(userId, MAIN_MENU);
            
            sendMainMenu(userId, "✅ **Débito Registrado!**\n\n" +
                    "💸 Valor: R$ " + formatCurrency(amount) + "\n" +
                    "📝 Descrição: " + text.trim() + "\n\n" +
                    "Sua despesa foi registrada com sucesso!");
        } else {
            sendMainMenu(userId, "❌ Ocorreu um erro. Por favor, comece novamente.");
        }
    }
    
    private void showBalance(Long userId) {
        Double balance = Database.getBalance(userId);
        String nickname = Database.getUserNickname(userId);
        
        sendMainMenu(userId, "💰 **Saldo Atual**\n\n" +
                "👤 " + nickname + "\n" +
                "💎 Saldo: R$ " + formatCurrency(balance) + "\n\n" +
                "*Use as opções abaixo para movimentar sua conta*");
    }
    
    private void showStatement(Long userId) {
        List<Transaction> transactions = Database.getStatement(userId, 10);
        String nickname = Database.getUserNickname(userId);
        Double balance = Database.getBalance(userId);
        
        if (transactions.isEmpty()) {
            sendMainMenu(userId, "📭 **Extrato**\n\n" +
                    "Nenhuma transação registrada ainda.\n\n" +
                    "Use as opções abaixo para fazer sua primeira movimentação!");
        } else {
            StringBuilder response = new StringBuilder();
            response.append("📋 **Extrato - ").append(nickname).append("**\n\n");
            
            for (Transaction t : transactions) {
                String emoji = t.getType().equals("credit") ? "⬆️💰" : "⬇️💸";
                String tipo = t.getType().equals("credit") ? "CRÉDITO" : "DÉBITO";
                String valor = "R$ " + formatCurrency(t.getAmount());
                String data = t.getTimestamp().substring(0, 16); // Formata a data
                
                response.append(emoji).append(" **").append(tipo).append("**\n");
                response.append("   Valor: ").append(valor).append("\n");
                response.append("   Descrição: ").append(t.getDescription()).append("\n");
                response.append("   Data: ").append(data).append("\n\n");
            }
            
            response.append("💎 **Saldo Total: R$ ").append(formatCurrency(balance)).append("**");
            sendMainMenu(userId, response.toString());
        }
    }
    
    private double parseAmount(String text) throws ParseException {
        // Substitui vírgula por ponto para parse
        String normalized = text.replace(',', '.');
        NumberFormat format = NumberFormat.getInstance(Locale.US);
        return format.parse(normalized).doubleValue();
    }
    
    private String formatCurrency(double value) {
        NumberFormat format = NumberFormat.getCurrencyInstance(new Locale("pt", "BR"));
        return format.format(value);
    }
    
    private void sendMainMenu(Long userId, String text) {
        SendMessage message = new SendMessage();
        message.setChatId(userId.toString());
        message.setText(text);
        message.setReplyMarkup(createMainKeyboard());
        try {
            execute(message);
        } catch (TelegramApiException e) {
            System.out.println("❌ Erro ao enviar mensagem: " + e.getMessage());
        }
    }
    
    private void sendTextMessage(Long userId, String text) {
        SendMessage message = new SendMessage();
        message.setChatId(userId.toString());
        message.setText(text);
        try {
            execute(message);
        } catch (TelegramApiException e) {
            System.out.println("❌ Erro ao enviar mensagem: " + e.getMessage());
        }
    }
    
    private ReplyKeyboardMarkup createMainKeyboard() {
        ReplyKeyboardMarkup keyboardMarkup = new ReplyKeyboardMarkup();
        List<KeyboardRow> keyboard = new ArrayList<>();
        
        KeyboardRow row1 = new KeyboardRow();
        row1.add("➕ Saldo Inicial");
        row1.add("💳 Adicionar Crédito");
        keyboard.add(row1);
        
        KeyboardRow row2 = new KeyboardRow();
        row2.add("💸 Adicionar Débito");
        row2.add("📊 Saldo Atual");
        keyboard.add(row2);
        
        KeyboardRow row3 = new KeyboardRow();
        row3.add("📋 Extrato");
        keyboard.add(row3);
        
        keyboardMarkup.setKeyboard(keyboard);
        keyboardMarkup.setResizeKeyboard(true);
        keyboardMarkup.setOneTimeKeyboard(false);
        
        return keyboardMarkup;
    }
}