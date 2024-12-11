<script setup>
  import { ref, h, watch, nextTick, onMounted  } from 'vue'
  import { VueFlow, useVueFlow, Panel } from '@vue-flow/core'
  import { Background } from '@vue-flow/background'
  import { ControlButton, Controls } from '@vue-flow/controls'
  import { MiniMap } from '@vue-flow/minimap'
  import Icon from './VueFlow/Icon.vue'
  import PromptNode from './VueFlow/Nodes/PromptNode.vue'
  import ModelNode from './VueFlow/Nodes/ModelNode.vue'
  import ChainNode from './VueFlow/Nodes/ChainNode.vue'
  import VarNode from './VueFlow/Nodes/VarNode.vue'
  import VisualNode from './VueFlow/Nodes/VisualNode.vue'
  import WebSearchNode from './VueFlow/Nodes/WebSearchNode.vue'
  import Sidebar from './VueFlow/Sidebar.vue'
  import SaveAndUpload from './VueFlow/SaveAndUpload.vue'
  import useDragAndDrop from './VueFlow/useDnD.js'
  import { useDialog } from './VueFlow/DeleteDialog/useDialog.js'
  import Dialog from './VueFlow/DeleteDialog/Dialog.vue'
  import { useLayout } from './VueFlow/Layouting/useLayout.js'
  import { useRoute, onBeforeRouteLeave } from 'vue-router';

  const agentID = ref(-1)
  const nodes = ref([])
  const edges = ref([])

  const { onInit, onConnect, addEdges, setViewport, toObject, onNodesChange, onEdgesChange,
          applyNodeChanges, applyEdgeChanges, fitView, getNodes, getEdges, setNodes, setEdges} = useVueFlow()
  const { onDragOver, onDrop, onDragLeave } = useDragAndDrop()
  const dialog = useDialog()
  const route = useRoute();
  const lsKey = 'agents'
  
  const { layout } = useLayout()

  const dark = ref(false)

  const errorText = ref('')
    const snackbar = ref({
        show: false,
        color: "error",
        timeout: 5000,
    });

  onInit((vueFlowInstance) => {
    vueFlowInstance.fitView()
  })

  onConnect((connection) => {
    addEdges(connection)
  })

  onMounted(() => {
    const lsData = JSON.parse(localStorage.getItem(lsKey));
    for (let i = 0; i < lsData.length; i++) {
      if (lsData[i].to === route.path) {
        console.log("Nodes", lsData[i].nodes);
        console.log("Edges", lsData[i].edges);
        if (lsData[i].nodes !== null && lsData[i].edges !== null) {
          setNodes(lsData[i].nodes)
          setEdges(lsData[i].edges)
        }
        
        agentID.value = lsData[i].id
        break
      }
    }

    if (route?.query?.needLayouting) {
      setTimeout(() => layoutGraph('LR'), 200); 
      route.query.needLayouting = false
    }

    fitView()
  });

  onBeforeRouteLeave((to, from) => {
    const lsData = JSON.parse(localStorage.getItem(lsKey));
    if (lsData) {
      for (let i = 0; i < lsData.length; i++) {
        if (lsData[i].id === agentID.value) {
          lsData[i].nodes = getNodes.value
          lsData[i].edges = getEdges.value
          break
        }
      }
      localStorage.setItem(lsKey, JSON.stringify(lsData));
    }
  });

  watch(() => route.path, (newPath, oldPath) => {
    let lsData = JSON.parse(localStorage.getItem(lsKey));
    for (let i = 0; i < lsData.length; i++) {
      if (lsData[i].to === oldPath) {
        lsData[i].nodes = getNodes.value
        lsData[i].edges = getEdges.value
        break
      }
    }
    localStorage.setItem(lsKey, JSON.stringify(lsData));
    lsData = JSON.parse(localStorage.getItem(lsKey));
    for (let i = 0; i < lsData.length; i++) {
      if (lsData[i].to === newPath) {
        if (lsData[i].nodes !== null && lsData[i].edges !== null) {
          setNodes(lsData[i].nodes)
          setEdges(lsData[i].edges)
        }
        
        agentID.value = lsData[i].id
        fitView()
        break
      }
    }
  });

  function updatePos() {
    nodes.value = nodes.value.map((node) => {
      return {
        ...node,
        position: {
          x: Math.random() * 400,
          y: Math.random() * 400,
        },
      }
    })
  }

  function logToObject() {
    console.log(toObject())
  }

  function resetTransform() {
    setViewport({ x: 0, y: 0, zoom: 1 })
  }

  function toggleDarkMode() {
    dark.value = !dark.value
  }

  function dialogMsg(id) {
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
      [`Are you sure?`, h('br'), h('span', `[ELEMENT_ID: ${id}]`)],
    )
  }

   onNodesChange(async (changes) => {
    nodes.value = getNodes.value
    const edges = getEdges.value
    
    const nextChanges = []
    const edgesToRemove = []

    for (const change of changes) {
      if (change.type === 'remove') {
        const isConfirmed = await dialog.confirm(dialogMsg(change.id))

        if (isConfirmed) {
          nextChanges.push(change)
          
          const connectedEdges = edges.filter(edge => 
            edge.source === change.id || edge.target === change.id
          )
          
          edgesToRemove.push(...connectedEdges.map(edge => ({ id: edge.id, type: 'remove' })))
        }
      } else {
        nextChanges.push(change)
      }
    }

    applyNodeChanges(nextChanges)

    if (edgesToRemove.length > 0) {
      applyEdgeChanges(edgesToRemove)
    }
  })

  onEdgesChange(async (changes) => {
    edges.value = getEdges.value

    const nextChanges = []

    for (const change of changes) {
      if (change.type === 'remove') {
        const isConfirmed = await dialog.confirm(dialogMsg(change.id))

        if (isConfirmed) {
          nextChanges.push(change)
        }
      } else {
        nextChanges.push(change)
      }
    }

    applyEdgeChanges(nextChanges)
  })

  async function layoutGraph(direction) {
    nodes.value = layout(getNodes.value, getEdges.value, direction)

    nextTick(() => {
      fitView()
    })
  }

  function showSnackbar(text) {
    errorText.value = text
    snackbar.value.show = true
  }
