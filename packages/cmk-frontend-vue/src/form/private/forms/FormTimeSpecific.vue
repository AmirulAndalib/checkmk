<!--
Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import type * as FormSpec from 'cmk-shared-typing/typescript/vue_formspec_components'
import CmkButton from 'cmk-ui-library/components/CmkButton'
import CmkHelpText from 'cmk-ui-library/components/CmkHelpText.vue'
import CmkSpace from 'cmk-ui-library/components/CmkSpace.vue'
import CmkInlineValidation from 'cmk-ui-library/components/user-input/CmkInlineValidation.vue'
import { untranslated } from 'cmk-ui-library/lib/i18n'
import { immediateWatch } from 'cmk-ui-library/lib/watch'
import { computed, ref } from 'vue'

import FormEditDispatcher from '@/form/private/FormEditDispatcher/FormEditDispatcher.vue'
import { type ValidationMessages } from '@/form/private/validation'

const props = defineProps<{
  spec: FormSpec.TimeSpecific
  backendValidation: ValidationMessages
}>()

const data = defineModel<unknown>('data', { required: true })

const embeddedValidation = ref<ValidationMessages>([])
const localValidation = ref<string[]>([])

immediateWatch(
  () => props.backendValidation,
  (newValidation: ValidationMessages) => {
    embeddedValidation.value = []
    localValidation.value = []
    newValidation.forEach((msg) => {
      if (msg.location.length === 0) {
        localValidation.value.push(msg.message)
      } else {
        embeddedValidation.value.push(msg)
      }
    })
  }
)

const timespecificActive = computed(() => {
  if (data.value !== null && typeof data.value === 'object') {
    return 'tp_default_value' in data.value
  }
  return false
})

type TimeSpecificData = {
  tp_default_value: unknown
  tp_values: unknown[]
}

function toggleTimeSpecific() {
  if (timespecificActive.value) {
    data.value = (data.value as TimeSpecificData).tp_default_value
  } else {
    data.value = { tp_default_value: data.value, tp_values: [] }
  }
}
</script>

<template>
  <span>
    <CmkButton type="button" @click="toggleTimeSpecific">
      {{ timespecificActive ? spec.i18n.disable : spec.i18n.enable }} </CmkButton
    ><CmkSpace size="small" /><CmkHelpText :help="untranslated(spec.help)" />
    <br />
    <CmkSpace size="small" direction="vertical" />
    <CmkInlineValidation :validation="localValidation"></CmkInlineValidation>
    <template v-if="timespecificActive">
      <FormEditDispatcher
        v-model:data="data"
        :spec="spec.parameter_form_enabled as FormSpec.Components"
        :backend-validation="embeddedValidation"
      />
    </template>
    <template v-else>
      <FormEditDispatcher
        v-model:data="data"
        :spec="spec.parameter_form_disabled as FormSpec.Components"
        :backend-validation="embeddedValidation"
      />
    </template>
    <br />
  </span>
</template>
