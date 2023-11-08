from uuid import uuid4

from telegram import (
    Update,
    BotCommand,
    InlineQueryResultArticle,
    InputTextMessageContent
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    Defaults,
    filters,
    CallbackQueryHandler,
    InlineQueryHandler
)

import command
import common
import query as qy
from manager import manager
from text import *


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query
    if query == "":
        return
    elif update.inline_query.from_user.id not in common.admin:
        return
    if query.startswith("/add_server"):
        result = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=f"{ADD_SERVER} > {query.replace('/add_server ', '', 1)}",
                input_message_content=InputTextMessageContent(query)
            )
        ]
        await update.inline_query.answer(result)
        return
    elif query.startswith("/remove_server"):
        result = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=f"{REMOVE_SERVER} > {server_name}",
                input_message_content=InputTextMessageContent(f"/remove_server {server_id}")
            )
            for server_id, server_name in manager.get_server_enum()
        ]
        await update.inline_query.answer(result)
        return
    elif query.startswith("/rename_server"):
        server_id = query.replace("/rename_server ", '', 1).split(" ")[0]
        result = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=f"{RENAME_SERVER} > {manager.get_server_name(server_id)}",
                input_message_content=InputTextMessageContent(query)
            )
        ]
        await update.inline_query.answer(result)
        return
    elif query.startswith("/add_user"):
        result = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=f"{ADD_USER} > {query.replace('/add_user ', '', 1)}",
                input_message_content=InputTextMessageContent(query)
            )
        ]
        await update.inline_query.answer(result)
        return
    elif query.startswith("/remove_user"):
        result = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=f"{REMOVE_USER} > {user_name}",
                input_message_content=InputTextMessageContent(f"/remove_user {user_name}")
            )
            for user_name in manager.get_user_list()
        ]
        await update.inline_query.answer(result)
        return
    elif query.startswith("/rename_user"):
        user_name = query.replace("/rename_user ", '', 1).split(" ")[0]
        result = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=f"{RENAME_USER} > {user_name}",
                input_message_content=InputTextMessageContent(query)
            )
        ]
        await update.inline_query.answer(result)
        return
    elif query.startswith("/sub_server"):
        server_id, name, *_ = query.replace("/sub_server ", '', 1).split(" ")
        result = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=f"{SUB_SERVER}\n{manager.get_server_name(server_id)}\n{name}",
                input_message_content=InputTextMessageContent(query)
            )
        ]
        await update.inline_query.answer(result)
        return
    elif query.startswith("/remove_sub"):
        server_id = query.replace("/remove_sub ", '', 1).split(" ")[0]
        result = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=f"{REMOVE_SUB} > {manager.get_server_name(server_id)} > {user_name}",
                input_message_content=InputTextMessageContent(f"/remove_sub {server_id} {user_name}")
            )
            for user_name in manager.get_sub_user(server_id)
        ]
        await update.inline_query.answer(result)
        return
    elif query.startswith("/set_user_target"):
        user_name = query.replace("/set_user_target ", '', 1).split(" ")[0]
        result = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=f"{SET_TARGET} > {user_name} > {target}",
                input_message_content=InputTextMessageContent(f"/set_user_target {user_name} {target}")
            )
            for target in ["clash", "mixed"]
        ]
        await update.inline_query.answer(result)
        return
    elif query.startswith("/set_url"):
        result = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=f"{SET_URL} > {query.replace('/set_url ', '', 1)}",
                input_message_content=InputTextMessageContent(query)
            )
        ]
        await update.inline_query.answer(result)
        return
    elif query.startswith("/set_pw"):
        result = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=f"{SET_PW} > {query.replace('/set_pw ', '', 1)}",
                input_message_content=InputTextMessageContent(query)
            )
        ]
        await update.inline_query.answer(result)
        return


async def post_init(application: Application) -> None:
    commands = [
        BotCommand('start', CMD_START),
    ]
    await application.bot.set_my_commands(commands)
    await application.bot.set_my_description(DESCRIPTION)
    await application.bot.set_my_short_description(DESCRIPTION)


def main():
    defaults = Defaults(parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True, allow_sending_without_reply=True)
    application = (ApplicationBuilder()
                   .token(common.token)
                   .defaults(defaults)
                   .post_init(post_init)
                   .build())

    user_filter = filters.User()
    user_filter.add_user_ids(common.admin)

    handlers = [
        CommandHandler('start', command.start, filters=user_filter),
        CommandHandler('add_server', command.add_server, filters=user_filter),
        CommandHandler('remove_server', command.remove_server, filters=user_filter),
        CommandHandler('rename_server', command.rename_server, filters=user_filter),
        CommandHandler('add_user', command.add_user, filters=user_filter),
        CommandHandler('remove_user', command.remove_user, filters=user_filter),
        CommandHandler('rename_user', command.rename_user, filters=user_filter),
        CommandHandler('sub_server', command.sub_server, filters=user_filter),
        CommandHandler('remove_sub', command.remove_sub, filters=user_filter),
        CommandHandler('set_user_target', command.set_user_target, filters=user_filter),
        CommandHandler('set_url', command.set_url, filters=user_filter),
        CommandHandler('set_pw', command.set_pw, filters=user_filter),
        CallbackQueryHandler(qy.server, pattern=r'^server$'),
        CallbackQueryHandler(qy.reorder, pattern=r'^reorder'),
        CallbackQueryHandler(qy.user, pattern=r'^user$'),
        CallbackQueryHandler(qy.sub, pattern=r'^sub$'),
        CallbackQueryHandler(qy.sub_server, pattern=r'^sub_server\|'),
        CallbackQueryHandler(qy.url, pattern=r'^url$'),
        CallbackQueryHandler(qy.link, pattern=r'^link$'),
        CallbackQueryHandler(qy.user_link, pattern=r'^user_link\|'),
        CallbackQueryHandler(qy.export, pattern=r'^export$'),
        CallbackQueryHandler(qy.save, pattern=r'^save_sub$'),
        CallbackQueryHandler(qy.back, pattern=r'^back$'),
        InlineQueryHandler(inline_query),
    ]

    application.add_handlers(handlers)

    application.run_polling()


if __name__ == '__main__':
    main()
