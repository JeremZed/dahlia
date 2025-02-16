// src/App.vue
<template>
  <div id="app">
    <nav class="navbar">
      <router-link to="/">Accueil</router-link> |
      <router-link to="/about">À propos</router-link>
    </nav>
    <router-view />
  </div>
</template>

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