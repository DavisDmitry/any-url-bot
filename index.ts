import { Bot, webhookCallback, InlineKeyboard } from 'grammy/web'

declare global {
  const BOT_TOKEN: string
  const SECRET_TOKEN: string // header 'X-Telegram-Bot-Api-Secret-Token'
}

const startText = 'Send me an HTTPS URL'
const invalidURLText = 'The URL you sent is invalid'

const bot = new Bot(BOT_TOKEN)

bot.command('start', ctx => {
  return ctx.reply(startText)
})

bot.on('message:text', async ctx => {
  try {
    const url = validateURL(ctx.msg.text)
    return ctx.reply(ctx.msg.text, {
      reply_markup: new InlineKeyboard([
        [{ text: 'WebApp', web_app: { url: url.toString() } }]
      ])
    })
  } catch {
    return ctx.reply(invalidURLText)
  }
})

addEventListener(
  'fetch',
  webhookCallback(bot, 'cloudflare', { secretToken: SECRET_TOKEN })
)

const urlHostRegex = new RegExp(
  '(?<ipv4>(?:d{1,3}.){3}d{1,3})(?=$|[/:#?])|' +
    '(?<ipv6>[[A-F0-9]*:[A-F0-9:]+])(?=$|[/:#?])|' +
    '(?<domain>[^s/:?#]+)'
)

function validateURL(input: string): URL {
  if (!(input.startsWith('http://') || input.startsWith('https://')))
    input = `https://${input}`
  const url = new URL(input)
  if (!urlHostRegex.test(url.hostname)) throw 'Invalid hostname'
  return url
}
