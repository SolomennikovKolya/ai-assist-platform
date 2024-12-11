<script setup>
    import { ref  } from 'vue'
    import { Handle, Position, useVueFlow } from '@vue-flow/core'
    import axios from 'axios';

    const response = ref(null);
    const error = ref(null);

    const { getNodes, getEdges } = useVueFlow()   
    
    const props = defineProps({
      id: String,
      data: Object,
    });

    const emit = defineEmits(['input-snackbar']);

    function extractFieldsFromArray(array, fieldsToExtract) {
      return array.map(item => {
        const extractedItem = {};
        fieldsToExtract.forEach(field => {
          if (item.hasOwnProperty(field)) {
            extractedItem[field] = item[field];
          }
        });
        return extractedItem;
      });
    }

    const sendPostRequest = async () => {
      try {
        const fieldsForNodes = ['id', 'type', 'data'];
        const fieldsForEdges = ['id', 'source', 'target', 'sourceHandle', 'targetHandle'];

        const nodesToSend = extractFieldsFromArray(getNodes.value, fieldsForNodes);
        const edgesToSend = extractFieldsFromArray(getEdges.value, fieldsForEdges);

        const jsonData = {
          nodes: nodesToSend,
          edges: edgesToSend,
          startNodeID: props.id,
        };

        console.log('отправили на сервер', jsonData);

        const result = await axios.post('http://127.0.0.1:5000/api/start', jsonData, {
          headers: {
            'Content-Type': 'application/json'
          }
        });

        response.value = result.data;
        console.log('Ответ сервера:', response.value);
        for (const [nodeID, text] of Object.entries(response.value)) {
          if (nodeID === 'warning') {
            emit('input-snackbar', text)
            throw new Error(text);
          }
          FindVisualAndUpdate(nodeID, text); 
        }
      } catch (err) {
        error.value = err;
        console.error('Ошибка при отправке запроса:', error.value);
      }
    }

    function FindVisualAndUpdate(nodeID, text) {
      let id = nodeID

      getEdges.value.forEach(edge => {
        if (edge.source === id && edge.targetNode.type === 'visual') {
          edge.targetNode.data.text_to_visual = text
        }
      })
    }
</script>

<template>
  <div>
    <p class="title">CHAIN</p>

    <v-divider></v-divider>

    <div style="margin: 10px 0px 0px">
      <Handle type="target" style="position: inherit;transform: translate(-355%, 0);" :id="props.data.meta.targetModelID" :position="Position.Left" />
      <div class="title input-model">
        <div class="text-h5 text-border">Model</div>
      </div>
    </div>

    <div style="margin: 10px 0px 0px">
      <Handle type="target" style="position: inherit;transform: translate(-305%, 0);" :id="props.data.meta.targetPromptID" :position="Position.Left" />
      <div class="title input-prompt">
        <div class="text-h5 text-border">Prompt</div>
      </div>
    </div>

    <div style="margin: 10px 0px 0px">
      <Handle type="target" style="position: inherit;transform: translate(-385%, 0);" :id="props.data.meta.targetToolsID" :position="Position.Left" />
      <div class="title input-tools">
        <div class="text-h5 text-border">Tools</div>
      </div>
    </div>

    <button 
      @click="sendPostRequest" class="start-button"
      style="margin: 10px 0px 10px">
        Start
    </button>
    
    <v-divider></v-divider>

    <div>
      <div class="title output">
        <div class="text-h5 text-border">Output</div>
      </div>
      <Handle type="source" style="position: inherit; transform: translate(330%, 0);" :id="props.data.meta.sourceOutputID" :position="Position.Right" />
    </div>
  </div>   
</template>

<style>
  .vue-flow__node-chain .text-h5 {
    font-size: 16px !important;
  }

  .vue-flow__node-chain .text-border {
    padding: 5px 50px;
    border: 1px solid #ccc;
    border-radius: 8px;
    display: inline-block;
    box-shadow:0 0 5px #0000004d;
  }

  .vue-flow__node-chain .title {
    display: inline-block;
    align-items: center; 
    justify-content: center;
  }

  .vue-flow__node-chain .output {
    margin: 10px 0px 5px;
    transform: translate(3px, 0px);
  }

  .vue-flow__node-chain .input-model {
    transform: translate(-4px, 0px);
  }

  .vue-flow__node-chain .input-prompt {
    transform: translate(-4px, 0px);
  }

  .vue-flow__node-chain .input-tools {
    transform: translate(-4px, 0px);
  }

  .vue-flow__node-chain {
    text-align: center;
    gap:4px;
    padding:5px 6px;
    border-radius:8px;
    box-shadow:0 0 10px #0003;
    width: 202px;
  }

  .vue-flow__node-chain.selected {
    box-shadow:0 0 0 2px #8a00ad
  }

  .vue-flow__node-chain .vue-flow__handle {
    height:8px;
    width:8px;
    border-radius:4px;
    background-color:#8a00ad
  }

  .vue-flow__node-chain .vue-flow__handle-left {
    margin-top: 1px;
    display: inline-block;
  }

  .vue-flow__node-chain .vue-flow__handle-right {
    margin-top: 1px;
    display: inline-block;
  }

  .vue-flow__node-chain .start-button {
      border:none;
      cursor:pointer;
      background-color:#4a5568;
      border-radius:10px;
      color:#fff;
      box-shadow:0 0 5px #0000004d;
      width:160px;
      height:28px;
      font-size:13px;
  }
</style>
