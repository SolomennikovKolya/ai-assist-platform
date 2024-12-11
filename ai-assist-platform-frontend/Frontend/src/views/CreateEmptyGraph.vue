<script setup>
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import InputWithTitle from '../views/VueFlow/Components/InputWithTitle.vue'
    import createPage from './createPage.js'

    const props = defineProps({
        text_for_agent: String,
        api_key: String,
    });

    const snackbar = ref({
        show: false
    });

    const agentName = ref('')
    const lsKey = 'agents'
    let lsData = null;
    const router = useRouter();

    function updateLsData() {
        const agentsData = localStorage.getItem(lsKey);
        lsData = agentsData ? JSON.parse(agentsData) : [];
    }

    window.addEventListener('storage', function(event) {
        if (event.key === lsKey) {
            updateLsData();
        }
    });

    updateLsData();

    function checkAndCreatePage() {
        if (agentName.value === '') {
            snackbar.value.show = true;
            return
        }
        createPage(lsData, null, null, false, agentName.value, router, lsKey)
    }
</script>


<template>
    <div class="container-text-graph">
        <div class="text-h4">
            Agent name
        </div>
        <InputWithTitle 
            placeHolder="Введите название агента" 
            :value="agentName"
            @input="v => agentName = v"
            />
            
        <button 
            @click="checkAndCreatePage" 
            class="create-button"
            style="margin: 30px 0px 0"
        >
                Create
        </button>

        <v-snackbar
        v-model="snackbar.show"
        class="snackbar-text"
        :timeout="2000"
        color="warning"
        variant="outlined"
        >
            Please enter the agent name!
        </v-snackbar>
    </div>
    
</template>

<style>
    .container-text-graph {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80vh;
        flex-direction: column;
    }

    .container-text-graph .text-h4 {
        margin-bottom: 20px;
    }

    .container-text-graph .simple-input {
        font-size: 20px;
        width: 80vh;
        height: 40px;
        background: #dfdfdf;
        box-shadow: 0 0 10px #00000031;
    }

    .container-text-graph .create-button {
        border:none;
        cursor:pointer;
        background-color:#4a5568;
        border-radius:20px;
        color:#fff;
        box-shadow:0 0 5px #0000004d;
        width:30vh;
        height:5vh;
        font-size:25px;
    }

    .snackbar-text .v-snackbar__content {
        font-size: 18px;
        text-align: center; 
    }
</style>