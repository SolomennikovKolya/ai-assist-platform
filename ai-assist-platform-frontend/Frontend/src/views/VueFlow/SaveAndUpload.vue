<script setup>
    import { ref } from 'vue'
    import { Panel, useVueFlow } from '@vue-flow/core'
    import Icon from './Icon.vue'
    import { saveAs } from 'file-saver';

    const flowKey = 'vue-flow--save-upload'

    const emit = defineEmits(['upload-short-graph']);

    const { toObject, fromObject, getNodes, setNodes} = useVueFlow()
    
    const fileInput = ref(null);

    function onSaveLS() {
        localStorage.setItem(flowKey, JSON.stringify(toObject()))
    }

    function onSaveFile() {
        const fileContent = JSON.stringify(toObject());
        const blob = new Blob([fileContent], { type: 'text/plain;charset=utf-8' });
        saveAs(blob, 'Your Nodes.json');
    };

    function onUploadLS() {
        const flow = JSON.parse(localStorage.getItem(flowKey))
        if (flow) {
            fromObject(flow)
        }
    }

    function onUploadFile() {
        fileInput.value.click();
    }

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = (e) => {
                const fileContent = e.target.result;
                const flow = JSON.parse(fileContent);
                if (flow) {
                    fromObject(flow)
                } else {
                    console.log("Ошибка загрузки файла: Неверный формат данных");
                }
            };

            reader.readAsText(file);
        } else {
            console.log("Ошибка загрузки файла: Не удалось загрузить файл");
        }
    };
</script>

<template>
  <Panel position="top-left">
    <div class="buttons">
      <button title="Save to localstorage" @click="onSaveLS">
        <Icon name="save-to-ls" />
      </button>
      <button title="Save to file" @click="onSaveFile">
        <Icon name="save-to-file" />
      </button>
      <button title="Upload from localstorage" @click="onUploadLS">
        <Icon name="upload-from-ls" />
      </button>
      <button title="Upload from file" @click="onUploadFile">
        <Icon name="upload-from-file" />
      </button>
      <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none" />
    </div>
  </Panel>
</template>

<style scoped>
    .vue-flow__panel {
        background-color:#2d3748;
        padding: 8px;
        border-radius:8px;
        box-shadow:0 0 10px #00000080
    }

    .basic-flow.dark .vue-flow__panel {
        background-color:#38444d;
    }

    .vue-flow__panel .buttons {
        display:flex;
        gap:8px
    }

    .vue-flow__panel button {
        border:none;
        cursor:pointer;
        background-color:#4a5568;
        border-radius:8px;
        color:#fff;
        box-shadow:0 0 10px #0000004d;
        width:40px;
        height:40px;
        font-size:16px;
        display:flex;
        align-items:center;
        justify-content:center
    }

    .basic-flow.dark .vue-flow__panel button {
        background-color: #60638d;
    }

    .vue-flow__panel button:hover {
        background-color:#2563eb;
        transition:background-color .2s
    }

    .basic-flow.dark .vue-flow__panel button:hover {
        background-color:#8a00ad;
        transition:background-color .2s
    }

    .vue-flow__panel button svg {
        width:100%;
        height:100%
    }
</style>