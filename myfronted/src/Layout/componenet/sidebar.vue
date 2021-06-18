<template>
  <div class="sidebar">
    <el-menu default-active="1-4-1"
             class="el-menu-vertical-demo sidebar"
             @open="handleOpen"
             @close="handleClose"
             :collapse="isCollapse"
             background-color="#545c64"
             text-color="#fff"
             active-text-color="black">
      <sidebar-item v-for="route in routes" :key="route.path" :item="route" :path="route.path"></sidebar-item>
    </el-menu>
  </div>
</template>

<script>
import SidebarItem from "@/Layout/componenet/sidebarItem";
export default {
  name: "sidebar",
  components: {SidebarItem},
  data() {
    return {
      isCollapse: false
    }
  },
  computed:{
    routes:function (){
     return this.$router.options.routes
    }
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    activeMenu() {
      this.isCollapse = !this.isCollapse
    }
  },

}
</script>

<style scoped>
.sidebar {
  width: 100%;
  height: 100%;
  padding: 0;
}
</style>