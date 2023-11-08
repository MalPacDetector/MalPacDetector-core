import domains from './top-domains.json'

export const IP_Pattern = /(\d{1,3}\.){3}\d{1,3}/

export const base64_Pattern = /^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/

// eslint-disable-next-line no-useless-escape
export const byteString_Pattern = /\".*(\\x[0-9a-f]{2})+.*\"/i

let domain_pattern: RegExp

export function getDomainPattern () {
  if (domain_pattern) {
    return domain_pattern
  }
  let domain_pattern_string = '([a-zA-Z0-9\\-]+\\.)+'
  const domainArr = domains['most-used-tlds']
  for (let i = 0; i < domainArr.length; i++) {
    const domain = domainArr[i].substring(1)
    if (i === 0) {
      domain_pattern_string += '(' + domain + '|'
    } else if (i < domainArr.length - 1) {
      domain_pattern_string += domain + '|'
    } else {
      domain_pattern_string += domain + ')'
    }
  }
  domain_pattern = new RegExp(domain_pattern_string)
  return domain_pattern
}

export const Network_Command_Pattern = /(curl)|(wget)|(host)|(ping)|(\/dev\/tcp)|(ping)/

export const SensitiveStringPattern = /(\/etc\/shadow)|(\.bashrc)|(.zshrc)|(\/etc\/hosts)|(\/etc\/passwd)|(\/bin\/sh)/
