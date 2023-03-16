<template>
  <!-- <div id="nav"></div> -->
  <router-view/>
</template>

<script>
import {reactive} from "vue"
//import firebase from "firebase/app"

const store = {
  state: reactive({
    username: "Guest",
    uid: "",
    inQueue: false,
    apiKey: "",
  })
}

export default {
  name: 'App',
  provide: {
      store
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>


