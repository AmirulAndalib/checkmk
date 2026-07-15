<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->

<script setup lang="ts">
import type { CmkWizardStepProps } from 'cmk-ui-library/components/CmkWizard'
import { CmkWizardButton, CmkWizardStep } from 'cmk-ui-library/components/CmkWizard'
import CmkHeading from 'cmk-ui-library/components/typography/CmkHeading.vue'
import usei18n from 'cmk-ui-library/lib/i18n'

const { _t } = usei18n()

defineProps<CmkWizardStepProps>()
</script>

<template>
  <CmkWizardStep :index="index" :is-completed="isCompleted">
    <template #header>
      <CmkHeading type="h2"> {{ _t('Open or register Microsoft Azure Entra ID app') }}</CmkHeading>
    </template>

    <template #content>
      <ol>
        <li>
          {{ _t('Open Microsoft Azure and navigate to Microsoft Entra ID.') }}
        </li>
        <li>{{ _t('Open registered app or add a new app registration.') }}</li>
      </ol>
    </template>

    <template #actions>
      <CmkWizardButton type="next" />
    </template>
  </CmkWizardStep>
</template>
