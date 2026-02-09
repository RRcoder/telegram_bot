import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env
TOKEN_BOT = os.getenv("TOKEN_BOT")

import logging
import yfinance as yf
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuración de logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context):
    await update.message.reply_text("¡Hola! Envíame /stock seguido del ticker (ej: /stock AAPL) para ver precio y fundamentales.")

async def get_stock(update: Update, context):
    if not context.args:
        await update.message.reply_text("Por favor, indica un ticker. Ejemplo: /stock MSFT")
        return

    ticker_symbol = context.args[0].upper()
    await update.message.reply_text(f"🔍 Buscando datos de {ticker_symbol}...")

    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info

        # Extracción de datos (si no existen, ponemos 'N/A')
        precio = info.get('currentPrice', 'N/A')
        moneda = info.get('currency', 'USD')
        nombre = info.get('longName', ticker_symbol)
        
        # Datos Fundamentales
        eps = info.get('trailingEps', 'N/A')
        pe_ratio = info.get('trailingPE', 'N/A')
        mkt_cap = info.get('marketCap', 'N/A')
        div_yield = info.get('dividendYield', 0) * 100 # Convertir a %

        mensaje = (
            f"<b>📊 {nombre} ({ticker_symbol})</b>\n"
            f"----------------------------------\n"
            f"💰 <b>Precio:</b> {precio} {moneda}\n\n"
            f"<b>Análisis Fundamental:</b>\n"
            f"• <b>EPS (Utilidad por Acción):</b> {eps}\n"
            f"• <b>P/E Ratio:</b> {pe_ratio}\n"
            f"• <b>Market Cap:</b> {mkt_cap:,} {moneda}\n"
            f"• <b>Dividend Yield:</b> {div_yield:.2f}%\n"
            f"----------------------------------"
        )

        await update.message.reply_html(mensaje)

    except Exception as e:
        await update.message.reply_text(f"❌ Error al buscar {ticker_symbol}. Asegúrate de que el ticker sea correcto.")

if __name__ == '__main__':
    application = Application.builder().token(TOKEN_BOT).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stock", get_stock))
    
    print("Bot en marcha... Presiona Ctrl+C para detener.")
    application.run_polling()
