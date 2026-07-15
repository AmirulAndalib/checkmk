<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->

<script setup lang="ts">
import CmkLabel from 'cmk-ui-library/components/CmkLabel.vue'
import type { CmkWizardStepProps } from 'cmk-ui-library/components/CmkWizard'
import { CmkWizardButton, CmkWizardStep } from 'cmk-ui-library/components/CmkWizard'
import CmkHeading from 'cmk-ui-library/components/typography/CmkHeading.vue'
import CmkParagraph from 'cmk-ui-library/components/typography/CmkParagraph.vue'
import CmkCheckbox from 'cmk-ui-library/components/user-input/CmkCheckbox.vue'
import CmkInput from 'cmk-ui-library/components/user-input/CmkInput.vue'
import CmkLabelRequired from 'cmk-ui-library/components/user-input/CmkLabelRequired.vue'
import useId from 'cmk-ui-library/lib/useId'
import { computed, ref } from 'vue'

defineProps<CmkWizardStepProps>()

const nameId = useId()
const checkboxChecked = ref(false)
const yourName = ref<string>('')

const displayErrors = ref(false)

const getCheckboxErrors = () => {
  const errors: string[] = []
  if (!checkboxChecked.value) {
    errors.push('This checkbox needs to be checked')
  }
  return errors
}

const getNameErrors = () => {
  const errors: string[] = []
  const name = yourName.value.trim()
  if (name.length === 0) {
    errors.push('Your name is required')
  } else if (name.length > 10) {
    errors.push('Name cannot be longer than 10 characters')
  }
  return errors
}

const checkboxErrors = computed(() => {
  return displayErrors.value ? getCheckboxErrors() : []
})

const yourNameErrors = computed(() => {
  return displayErrors.value ? getNameErrors() : []
})

async function validate(): Promise<boolean> {
  displayErrors.value = true
  return getCheckboxErrors().length === 0 && getNameErrors().length === 0
}
</script>

<template>
  <CmkWizardStep :index="index" :is-completed="isCompleted">
    <template #header>
      <CmkHeading>Step 1</CmkHeading>
    </template>
    <template #content>
      <CmkParagraph> This is the content of the first step. </CmkParagraph>
      <CmkCheckbox
        v-model="checkboxChecked"
        label="This checkbox needs to be checked to proceed."
        :external-errors="checkboxErrors"
      />
      <CmkLabel :for="nameId">
        Choose a name
        <CmkLabelRequired />
      </CmkLabel>
      <CmkInput
        :id="nameId"
        v-model="yourName"
        type="text"
        field-size="medium"
        :external-errors="yourNameErrors"
      />
    </template>
    <template #actions>
      <CmkWizardButton type="next" :validation-cb="validate" />
    </template>
    <template #recap>
      <p>Thank you, {{ yourName }}</p>
    </template>
  </CmkWizardStep>
</template>
