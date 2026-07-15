<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import type { Autocompleter } from 'cmk-shared-typing/typescript/vue_formspec_components'
import { computed } from 'vue'

import usei18n from '@/lib/i18n'
import useId from '@/lib/useId'

import CmkLabel from '@/components/CmkLabel.vue'
import FormAutocompleter from '@/components/FormAutocompleter/FormAutocompleter.vue'
import CmkLabelRequired from '@/components/user-input/CmkLabelRequired.vue'

import { hostServiceContext } from './utils'

const {
  modelValue,
  hostName,
  required = false
} = defineProps<{
  modelValue: string | null
  hostName: string | null
  required?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string | null]
}>()

const { _t } = usei18n()

const serviceNameId = useId()

const serviceAutocompleter = computed<Autocompleter>(() => ({
  fetch_method: 'rest_autocomplete',
  data: {
    ident: 'monitored_service_description',
    params: {
      strict: true,
      literal_search: true,
      context: hostServiceContext(hostName, null)
    }
  }
}))
</script>

<template>
  <div class="graphing-service-name-select">
    <CmkLabel variant="subtitle" :for="serviceNameId">
      {{ _t('Service') }}<CmkLabelRequired :show="required" space="before" />
    </CmkLabel>
    <FormAutocompleter
      :id="serviceNameId"
      :model-value="modelValue"
      :autocompleter="serviceAutocompleter"
      :size="0"
      :placeholder="_t('Select service')"
      width="wide"
      floating
      @update:model-value="emit('update:modelValue', $event)"
    />
  </div>
</template>

<style scoped>
.graphing-service-name-select {
  display: flex;
  flex-direction: column;
  gap: var(--dimension-3);
}
</style>
