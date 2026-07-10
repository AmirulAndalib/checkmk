<!--
Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->

<script setup lang="ts">
const modelValue = defineModel({ type: String, default: '#ff0000' })

defineProps<{
  boxed?: boolean | undefined
}>()
</script>

<template>
  <input
    v-model="modelValue"
    class="cmk-color-picker"
    :class="{ 'cmk-color-picker--boxed': boxed }"
    type="color"
  />
</template>

<style scoped>
.cmk-color-picker {
  width: 26px;
  height: 30px;
  padding: 0;
  margin: 0;
  border: 1px solid var(--ux-theme-6);
  border-radius: var(--border-radius-half);
  background: transparent;
  cursor: pointer;

  &:focus-visible {
    outline: revert;
  }
}

.cmk-color-picker::-webkit-color-swatch-wrapper {
  padding: 0;
}

.cmk-color-picker::-webkit-color-swatch {
  border: none;
  border-radius: 1px;
}

.cmk-color-picker::-moz-color-swatch {
  border: none;
  border-radius: 1px;
}

.cmk-color-picker--boxed {
  box-sizing: border-box;
  width: var(--dimension-7);
  height: var(--dimension-7);
  padding: 3px;
  background: var(--ux-theme-0);

  &:hover {
    background: var(--ux-theme-2);
  }
}
</style>
