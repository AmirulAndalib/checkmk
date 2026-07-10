/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { type Ref, ref, watch } from 'vue'

import type { DateTimeRange } from '@/components/date-time'

import { useGlobalTimeRange } from '../GlobalTimePicker/useGlobalTimeRange'
import type { RequestedTimeRange } from '../types'

function toRequestedTimeRange(range: DateTimeRange): RequestedTimeRange {
  return {
    start: Math.floor(range.from.toDate().getTime() / 1000),
    end: Math.floor(range.to.toDate().getTime() / 1000)
  }
}

/**
 * The requested (user-chosen) time range for a graph data fetch owner.
 *
 * Seeded from the page's global time picker if one has already published a range,
 * otherwise from `initial`; follows every subsequent picker change. The returned ref
 * stays writable so local interactions (e.g. brush zoom) can update it directly.
 *
 * Call this from the component that owns the data fetch (e.g. a graph group or a
 * standalone panel host), not from presentational components like GraphPanel.
 */
export function useRequestedTimeRange(initial: RequestedTimeRange): Ref<RequestedTimeRange> {
  const { activeTimeRange } = useGlobalTimeRange()

  const requestedTimeRange = ref<RequestedTimeRange>(
    activeTimeRange.value === null ? { ...initial } : toRequestedTimeRange(activeTimeRange.value)
  )

  // Mount order of the picker and the fetch owner is DOM-driven: if the picker mounts
  // later, its initial publish arrives through this watch and replaces the seed.
  watch(activeTimeRange, (val) => {
    if (val !== null) {
      requestedTimeRange.value = toRequestedTimeRange(val)
    }
  })

  return requestedTimeRange
}
