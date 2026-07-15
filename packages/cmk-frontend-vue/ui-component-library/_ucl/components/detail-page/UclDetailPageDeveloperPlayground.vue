<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkAccordion from 'cmk-ui-library/components/CmkAccordion/CmkAccordion.vue'
import CmkAccordionItem from 'cmk-ui-library/components/CmkAccordion/CmkAccordionItem.vue'
import CmkIcon from 'cmk-ui-library/components/CmkIcon'
import CmkSpace from 'cmk-ui-library/components/CmkSpace.vue'
import { computed, ref } from 'vue'

const openedItems = ref<string[]>([])
const isDeveloperOpen = computed(() => openedItems.value.includes('developer-playground'))
</script>

<template>
  <div class="ucl-detail-page-developer-playground__section">
    <CmkAccordion v-model="openedItems" :max-open="1" :min-open="0">
      <CmkAccordionItem value="developer-playground">
        <template #header>
          <CmkIcon
            name="tree-closed"
            size="xsmall"
            :rotate="isDeveloperOpen ? 90 : 0"
            aria-hidden="true"
          />
          <CmkSpace size="small" />
          <span> Developer Playground </span>
        </template>

        <template #content>
          <slot></slot>
        </template>
      </CmkAccordionItem>
    </CmkAccordion>
  </div>
</template>

<style scoped>
.ucl-detail-page-developer-playground__section {
  display: flex;
  flex-direction: column;
  gap: var(--dimension-6);
}
</style>
