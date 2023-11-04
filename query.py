from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

import common
from manager import manager
from text import *


async def server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    kb = [[InlineKeyboardButton(name, switch_inline_query_current_chat=f"/rename_server {server_id} ")]
          for server_id, name in manager.get_server_enum()]
    kb.append([
        InlineKeyboardButton(ADD, switch_inline_query_current_chat="/add_server "),
        InlineKeyboardButton(REMOVE, switch_inline_query_current_chat="/remove_server "),
    ])
    kb.append([InlineKeyboardButton(BACK, callback_data="back")])
    reply_markup = InlineKeyboardMarkup(kb)
    await query.edit_message_text(SERVER, reply_markup=reply_markup)


async def user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    kb = [[InlineKeyboardButton(name, switch_inline_query_current_chat=f"/rename_user {name} ")]
          for name in manager.get_user_list()]
    kb.append([
        InlineKeyboardButton(ADD, switch_inline_query_current_chat="/add_user "),
        InlineKeyboardButton(REMOVE, switch_inline_query_current_chat="/remove_user "),
    ])
    kb.append([InlineKeyboardButton(BACK, callback_data="back")])
    reply_markup = InlineKeyboardMarkup(kb)
    await query.edit_message_text(USER, reply_markup=reply_markup)


async def sub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    kb = [[InlineKeyboardButton(server_name, callback_data=f"sub_server|{server_id}")]
          for server_id, server_name in manager.get_server_enum()]
    kb.append([InlineKeyboardButton(BACK, callback_data="back")])
    reply_markup = InlineKeyboardMarkup(kb)
    await query.edit_message_text(MSG_SUB_SERVER, reply_markup=reply_markup)


async def sub_server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    server_id = query.data.split("|")[1]
    kb = [[
        InlineKeyboardButton(
            (KEY_HAS_SUB if user_name in manager.get_sub_user(server_id) else KEY_NO_SUB) + user_name,
            switch_inline_query_current_chat=f"/sub_server {server_id} {user_name} "
        )
    ] for user_name in manager.get_user_list()]
    kb.append([InlineKeyboardButton(REMOVE, switch_inline_query_current_chat=f"/remove_sub {server_id} ")])
    kb.append([InlineKeyboardButton(BACK, callback_data="sub")])
    reply_markup = InlineKeyboardMarkup(kb)
    await query.edit_message_text(MSG_SUB_SERVER_USER, reply_markup=reply_markup)


async def save(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if manager.save_sub():
        await update.effective_chat.send_message(MSG_SAVE_SUCCESS)
    else:
        await update.effective_chat.send_message(MSG_SAVE_FAIL)


async def url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    kb = [[
        InlineKeyboardButton(
            f"{user_name} | {manager.get_user_target(user_name)}",
            switch_inline_query_current_chat=f"/set_user_target {user_name} "
        )
    ] for user_name in manager.get_user_list()]
    kb.append([
        InlineKeyboardButton(SET_URL, switch_inline_query_current_chat="/set_url "),
        InlineKeyboardButton(SET_PW, switch_inline_query_current_chat="/set_pw "),
    ])
    kb.append([InlineKeyboardButton(BACK, callback_data="back")])
    reply_markup = InlineKeyboardMarkup(kb)
    await query.edit_message_text(URL, reply_markup=reply_markup)


async def link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    kb = [[InlineKeyboardButton(user_name, callback_data=f"user_link|{user_name}")] for user_name in
          manager.get_user_list()]
    kb.append([InlineKeyboardButton(EXPORT, callback_data="export")])
    kb.append([InlineKeyboardButton(BACK, callback_data="back")])
    reply_markup = InlineKeyboardMarkup(kb)
    await query.edit_message_text(LINK, reply_markup=reply_markup)


def get_link(sub_link: str) -> str:
    url, pw = manager.get_url_pw()
    return f"{url}/getprofile?name=profiles/{sub_link}.ini&token={pw}"


async def user_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    name = query.data.split("|")[1]
    await query.answer()
    message = f"{name}: <code>{get_link(manager.get_link(name))}</code>"
    await update.effective_chat.send_message(message)


async def export(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    message = "".join([f"{user_name}: <code>{get_link(sub_link)}</code>\n"
                       for user_name, sub_link in manager.get_link_enum()])
    await update.effective_chat.send_message(message)


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(MSG_START, reply_markup=common.start_kb)
