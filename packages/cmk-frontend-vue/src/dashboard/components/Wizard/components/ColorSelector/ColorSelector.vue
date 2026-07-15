<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkColorPicker from 'cmk-ui-library/components/CmkColorPicker.vue'
import CmkDropdown from 'cmk-ui-library/components/CmkDropdown/CmkDropdown.vue'
import type { Suggestion } from 'cmk-ui-library/components/CmkSuggestions'
import usei18n from 'cmk-ui-library/lib/i18n'
import { computed } from 'vue'

const { _t } = usei18n()

interface ColorSelectorProps {
  staticOptions: Suggestion[]
}

const props = defineProps<ColorSelectorProps>()

const color = defineModel<string>('color', { required: true })
const staticOptionNames = computed(() => props.staticOptions.map((option) => option.name))

const mainSelectorOption = computed({
  get(): string {
    return staticOptionNames.value.includes(color.value) ? color.value : '__color__'
  },

  set(newOption: string | null) {
    if (newOption === null) {
      color.value = staticOptionNames.value[0]!
    } else {
      color.value = staticOptionNames.value.includes(newOption) ? newOption : '#FFFFFF'
    }
  }
})

const extendedSuggestions = computed(() => [
  ...props.staticOptions,
  { name: '__color__', title: _t('Use the following color') }
])
</script>

<template>
  <div>
    <CmkDropdown
      v-model="mainSelectorOption as string"
      :label="_t('Select option')"
      :options="{
        type: 'fixed',
        suggestions: extendedSuggestions
      }"
    />
    <div>
      <CmkColorPicker
        v-if="!staticOptionNames.includes(color)"
        v-model="color"
        style="margin-right: 10px"
      />
    </div>
  </div>
</template>
