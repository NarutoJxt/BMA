<template>
  <div v-if="!item.hidden">
    <el-menu-item v-if="checkChild(item.children,item) && (!onlyOneChild.children || onlyOneChild.noShowingChildren) && !item.alwaysShow" :index="item.path" >
      <el-link :href="item.path" style="color: white" :icon="item.icon">{{ item.name }}</el-link>
    </el-menu-item>
    <el-submenu v-else :index="item.path">
      <template slot="title" >
          <el-link :href="item.path" style="color: white" :icon="item.icon">{{ item.name }}</el-link>
      </template>
        <sidebar-item
            v-for="route in item.children" :key="route.padding" :item="route" :path="route.path"
        ></sidebar-item>
    </el-submenu>
  </div>

</template>

<script>
export default {
name: "sidebarItem",
  props:{
    item:{},
    path:null
  },
  methods:{
    checkChild(itemChildren=[],item){
        const showingChildren = itemChildren.filter(item=>{
          if(item.hidden){
            return false
          }else {
            this.onlyOneChild = item
            return true
          }
        })
      if(showingChildren.length === 1){
        return true
      }
      if(showingChildren.length === 0){
        this.onlyOneChild = {...item,path:"",noShowingChildren: true}
        return true
      }
    },
  }
}
</script>

<style scoped>

</style>