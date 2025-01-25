from telegram import Update, ChatPermissions
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Replace with your bot token
TOKEN = "YOUR_BOT_TOKEN"

# Dictionary to track warnings
warnings = {}

# Maximum warnings before muting a user
MAX_WARNINGS = 3

# Welcome new members
def welcome_new_user(update: Update, context: CallbackContext):
    for new_member in update.message.new_chat_members:
        username = new_member.username or new_member.first_name
        update.message.reply_text(f"Welcome, {username}! 🎉 Please follow the group rules and enjoy your stay!")

# Warn users for sending links
def warn_links(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user.id
    chat_id = update.message.chat_id

    # Check if the message contains a link
    if Filters.entity("url").filter(update.message):
        # Increase warning count for the user
        warnings[user_id] = warnings.get(user_id, 0) + 1
        warning_count = warnings[user_id]

        # Warn the user
        update.message.reply_text(
            f"🚫 {user.first_name}, sending links is not allowed! This is warning {warning_count}/{MAX_WARNINGS}."
        )

        # Check if the user has exceeded the warning limit
        if warning_count >= MAX_WARNINGS:
            # Mute the user
            context.bot.restrict_chat_member(
                chat_id,
                user_id,
                permissions=ChatPermissions(can_send_messages=False),
            )
            update.message.reply_text(
                f"❌ {user.first_name} has been muted for exceeding the warning limit."
            )

# Main function
def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Handler for new chat members
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_new_user))

    # Handler for messages containing links
    dispatcher.add_handler(MessageHandler(Filters.entity("url"), warn_links))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

