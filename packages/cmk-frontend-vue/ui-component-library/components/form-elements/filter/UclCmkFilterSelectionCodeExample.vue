<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import {
  CmkFilterSelection,
  getCategoryDefinition,
  parseFilterTypes,
  useFilters,
  useProvideFilterDefinitions
} from 'cmk-ui-library/components/filter'
import { computed, onBeforeMount } from 'vue'

// Definitions become available to all filter components below this component.
// Usually called once in an app root.
const { filterDefinitions, loadFilterDefinitions } = useProvideFilterDefinitions()
onBeforeMount(loadFilterDefinitions)

const filters = useFilters()
const categoryFilter = computed(() =>
  filterDefinitions.value
    ? (parseFilterTypes(filterDefinitions.value, new Set(['host'])).get('host') ?? [])
    : []
)
</script>

<template>
  <CmkFilterSelection
    :category-filter="categoryFilter"
    :category-definition="getCategoryDefinition('host')"
    :filters="filters"
  />
</template>
