import { Bot, Composer, webhookCallback, InlineKeyboard, GrammyError } from 'grammy/web'

const START_TEXT = 'Send me an HTTPS URL'
const INVALID_URL_TEXT = 'The URL you sent is invalid'
const INTERNAL_ERROR_TEXT = 'Internal error.'

const router = new Composer()

router.command('start', ctx => ctx.reply(START_TEXT))

router.on('message:text', async ctx => {
  try {
    await ctx.reply(ctx.msg.text, {
      reply_markup: new InlineKeyboard([
        [
          {
            text: 'WebApp',
            web_app: { url: makeURL(ctx.msg.text) }
          }
        ]
      ])
    })
  } catch (err) {
    if (
      err instanceof GrammyError &&
      /Bad Request: inline keyboard button Web App URL '.+' is invalid: .+/.test(
        err.description
      )
    ) {
      return ctx.reply(INVALID_URL_TEXT)
    }
    await ctx.reply(INTERNAL_ERROR_TEXT)
    throw err
  }
})

function makeURL(url: string): string {
  url = url.replace('http://', 'https://')
  if (!url.startsWith('https://')) {
    url = `https://${url}`
  }
  return url
}

export interface Env {
  BOT_TOKEN: string
  SECRET_TOKEN: string // header 'X-Telegram-Bot-Api-Secret-Token'
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const bot = new Bot(env.BOT_TOKEN, {})
    bot.use(router)
    const callback = webhookCallback(bot, 'cloudflare-mod', {
      secretToken: env.SECRET_TOKEN
    })
    try {
      return await callback(request)
    } catch (err) {
      console.log(err)
      return new Response(null, { status: 500 })
    }
  }
}
