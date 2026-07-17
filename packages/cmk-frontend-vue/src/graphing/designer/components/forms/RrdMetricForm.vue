<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import type { Autocompleter } from 'cmk-shared-typing/typescript/vue_formspec_components'
import { computed } from 'vue'

import usei18n from '@/lib/i18n'

import CmkDropdown from '@/components/CmkDropdown'
import CmkLabel from '@/components/CmkLabel.vue'
import CmkToggleButtonGroup, {
  type ToggleButtonOption
} from '@/components/CmkToggleButtonGroup.vue'

import FormAutocompleter from '@/form/private/FormAutocompleter/FormAutocompleter.vue'

import { resolveMetricColor } from '../../api'
import type { GraphItemsStore } from '../../composables/useGraphItems'
import type { DraftRRDMetricItem } from '../../drafts'

const { item, store } = defineProps<{
  item: DraftRRDMetricItem
  store: GraphItemsStore
}>()

const { _t } = usei18n()

const modeOptions: ToggleButtonOption[] = [
  { label: _t('Single metric'), value: 'single' },
  { label: _t('Dynamic query'), value: 'query', disabled: true }
]

const hostAutocompleter: Autocompleter = {
  fetch_method: 'rest_autocomplete',
  data: { ident: 'monitored_hostname', params: { strict: true } }
}

const serviceAutocompleter = computed<Autocompleter>(() => ({
  fetch_method: 'rest_autocomplete',
  data: {
    ident: 'monitored_service_description',
    params: {
      strict: true,
      literal_search: true,
      context: item.host_name === null ? {} : { host: { host: item.host_name } }
    }
  }
}))

const metricAutocompleter = computed<Autocompleter>(() => ({
  fetch_method: 'rest_autocomplete',
  data: {
    ident: 'monitored_metrics',
    params: {
      strict: true,
      context: {
        ...(item.host_name === null ? {} : { host: { host: item.host_name } }),
        ...(item.service_name === null ? {} : { service: { service: item.service_name } })
      }
    }
  }
}))

const consolidationSuggestions = {
  type: 'fixed' as const,
  suggestions: [
    { name: 'avg', title: _t('Average') },
    { name: 'min', title: _t('Minimum') },
    { name: 'max', title: _t('Maximum') }
  ]
}

/** Selecting upstream clears the dependent selections (host -> service -> metric). */
function onHostChange(hostName: string | null): void {
  store.replace({ ...item, host_name: hostName, service_name: null, metric_name: null })
}

function onServiceChange(serviceName: string | null): void {
  store.replace({ ...item, service_name: serviceName, metric_name: null })
}

async function onMetricChange(metricName: string | null): Promise<void> {
  store.replace({ ...item, metric_name: metricName })
  if (metricName === null) {
    return
  }
  let color: string | null
  try {
    color = await resolveMetricColor(metricName)
  } catch {
    // The canonical color is cosmetic — keep the row's current color.
    return
  }
  // Skip stale responses: the row may be gone or on another metric by now.
  const rowStillExists = store.items.value.some((candidate) => candidate.id === item.id)
  if (color !== null && rowStillExists && item.metric_name === metricName) {
    store.patch(item.id, { color })
  }
}

function onConsolidationChange(value: string | null): void {
  if (value === 'avg' || value === 'min' || value === 'max') {
    store.replace({ ...item, consolidation: value })
  }
}
</script>

<template>
  <div class="graphing-rrd-metric-form">
    <CmkToggleButtonGroup :options="modeOptions" model-value="single" />

    <CmkLabel>{{ _t('Show') }}</CmkLabel>

    <div class="graphing-rrd-metric-form__field">
      <CmkLabel variant="subtitle">{{ _t('Host name') }}</CmkLabel>
      <FormAutocompleter
        :model-value="item.host_name"
        :autocompleter="hostAutocompleter"
        :size="0"
        :placeholder="_t('Select host')"
        width="wide"
        @update:model-value="onHostChange"
      />
    </div>

    <div class="graphing-rrd-metric-form__field">
      <CmkLabel variant="subtitle">{{ _t('Service') }}</CmkLabel>
      <FormAutocompleter
        :model-value="item.service_name"
        :autocompleter="serviceAutocompleter"
        :size="0"
        :placeholder="_t('Select service')"
        width="wide"
        @update:model-value="onServiceChange"
      />
    </div>

    <div class="graphing-rrd-metric-form__field">
      <CmkLabel variant="subtitle">{{ _t('Service metric') }}</CmkLabel>
      <FormAutocompleter
        :model-value="item.metric_name"
        :autocompleter="metricAutocompleter"
        :size="0"
        :placeholder="_t('Select metric')"
        width="wide"
        @update:model-value="onMetricChange"
      />
    </div>

    <div class="graphing-rrd-metric-form__field">
      <CmkLabel variant="subtitle">{{ _t('Then consolidate by') }}</CmkLabel>
      <CmkDropdown
        :model-value="item.consolidation"
        :options="consolidationSuggestions"
        :label="_t('Consolidation function')"
        @update:model-value="onConsolidationChange"
      />
    </div>
  </div>
</template>

<style scoped>
.graphing-rrd-metric-form {
  display: flex;
  flex-direction: column;
  gap: var(--dimension-5);
  padding: var(--dimension-7);
}

.graphing-rrd-metric-form__field {
  display: flex;
  flex-direction: column;
  gap: var(--dimension-3);
}
</style>
