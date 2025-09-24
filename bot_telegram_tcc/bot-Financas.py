import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, 
    ContextTypes, ConversationHandler
)

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Estados da conversa
NAME, SALARY, CONTINUE, OPTIONS = range(4)

# Token do bot (substitua pelo seu token)
TELEGRAM_BOT_TOKEN = "8292391534:AAH-4gIJm5czycQuSQtqltqSifBAx5oR_SY"

class FinanceBot:
    def __init__(self):
        self.user_data = {}

    # Função para verificar se a conversa está ativa (mesma lógica do código fornecido)
    def is_conversation_active(self, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
        """Verifica se a conversa está ativa para este usuário"""
        return context.user_data.get('active', True)  # Por padrão, a conversa está ativa

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Inicia a conversa e pergunta o nome"""
        # Ativa a conversa ao receber /start (mesma lógica do código fornecido)
        context.user_data['active'] = True
        
        await update.message.reply_text(
            "Olá! Sou o Edu, seu assistente de educação financeira.\n"
            "Qual o seu nome?"
        )
        return NAME

    # Função para responder ao comando /stop (mesma lógica do código fornecido)
    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Comando /stop - para a conversa"""
        # Desativa a conversa ao receber /stop
        context.user_data['active'] = False
        await update.message.reply_text(
            'Até logo! Foi um prazer ajudar. Use /start para iniciar novamente.',
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    async def get_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Armazena o nome e pergunta o salário"""
        # Verifica se a conversa está ativa antes de responder
        if not self.is_conversation_active(context, update.effective_user.id):
            return ConversationHandler.END
            
        user_name = update.message.text
        context.user_data['name'] = user_name
        
        await update.message.reply_text(
            f"Prazer, {user_name}! Estou aqui para te ajudar a definir a sugestão de orçamento mensal.\n"
            "Sendo assim preciso saber, qual o valor do seu salário líquido em reais? "
            "Adicione apenas o valor, assim como o exemplo: 1000,00"
        )
        return SALARY

    async def get_salary(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Processa o salário e mostra as estimativas"""
        # Verifica se a conversa está ativa antes de responder
        if not self.is_conversation_active(context, update.effective_user.id):
            return ConversationHandler.END
            
        try:
            salary_text = update.message.text.replace(',', '.').replace('R$', '').strip()
            salary = float(salary_text)
            
            if salary <= 0:
                await update.message.reply_text("Por favor, digite um valor válido maior que zero. Exemplo: 1000,00")
                return SALARY
            
            context.user_data['salary'] = salary
            
            # Calculos
            total_gastar = salary * 0.65
            total_economizar = salary * 0.25
            habitacao = salary * 0.28
            transporte = salary * 0.10
            substancia = salary * 0.25
            lazer = salary * 0.12
            
            response = (
                f"De modo geral, o total previsto para você gastar é de R${total_gastar:.2f}. "
                f"Assim você terá um total de R${total_economizar:.2f} para economizar ou investir ou mesmo quitar dívidas.\n\n"
                f"Certo! Fiz a estimativa inicial e essa é a minha sugestão de divisão dos seus gastos mensais:\n\n"
                f"🏠 Habitação: R${habitacao:.2f}\n"
                f"🚗 Transporte: R${transporte:.2f}\n"
                f"🛒 Substância: R${substancia:.2f}\n"
                f"🎉 Lazer: R${lazer:.2f}\n\n"
                f"E agora?\n\n"
                f"1 - Gostaria de ajuda para analisar se os seus gastos estão de acordo com o previsto?\n"
                f"2 - Ou gostaria de finalizar este atendimento?"
            )
            
            # Teclado com opções (botões menores)
            keyboard = [['1'], ['2']]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            
            await update.message.reply_text(response, reply_markup=reply_markup)
            return OPTIONS
            
        except ValueError:
            await update.message.reply_text("Por favor, digite um valor numérico válido. Exemplo: 1000,00")
            return SALARY

    async def handle_options(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Processa a opção escolhida pelo usuário"""
        # Verifica se a conversa está ativa antes de responder
        if not self.is_conversation_active(context, update.effective_user.id):
            return ConversationHandler.END
            
        choice = update.message.text
        user_name = context.user_data.get('name', 'amigo')
        
        if choice == '1':
            await update.message.reply_text(
                "Para analisar seus gastos reais, você precisará:\n\n"
                "1. Anotar todos os seus gastos do mês\n"
                "2. Classificar por categorias\n"
                "3. Comparar com nossa sugestão\n"
                "4. Ajustar onde necessário\n\n"
                "Posso te ajudar com isso em uma próxima conversa!\n\n"
                "Use /start para começar novamente.",
                reply_markup=ReplyKeyboardRemove()
            )
        elif choice == '2':
            await update.message.reply_text(
                f"Certo {user_name}, foi um prazer te acompanhar nessa jornada. Volte sempre!",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            # Teclado com opções (botões menores)
            keyboard = [['1'], ['2']]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text(
                "Por favor, escolha 1 ou 2:",
                reply_markup=reply_markup
            )
            return OPTIONS
        
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancela a conversa"""
        await update.message.reply_text(
            'Conversa cancelada. Use /start para começar novamente.',
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando de ajuda"""
        help_text = (
            "🤖 **Edu - Assistente Financeiro**\n\n"
            "Comandos disponíveis:\n"
            "/start - Iniciar planejamento financeiro\n"
            "/stop - Parar conversa atual\n"
            "/help - Mostrar esta mensagem\n"
            "/cancel - Cancelar conversa atual\n\n"
            "Eu ajudo você a organizar seu orçamento mensal!"
        )
        await update.message.reply_text(help_text)

def main() -> None:
    """Função principal"""
    # Criar aplicação
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Inicializar bot
    finance_bot = FinanceBot()
    
    # Criar ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', finance_bot.start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, finance_bot.get_name)],
            SALARY: [MessageHandler(filters.TEXT & ~filters.COMMAND, finance_bot.get_salary)],
            OPTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, finance_bot.handle_options)],
        },
        fallbacks=[
            CommandHandler('cancel', finance_bot.cancel),
            CommandHandler('stop', finance_bot.stop_command)
        ],
    )
    
    # Adicionar handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("stop", finance_bot.stop_command))
    application.add_handler(CommandHandler("help", finance_bot.help_command))
    application.add_handler(CommandHandler("cancel", finance_bot.cancel))
    
    # Iniciar bot
    print("🤖 Edu Bot iniciado! Pressione Ctrl+C para parar.")
    application.run_polling()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f"Erro ao iniciar bot: {e}")