/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import type { ScaleLinear, ScaleTime } from 'd3-scale'
import { type Ref, computed, onBeforeUnmount, ref } from 'vue'

import { type SelectionPoints, clampSpan, selectionRect } from './interaction/selection'
import type { TimeRange, ZoomMode, ZoomPayload } from './types'

// A drag shorter than this on the active axis is treated as a click, not a zoom.
const DRAG_THRESHOLD_PX = 4

export interface ZoomGestureOptions {
  zoomMode: () => ZoomMode
  timeRange: () => TimeRange
  minTimeRange: () => number | null
  minValueRange: () => number | null
  // Plot dimensions in CSS px.
  plotWidth: Ref<number>
  plotHeight: Ref<number>
  // The live scale instances the renderer draws with, used to invert pixels → time/value.
  xScale: ScaleTime<number, number>
  yScale: ScaleLinear<number, number>
  // Shared with the pan gesture, so the owning component (the canvas-ref owner) supplies it.
  plotCoords: (ev: MouseEvent) => { x: number; y: number } | null
  onZoom: (payload: ZoomPayload) => void
}

export function useZoomGesture(options: ZoomGestureOptions) {
  // Drag rectangle in plot-relative pixels; null = no drag in progress.
  const selection = ref<SelectionPoints | null>(null)
  const plotCursor = computed(() => (options.zoomMode() === 'value' ? 'ns-resize' : 'ew-resize'))
  const selectionBand = computed(() =>
    selection.value
      ? selectionRect(options.zoomMode(), selection.value, {
          left: 0,
          top: 0,
          width: options.plotWidth.value,
          height: options.plotHeight.value
        })
      : null
  )

  function onPlotMouseDown(ev: MouseEvent): void {
    if (ev.button !== 0) {
      return
    }
    const point = options.plotCoords(ev)
    if (!point) {
      return
    }
    selection.value = { x0: point.x, y0: point.y, x1: point.x, y1: point.y }
    window.addEventListener('mousemove', onPlotDragMove)
    window.addEventListener('mouseup', onPlotDragEnd)
  }

  function onPlotDragMove(ev: MouseEvent): void {
    const current = selection.value
    const point = options.plotCoords(ev)
    if (!current || !point) {
      return
    }
    selection.value = { ...current, x1: point.x, y1: point.y }
  }

  function onPlotDragEnd(): void {
    window.removeEventListener('mousemove', onPlotDragMove)
    window.removeEventListener('mouseup', onPlotDragEnd)
    const drag = selection.value
    selection.value = null
    if (!drag) {
      return
    }
    if (options.zoomMode() === 'value') {
      if (Math.abs(drag.y1 - drag.y0) < DRAG_THRESHOLD_PX) {
        return
      }
      const valueA = options.yScale.invert(drag.y0)
      const valueB = options.yScale.invert(drag.y1)
      const [min, max] = clampSpan(
        [Math.min(valueA, valueB), Math.max(valueA, valueB)],
        options.minValueRange()
      )
      options.onZoom({ timeRange: options.timeRange(), valueRange: { min, max } })
      return
    }
    if (Math.abs(drag.x1 - drag.x0) < DRAG_THRESHOLD_PX) {
      return
    }
    const range = options.timeRange()
    const timeA = (options.xScale.invert(Math.min(drag.x0, drag.x1)) as Date).getTime() / 1000
    const timeB = (options.xScale.invert(Math.max(drag.x0, drag.x1)) as Date).getTime() / 1000
    const [start, end] = clampSpan([timeA, timeB], options.minTimeRange())
    // step is carried unchanged: a time-zoom-in redraws held data, so it only feeds the
    // tick-density heuristic, never a refetch.
    options.onZoom({ timeRange: { start, end, step: range.step } })
  }

  onBeforeUnmount(() => {
    window.removeEventListener('mousemove', onPlotDragMove)
    window.removeEventListener('mouseup', onPlotDragEnd)
  })

  return { selectionBand, plotCursor, onPlotMouseDown }
}
