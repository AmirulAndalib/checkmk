<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script lang="ts">
import codeExample from './UclCmkFilterSelectionCodeExample.vue?raw'
</script>

<script setup lang="ts">
import {
  UclDetailPageCodeExample,
  UclDetailPageComponent,
  UclDetailPageHeader,
  UclDetailPageLayout
} from '@ucl/_ucl/components/detail-page'
import {
  CmkFilterSelection,
  getCategoryDefinition,
  parseFilterTypes,
  useFilters,
  useProvideFilterDefinitions
} from 'cmk-ui-library/components/filter'

import { SAMPLE_FILTER_DEFINITIONS } from './sampleFilterDefinitions'

defineProps<{ screenshotMode: boolean }>()

useProvideFilterDefinitions({ definitions: SAMPLE_FILTER_DEFINITIONS, groups: {} })

const filters = useFilters({ site: { site: 'central' } })
const categoryFilter = parseFilterTypes(SAMPLE_FILTER_DEFINITIONS, new Set(['host'])).get('host')!
</script>

<template>
  <UclDetailPageLayout>
    <UclDetailPageHeader>CmkFilterSelection</UclDetailPageHeader>

    <UclDetailPageComponent>
      <div class="ucl-cmk-filter-selection__container">
        <CmkFilterSelection
          :category-filter="categoryFilter"
          :category-definition="getCategoryDefinition('host')"
          :filters="filters"
        />
      </div>
    </UclDetailPageComponent>

    <UclDetailPageCodeExample :code="codeExample" />
  </UclDetailPageLayout>
</template>

<style scoped>
.ucl-cmk-filter-selection__container {
  width: 400px;
}
</style>
