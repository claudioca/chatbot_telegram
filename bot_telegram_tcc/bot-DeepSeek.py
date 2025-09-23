import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import requests
import json

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configurações (substitua com suas chaves)
DEEPSEEK_API_KEY = "sua_chave_deepseek_aqui"  # ← Substitua!
TELEGRAM_BOT_TOKEN = "seu_token_telegram_aqui"  # ← Substitua!

class DeepSeekChatBot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    async def gerar_resposta(self, mensagem):
        """Envia mensagem para API da DeepSeek e retorna resposta"""
        try:
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system", 
                        "content": "Você é um assistente útil e amigável. Responda de forma clara e concisa."
                    },
                    {
                        "role": "user",
                        "content": mensagem
                    }
                ],
                "stream": False,
                "temperature": 1.4
            }
            
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                return f"❌ Erro na API: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"❌ Erro: {str(e)}"

# Inicializar o bot da DeepSeek
deepseek_bot = DeepSeekChatBot(DEEPSEEK_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Função que lida com as mensagens recebidas"""
    user_message = update.message.text
    
    # Mostrar que está processando
    await update.message.chat.send_action(action="typing")
    
    # Obter resposta da DeepSeek
    resposta = await deepseek_bot.gerar_resposta(user_message)
    
    # Enviar resposta de volta
    await update.message.reply_text(resposta)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    welcome_text = """
    🤖 **Olá! Eu sou um bot inteligente!**
    
    Eu uso a API da DeepSeek para conversar com você.
    
    **Comandos disponíveis:**
    /start - Mostra esta mensagem
    /sobre - Informações sobre o bot
    
    **Como usar:**
    Apenas digite sua mensagem e eu responderei!
    """
    await update.message.reply_text(welcome_text)

async def sobre_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /sobre"""
    sobre_text = """
    ℹ️ **Sobre este bot:**
    
    Desenvolvido para estudos com:
    - Python
    - python-telegram-bot
    - DeepSeek API
    
    🔗 **GitHub:** [link para seu repositório]
    """
    await update.message.reply_text(sobre_text)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manipulador de erros"""
    logging.error(f"Erro: {context.error}")
    if update and update.message:
        await update.message.reply_text("❌ Ocorreu um erro. Tente novamente.")

def main():
    """Função principal"""
    # Criar aplicação do Telegram
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Adicionar handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.Regex(r'^/start'), start_command))
    application.add_handler(MessageHandler(filters.Regex(r'^/sobre'), sobre_command))
    
    # Adicionar handler de erros
    application.add_error_handler(error_handler)
    
    # Iniciar o bot
    print("🤖 Bot iniciado! Pressione Ctrl+C para parar.")
    application.run_polling()

if __name__ == '__main__':
    main()