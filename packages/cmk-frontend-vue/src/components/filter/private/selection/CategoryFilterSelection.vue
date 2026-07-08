<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import { computed } from 'vue'

import CmkFilterSelection from '../../CmkFilterSelection.vue'
import { useFilterDefinitions } from '../../useFilterDefinitions.ts'
import type { Filters } from '../../useFilters.ts'
import { parseFilterTypes } from '../../utils.ts'
import { CATEGORY_DEFINITIONS } from './utils.ts'

interface Props {
  filters: Filters
  filterCategory: keyof typeof CATEGORY_DEFINITIONS
}

const props = defineProps<Props>()

const filterDefinitions = useFilterDefinitions()
const filterCategories = parseFilterTypes(filterDefinitions, new Set([props.filterCategory]))

const categoryDefinition = computed(() => CATEGORY_DEFINITIONS[props.filterCategory])
</script>

<template>
  <CmkFilterSelection
    :filters="filters"
    :category-filter="filterCategories.get(props.filterCategory)!"
    :category-definition="categoryDefinition!"
  />
</template>
