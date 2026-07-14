<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import { computed } from 'vue'

import usei18n from '@/lib/i18n'
import type { TranslatedString } from '@/lib/i18nString'

import CmkTag, { type Colors } from '@/components/CmkTag.vue'

export interface StateSegment {
  label: TranslatedString
  count: number
  color: Colors
}

const props = defineProps<{ segments: StateSegment[] }>()

const { _t } = usei18n()

const total = computed(() => props.segments.reduce((sum, segment) => sum + segment.count, 0))

/** Only non-zero segments occupy space in the bar; the legend still lists all of them. */
const barSegments = computed(() => props.segments.filter((segment) => segment.count > 0))

const ariaLabel = computed<string>(() =>
  total.value === 0
    ? _t('No services')
    : barSegments.value
        .map((segment) => _t('%{count} %{label}', { count: segment.count, label: segment.label }))
        .join(', ')
)
</script>

<template>
  <div class="cmk-state-count-bar">
    <div class="cmk-state-count-bar__bar" role="img" :aria-label="ariaLabel">
      <template v-if="total > 0">
        <div
          v-for="(segment, index) in barSegments"
          :key="index"
          class="cmk-state-count-bar__segment"
          :class="`cmk-state-count-bar__segment--${segment.color}`"
          :style="{ flexGrow: segment.count }"
        />
      </template>
      <div
        v-else
        class="cmk-state-count-bar__segment cmk-state-count-bar__segment--empty"
        :style="{ flexGrow: 1 }"
      />
    </div>
    <ul class="cmk-state-count-bar__legend">
      <li
        v-for="(segment, index) in segments"
        :key="index"
        class="cmk-state-count-bar__legend-item"
      >
        <CmkTag :color="segment.color" variant="fill" size="small" :content="segment.label" />
        <span class="cmk-state-count-bar__legend-count">{{ segment.count }}</span>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.cmk-state-count-bar {
  display: flex;
  flex-direction: column;
  gap: var(--dimension-4);
}

.cmk-state-count-bar__bar {
  display: flex;
  width: 100%;
  height: var(--dimension-x);
  overflow: hidden;
  border-radius: var(--border-radius);
}

.cmk-state-count-bar__segment {
  flex-basis: 0;
  height: 100%;
}

.cmk-state-count-bar__segment--success {
  background-color: var(--success);
}

.cmk-state-count-bar__segment--warning {
  background-color: var(--color-warning);
}

.cmk-state-count-bar__segment--danger {
  background-color: var(--color-danger);
}

.cmk-state-count-bar__segment--unknown {
  background-color: var(--color-unknown);
}

/* PENDING and the empty track both use the neutral grey — there is no --color-pending. */
.cmk-state-count-bar__segment--default,
.cmk-state-count-bar__segment--empty {
  background-color: var(--state-count-bar-neutral);
}

.cmk-state-count-bar__legend {
  display: flex;
  flex-wrap: wrap;
  gap: var(--dimension-4);
  padding: 0;
  margin: 0;
  list-style: none;
}

.cmk-state-count-bar__legend-item {
  display: flex;
  align-items: center;
  gap: var(--dimension-3);
}

.cmk-state-count-bar__legend-count {
  font-weight: var(--font-weight-bold);
}

body[data-theme='facelift'] .cmk-state-count-bar {
  --state-count-bar-neutral: var(--color-daylight-grey-50);
}

body[data-theme='modern-dark'] .cmk-state-count-bar {
  --state-count-bar-neutral: var(--color-midnight-grey-50);
}
</style>
