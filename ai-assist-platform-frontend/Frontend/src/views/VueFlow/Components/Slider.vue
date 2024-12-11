<script setup>
    const props = defineProps({
        title: String,
        min: Number,
        max: Number,
        defaultValue: Number,
        numberFixed: Number,
        value: Number,
    });

    const emit = defineEmits(['input']);

    const updateValue = (value) => {
        if (typeof value !== "string" && typeof value !== "number") {
            return
        }

        const numericValue = parseFloat(value);
        let newValue = 0;
        
        if (typeof value === "number") {
            if (!isNaN(numericValue)) {
                newValue = parseFloat(numericValue.toFixed(props.numberFixed));
            } else {
                newValue = 0;
            }
        }

        if (typeof value === "string") {
            if (value.charAt(value.length - 1) !== '.' && !isNaN(numericValue)) {
                newValue = parseFloat(numericValue.toFixed(props.numberFixed));
            } else if (value.charAt(value.length - 1) !== '.') {
                newValue = 0;
            } else {
                newValue = numericValue
            }
        }

        if (newValue > props.max) {
            newValue = props.max
        } else if (newValue < props.min) {
            newValue = props.min
        }

        emit('input', newValue)
    };
</script>

<template>
    <div>
        <div class="text-h5">
            {{props.title}}
        </div>
         <v-slider
            :model-value="value"
            :max="max"
            :min="min"
            class="align-center"
            hide-details
            @mousedown.stop
            @update:modelValue="updateValue"
            @input="updateValue"
            thumb-size="12"
        > 
            <template v-slot:append>
                <input class="slider-input" :value="value" @input="event => updateValue(event.target.value)"/>
            </template> 
        </v-slider>
    </div>
</template>

<style>
    .v-slider .slider-input {
        font-size: 10px;
        min-height: 20px;
        height: 20px;
        min-width: 20px;
        width: 32px;
        padding:4px 5px;
        border:none;
        border-radius:8px;
        background-color: #c2c2c2;
        box-shadow:0 0 5px #00000031;
    }

    .v-input--horizontal .v-input__append {
        margin-inline-start: 10px;
    }

    .v-slider.v-input--horizontal > .v-input__control {
        min-height: 25px;
    }
</style>