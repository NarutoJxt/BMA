import router from "./router"
const {getToken} = require("@/utils/auth");
const whiteList = ["/login","/register"]
router.beforeEach((to, from, next) => {
  var hasToken = getToken()
    if(hasToken){
        next()
    }else {
        if(whiteList.indexOf(to.path) === -1 ){
            next({path:"/login"})
        }
        else {
            next()
        }
    }
})
