<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import type { Autocompleter } from 'cmk-shared-typing/typescript/vue_formspec_components'

import usei18n from '@/lib/i18n'
import useId from '@/lib/useId'

import CmkLabel from '@/components/CmkLabel.vue'
import CmkLabelRequired from '@/components/user-input/CmkLabelRequired.vue'

import FormAutocompleter from '@/form/private/FormAutocompleter/FormAutocompleter.vue'

const { modelValue, required = false } = defineProps<{
  modelValue: string | null
  required?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string | null]
}>()

const { _t } = usei18n()

const hostNameId = useId()

const hostAutocompleter: Autocompleter = {
  fetch_method: 'rest_autocomplete',
  data: { ident: 'monitored_hostname', params: { strict: true } }
}
</script>

<template>
  <div class="graphing-host-name-select">
    <CmkLabel variant="subtitle" :for="hostNameId">
      {{ _t('Host name') }}<CmkLabelRequired :show="required" space="before" />
    </CmkLabel>
    <FormAutocompleter
      :id="hostNameId"
      :model-value="modelValue"
      :autocompleter="hostAutocompleter"
      :size="0"
      :placeholder="_t('Select host')"
      width="wide"
      floating
      @update:model-value="emit('update:modelValue', $event)"
    />
  </div>
</template>

<style scoped>
.graphing-host-name-select {
  display: flex;
  flex-direction: column;
  gap: var(--dimension-3);
}
</style>
