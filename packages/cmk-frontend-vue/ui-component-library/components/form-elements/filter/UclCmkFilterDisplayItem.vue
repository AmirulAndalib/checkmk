<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script lang="ts">
import codeExample from './UclCmkFilterDisplayItemCodeExample.vue?raw'
</script>

<script setup lang="ts">
import {
  UclDetailPageCodeExample,
  UclDetailPageComponent,
  UclDetailPageHeader,
  UclDetailPageLayout
} from '@ucl/_ucl/components/detail-page'
import {
  CmkFilterDisplayItem,
  type ConfiguredFilters,
  useProvideFilterDefinitions
} from 'cmk-ui-library/components/filter'

import { SAMPLE_FILTER_DEFINITIONS } from './sampleFilterDefinitions'

defineProps<{ screenshotMode: boolean }>()

useProvideFilterDefinitions({ definitions: SAMPLE_FILTER_DEFINITIONS, groups: {} })

const configuredFilters: ConfiguredFilters = {
  hostregex: { host_regex: 'db-server.*' },
  site: { site: 'central' },
  hoststate: { hst0: 'on', hst1: 'on', hst2: 'off' }
}
</script>

<template>
  <UclDetailPageLayout>
    <UclDetailPageHeader>CmkFilterDisplayItem</UclDetailPageHeader>

    <UclDetailPageComponent>
      <div class="ucl-cmk-filter-display-item__container">
        <CmkFilterDisplayItem
          v-for="(configuredValues, filterId) in configuredFilters"
          :key="filterId"
          :filter-id="filterId"
          :configured-values="configuredValues"
        />
      </div>
    </UclDetailPageComponent>

    <UclDetailPageCodeExample :code="codeExample" />
  </UclDetailPageLayout>
</template>

<style scoped>
.ucl-cmk-filter-display-item__container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 400px;
}
</style>
