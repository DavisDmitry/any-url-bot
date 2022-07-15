# Any URL Bot

A [simple Telegram bot](https://t.me/any_url_bot) that opens links like a WebApp

## Deployment

You can deploy it with Docker (and docker compose).

[docker-compose.yml example](https://github.com/DavisDmitry/any-url-bot/blob/master/docker-compose.yml)

### Environment variables

* LOG_LEVEL: one of "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"
* BOT_TOKEN
* WEBHOOK_URL: must be a valid HTTPS URL
* WEBHOOK_SECRET: optional, can only consist A-z, 0-9, "-" and"_"
