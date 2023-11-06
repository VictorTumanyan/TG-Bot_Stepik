from config.config import load_config

config = load_config('./.env')

bot_token = config.tg_bot.token
superadmin = config.tg_bot.admin_ids[0]

print(config.tg_bot.token)