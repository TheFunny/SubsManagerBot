from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from common import start_kb
from manager import manager
from text import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_action(ChatAction.TYPING)
    await update.message.reply_text(MSG_START, reply_markup=start_kb)


async def add_server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_action(ChatAction.TYPING)
    if not context.args:
        await update.message.reply_text(MSG_ADD_SERVER_FAIL)
        return
    if manager.add_server(" ".join(context.args)):
        await update.message.reply_text(MSG_ADD_SERVER_SUCCESS)
    else:
        await update.message.reply_text(MSG_ADD_SERVER_FAIL)


async def remove_server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_action(ChatAction.TYPING)
    if len(context.args) != 1:
        await update.message.reply_text(MSG_REMOVE_SERVER_FAIL)
        return
    if manager.remove_server(context.args[0]):
        await update.message.reply_text(MSG_REMOVE_SERVER_SUCCESS)
    else:
        await update.message.reply_text(MSG_REMOVE_SERVER_FAIL)


async def rename_server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_action(ChatAction.TYPING)
    if len(context.args) < 2:
        await update.message.reply_text(MSG_RENAME_SERVER_FAIL)
        return
    server_name = " ".join(context.args[1:])
    if manager.rename_server(context.args[0], server_name):
        await update.message.reply_text(MSG_RENAME_SERVER_SUCCESS)
    else:
        await update.message.reply_text(MSG_RENAME_SERVER_FAIL)


async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_action(ChatAction.TYPING)
    if not context.args:
        await update.message.reply_text(MSG_ADD_USER_FAIL)
        return
    if manager.add_user("-".join(context.args)):
        await update.message.reply_text(MSG_ADD_USER_SUCCESS)
    else:
        await update.message.reply_text(MSG_ADD_USER_FAIL)


async def remove_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_action(ChatAction.TYPING)
    if len(context.args) != 1:
        await update.message.reply_text(MSG_REMOVE_USER_FAIL)
        return
    if manager.remove_user(context.args[0]):
        await update.message.reply_text(MSG_REMOVE_USER_SUCCESS)
    else:
        await update.message.reply_text(MSG_REMOVE_USER_FAIL)


async def rename_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_action(ChatAction.TYPING)
    if len(context.args) < 2:
        await update.message.reply_text(MSG_RENAME_USER_FAIL)
        return
    user_name = "-".join(context.args[1:])
    if manager.rename_user(context.args[0], user_name):
        await update.message.reply_text(MSG_RENAME_USER_SUCCESS)
    else:
        await update.message.reply_text(MSG_RENAME_USER_FAIL)


async def sub_server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_action(ChatAction.TYPING)
    if len(context.args) != 3:
        await update.message.reply_text(MSG_SUB_SERVER_FAIL)
        return
    if manager.add_sub(context.args[1], context.args[0], context.args[2]):
        await update.message.reply_text(MSG_SUB_SERVER_SUCCESS)
    else:
        await update.message.reply_text(MSG_SUB_SERVER_FAIL)


async def remove_sub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_action(ChatAction.TYPING)
    if len(context.args) != 2:
        await update.message.reply_text(MSG_REMOVE_SUB_FAIL)
        return
    if manager.remove_sub(context.args[1], context.args[0]):
        await update.message.reply_text(MSG_REMOVE_SUB_SUCCESS)
    else:
        await update.message.reply_text(MSG_REMOVE_SUB_FAIL)


async def set_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_action(ChatAction.TYPING)
    if len(context.args) != 1:
        await update.message.reply_text(MSG_SET_URL_FAIL)
        return
    if manager.set_url(context.args[0]):
        await update.message.reply_text(MSG_SET_URL_SUCCESS)
    else:
        await update.message.reply_text(MSG_SET_URL_FAIL)


async def set_user_target(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_action(ChatAction.TYPING)
    if len(context.args) != 2:
        await update.message.reply_text(MSG_SET_USER_TARGET_FAIL)
        return
    if manager.set_user_target(context.args[0], context.args[1]):
        await update.message.reply_text(MSG_SET_USER_TARGET_SUCCESS)
    else:
        await update.message.reply_text(MSG_SET_USER_TARGET_FAIL)


async def set_pw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_action(ChatAction.TYPING)
    if len(context.args) != 1:
        await update.message.reply_text(MSG_SET_PW_FAIL)
        return
    if manager.set_pw(context.args[0]):
        await update.message.reply_text(MSG_SET_PW_SUCCESS)
    else:
        await update.message.reply_text(MSG_SET_PW_FAIL)
