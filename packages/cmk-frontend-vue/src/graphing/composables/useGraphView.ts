/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { computed, ref } from 'vue'

import type { TimeRange, ValueRange } from '../components/TimeSeriesGraph/types'

// Intent vocabulary:
// - rangeCommit: a new committed range arrived upstream (picker/fetch); clear inspection
//   so the fresh baseline shows through.
// - zoomTransient: a drag-zoom. With a valueRange → value-zoom (X unchanged, set Y window).
//   Without → time-zoom (set X window and re-autoscale Y by clearing the value overlay).
// - pan: a span-preserving X shift (x-axis drag). Sets the X overlay only and leaves any
//   value-zoom Y overlay intact; transient like zoom, so reset returns to the baseline.
export type GraphIntent =
  | { kind: 'rangeCommit'; timeRange: TimeRange }
  | { kind: 'zoomTransient'; timeRange: TimeRange; valueRange?: ValueRange }
  | { kind: 'pan'; timeRange: TimeRange }
  | { kind: 'reset' }

export function useGraphView(getBaseline: () => TimeRange) {
  const inspectionTimeRange = ref<TimeRange | null>(null)
  const inspectionValueRange = ref<ValueRange | null>(null)

  // Inspection overlays the baseline when present; otherwise the baseline shows through.
  const timeRange = computed(() => inspectionTimeRange.value ?? getBaseline())
  const valueRange = computed(() => inspectionValueRange.value)
  const inspectionActive = computed(
    () => inspectionTimeRange.value !== null || inspectionValueRange.value !== null
  )

  function handleIntent(intent: GraphIntent): void {
    switch (intent.kind) {
      case 'rangeCommit':
        // The baseline is set upstream (the getter source); here we only clear inspection
        // so the new baseline becomes the visible view.
        inspectionTimeRange.value = null
        inspectionValueRange.value = null
        break
      case 'zoomTransient':
        if (intent.valueRange) {
          inspectionValueRange.value = intent.valueRange // value-zoom: X unchanged
        } else {
          inspectionTimeRange.value = intent.timeRange // time-zoom: X-extent change…
          inspectionValueRange.value = null // …re-autoscale Y
        }
        break
      case 'pan':
        // Span-preserving shift. Transient like zoom: set the X overlay only and leave
        // inspectionValueRange (a prior value-zoom) untouched. Reset returns to baseline.
        inspectionTimeRange.value = intent.timeRange
        break
      case 'reset':
        inspectionTimeRange.value = null
        inspectionValueRange.value = null
        break
    }
  }

  return { timeRange, valueRange, inspectionActive, handleIntent }
}
