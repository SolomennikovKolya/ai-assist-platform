<script setup>
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import TextAreaWithTitle from '../views/VueFlow/Components/TextAreaWithTitle.vue'
    import InputWithTitle from '../views/VueFlow/Components/InputWithTitle.vue'
    import createPage from './createPage.js'
    import axios from 'axios'

    const props = defineProps({
        text_for_agent: String,
        api_key: String,
    });

    const router = useRouter();
    const lsKey = 'agents'

    const textForAgent = ref('')
    const apiKey = ref('')

    const error = ref(null);
    const response = ref(null);

    const errorText = ref('')
    const snackbar = ref({
        show: false,
        color: "warning",
        timeout: 2000,
    });

    const sendPostGenerateGraph = async () => {
        if (textForAgent.value === '' || apiKey.value === '') {
            if (textForAgent.value === '') {
                errorText.value = 'Please enter the agent description!'
            } else {
                errorText.value = 'Please enter the api key!'
            }
            snackbar.value.timeout = 2000
            snackbar.value.color = "warning"
            snackbar.value.show = true;
            
            return
        }
        try {
            let wasError = false
            const jsonData = {
                agent_description: textForAgent,
                api_key: apiKey
            };

            console.log('отправили на сервер', jsonData);

            errorText.value = 'Successfully!'
            snackbar.value.color = "success"
            snackbar.value.timeout = 2000
            snackbar.value.show = true;
            
            setTimeout(() => { 
                if (!wasError) {
                    errorText.value = 'Loading...';
                    snackbar.value.timeout = -1;
                    snackbar.value.show = true;
                }
             }, 3000) 

            const result = await axios.post('http://127.0.0.1:5000/api/generate', jsonData, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            response.value = result.data;
            console.log('Ответ сервера:', response.value);
            const flow = response.value;

            for (const [element, text] of Object.entries(response.value)) {
                if (element === 'warning') {
                    errorText.value = 'Error: ' + text
                    snackbar.value.color = "error"
                    snackbar.value.timeout = 5000
                    snackbar.value.show = true;
                    wasError = true
                    throw new Error(text);
                }
            }

            flow.nodes.forEach(node => {
                node.position = {
                    x: 0,
                    y: 0
                };
            });
            const agentsData = localStorage.getItem(lsKey);
            const lsData = agentsData ? JSON.parse(agentsData) : null;
            createPage(lsData, flow.nodes, flow.edges, true, textForAgent.value, router, lsKey)
        } catch (err) {
            error.value = err;
            console.error('Ошибка при отправке запроса:', error.value);
        }
    }
</script>


<template>
    <div class="container-text-graph">
        <div class="text-h4">
            Creating an agent by description
        </div>
        <div class="textarea-container-text-graph">
        <TextAreaWithTitle 
            class="textAreaAgent"
            placeHolder='Введите описание агента
Например: "Агент по созданию анекдотов"'
            :rowsTA="4"  
            :value="textForAgent"
            @input="v => textForAgent = v"/>
        </div>
        <div class="text-h4" style="margin: 20px 0 10px;">
            API Key
        </div>
        <InputWithTitle 
            placeHolder="Введите API Key" 
            :value="apiKey"
            @input="v => apiKey = v"
            />

        <button 
            @click="sendPostGenerateGraph" class="generate-button"
            style="margin: 30px 0px 0">
                Generate graph
        </button>

        <v-snackbar
        v-model="snackbar.show"
        class="snackbar-text"
        :timeout="snackbar.timeout"
        :color="snackbar.color"
        variant="outlined"
        >
        <v-progress-circular
            v-if="errorText === 'Loading...'"
            color="success"
            :size="30"
            :width="4"
            indeterminate
        ></v-progress-circular>
        {{ errorText }}
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

    .container-text-graph .textarea-container-text-graph {
        width: 100%;
        max-width: 400px;
    }

    .textAreaAgent {
        text-align: center;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    .textAreaAgent .textarea-wrapper {
        width: 80vh;
        box-shadow: 0 0 10px #00000031;
    }

    .textAreaAgent .textarea-wrapper:focus-within {
        box-shadow: 0 0 10px #00000031;
    }

    .textAreaAgent .textarea-wrapper textarea {
        font-size: 20px;
        background: #dfdfdf; 
        scrollbar-width: auto;       
    }

    .container-text-graph .simple-input {
        font-size: 20px;
        width: 80vh;
        height: 40px;
        background: #dfdfdf;
        box-shadow: 0 0 10px #00000031;
    }

    .container-text-graph .generate-button {
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