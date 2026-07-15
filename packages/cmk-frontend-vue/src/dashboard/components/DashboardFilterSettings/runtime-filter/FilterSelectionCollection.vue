<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkLabel from 'cmk-ui-library/components/CmkLabel.vue'
import {
  CmkAddFilterMessage,
  CmkRemoveFilterButton,
  type FilterDefinition
} from 'cmk-ui-library/components/filter'

interface Props {
  title: string
  filters: string[]
  filterDefinitions: Record<string, FilterDefinition>
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'remove-filter': [filterId: string]
}>()
</script>

<template>
  <div class="db-filter-selection-collection__container">
    <CmkLabel variant="title">{{ title }}</CmkLabel>
    <div
      v-for="(filterId, index) in filters"
      :key="index"
      class="db-filter-selection-collection__item"
    >
      <span class="db-filter-selection-collection__item-title">
        {{ props.filterDefinitions[filterId]!.title }}
      </span>
      <CmkRemoveFilterButton
        :filter-name="props.filterDefinitions[filterId]!.title || ''"
        @remove="() => emit('remove-filter', filterId)"
      />
    </div>
    <CmkAddFilterMessage />
  </div>
</template>

<style scoped>
.db-filter-selection-collection__container {
  display: flex;
  flex-direction: column;
  gap: var(--dimension-4);
}

.db-filter-selection-collection__item {
  background-color: var(--ux-theme-3);
  padding: var(--dimension-5) var(--dimension-4) var(--dimension-5) var(--dimension-7);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.db-filter-selection-collection__item-title {
  flex: 1;
}
</style>
