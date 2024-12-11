<script setup>
    import { computed, ref, watch, onMounted  } from 'vue'
    import { Handle, Position, useVueFlow } from '@vue-flow/core'
    import Slider from '../Components/Slider.vue'
    import InputWithTitle from '../Components/InputWithTitle.vue'

    const props = defineProps({
      id: String,
      data: Object,
    });

    const { updateNodeData } = useVueFlow()   
</script>

<template>
  <div>
    <p class="title">MODEL</p>

    <v-divider></v-divider>

    <InputWithTitle 
      title="API key" 
      placeHolder="Введите API key" 
      :value="props.data.api_key" 
      style="margin: 5px 0px 10px 0px"
      @input="v => $emit('input-api_key', v)"/>
    <div style="margin: 5px 0px 0px 0px">
      <div class="text-h5">Model Name</div>
    </div>
    <div class="custom-select" style="margin: 0px 0px 20px 0px;">
      <select v-model="props.data.model_name" name="Model">
        <option value="gpt-4o-mini">gpt-4o-mini</option>
        <option value="gpt-4o">gpt-4o</option>
        <option value="gpt-4-turbo">gpt-4-turbo</option>
        <option value="gpt-4">gpt-4</option>
        <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
      </select>
    </div>

    <v-expansion-panels style="margin: 2px 0px 10px 0px">
      <v-expansion-panel>
        <v-expansion-panel-title>
          Model settings
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <Slider 
            title="Temperature" 
            :min="0" 
            :max="2" 
            :numberFixed="2"
            :value="props.data.temperature" 
            @input="v => $emit('input-temperature', v)"/>
          <Slider 
            title="Top p" 
            :min="0" 
            :max="1" 
            :numberFixed="2"
            :value="props.data.top_p"
            @input="v => $emit('input-top_p', v)"/>
          <Slider 
            title="Max Tokens" 
            :min="1" 
            :max="8000"  
            :numberFixed="0"
            :value="props.data.max_tokens"
            @input="v => $emit('input-max_tokens', v)"/>

          <InputWithTitle 
            title="Stop sequences" 
            placeHolder="" 
            :value="props.data.stop_seq"
            style="margin: 0px 15px; width: 160px"
            @input="v => $emit('input-stop_seq', v)"/>

          <Slider 
            title="Frequency penalty" 
            :min="0" 
            :max="2" 
            :numberFixed="2"
            :value="props.data.freq_penalty"
            @input="v => $emit('input-freq_penalty', v)"/>
          <Slider 
            title="Presence penalty" 
            :min="0" 
            :max="2" 
            :numberFixed="2"
            :value="props.data.pres_penalty"
            @input="v => $emit('input-pres_penalty', v)"/>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

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
  .vue-flow__node-model .text-h5 {
    font-size: 16px !important;
  }

  .vue-flow__node-model .text-border {
    padding: 5px 50px;
    border: 1px solid #ccc;
    border-radius: 8px;
    display: inline-block;
    box-shadow:0 0 5px #0000004d;
  }

  .vue-flow__node-model .output {
    display: inline-block;
    align-items: center; 
    justify-content: center;
    transform: translate(3px, 0px);
    margin: 10px 0px 5px;
  }

  .vue-flow__node-model {
    display:flex;
    align-items:center;
    text-align: center;
    gap:4px;
    padding:5px 6px;
    border-radius:8px;
    box-shadow:0 0 10px #0003;
  }

  .vue-flow__node-model.selected {
    box-shadow:0 0 0 2px #8a00ad
  }

  .vue-flow__node-model .v-expansion-panel-title {
    padding: 8px;
    min-height: 20px;
    font-size: 13px;
  }

  .vue-flow__node-model .v-expansion-panel {
    box-shadow:0px 2px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.089)), 0 0 5px #00000031;
    border-radius: 10px;
    min-height: 20px;
    background-color:#f3f4f6;
  }

  .basic-flow.dark .vue-flow__node-model .v-expansion-panel {
    background-color:#4a5568;
    color: #fffffb;
  }

  .vue-flow__node-model .v-expansion-panel--active > .v-expansion-panel-title:not(.v-expansion-panel-title--static) {
    min-height: 20px;
  }

  .vue-flow__node-model .vue-flow__handle {
    height:8px;
    width:8px;
    border-radius:4px;
    background-color:#8a00ad
  }

  .vue-flow__node-model .vue-flow__handle-right {
    margin-top: 1px;
    transform: translate(330%, 0);
    display: inline-block;
  }

  .vue-flow__node-model .v-expansion-panel-text__wrapper {
    padding: 5px 0px;
  }
  
  .vue-flow__node-model .v-field__field {
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
