<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkMultitoneIcon from 'cmk-ui-library/components/CmkIcon/CmkMultitoneIcon.vue'

interface Props {
  isActive: boolean
}
defineProps<Props>()
</script>

<template>
  <span class="cmk-filter-selection-active-icon">
    <CmkMultitoneIcon
      v-if="isActive"
      name="check-circle"
      :primary-color="{ custom: 'var(--cmk-filter-selection-active-icon-color)' }"
    />
  </span>
</template>

<style scoped>
.cmk-filter-selection-active-icon {
  width: var(--dimension-6);
  height: var(--dimension-6);
  min-width: var(--dimension-6);
  min-height: var(--dimension-6);
  display: inline-block;
  flex-shrink: 0;

  --cmk-filter-selection-active-icon-color: var(--color-corporate-green-70);
}

body[data-theme='modern-dark'] .cmk-filter-selection-active-icon {
  --cmk-filter-selection-active-icon-color: var(--color-corporate-green-50);
}
</style>
