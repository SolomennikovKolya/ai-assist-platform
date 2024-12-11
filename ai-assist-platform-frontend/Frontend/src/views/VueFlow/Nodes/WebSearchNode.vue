<script setup>
    import { Handle, Position } from '@vue-flow/core'
    import InputWithTitle from '../Components/InputWithTitle.vue'

    const props = defineProps({
      id: String,
      data: Object,
    });
</script>

<template>
  <div>
    <p class="title">WEB SEARCH</p>

    <v-divider></v-divider>

    <InputWithTitle 
      title="API key" 
      placeHolder="Введите API key" 
      :value="props.data.api_key" 
      style="margin: 5px 0px 10px 0px"
      @input="v => $emit('input-api_key', v)"/>

    <v-divider></v-divider>

    <div>
      <div class="output">
        <div class="text-h5 text-border">Output</div>
        
      </div>
      <Handle type="source" style="position: inherit;" :id="props.data.meta.sourceOutputID" :position="Position.Right" />
    </div>
  </div>   
</template>

<style>
  .vue-flow__node-websearch .text-h5 {
    font-size: 16px !important;
  }

  .vue-flow__node-websearch .text-border {
    padding: 5px 50px;
    border: 1px solid #ccc;
    border-radius: 8px;
    display: inline-block;
    box-shadow:0 0 5px #0000004d;
  }

  .vue-flow__node-websearch .output {
    display: inline-block;
    align-items: center; 
    justify-content: center;
    transform: translate(3px, 0px);
    margin: 10px 0px 5px;
  }

  .vue-flow__node-websearch {
    display:flex;
    align-items:center;
    text-align: center;
    gap:4px;
    padding:5px 6px;
    border-radius:8px;
    box-shadow:0 0 10px #0003;
  }

  .vue-flow__node-websearch.selected {
    box-shadow:0 0 0 2px #8a00ad
  }

  .vue-flow__node-websearch .v-expansion-panel-title {
    padding: 8px;
    min-height: 20px;
    font-size: 13px;
  }

  .vue-flow__node-websearch .v-expansion-panel {
    box-shadow:0px 2px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.089)), 0 0 5px #00000031;
    border-radius: 10px;
    min-height: 20px;
    background-color:#f3f4f6;
  }

  .basic-flow.dark .vue-flow__node-websearch .v-expansion-panel {
    background-color:#4a5568;
    color: #fffffb;
  }

  .vue-flow__node-websearch .v-expansion-panel--active > .v-expansion-panel-title:not(.v-expansion-panel-title--static) {
    min-height: 20px;
  }

  .vue-flow__node-websearch .vue-flow__handle {
    height:8px;
    width:8px;
    border-radius:4px;
    background-color:#8a00ad
  }

  .vue-flow__node-websearch .vue-flow__handle-right {
    margin-top: 1px;
    transform: translate(330%, 0);
    display: inline-block;
  }

  .vue-flow__node-websearch .v-expansion-panel-text__wrapper {
    padding: 5px 0px;
  }
  
  .vue-flow__node-websearch .v-field__field {
    min-height: 10px;
    height: 10px;
  }

  .v-label.v-field-label {
    margin-inline-start: 6px;
    font-size: 10px;
  }

  .custom-select {
    position: relative;
    display: inline-block;
  }

  .custom-select select {
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    background-color: #fbfbfb;
    padding: 0px 0px 0px 8px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 11px;
    height: 24px;
    width: 190px;
    outline: none;
    box-shadow:0 0 5px #00000031
  }

  .basic-flow.dark .custom-select select{
    background-color: #60638d;
    color: white;
  }

  .custom-select select:focus {
    outline: 1px solid #8a00ad;
  }

  .basic-flow.dark .custom-select select:focus {
    outline: 1px solid #2563eb;
  }

  .custom-select option {
    font-size: 30px;
    padding: 12px;
  }

  .basic-flow.dark .custom-select option {
    color: white;
  }

  .custom-select::after {
    content: '\25BC';
    font-size: 15px;
    color: #343434;
    position: absolute;
    top: 50%;
    right: 8px;
    transform: translateY(-45%);
    pointer-events: none;
  }

  .basic-flow.dark .custom-select::after{
    color: #afafaf;
  }
</style>
