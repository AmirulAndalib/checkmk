/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { type Ref, computed, ref } from 'vue'

import type { HorizontalLine, Metric } from '../components/TimeSeriesGraph'
import type { ConsolidationFn } from '../components/consolidation'

export function useGraphVisibility(
  getMetrics: () => Metric[],
  getHorizontalLines: () => HorizontalLine[],
  options: {
    hiddenMetricNames?: Ref<string[]>
    hiddenLineNames?: Ref<string[]>
    highlightedMetricName?: Ref<string | null>
    defaultConsolidationFunction?: ConsolidationFn
  } = {}
) {
  const hiddenMetricNames = options.hiddenMetricNames ?? ref<string[]>([])
  const hiddenLineNames = options.hiddenLineNames ?? ref<string[]>([])
  const highlightedMetricName = options.highlightedMetricName ?? ref<string | null>(null)
  const activeConsolidationFunction = ref<ConsolidationFn>(
    options.defaultConsolidationFunction ?? 'max'
  )

  const visibleMetrics = computed(() =>
    getMetrics().filter((m) => !hiddenMetricNames.value.includes(m.metadata.name))
  )

  const visibleHorizontalLines = computed(() =>
    getHorizontalLines().filter((l) => !hiddenLineNames.value.includes(l.name))
  )

  function setConsolidationFunction(val: ConsolidationFn) {
    activeConsolidationFunction.value = val
  }

  return {
    hiddenMetricNames,
    hiddenLineNames,
    highlightedMetricName,
    activeConsolidationFunction,
    visibleMetrics,
    visibleHorizontalLines,
    setConsolidationFunction
  }
}
