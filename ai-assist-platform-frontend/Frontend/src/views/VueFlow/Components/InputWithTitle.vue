<script setup>
    const props = defineProps({
        title: String,
        placeHolder: String,
        value: String,
        widthInput: Number,
        heightInput: Number,
    });

    const emit = defineEmits(['input']);
</script>


<template>
    <div>
        <div>
        <div class="text-h5">{{props.title}}</div>
        </div>
        <div class="d-flex align-center" style="margin: 2px 0px 10px 0px">
            <input 
                class="simple-input" 
                :value="value" 
                :placeholder="placeHolder"
                @input="event => emit('input', event.target.value)"/>
        </div>
    </div>
</template>

<style>
    .simple-input {
        font-size: 10px;
        width: 190px;
        height: 20px;
        flex:1;
        padding:4px 5px;
        border:none;
        border-radius:8px;
        box-shadow:0 0 5px #00000031;
        background:#fdfdfd;
    }

    .basic-flow.dark .simple-input {
        background:#60638d;
        color: #fffffb;
    }

    .basic-flow.dark .simple-input::placeholder{
        color: #c0c0c0;
    }

    .simple-input:focus-visible {
        outline:none;
        box-shadow:0 0 0 1px #8a00ad;
        transition:box-shadow .2s
    }

    .basic-flow.dark .simple-input:focus-visible {
        box-shadow:0 0 0 1px #2563eb;
    }
</style>