<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import type { TranslatedString } from 'cmk-ui-library/lib/i18nString'
import useId from 'cmk-ui-library/lib/useId'

interface RadioButtonProp {
  value: string
  label?: TranslatedString
  disabled?: boolean
  name?: string
}

defineProps<RadioButtonProp>()
const model = defineModel<string>({ required: true })
const id = useId()
</script>

<template>
  <div class="db-radio-button__container">
    <input
      :id="id"
      v-model="model"
      type="radio"
      :value="value"
      :disabled="!!disabled"
      :name="name || ''"
    />
    <label v-if="label" :for="id">{{ label }}</label>
  </div>
</template>
<style scoped>
.db-radio-button__container {
  display: flex;
  align-items: center;
}
</style>
