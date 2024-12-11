<script setup>
  import { ref, h } from 'vue';
  import { useRouter } from 'vue-router';
  import { useDialog } from './views/VueFlow/DeleteDialog/useDialog.js'

  const drawer = ref(false);
  const isDarkMode = ref(false);
  const router = useRouter();
  const dialog = useDialog()

  const items = [
    { title: 'Create empty Agent', to: '/create_empty_graph' },
    { title: 'Create Agent based on text', to: '/create_text_graph' },
  ];

  const lsKey = 'agents'
  let lsData = localStorage.getItem(lsKey);

  function updateLsData() {
    lsData = JSON.parse(localStorage.getItem(lsKey));
  }

  updateLsData();

  const checkInterval = 500;
  let lastStoredValue = lsData;

  function checkLocalStorage() {
      const currentStoredValue = localStorage.getItem(lsKey);
      if (currentStoredValue !== lastStoredValue) {
          lastStoredValue = currentStoredValue;
          updateLsData();
      }
  }

  setInterval(checkLocalStorage, checkInterval);

  function dialogMsg(name) {
    return h(
      'span',
      {
        style: {
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '8px',
        },
      },
      [`Are you sure?`, h('br'), h('span', `Agent: ${name}`)],
    )
  }

  async function  deleteAgent(agent) {
    const agentID = agent.id    
    const isConfirmed = await dialog.confirm(dialogMsg(agent.title))

    if (isConfirmed) {
      updateLsData()
      if (lsData) {
        const index = lsData.findIndex(agent => agent.id === agentID);

        if (index !== -1) {
            lsData.splice(index, 1);
        }
        localStorage.setItem(lsKey, JSON.stringify(lsData));
      }
      setTimeout(() => { router.push('/create_empty_graph'); }, 200) //dirty hack
      // location.href = '/create_empty_graph'
    }
  }
  
</script>

<template>
  <v-app id="inspire" :class="{'dark-mode': isDarkMode}">
    <v-navigation-drawer v-model="drawer" :class="{'dark-drawer': isDarkMode}" >
      <v-list-item>
        <v-list-item-title class="text-h6">
          Assistants
        </v-list-item-title>
      </v-list-item>

      <v-divider></v-divider>

      <v-list nav>
        <div v-for="item in items" :key="item.title">
          <v-list-item prepend-icon='mdi-pencil' :title="item.title" :to="item.to"></v-list-item>
        </div>
      </v-list>

      <v-divider></v-divider>

      <v-list nav>
        <div v-for="agent in lsData" :key="agent.id">
          <v-list-item prepend-icon='mdi-chat' :title="agent.title" :to="agent.to">
            <template v-slot:append>
              <v-icon @click="deleteAgent(agent)" class="ml-2">mdi-close</v-icon>
            </template>
          </v-list-item>
        </div>
      </v-list>

    </v-navigation-drawer>

    <v-app-bar
      color="#e5c2af"
      dark
      height="90"
      style="background-image: url('mountains.jpg'); background-size: cover; background-position: center;"
    >
      <template v-slot:img="{ props }">
      <v-img
      v-bind="props"
      ></v-img>
      </template>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>AI-Assist Platform</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-show="!isDarkMode" @click="isDarkMode = !isDarkMode" icon>
        <v-icon>mdi-weather-night</v-icon>
      </v-btn>
      <v-btn v-show="isDarkMode" @click="isDarkMode = !isDarkMode" icon>
        <v-icon>mdi-weather-sunny</v-icon>
      </v-btn>
    </v-app-bar>

    

    <v-main>
      <router-view :isDarkMode="isDarkMode"></router-view> 
    </v-main>
  </v-app>
</template>

<style>
  .dark-mode {
    background-color: #333;
    color: #dddddd;
  }
  .dark-drawer {
    background-color: #1d1d1d;
    color: #fff;
  }
  
  pre {
    background: #f5f5f5;
    padding: 1em;
    border-radius: 5px;
    overflow: auto;
  }

  code {
    background: #f5f5f5;
    padding: 0.2em 0.4em;
    border-radius: 3px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
  }

  table, th, td {
    border: 1px solid #ddd;
  }

  th, td {
    padding: 0.5em;
    text-align: left;
  }

  ul, ol {
    margin: 1em 0;
    padding-left: 1.5em;
  }

  blockquote {
    margin: 1em 0;
    padding: 0.5em 1em;
    border-left: 3px solid #ccc;
    background: #f9f9f9;
  }
  
  .v-list-item__prepend {
    width: 30px;
  }

  .v-list-item {
    border-radius: 20px;
  }

</style>