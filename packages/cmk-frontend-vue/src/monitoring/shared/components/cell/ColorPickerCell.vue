<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->

<script setup lang="ts">
import CmkColorPicker from 'cmk-ui-library/components/CmkColorPicker.vue'

import BaseCell, { type CellVerticalAlign } from './BaseCell.vue'

defineProps<{
  columnId?: string | undefined
  verticalAlign?: CellVerticalAlign | undefined
}>()

const color = defineModel<string>({ required: true })
</script>

<template>
  <BaseCell :column-id="columnId" :vertical-align="verticalAlign">
    <CmkColorPicker
      v-model="color"
      size="small"
      class="monitoring-color-picker-cell"
      :class="{ 'monitoring-color-picker-cell--vertical-middle': verticalAlign === 'middle' }"
    />
  </BaseCell>
</template>

<style scoped>
/* The swatch is inline-flex; align it explicitly instead of on the text baseline. */
.monitoring-color-picker-cell {
  vertical-align: top;
}

.monitoring-color-picker-cell--vertical-middle {
  vertical-align: middle;
}
</style>
