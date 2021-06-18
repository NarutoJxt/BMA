<template>
  <div class="login-container">
    <el-form ref="registerForm" :show-message="showMessage" :rules="registerRules" :model="registerForm"
             class="login-form" autocomplete="on" label-position="left">
      <div class="title-container">
        <h3 class="title">Register Form</h3>
      </div>
      <el-form-item prop="username" :required="true" :error="unameError">
        <el-input
            v-model="registerForm.username"
            name="username"
            placeholder="username"
        >
        </el-input>
      </el-form-item>
      <el-form-item prop="email" :required="true" :error="emailError">
        <el-input
            v-model="registerForm.email"
            name="email"
            placeholder="email"
        >
        </el-input>
      </el-form-item>
      <el-form-item prop="password" :required="true" :error="pwdError">
        <el-input
            v-model="registerForm.password"
            name="password"
            placeholder="password"
            type="password"
        >
        </el-input>
      </el-form-item>
      <el-form-item prop="password1" :required="true" :error="pwd1Error">
        <el-input
            v-model="registerForm.password1"
            name="password1"
            placeholder="password1"
            type="password"
        >
        </el-input>
      </el-form-item>
      <span class="error">{{ otherError}}</span>
      <el-button type="primary" style="width:100%;margin-bottom:30px;" round v-on:click="register">注册</el-button>

    </el-form>

  </div>
</template>

<script>
import {register} from "@/api/user"
import cookie from "@/static/js/cookie"

export default {
  name: 'register',
  data() {
    return {
      showMessage: true,
      registerForm: {
        username: "",
        password: "",
        password1: "",
        email: ""
      },
      registerRules: {
        username: [{required: true, trigger: "blur"}],
        password: [{required: true, trigger: "blur"}],
        password1: [{required: true, trigger: "blur"}],
        email: [{required: true, trigger: "blur"}]
      },
      otherError:"",
      pwdError:"",
      unameError:"",
      emailError:"",
      pwd1Error:""
    }
  },
  methods: {
    register() {
      var that = this
      register(this.registerForm).then((response) => {
        var errors = response.data
        var token = errors.token
        if(token){
          cookie.setCookie("name",errors.name,7)
          cookie.setCookie("token",token,7)
          this.$router.push({name:"login"})
        }
      }).catch((errors) => {
        var error = errors.response.data
          that.otherError = error.non_field_errors?error.non_field_errors[0]:""
          that.pwdError = error.password?error.password[0]:""
          that.pwdError = error.password1?error.password1[0]:""
          that.unameError = error.username?error.username[0]:""
          that.emailError = error.email?error.email[0]:""
      })
    }
  }
}
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: #283443;
$light_gray: #fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

.error {
  color: orangered;
  position: relative;
  right: 220px;
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 100%;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }

  .thirdparty-button {
    position: absolute;
    right: 0;
    bottom: 6px;
  }

  .register-link {
    position: relative;
    right: 215px;
    bottom: 20px;
  }

  .password-find {
    position: relative;
    left: 200px;
    bottom: 20px;
  }

  @media only screen and (max-width: 470px) {
    .thirdparty-button {
      display: none;
    }
  }
}
</style>
