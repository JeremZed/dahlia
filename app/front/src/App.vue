<template>
  <div id="app">
    <nav class="navbar">
      <router-link to="/">Accueil</router-link> |
      <router-link to="/about">À propos</router-link>
    </nav>
    <div>
      <h2>Mises à jour du monde :</h2>
      <ul>
        <li v-for="(msg, index) in messages" :key="index">
          {{ msg }}
        </li>
      </ul>
    </div>
    <router-view />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import useWebSocket from './components/useWebSocket';

let is_ssl = process.env.FASTAPI_SSL_ENABLED
let host = process.env.FASTAPI_IP
let port = process.env.FASTAPI_PORT

let protocol = 'ws'
if(is_ssl == 'true'){
  protocol = 'wss'
}

let url = ""+protocol+"://"+host+":"+port+"/ws"
console.log("url : ", url)
const { sendMessage, messages } = useWebSocket(url);

function moveEntity(entity) {
  sendMessage({ entity, action: "move" });
}

// Simulation d'un déplacement toutes les 3 secondes
setInterval(() => {
  moveEntity("bot1");
}, 3000);
</script>

<style>
.navbar {
  padding: 20px;
  background-color: #f8f9fa;
}
.navbar a {
  margin: 0 10px;
  text-decoration: none;
  color: #2c3e50;
}
.navbar a.router-link-active {
  color: #42b983;
}
</style>
