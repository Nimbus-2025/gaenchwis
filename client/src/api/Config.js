import Proxy from "./Proxy"

const Config = {
  clientId: "6dnsfj8d7327ghh5sg62eqbru0",
  tokenUrl: `${Proxy.domain}/oauth2/token`,
  domain: Proxy.domain,
  redirectUrl: Proxy.callback,
  scope: "email openid profile",
  chromeExtension: "llanbjflabjnkhppccaoaaogekblghfj",
  server: Proxy.server
}

export default Config;