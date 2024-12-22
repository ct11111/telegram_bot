import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

group_balances = {}

# 替换为你自己的 Telegram 用户 ID
OWNER_ID = 7157180289

async def handle_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text.strip()
    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 余额 +xxx
    if text.startswith("余额 +"):
        try:
            if update.effective_user.id != OWNER_ID:
                return

            amount = float(text.replace("余额 +", "").strip())
            group_balances[chat_id] = group_balances.get(chat_id, 0) + amount
            await update.message.reply_text(
                f"{current_time}\n余额已增加 {amount}，当前余额：{group_balances[chat_id]}"
            )
        except ValueError:
            await update.message.reply_text("请检查金额格式")

    # 余额 -xxx
    elif text.startswith("余额 -"):
        try:
            if update.effective_user.id != OWNER_ID:
                return

            amount = float(text.replace("余额 -", "").strip())
            group_balances[chat_id] = group_balances.get(chat_id, 0) - amount
            await update.message.reply_text(
                f"{current_time}\n余额已减少 {amount}，当前余额：{group_balances[chat_id]}"
            )
        except ValueError:
            await update.message.reply_text("请检查金额格式")

    # 仅输入 余额
    elif text == "余额":
        current_balance = group_balances.get(chat_id, 0)
        await update.message.reply_text(
            f"{current_time}\n当前余额：{current_balance}"
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text.startswith("余额"):
        await handle_balance(update, context)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("记账机器人已启动，欢迎使用！")

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # 替换成你从 BotFather 获得的 Token
    BOT_TOKEN = "7886185422:AAHy0kk5rT-QVUCH1ond7ckmOXWI7euOAYE"

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
