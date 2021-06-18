import Cookies from '@/static/js/cookie'

const TokenKey = 'token'

export function getToken() {
  return Cookies.getCookie(TokenKey)
}

export function setToken(token) {
  return Cookies.setCookie(TokenKey, token)
}

export function removeToken() {
  return Cookies.delCookie(TokenKey)
}
