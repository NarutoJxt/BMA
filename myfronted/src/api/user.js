import {base_url} from "@/api/settings";
import axios from "axios"
export function login(params){
    var res = axios.post(
        base_url + "/login/",
        params
    )
    return res
}
export function register(params){
    return axios.post(
        base_url + "/register/",
        params
    )
}
