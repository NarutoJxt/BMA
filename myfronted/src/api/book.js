import request from '@/utils/request'
import {base_url} from "@/api/settings"
export function get_book_index_data(params) {
  return request({
    url: base_url + '/book/index/',
    params
  })
}
