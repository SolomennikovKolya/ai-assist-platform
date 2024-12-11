<script setup>
    import { computed } from 'vue'
    import { Handle, Position } from '@vue-flow/core'
    import MarkdownIt from 'markdown-it';
    import markdownItKatexGpt from 'markdown-it-katex-gpt'
    import { VueMermaidRender } from 'vue-mermaid-render'

    const props = defineProps({
        id: String,
        data: Object,
    });

    const md = new MarkdownIt({ 
      html: true,
      linkify: true,
      typographer: true 
    });
    md.use(markdownItKatexGpt)

    let arrTexts = computed(() => {
        let parts = props.data.text_to_visual.split('\`\`\`mermaid\n')

        let result = [];
        for (let i = 0; i < parts.length; i++) {
            if (i === 0) {
                result.push(parts[i].trim());
            } else {
                let subparts = parts[i].split('\`\`\`');
                result.push(subparts);
            }
        }

        return result.flat()
    })
</script>

<template>
  <div>
    <div class="container">
      <p class="title">VISUAL</p>
        <v-dialog>
          <template v-slot:activator="{ props: activatorProps }">
            <v-btn 
              v-bind="activatorProps"
              icon="mdi-fullscreen" 
              size="small"
              class="v-button"
            ></v-btn>
          </template>

          <template v-slot:default="{ isActive }">
            <v-card>
              <div style="padding: 15px; font-size: 18px;">
                  <div v-for="(text, index) in arrTexts" :key="index">
                      <div v-if="(index % 2) === 0" v-html="md.render(text)" />
                      <VueMermaidRender v-else :content="text" />
                  </div>
              </div>
              <template v-slot:actions>
                <v-btn
                  class="close-button"
                  text="Close"
                  @click="isActive.value = false"
                ></v-btn>
              </template>
            </v-card>
          </template>
        </v-dialog>
    </div>

    <v-divider></v-divider>
    <div class="text-border">
        <Handle type="target" :id="props.data.meta.targetInputID" :position="Position.Left" />
        <div>
          <div v-for="(text, index) in arrTexts" :key="index">
              <div v-if="(index % 2) === 0" v-html="md.render(text)" />
              <VueMermaidRender v-else :content="text" />
          </div>
        </div>
    </div>
  </div>
</template>

<style>
  .vue-flow__node-visual .text-h5 {
    font-size: 16px !important;
  }

  .vue-flow__node-visual .text-border {
    overflow: hidden;
    padding: 5px 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow:0 0 5px #0000004d;
    margin: 10px 5px;
    font-size: 10px;
    min-height: 60px;
    max-height: 200px;
    background: #f9f9f9;
  }

  .basic-flow.dark .vue-flow__node-visual .text-border {
    background:#60638d;
    border: none;
  }

  .full-screen {
    padding: 10px;
    border: 1px solid #ccc;
    box-shadow:0 0 5px #0000004d;
    margin: 10px 5px;
    min-height: 60px;
    font-size: 18px;
  }

  .basic-flow.dark .full-screen {
    background:#60638d;
    color: #ffffff;
  }

  .vue-flow__node-visual .title {
    margin: 0px 0px 0px 20px;
    flex-grow: 1;
    text-align: center;
  }

  .vue-flow__node-visual .input {
    display: inline-block;
    align-items: center; 
    justify-content: center;
  }

  .vue-flow__node-visual .vue-flow__handle {
    height:8px;
    width:8px;
    border-radius:4px;
    background-color:#8a00ad
  }

  .vue-flow__node-visual .vue-flow__handle-left {
    top:68px;
  }

  .vue-flow__node-visual {
    text-align: center;
    gap:4px;
    padding:5px 6px;
    border-radius:8px;
    box-shadow:0 0 10px #0003;
    width: 202px;
    min-height: 100px;
  }

  .vue-flow__node-visual.selected {
      box-shadow:0 0 0 2px #8a00ad
  }

  .vue-flow__node-visual .v-button {
    width: 20px;
    height: 20px;
    color: white;
    background-color: #4a5568;
  }

  .close-button {
    width: 20px;
    background-color: #4a5568;
    margin: 0px 10px 10px 0px;
  }

  .close-button .v-btn__content{
    color: white;
  }

  .vue-flow__node-visual .container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    margin: 0px 0px 4px;
  }

  .v-dialog > .v-overlay__content {
    max-width: 60% !important;
    max-height: 80%;
    border-radius: 10px;
  }

  .v-dialog > .v-overlay__content > .v-card {
    border-radius: 20px;
  }
  
  @import 'katex/dist/katex.min.css';
</style>