import topDomains from './top-domains.json'
import domainList from './domain_list.json'

export const IP_Pattern = /(?:^|\s)(?!0\.0\.0\.0|127\.0\.0\.1|10(\.\d{1,3}){3}|172\.(1[6-9]|2[0-9]|3[0-1])(\.\d{1,3}){2}|192\.168(\.\d{1,3}){2})(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?:\s|$)/g

export const base64_Pattern = /^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/

// eslint-disable-next-line no-useless-escape
export const byteString_Pattern = /\".*(\\x[0-9a-f]{2})+.*\"/i

const schema_pattern_string = '(?:http|https|ftp|sftp|ssh|smtp|imap|pop3|ldap|dns|telnet|nfs|rdp|webdav|irc):\\/\\/'

let domain_pattern: RegExp

export function getDomainPattern () {
  if (domain_pattern) {
    return domain_pattern
  }
  let domain_pattern_string = '(?:[a-zA-Z0-9\\-]+\\.)+'
  const domainArr = topDomains['most-used-tlds']
  for (let i = 0; i < domainArr.length; i++) {
    const domain = domainArr[i].substring(1)
    if (i === 0) {
      domain_pattern_string += '(?:' + domain + '|'
    } else if (i < domainArr.length - 1) {
      domain_pattern_string += domain + '|'
    } else {
      domain_pattern_string += domain + ')'
    }
  }
  domain_pattern = new RegExp(domain_pattern_string)
  return domain_pattern
}

export const Network_Command_Pattern = /(curl)|(wget)|(host)|(ping)|(\/dev\/tcp)/

export const SensitiveStringPattern = /(\/etc\/shadow)|(\.bashrc)|(.zshrc)|(\/etc\/hosts)|(\/etc\/passwd)|(\/bin\/sh)/

export function getDomainType(domain: string) {
  domain = domain.substring(domain.indexOf('://') + 3)
  if(domainList.white_domain_list.includes(domain)) {
    return 1
  } else if (domainList.black_domain_list.includes(domain)) {
    return 4
  } else if (domainList.common_domain_list.includes(domain)) {
    return 2
  } else {
    return 3
  }
}

export function getDomainsType(domains: string[]) {
  const result: number[] = []
  for (const domain of domains) {
    result.push(getDomainType(domain))
  }
  return Math.min(...result)
}