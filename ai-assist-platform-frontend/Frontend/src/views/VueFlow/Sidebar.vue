<script setup>
import useDragAndDrop from './useDnD'

const { onDragStart } = useDragAndDrop()
</script>

<template>
  <aside>
    <div class="description">You can drag these nodes to the pane.</div>

    <div class="nodes">
      <div class="mini_nodes mini_vue-flow__node-prompt" :draggable="true" @dragstart="onDragStart($event, 'prompt')">Prompt Node</div>

      <div class="mini_nodes mini_vue-flow__node-model" :draggable="true" @dragstart="onDragStart($event, 'model')">Model Node</div>

      <div class="mini_nodes mini_vue-flow__node-chain" :draggable="true" @dragstart="onDragStart($event, 'chain')">Chain Node</div>

      <div class="mini_nodes mini_vue-flow__node-var" :draggable="true" @dragstart="onDragStart($event, 'var')">Var Node</div>

      <div class="mini_nodes mini_vue-flow__node-visual" :draggable="true" @dragstart="onDragStart($event, 'visual')">Visual Node</div>

      <div class="mini_nodes mini_vue-flow__node-websearch" :draggable="true" @dragstart="onDragStart($event, 'websearch')">WebSearch Node</div>
    </div>
  </aside>
</template>

<style>
    .mini_vue-flow__node-input {
        color: var(--vf-node-text);
        background: var(--vf-node-bg);
        border-color: var(--vf-node-color, #0038b1);
        padding: 30px;
        border-radius: 10px;
        width: 250px;
        font-size: 20px;
        text-align: center;
        border-width: 3px; 
        border-style: solid;
    }

    .basic-flow.dark .mini_vue-flow__node-input,
    .basic-flow.dark .mini_vue-flow__node-default,
    .basic-flow.dark .mini_vue-flow__node-output,
    .basic-flow.dark .mini_vue-flow__node-custom,
    .basic-flow.dark .mini_vue-flow__node-operator,
    .basic-flow.dark .mini_vue-flow__node-result,
    .basic-flow.dark .mini_vue-flow__node-prompt,
    .basic-flow.dark .mini_vue-flow__node-model,
    .basic-flow.dark .mini_vue-flow__node-chain,
    .basic-flow.dark .mini_vue-flow__node-var,
    .basic-flow.dark .mini_vue-flow__node-visual,
    .basic-flow.dark .mini_vue-flow__node-websearch {
        color: white;
        background: #4a5568;
    }

    .mini_nodes {
        color: var(--vf-node-text);
        background: var(--vf-node-bg);
        padding: 30px;
        border-radius: 10px;
        width: 250px;
        font-size: 20px;
        text-align: center;
        border-width: 3px; 
        border-style: solid;
    }

    .mini_vue-flow__node-default.mini_nodes {
        border-color: var(--vf-node-color, #000000);
    }

    .mini_vue-flow__node-output.mini_nodes {
        border-color: var(--vf-node-color, #ff0072);
    }

    .mini_vue-flow__node-custom {
        border-color: var(--vf-node-color, #ec4899);
    }

    .mini_vue-flow__node-operator {
        border-color: var(--vf-node-color, #2563eb);
    }

    .mini_vue-flow__node-result {
        border-color: var(--vf-node-color, #7bffc3);
    }

    .mini_vue-flow__node-prompt,
    .mini_vue-flow__node-model,
    .mini_vue-flow__node-chain,
    .mini_vue-flow__node-var,
    .mini_vue-flow__node-visual,
    .mini_vue-flow__node-websearch {
        border-color: var(--vf-node-color, #8a00ad);
    }

    .dnd-flow {
        flex-direction:column;
        display:flex;
        height:100%
    }

    .dnd-flow aside {
        color:#fff;
        font-weight:700;
        padding:15px 0px 0px 10px;
        font-size:18px;
        background:#10b981bf;
        -webkit-box-shadow:0px 5px 10px 0px rgba(0,0,0,.3);
        box-shadow:0 5px 10px #0000004d;
        overflow: auto;
        min-width: 290px !important;
        height: calc(100vh - 90px);
    }

    .basic-flow.dark .dnd-flow aside {
        background:#10b981bf;
    }

    .dnd-flow aside .nodes>* {
        margin-bottom:10px;
        cursor:grab;
        font-weight:500;
        -webkit-box-shadow:5px 5px 10px 2px rgba(0,0,0,.25);
        box-shadow:5px 5px 10px 2px #00000040
    }

    .dnd-flow aside .description {
        margin-bottom:10px
    }

    .dnd-flow .vue-flow-wrapper {
        flex-grow:1;
        height:100%
    }

    @media screen and (min-width: 640px) {
        .dnd-flow {
            flex-direction:row
        }

        .dnd-flow aside {
            min-width:25%
        }
    }

    @media screen and (max-width: 639px) {
        .dnd-flow aside .nodes {
        display:flex;
        flex-direction:row;
        gap:5px;
    }
}
</style>