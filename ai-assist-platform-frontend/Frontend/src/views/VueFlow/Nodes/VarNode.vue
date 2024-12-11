<script setup>
  import { Handle, Position } from '@vue-flow/core'
  import TextAreaWithTitle from '../Components/TextAreaWithTitle.vue'

  const props = defineProps({
    id: String,
    data: Object,
  });
</script>

<template>
  <div>
    <p class="title">VAR</p>

    <v-divider></v-divider>
    <TextAreaWithTitle 
      placeHolder="Введите необходимые данные" 
      :rowsTA="4" 
      :colsTA="34" 
      :value="props.data.var"
      style="margin: 10px 0px 10px 0px"
      @input="v => $emit('input-var', v)"/>

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
  .vue-flow__node-var .text-h5 {
    font-size: 16px !important;
  }

  .vue-flow__node-var .text-border {
    padding: 5px 50px;
    border: 1px solid #ccc;
    border-radius: 8px;
    display: inline-block;
    box-shadow:0 0 5px #0000004d;
  }

  .vue-flow__node-var .output {
    display: inline-block;
    align-items: center; 
    justify-content: center;
    transform: translate(3px, 0px);
    margin: 10px 0px 5px;
  }

  .vue-flow__node-var .inline-block-text {
    display: inline-block;
    align-content: unset;
    font-size: 10px;
    position: relative;
    right: 12px;
  }

  .vue-flow__node-var .vue-flow__handle {
    height:8px;
    width:8px;
    border-radius:4px;
    background-color:#8a00ad
  }

  .vue-flow__node-var .vue-flow__handle-right {
    margin-top: 1px;
    transform: translate(330%, 0);
    display: inline-block;
  }

  .vue-flow__node-var {
    display:flex;
    align-items:center;
    text-align: center;
    gap:4px;
    padding:5px 6px;
    border-radius:8px;
    box-shadow:0 0 10px #0003;
  }

  .vue-flow__node-var.selected {
      box-shadow:0 0 0 2px #8a00ad
  }
</style>