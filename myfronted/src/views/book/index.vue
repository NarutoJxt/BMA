<template>
  <el-container direction="vertical" class="book-header">
    <el-header>
      <h3>藏书阁</h3>
      <el-menu
          :default-active="activeIndex2"
          class="el-menu-demo "
          mode="horizontal"
          @select="handleSelect"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b">
        <el-menu-item index="1">
          <el-link href="/dashboard">
            首页
          </el-link>
        </el-menu-item>
        <el-submenu index="2">
          <template slot="title">我的工作台</template>
          <el-menu-item index="2-1">选项1</el-menu-item>
          <el-menu-item index="2-2">选项2</el-menu-item>
          <el-menu-item index="2-3">选项3</el-menu-item>
          <el-submenu index="2-4">
            <template slot="title">选项4</template>
            <el-menu-item index="2-4-1">选项1</el-menu-item>
            <el-menu-item index="2-4-2">选项2</el-menu-item>
            <el-menu-item index="2-4-3">选项3</el-menu-item>
          </el-submenu>
        </el-submenu>
        <el-menu-item index="3" disabled>消息中心</el-menu-item>
        <el-menu-item index="4"><a href="https://www.ele.me" target="_blank">订单管理</a></el-menu-item>
      </el-menu>
    </el-header>
    <el-main class="main-container">

    </el-main>

  </el-container>
</template>

<script>
import {get_book_index_data} from "@/api/book";

export default {
  name: "index",
  data(){
    return {
      book_data:[],
            activeIndex: '1',
        activeIndex2: '1'
    }
  },
  created() {
    this.get_index_data()
  },
  methods:{
    get_index_data(){
      get_book_index_data().then((response)=>{
        this.book_data = response.data;
        console.log(this.book_data)
      })
    },
     handleSelect(key, keyPath) {
        console.log(key, keyPath);
      }
  }
}
</script>

<style scoped>
.book-header {
  width: 100%;
  height: 100%;
}
.main-container{
  position: relative;
  margin-top: 48px;
  left: 10%;
  width: 70%;
}

.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
}
  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }
</style>