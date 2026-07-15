<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script lang="ts">
import codeExample from './UclCmkFilterInputItemCodeExample.vue?raw'
</script>

<script setup lang="ts">
import {
  UclDetailPageCodeExample,
  UclDetailPageComponent,
  UclDetailPageHeader,
  UclDetailPageLayout
} from '@ucl/_ucl/components/detail-page'
import {
  CmkFilterInputItem,
  type ConfiguredFilters,
  useProvideFilterDefinitions
} from 'cmk-ui-library/components/filter'
import { ref } from 'vue'

import { SAMPLE_FILTER_DEFINITIONS } from './sampleFilterDefinitions'

defineProps<{ screenshotMode: boolean }>()

useProvideFilterDefinitions({ definitions: SAMPLE_FILTER_DEFINITIONS, groups: {} })

const configuredFilters = ref<ConfiguredFilters>({
  hostregex: { host_regex: 'db-server.*' },
  site: { site: 'central' },
  hoststate: { hst0: 'on', hst1: 'on', hst2: 'off' }
})
</script>

<template>
  <UclDetailPageLayout>
    <UclDetailPageHeader>CmkFilterInputItem</UclDetailPageHeader>

    <UclDetailPageComponent>
      <div class="ucl-cmk-filter-input-item__container">
        <CmkFilterInputItem
          v-for="filterId in Object.keys(SAMPLE_FILTER_DEFINITIONS)"
          :key="filterId"
          :filter-id="filterId"
          :configured-filter-values="configuredFilters[filterId] ?? null"
          @update-filter-values="(id, values) => (configuredFilters[id] = values)"
        />
      </div>
    </UclDetailPageComponent>

    <UclDetailPageCodeExample :code="codeExample" />
  </UclDetailPageLayout>
</template>

<style scoped>
.ucl-cmk-filter-input-item__container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 400px;
}
</style>
