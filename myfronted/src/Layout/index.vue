<template>
  <div class="main-container">
    <sidebar class="sidebar"></sidebar>
    <router-view class="main-body" ></router-view>
  </div>
</template>

<script>
import Sidebar from "@/Layout/componenet/sidebar";
export default {
  name: "index",
  components: {Sidebar},
}
</script>


<style lang="scss"  scoped>
.main-container{
  height: 100%;
}
.sidebar{
  width: 12%;
  height: 100%;
  padding: 0;
      &.mobile.openSidebar{
      position: fixed;
      top: 0;
    }
}
.main-body{
  position: absolute;left: 11%;top: 0;padding: 0;
  width: 88%;
  height: 100%;
}
</style>