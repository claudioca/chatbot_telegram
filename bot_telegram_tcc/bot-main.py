from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes
from telegram.ext import filters

# Token fornecido pelo BotFather
TOKEN = "TOKEN"

# Função para responder ao comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Ativa a conversa ao receber /start
    context.user_data['active'] = True
    await update.message.reply_text('Olá! Eu sou um bot. Como posso ajudar?')

# Função para responder ao comando /stop
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Desativa a conversa ao receber /stop
    context.user_data['active'] = False
    await update.message.reply_text('Até logo! Foi um prazer ajudar. Use /start para iniciar novamente.')

# Função para verificar se a conversa está ativa
def is_conversation_active(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:

    # Verifica se a conversa está ativa para este usuário
    # Usamos user_data específico para cada usuário
    return context.user_data.get('active', True)  # Por padrão, a conversa está ativa


# Função para responder a mensagens de texto
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Verifica se a conversa está ativa antes de responder
    if not is_conversation_active(context, update.effective_user.id):
        # Se a conversa não está ativa, não responde
        return
    
    # Repete a mensagem do usuário apenas se a conversa estiver ativa
    await update.message.reply_text(update.message.text)


def main():
    # Cria o Updater e passa o token do bot.
    application = Application.builder().token(TOKEN).build()

    # Registra handlers para comandos e mensagens
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Adiciona filtro personalizado para verificar se a conversa está ativa
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE, 
        echo
    ))

    # Inicia o bot
    print("Bot iniciado...")
    application.run_polling()

if __name__ == '__main__':
    main()


   
