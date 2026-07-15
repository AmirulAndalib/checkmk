<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script lang="ts">
import codeExample from './UclCmkStateCountBarCodeExample.vue?raw'
</script>

<script setup lang="ts">
import {
  UclDetailPageAccessibility,
  UclDetailPageCodeExample,
  UclDetailPageComponent,
  UclDetailPageDeveloperPlayground,
  UclDetailPageHeader,
  UclDetailPageLayout
} from '@ucl/_ucl/components/detail-page'
import CmkStateCountBar, { type StateSegment } from 'cmk-ui-library/components/CmkStateCountBar.vue'
import usei18n from 'cmk-ui-library/lib/i18n'

import UclCmkStateCountBarDev from './UclCmkStateCountBarDev.vue'

defineProps<{ screenshotMode: boolean }>()

const { _t } = usei18n()

const segments: StateSegment[] = [
  { label: _t('OK'), count: 24, color: 'success' },
  { label: _t('WARN'), count: 3, color: 'warning' },
  { label: _t('CRIT'), count: 1, color: 'danger' },
  { label: _t('UNKNOWN'), count: 0, color: 'unknown' },
  { label: _t('PENDING'), count: 2, color: 'default' }
]
</script>

<template>
  <UclDetailPageLayout>
    <UclDetailPageHeader>CmkStateCountBar</UclDetailPageHeader>

    <UclDetailPageComponent>
      <div class="ucl-cmk-state-count-bar__demo">
        <CmkStateCountBar :segments="segments" />
      </div>
    </UclDetailPageComponent>

    <UclDetailPageCodeExample :code="codeExample" />

    <UclDetailPageAccessibility :data="[]" />

    <UclDetailPageDeveloperPlayground>
      <UclCmkStateCountBarDev :screenshot-mode="screenshotMode" />
    </UclDetailPageDeveloperPlayground>
  </UclDetailPageLayout>
</template>

<style scoped>
.ucl-cmk-state-count-bar__demo {
  width: 320px;
}
</style>
