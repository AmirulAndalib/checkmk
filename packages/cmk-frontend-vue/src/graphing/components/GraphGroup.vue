<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->

<!--
Entry-point component for rendering a group of graphs fetched from the REST API.
Registered as the cmk-graph-group custom element via defineCmkComponent in main.ts.
-->

<script setup lang="ts">
import type { CmkTimeSeriesGraph } from 'cmk-shared-typing/typescript/cmk_time_series_graph'
import { ref } from 'vue'

import usei18n from '@/lib/i18n'

import { useGraphData } from '../composables/useGraphData'
import { useRequestedTimeRange } from '../composables/useRequestedTimeRange'
import GraphPanel from './GraphPanel.vue'
import type { ConsolidationFn } from './consolidation'

const { _t } = usei18n()

const props = withDefaults(
  defineProps<{
    site_id: string
    host_name: string
    service_name: string
    initial_time_range_start: number
    initial_time_range_end: number
    graphs: CmkTimeSeriesGraph[]
    // Canvas width in CSS pixels; drives RRD step resolution. Defaults to 770
    // (= 70 ex × 11 px/ex, matching the legacy HTML graph default size).
    canvas_width?: number
  }>(),
  { canvas_width: 800 }
)

// Seeded from the backend-provided initial range, then follows the page's
// global time picker; brush zooms on individual panels write to it directly.
const requestedTimeRange = useRequestedTimeRange({
  start: props.initial_time_range_start,
  end: props.initial_time_range_end
})
const consolidationFn = ref<ConsolidationFn>('avg')

const { graphs, isLoading, error } = useGraphData(
  () => props.graphs,
  () => requestedTimeRange.value,
  () => props.canvas_width,
  () => consolidationFn.value
)
</script>

<template>
  <div class="graphing-graph-group">
    <div v-if="isLoading" class="graphing-graph-group__loading">{{ _t('Loading graphs…') }}</div>
    <div v-else-if="error" class="graphing-graph-group__error">{{ error }}</div>
    <template v-else>
      <GraphPanel
        v-for="(graph, i) in graphs"
        :key="i"
        class="graphing-graph-group__panel"
        :metrics="graph.metrics"
        :data-time-range="graph.timeRange"
        :requested-time-range="requestedTimeRange"
        :title="graph.title"
        :show-title="true"
        :show-timestamp="true"
        :show-burger-menu="true"
        :show-legend="true"
        :horizontal-lines="graph.horizontalLines"
        :canvas-width="canvas_width"
        @update:requested-time-range="requestedTimeRange = $event"
        @update:consolidation-fn="consolidationFn = $event"
      />
    </template>
  </div>
</template>

<style scoped lang="scss">
.graphing-graph-group {
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing) * 4);
}

.graphing-graph-group__loading,
.graphing-graph-group__error {
  padding: calc(var(--spacing) * 2);
  color: var(--font-color);
}

.graphing-graph-group__error {
  color: var(--color-state-crit-background);
}
</style>
