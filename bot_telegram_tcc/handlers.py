from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
import database as db

# Estados da conversa
GET_NAME, MAIN_MENU, GET_INITIAL, GET_CREDIT, GET_CREDIT_DESC, GET_DEBIT, GET_DEBIT_DESC = range(7)

def main_keyboard():
    """Teclado principal do bot"""
    keyboard = [
        ['➕ Saldo Inicial', '💳 Adicionar Crédito'],
        ['💸 Adicionar Débito', '📊 Saldo Atual'],
        ['📋 Extrato']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, input_field_placeholder="Escolha uma opção...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia a conversa com o usuário"""
    await update.message.reply_text(
        "👋 Olá! Sou seu assistente financeiro pessoal.\n\n"
        "Como você gostaria de ser chamado?"
    )
    return GET_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Recebe e salva o nome do usuário"""
    nickname = update.message.text.strip()
    user_id = update.effective_user.id
    
    if not nickname:
        await update.message.reply_text("❌ Por favor, digite um nome válido.")
        return GET_NAME
    
    db.add_user(user_id, nickname)
    
    await update.message.reply_text(
        f"🎉 Perfeito, {nickname}! Agora vamos gerenciar suas finanças.\n\n"
        "Use o menu abaixo para controlar seus gastos e ganhos:",
        reply_markup=main_keyboard()
    )
    return MAIN_MENU

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Menu principal - processa as escolhas do usuário"""
    text = update.message.text
    user_id = update.effective_user.id
    
    if text == '➕ Saldo Inicial':
        await update.message.reply_text(
            "💰 **Adicionar Saldo Inicial**\n\n"
            "Digite o valor do seu saldo inicial:\n"
            "Ex: 1000 ou 1500,50"
        )
        return GET_INITIAL
        
    elif text == '💳 Adicionar Crédito':
        await update.message.reply_text(
            "💳 **Adicionar Crédito**\n\n"
            "Digite o valor do crédito:\n"
            "Ex: 500 ou 750,25"
        )
        return GET_CREDIT
        
    elif text == '💸 Adicionar Débito':
        await update.message.reply_text(
            "💸 **Adicionar Débito**\n\n"
            "Digite o valor do débito:\n"
            "Ex: 150 ou 89,90"
        )
        return GET_DEBIT
        
    elif text == '📊 Saldo Atual':
        balance = db.get_balance(user_id)
        nickname = db.get_user_nickname(user_id)
        await update.message.reply_text(
            f"💰 **Saldo Atual**\n\n"
            f"👤 {nickname}\n"
            f"💎 Saldo: R$ {balance:,.2f}\n\n"
            f"*Use as opções abaixo para movimentar sua conta*",
            reply_markup=main_keyboard()
        )
        
    elif text == '📋 Extrato':
        transactions = db.get_statement(user_id)
        nickname = db.get_user_nickname(user_id)
        balance = db.get_balance(user_id)
        
        if not transactions:
            await update.message.reply_text(
                "📭 **Extrato**\n\n"
                "Nenhuma transação registrada ainda.\n\n"
                "Use as opções abaixo para fazer sua primeira movimentação!",
                reply_markup=main_keyboard()
            )
        else:
            response = f"📋 **Extrato - {nickname}**\n\n"
            
            for i, t in enumerate(transactions, 1):
                emoji = "⬆️💰" if t[0] == 'credit' else "⬇️💸"
                tipo = "CRÉDITO" if t[0] == 'credit' else "DÉBITO"
                valor = f"R$ {t[1]:,.2f}"
                data = t[3][:16]  # Formata a data
                
                response += f"{emoji} **{tipo}**\n"
                response += f"   Valor: {valor}\n"
                response += f"   Descrição: {t[2]}\n"
                response += f"   Data: {data}\n\n"
            
            response += f"💎 **Saldo Total: R$ {balance:,.2f}**"
            
            await update.message.reply_text(
                response,
                reply_markup=main_keyboard()
            )
    
    return MAIN_MENU

async def handle_initial(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa o saldo inicial"""
    try:
        amount_text = update.message.text.replace(',', '.').strip()
        amount = float(amount_text)
        
        if amount <= 0:
            await update.message.reply_text("❌ O valor deve ser maior que zero. Tente novamente:")
            return GET_INITIAL
            
        user_id = update.effective_user.id
        db.add_transaction(user_id, 'credit', amount, 'Saldo inicial')
        
        await update.message.reply_text(
            f"✅ **Saldo Inicial Registrado!**\n\n"
            f"💰 Valor: R$ {amount:,.2f}\n\n"
            f"Agora você pode adicionar créditos e débitos usando o menu abaixo:",
            reply_markup=main_keyboard()
        )
        return MAIN_MENU
        
    except ValueError:
        await update.message.reply_text(
            "❌ **Valor inválido!**\n\n"
            "Por favor, digite um valor numérico válido:\n"
            "Ex: 1000 ou 1500,50"
        )
        return GET_INITIAL

async def handle_credit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa o valor do crédito"""
    try:
        amount_text = update.message.text.replace(',', '.').strip()
        amount = float(amount_text)
        
        if amount <= 0:
            await update.message.reply_text("❌ O valor deve ser maior que zero. Tente novamente:")
            return GET_CREDIT
            
        context.user_data['credit_amount'] = amount
        await update.message.reply_text(
            "📝 **Origem do Crédito**\n\n"
            "Digite a origem deste valor:\n"
            "Ex: Salário, Freelance, Vendas, etc."
        )
        return GET_CREDIT_DESC
        
    except ValueError:
        await update.message.reply_text(
            "❌ **Valor inválido!**\n\n"
            "Por favor, digite um valor numérico válido:\n"
            "Ex: 500 ou 750,25"
        )
        return GET_CREDIT

async def handle_credit_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa a descrição do crédito"""
    description = update.message.text.strip()
    if not description:
        await update.message.reply_text("❌ Por favor, digite uma descrição válida:")
        return GET_CREDIT_DESC
        
    amount = context.user_data.get('credit_amount')
    if amount:
        user_id = update.effective_user.id
        db.add_transaction(user_id, 'credit', amount, description)
        
        await update.message.reply_text(
            f"✅ **Crédito Adicionado!**\n\n"
            f"💰 Valor: R$ {amount:,.2f}\n"
            f"📝 Origem: {description}\n\n"
            f"Seu saldo foi atualizado com sucesso!",
            reply_markup=main_keyboard()
        )
        # Limpa os dados temporários
        context.user_data.pop('credit_amount', None)
    else:
        await update.message.reply_text(
            "❌ Ocorreu um erro. Por favor, comece novamente.",
            reply_markup=main_keyboard()
        )
    
    return MAIN_MENU

async def handle_debit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa o valor do débito"""
    try:
        amount_text = update.message.text.replace(',', '.').strip()
        amount = float(amount_text)
        
        if amount <= 0:
            await update.message.reply_text("❌ O valor deve ser maior que zero. Tente novamente:")
            return GET_DEBIT
            
        context.user_data['debit_amount'] = amount
        await update.message.reply_text(
            "📝 **Descrição do Débito**\n\n"
            "Digite a descrição desta despesa:\n"
            "Ex: Aluguel, Supermercado, Transporte, etc."
        )
        return GET_DEBIT_DESC
        
    except ValueError:
        await update.message.reply_text(
            "❌ **Valor inválido!**\n\n"
            "Por favor, digite um valor numérico válido:\n"
            "Ex: 150 ou 89,90"
        )
        return GET_DEBIT

async def handle_debit_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa a descrição do débito"""
    description = update.message.text.strip()
    if not description:
        await update.message.reply_text("❌ Por favor, digite uma descrição válida:")
        return GET_DEBIT_DESC
        
    amount = context.user_data.get('debit_amount')
    if amount:
        user_id = update.effective_user.id
        db.add_transaction(user_id, 'debit', amount, description)
        
        await update.message.reply_text(
            f"✅ **Débito Registrado!**\n\n"
            f"💸 Valor: R$ {amount:,.2f}\n"
            f"📝 Descrição: {description}\n\n"
            f"Sua despesa foi registrada com sucesso!",
            reply_markup=main_keyboard()
        )
        # Limpa os dados temporários
        context.user_data.pop('debit_amount', None)
    else:
        await update.message.reply_text(
            "❌ Ocorreu um erro. Por favor, comece novamente.",
            reply_markup=main_keyboard()
        )
    
    return MAIN_MENU

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela a operação atual"""
    await update.message.reply_text(
        "❌ Operação cancelada.",
        reply_markup=main_keyboard()
    )
    return MAIN_MENU