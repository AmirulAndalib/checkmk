<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkCheckbox from 'cmk-ui-library/components/user-input/CmkCheckbox.vue'
import { untranslated } from 'cmk-ui-library/lib/i18n'
import { ref, watch } from 'vue'

import type { CheckboxConfig } from '../../types.ts'
import type { ComponentEmits, FilterComponentProps } from './types.ts'

const props = defineProps<FilterComponentProps<CheckboxConfig>>()
const emit = defineEmits<ComponentEmits>()

const getInitialValue = (): boolean => {
  const storedValue = props.configuredValues?.[props.component.id]
  if (storedValue !== undefined) {
    return storedValue === 'on'
  }
  return props.component.default_value
}

const box = ref(getInitialValue())

if (props.configuredValues === null) {
  const stringValue = box.value ? 'on' : ''
  emit('update-component-values', props.component.id, { [props.component.id]: stringValue })
}

watch(box, (newValue: boolean) => {
  const stringValue = newValue ? 'on' : ''
  emit('update-component-values', props.component.id, { [props.component.id]: stringValue })
})
</script>

<template>
  <CmkCheckbox v-model="box" :label="untranslated(component.label)" />
</template>
