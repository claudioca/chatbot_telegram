from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
import config
import database as db
import handlers as h
import datetime
import logging

# Configuração básica de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    """Função principal - versão síncrona e estável"""
    print("🚀 Inicializando Bot de Finanças Pessoais...")
    print("=" * 60)
    
    # Inicializa o banco de dados
    try:
        db.init_db()
        print("✅ Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        return

    # Cria a aplicação do bot
    try:
        application = Application.builder().token(config.BOT_TOKEN).build()
        print("✅ Aplicação do bot criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar aplicação: {e}")
        return

    # Configura o ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', h.start)],
        states={
            h.GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, h.get_name)],
            h.MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, h.main_menu)],
            h.GET_INITIAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, h.handle_initial)],
            h.GET_CREDIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, h.handle_credit)],
            h.GET_CREDIT_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, h.handle_credit_description)],
            h.GET_DEBIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, h.handle_debit)],
            h.GET_DEBIT_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, h.handle_debit_description)],
        },
        fallbacks=[CommandHandler('cancel', h.cancel)],
    )

    application.add_handler(conv_handler)

    # Mensagem de inicialização no console
    print("=" * 60)
    print("🤖 BOT DE FINANÇAS INICIADO COM SUCESSO!")
    print(f"⏰ Horário: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("📍 Bot está rodando e aguardando mensagens...")
    print("📍 Pressione Ctrl+C para parar o bot")
    print("=" * 60)
    print()

    # Inicia o bot
    try:
        application.run_polling(
            drop_pending_updates=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Bot interrompido pelo usuário (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ Erro durante a execução: {e}")
    finally:
        print("✅ Bot finalizado com sucesso!")

if __name__ == '__main__':
    main()