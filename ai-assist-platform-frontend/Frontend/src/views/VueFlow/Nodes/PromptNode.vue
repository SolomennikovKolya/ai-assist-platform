<script setup>
  import { Handle, Position } from '@vue-flow/core'
  import TextAreaWithTitle from '../Components/TextAreaWithTitle.vue'

  const props = defineProps({
    id: String,
    data: Object,
  });

  function addPromptValue() {
    let hash = crypto.randomUUID()
    let idTarget = `${hash}`
    props.data.prompt_values[idTarget] = { id: idTarget, name: '', value: ''};
    props.data.meta[idTarget] = hash;
  }

  function deletePromptValue(id) {
    delete props.data.prompt_values[id];
    delete props.data.meta[id];
  }

</script>

<template>
  <div>
    <p class="title">PROMPT</p>

    <v-divider></v-divider>
    <TextAreaWithTitle 
      title="Template" 
      placeHolder="Введите шаблон промта" 
      :rowsTA="4" 
      :colsTA="34" 
      style="margin: 5px 0px 15px 0px"
      :value="props.data.template"
      @input="v => $emit('input-template', v)"/>

    <div style="margin: 5px 0px 2px 0px">
      <div class="text-h5">Prompt Values</div>
    </div>
    <div>
        <button @click="addPromptValue" class="add-button">
          Add value
        </button>
    </div>
    
    <div v-if="(Object.keys(props.data.prompt_values)).length > 0">
      <p class="inline-block-text" style="margin: 0 30px 0 0;">Name</p>
      <p class="inline-block-text" style="margin: 0 0 0 40px;">Value</p>
    </div>
    <div v-for="promptValue in props.data.prompt_values" :key="promptValue.id">
      <Handle 
        :id="`${promptValue.id}`"   
        type="target" 
        style="position:inherit" 
        :position="Position.Left" />
      <input 
        class="small-input" 
        :id="`input-key-${promptValue.id}`" 
        v-model="promptValue.name" 
        style="margin: 0 2px 6px 0;"/>
      -
      <input 
        class="small-input" 
        :id="`input-value-${promptValue.id}`" 
        v-model="promptValue.value" 
        style="margin: 0 0 6px 2px;" />
      <v-btn 
      @click.stop="deletePromptValue(promptValue.id)" 
      icon="mdi-delete" 
      size="small"
      class="v-button"></v-btn>
    </div>

    <v-divider style="margin: 10px 0px 0px 0px"></v-divider>

    <div>
      <div class="output">
        <div class="text-h5 text-border">Output</div>
        
      </div>
      <Handle type="source" style="position: inherit;" :id="props.data.meta.sourceOutputID" :position="Position.Right" />
    </div>
  </div>
</template>

<style>
  .vue-flow__node-prompt .text-h5 {
    font-size: 16px !important;
  }

  .vue-flow__node-prompt .text-border {
    padding: 5px 50px;
    border: 1px solid #ccc;
    border-radius: 8px;
    display: inline-block;
    box-shadow:0 0 5px #0000004d;
  }

  .vue-flow__node-prompt .output {
    display: inline-block;
    align-items: center; 
    justify-content: center;
    transform: translate(3px, 0px);
    margin: 10px 0px 5px;
  }

  .vue-flow__node-prompt .inline-block-text {
    display: inline-block;
    align-content: unset;
    font-size: 10px;
    position: relative;
    right: 12px;
  }

  .vue-flow__node-prompt .vue-flow__handle {
    height:8px;
    width:8px;
    border-radius:4px;
    background-color:#8a00ad
  }

  .vue-flow__node-prompt .vue-flow__handle-right {
    margin-top: 1px;
    transform: translate(330%, 0);
    display: inline-block;
  }

  .vue-flow__node-prompt .vue-flow__handle-left {
    margin-right: -20px;
    transform: translate(-125%, 100%);
    float:left;
  }

  .vue-flow__node-prompt {
    display:flex;
    align-items:center;
    text-align: center;
    gap:4px;
    padding:5px 6px;
    border-radius:8px;
    box-shadow:0 0 10px #0003;
  }

  .vue-flow__node-prompt.selected {
      box-shadow:0 0 0 2px #8a00ad
  }

  .vue-flow__node-prompt .small-input {
      font-size: 10px;
      width: 75px;
      height: 20px;
      flex:1;
      padding:4px 5px;
      border:none;
      border-radius:8px;
      box-shadow:0 0 5px #00000031;
      background: #f9f9f9;
  }

  .vue-flow__node-prompt .small-input:focus {
      outline:none;
      box-shadow:0 0 0 1px #8a00ad;
      transition:box-shadow .2s
  }

  .basic-flow.dark .vue-flow__node-prompt .small-input {
    background:#60638d;
    color: #fffffb;
  }

  .vue-flow__node-prompt .add-button {
      border:none;
      cursor:pointer;
      background-color:#4a5568;
      border-radius:10px;
      color:#fff;
      box-shadow:0 0 5px #0000004d;
      width:160px;
      height:28px;
      font-size:12px;
  }

  .vue-flow__node-prompt .v-button {
    margin: 0 0 0 4px;
    width: 20px;
    height: 20px;
    background-color: #4a5568;
  }

  .vue-flow__node-prompt .v-btn__content {
    color: rgb(255, 255, 255);
  }

  .vue-flow__node-prompt .v-btn--icon .v-icon {
    --v-icon-size-multiplier: 0.75;
    font-size: var(--v-icon-size-multiplier);
  }
</style>