</script>

<template>
  <div class="dnd-flow">
    <v-snackbar
      v-model="snackbar.show"
      class="snackbar-text"
      :timeout="snackbar.timeout"
      :color="snackbar.color"
    >
      Error: {{ errorText }}
    </v-snackbar>
    
    <VueFlow
    :nodes="nodes"
    :edges="edges"
      :class="{ dark }"
      class="basic-flow"
   
      :default-viewport="{ zoom: 1.5 }"
      :apply-default="false"
      :min-zoom="0.2"
      :max-zoom="4"
      @dragover="onDragOver" 
      @dragleave="onDragLeave"
      @drop="onDrop"
    >
      <SaveAndUpload
      @upload-short-graph="layoutGraph('LR')"/>
    
      <Background class='vue-flow__background' pattern-color="#aaa" :gap="16" />

      <template #node-prompt="props">
        <PromptNode 
          v-bind="props" 
          @input-template="v => props.data.template = v"/>
      </template>

      <template #node-model="props">
        <ModelNode 
          v-bind="props" 
          @input-temperature="v => props.data.temperature = v"
          @input-top_p="v => props.data.top_p = v"
          @input-max_tokens="v => props.data.max_tokens = v"
          @input-freq_penalty="v => props.data.freq_penalty = v"
          @input-pres_penalty="v => props.data.pres_penalty = v"
          @input-stop_seq="v => props.data.stop_seq = v"
          @input-api_key="v => props.data.api_key = v"/>
      </template>

      <template #node-chain="props">
        <ChainNode 
          v-bind="props"
          @input-snackbar="v => showSnackbar(v)"/>
      </template>

      <template #node-var="props">
        <VarNode 
          v-bind="props"
          @input-var="v => props.data.var = v"/>
      </template>

      <template #node-visual="props">
        <VisualNode 
          v-bind="props"/>
      </template>

       <template #node-websearch="props">
        <WebSearchNode 
          v-bind="props"
          @input-api_key="v => props.data.api_key = v"/>
      </template>

      <MiniMap />
      <Controls position="bottom-left">
        <ControlButton title="Reset Transform" @click="resetTransform">
          <Icon name="reset" />
        </ControlButton>

        <ControlButton title="Shuffle Node Positions" @click="updatePos">
          <Icon name="update" />
        </ControlButton>

        <ControlButton title="set horizontal layout" @click="layoutGraph('TB')">
          <Icon name="horizontal" />
        </ControlButton>

        <ControlButton title="set vertical layout" @click="layoutGraph('LR')">
          <Icon name="vertical" />
        </ControlButton>

        <ControlButton title="Toggle Dark Mode" @click="toggleDarkMode">
          <Icon v-if="dark" name="sun" />
          <Icon v-else name="moon" />
        </ControlButton>

        <ControlButton title="Log `toObject`" @click="logToObject">
          <Icon name="log" />
        </ControlButton>
      </Controls>
      <Dialog />
    </VueFlow>
    <Sidebar 
    :class="{ dark }"
    class="basic-flow"
    />
  </div>
