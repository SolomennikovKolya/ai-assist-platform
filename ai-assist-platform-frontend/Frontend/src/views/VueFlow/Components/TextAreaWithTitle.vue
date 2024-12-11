<script setup>
    const props = defineProps({
        title: String,
        placeHolder: String,
        value: String,
        rowsTA: Number,
        colsTA: Number,
    });

    const emit = defineEmits(['input']);
</script>


<template>
    <div>
        <div>
            <div class="text-h5">{{props.title}}</div>
        </div>
        <div class="d-flex align-center textarea-wrapper" style="margin: 2px 0px 0px 0px; outline: none">
            <textarea 
              :value="value" 
              :rows="rowsTA" 
              :cols="colsTA" 
              style="outline: none" 
              :placeholder="placeHolder"
              @input="event => emit('input', event.target.value)"/>
        </div>
    </div>
</template>

<style>
  .textarea-wrapper {
    border-radius: 10px;
    overflow: auto; 
    box-shadow:0 0 5px #00000031;
    scrollbar-width: auto; 
  }

  .textarea-wrapper:focus-within {
    box-shadow: 0 0 0 1px #8a00ad;
  }

  .basic-flow.dark .textarea-wrapper:focus-within {
    box-shadow: 0 0 0 1px #2563eb;
  }

  .textarea-wrapper textarea {
    scrollbar-width: thin; 
    scrollbar-color: rgb(157, 157, 157) #ececec;
    font-size: 10px;
    flex:1;
    padding:4px 5px;
    border:none;
    border-radius:8px;
    resize: none; 
    overflow: auto; 
    background:#f9f9f9;
  }

  .basic-flow.dark .textarea-wrapper textarea {
    background:#60638d;
    color: #fffffb;
    scrollbar-color: rgb(33, 48, 82) #404d77;
  }

  .basic-flow.dark .textarea-wrapper ::placeholder {
      color: #c0c0c0;
  }
</style>