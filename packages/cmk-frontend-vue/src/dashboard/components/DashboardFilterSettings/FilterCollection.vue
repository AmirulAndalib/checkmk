<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkLabel from 'cmk-ui-library/components/CmkLabel.vue'
import { CmkAddFilterMessage, type ConfiguredValues } from 'cmk-ui-library/components/filter'
import { untranslated } from 'cmk-ui-library/lib/i18n'

interface Props {
  title: string
  filters: string[]
  getFilterValues: (filterId: string) => ConfiguredValues | null
  additionalItemLabel?: string | null
}

withDefaults(defineProps<Props>(), {
  additionalItemLabel: null
})
</script>

<template>
  <div class="db-filter-collection__container">
    <CmkLabel variant="title">{{ title }}</CmkLabel>
    <div
      v-for="(filterId, index) in filters"
      :key="filterId"
      class="db-filter-collection__item-container"
    >
      <slot
        :filter-id="filterId"
        :configured-filter-values="getFilterValues(filterId)"
        :index="index"
      />
    </div>
    <CmkAddFilterMessage v-if="additionalItemLabel" :label="untranslated(additionalItemLabel)" />
  </div>
</template>

<style scoped>
.db-filter-collection__container {
  display: flex;
  flex-direction: column;
  gap: var(--dimension-4);
}

.db-filter-collection__item-container {
  background-color: var(--ux-theme-3);
}
</style>
