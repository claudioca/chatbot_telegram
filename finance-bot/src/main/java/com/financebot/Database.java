package com.financebot;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class Database {
    private static final String DB_URL = "jdbc:sqlite:finance.db";
    
    public static void initDB() {
        try (Connection conn = DriverManager.getConnection(DB_URL);
             Statement stmt = conn.createStatement()) {
            
            // Tabela de usuários
            String sqlUsers = "CREATE TABLE IF NOT EXISTS users " +
                    "(user_id INTEGER PRIMARY KEY, nickname TEXT)";
            stmt.execute(sqlUsers);
            
            // Tabela de transações
            String sqlTransactions = "CREATE TABLE IF NOT EXISTS transactions " +
                    "(id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                    "user_id INTEGER, " +
                    "type TEXT, " +
                    "amount REAL, " +
                    "description TEXT, " +
                    "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)";
            stmt.execute(sqlTransactions);
            
            System.out.println("✅ Banco de dados SQLite inicializado!");
        } catch (SQLException e) {
            System.out.println("❌ Erro ao inicializar banco de dados: " + e.getMessage());
        }
    }
    
    public static void addUser(Long userId, String nickname) {
        String sql = "INSERT OR REPLACE INTO users(user_id, nickname) VALUES(?,?)";
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setLong(1, userId);
            pstmt.setString(2, nickname);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println("❌ Erro ao adicionar usuário: " + e.getMessage());
        }
    }
    
    public static void addTransaction(Long userId, String type, Double amount, String description) {
        String sql = "INSERT INTO transactions(user_id, type, amount, description) VALUES(?,?,?,?)";
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setLong(1, userId);
            pstmt.setString(2, type);
            pstmt.setDouble(3, amount);
            pstmt.setString(4, description);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println("❌ Erro ao adicionar transação: " + e.getMessage());
        }
    }
    
    public static Double getBalance(Long userId) {
        String sql = "SELECT SUM(CASE WHEN type='credit' THEN amount ELSE -amount END) FROM transactions WHERE user_id=?";
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setLong(1, userId);
            ResultSet rs = pstmt.executeQuery();
            if (rs.next()) {
                return rs.getDouble(1);
            }
        } catch (SQLException e) {
            System.out.println("❌ Erro ao obter saldo: " + e.getMessage());
        }
        return 0.0;
    }
    
    public static List<Transaction> getStatement(Long userId, int limit) {
        List<Transaction> transactions = new ArrayList<>();
        String sql = "SELECT type, amount, description, timestamp FROM transactions WHERE user_id=? ORDER BY timestamp DESC LIMIT ?";
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setLong(1, userId);
            pstmt.setInt(2, limit);
            ResultSet rs = pstmt.executeQuery();
            
            while (rs.next()) {
                transactions.add(new Transaction(
                    rs.getString("type"),
                    rs.getDouble("amount"),
                    rs.getString("description"),
                    rs.getString("timestamp")
                ));
            }
        } catch (SQLException e) {
            System.out.println("❌ Erro ao obter extrato: " + e.getMessage());
        }
        return transactions;
    }
    
    public static String getUserNickname(Long userId) {
        String sql = "SELECT nickname FROM users WHERE user_id=?";
        try (Connection conn = DriverManager.getConnection(DB_URL);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setLong(1, userId);
            ResultSet rs = pstmt.executeQuery();
            if (rs.next()) {
                return rs.getString("nickname");
            }
        } catch (SQLException e) {
            System.out.println("❌ Erro ao obter apelido: " + e.getMessage());
        }
        return "Usuário";
    }
}

class Transaction {
    private String type;
    private Double amount;
    private String description;
    private String timestamp;
    
    public Transaction(String type, Double amount, String description, String timestamp) {
        this.type = type;
        this.amount = amount;
        this.description = description;
        this.timestamp = timestamp;
    }
    
    // Getters
    public String getType() { return type; }
    public Double getAmount() { return amount; }
    public String getDescription() { return description; }
    public String getTimestamp() { return timestamp; }
}