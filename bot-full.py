"""
Documentación:
https://docs.python-telegram-bot.org/en/stable/
https://gpiozero.readthedocs.io/
"""
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
##################################################################
#%% Control de periféricos
import gpiozero

IR_pin = 3
IR_trigger = True

IR = gpiozero.DigitalInputDevice(IR_pin, pull_up=True) # Active (1) es LOW
IR.when_deactivated = IR_deactivated_fun # Deactivated = High = Detecta movimiento
#IR.when_activated = IR_activated_fun

##################################################################
#%% Bot
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

bot_token = "bot_token"
# id_nico = 192929292 # ID number. Eventualmente, para restringir acceso al bot
    
# Estado de alarma ###########################################################
estado_alarma = False
async def activarAlarma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    estado_alarma = True
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Alarma ACTIVADA.")
async def desactivarAlarma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    estado_alarma = False
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Alarma DESACTIVADA.")

# Funciones inútiles por ahora ###########################################################
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Qué mirás, bobo.")
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

    
if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Defino estado de alarma activado o desactivado
    activarAlarma_handler = CommandHandler('activarAlarma', activarAlarma)
    application.add_handler(activarAlarma_handler)
    desactivarAlarma_handler = CommandHandler('desactivarAlarma', desactivarAlarma)
    application.add_handler(desactivarAlarma_handler)
    
        
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)