</template>

<style>
/* import the necessary styles for Vue Flow to work */
@import '@vue-flow/core/dist/style.css';

/* import the default theme, this is optional but generally recommended */
@import '@vue-flow/core/dist/theme-default.css';

@import 'https://cdn.jsdelivr.net/npm/@vue-flow/core@1.38.5/dist/style.css';
@import 'https://cdn.jsdelivr.net/npm/@vue-flow/core@1.38.5/dist/theme-default.css';
@import 'https://cdn.jsdelivr.net/npm/@vue-flow/controls@latest/dist/style.css';
@import 'https://cdn.jsdelivr.net/npm/@vue-flow/minimap@latest/dist/style.css';
@import 'https://cdn.jsdelivr.net/npm/@vue-flow/node-resizer@latest/dist/style.css';


.button {
      transform-origin: top left;
      transform: translate(20%, 20%);
      width: 60px;
      height: 60px;
      background-color: #007bff;
      border-radius: 50%;
      box-shadow: 2px 2px 5px 1px rgba(0, 0, 0, 0.5);
    }
    
    .button svg {
        width: 24px;
        height: 24px;
        fill: none;
        stroke: white;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
        vertical-align: middle;
    }


  .vue-flow__node {
    background-color:#f3f4f6
  }

.vue-flow__edges path {
    stroke-width:2
}

.basic-flow {
  background-color:#edf2f7;
}

.basic-flow.dark .vue-flow__background {
  background:#2d3748;
}

.vue-flow__minimap {
  transform: scale(75%);
  transform-origin: bottom right;
}

.basic-flow.dark .vue-flow__minimap {
  background: #2d3748;
}

.basic-flow.dark .vue-flow__minimap-node {
  fill: #a4a4a4;
}

.basic-flow.dark .vue-flow__minimap-mask {
  fill: rgba(110, 110, 110, 0.6)
}

.basic-flow.dark {
    color:#fffffb;
}

.basic-flow.dark .vue-flow__node {
    background:#4a5568;
    color:#fffffb;
}

.basic-flow.dark .vue-flow__node.selected {
    background:#474765;
    box-shadow:0 0 0 2px #2563eb;
}

.basic-flow .vue-flow__controls {
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
    background: #FFFFFB;
}

.basic-flow.dark .vue-flow__controls {
    border:1px solid #FFFFFB;
    background: #333;
}

.vue-flow__controls {
    border: 1px solid rgba(185, 185, 185, 0.523);
    border-radius: 12px;
}

.basic-flow .vue-flow__controls .vue-flow__controls-button {
    border: 1px rgba(185, 185, 185, 0.523);
    border-radius: 12px;
}

.basic-flow .vue-flow__controls .vue-flow__controls-button svg{
    max-width: 200px;
    max-height: 200px;
    height: 100%;
    width: 100%;
}

.vue-flow__controls-button {
  width: 25px;
  height: 25px;
}

.basic-flow.dark .vue-flow__controls .vue-flow__controls-button {
    background:#333;
    fill:#fffffb;
    border: none;
}

.basic-flow.dark .vue-flow__controls .vue-flow__controls-button:hover {
    background:#4d4d4d
}

.basic-flow.dark .vue-flow__edge-textbg {
    fill:#292524
}

.basic-flow.dark .vue-flow__edge-text {
    fill:#fffffb
}

  .basic-flow .title {
    font-size: 13px;
    font-weight: bold;
    color: #333;
  }

  .basic-flow.dark .title {
    color: #fffffb;
  }
</style>