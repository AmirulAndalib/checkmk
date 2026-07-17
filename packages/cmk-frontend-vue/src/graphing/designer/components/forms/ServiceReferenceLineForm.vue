<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import type { Autocompleter } from 'cmk-shared-typing/typescript/vue_formspec_components'
import { computed } from 'vue'

import usei18n from '@/lib/i18n'
import type { TranslatedString } from '@/lib/i18nString'

import CmkDropdown from '@/components/CmkDropdown'
import CmkLabel from '@/components/CmkLabel.vue'

import FormAutocompleter from '@/form/private/FormAutocompleter/FormAutocompleter.vue'

import type { GraphItemsStore } from '../../composables/useGraphItems'
import { type DraftScalarItem, scalarColor } from '../../drafts'
import type { ScalarItem } from '../../types'

const { item, store, thresholds } = defineProps<{
  item: DraftScalarItem
  store: GraphItemsStore
  thresholds: { warning: string; critical: string }
}>()

const { _t } = usei18n()

const SCALAR_TYPE_TITLES: Record<ScalarItem['scalar_type'], TranslatedString> = {
  warning: _t('Warning'),
  critical: _t('Critical'),
  warning_lower: _t('Warning (lower)'),
  critical_lower: _t('Critical (lower)'),
  min: _t('Minimum'),
  max: _t('Maximum')
}
const SCALAR_TYPES = Object.keys(SCALAR_TYPE_TITLES) as ScalarItem['scalar_type'][]

const scalarTypeSuggestions = {
  type: 'fixed' as const,
  suggestions: SCALAR_TYPES.map((name) => ({ name, title: SCALAR_TYPE_TITLES[name] }))
}

/** A palette color to fall back to; never keeps a threshold color on the way out. */
function paletteFallback(color: string): string {
  return color === thresholds.warning || color === thresholds.critical
    ? store.nextColor.value
    : color
}

function onScalarTypeChange(value: string | null): void {
  const scalarType = SCALAR_TYPES.find((candidate) => candidate === value)
  if (scalarType !== undefined) {
    store.replace({
      ...item,
      scalar_type: scalarType,
      color: scalarColor(scalarType, paletteFallback(item.color), thresholds)
    })
  }
}

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

/** Selecting upstream clears the dependent selections (host -> service -> metric). */
function onHostChange(hostName: string | null): void {
  store.replace({ ...item, host_name: hostName, service_name: null, metric_name: null })
}

function onServiceChange(serviceName: string | null): void {
  store.replace({ ...item, service_name: serviceName, metric_name: null })
}

function onMetricChange(metricName: string | null): void {
  store.replace({ ...item, metric_name: metricName })
}
</script>

<template>
  <div class="graphing-service-reference-line-form">
    <div class="graphing-service-reference-line-form__field">
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

    <div class="graphing-service-reference-line-form__field">
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

    <div class="graphing-service-reference-line-form__field">
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

    <div class="graphing-service-reference-line-form__field">
      <CmkLabel variant="subtitle">{{ _t('Threshold') }}</CmkLabel>
      <CmkDropdown
        :model-value="item.scalar_type"
        :options="scalarTypeSuggestions"
        :label="_t('Threshold type')"
        @update:model-value="onScalarTypeChange"
      />
    </div>
  </div>
</template>

<style scoped>
.graphing-service-reference-line-form {
  display: flex;
  flex-direction: column;
  gap: var(--dimension-5);
  padding: var(--dimension-7);
}

.graphing-service-reference-line-form__field {
  display: flex;
  flex-direction: column;
  gap: var(--dimension-3);
}
</style>
