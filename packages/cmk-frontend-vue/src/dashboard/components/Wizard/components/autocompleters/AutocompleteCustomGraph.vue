<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import { type Autocompleter } from 'cmk-shared-typing/typescript/vue_formspec_components'
import FormAutocompleter from 'cmk-ui-library/components/FormAutocompleter/FormAutocompleter.vue'
import usei18n from 'cmk-ui-library/lib/i18n'
import type { TranslatedString } from 'cmk-ui-library/lib/i18nString'
import { computed } from 'vue'

const { _t } = usei18n()
const customGraph = defineModel<string | null>('customGraph', { required: true })

interface CmkAutocompleteServiceProps {
  hostName?: string | null
  placeholder?: TranslatedString
}

const props = defineProps<CmkAutocompleteServiceProps>()

const customGraphAutocompleter = computed(() => {
  const autocompleter: Autocompleter = {
    fetch_method: 'rest_autocomplete',
    data: {
      ident: 'custom_graphs',
      params: {
        strict: true,
        context: {}
      }
    }
  }
  return autocompleter
})
</script>

<template>
  <FormAutocompleter
    v-model="customGraph"
    :autocompleter="customGraphAutocompleter"
    :size="0"
    :placeholder="props.placeholder || _t('Select custom graph')"
  />
</template>
