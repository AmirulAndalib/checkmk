/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { render } from '@testing-library/vue'
import { scaleLinear, scaleTime } from 'd3-scale'
import { describe, expect, test, vi } from 'vitest'
import { defineComponent, h, ref } from 'vue'

import type { ZoomMode } from '@/graphing/components/TimeSeriesGraph/types'
import { useZoomGesture } from '@/graphing/components/TimeSeriesGraph/useZoomGesture'

// A 200×100px plot whose x maps to 1000..2000s and whose (screen-inverted) y maps to
// value 100..0. useZoomGesture uses onBeforeUnmount, so it runs inside a mounted harness.
function mountGesture(mode: ZoomMode) {
  const onZoom = vi.fn()
  const xScale = scaleTime()
    .domain([new Date(1000 * 1000), new Date(2000 * 1000)])
    .range([0, 200])
  const yScale = scaleLinear().domain([0, 100]).range([100, 0])
  let api!: ReturnType<typeof useZoomGesture>
  const harness = defineComponent({
    setup() {
      api = useZoomGesture({
        zoomMode: () => mode,
        timeRange: () => ({ start: 1000, end: 2000, step: 60 }),
        minTimeRange: () => null,
        minValueRange: () => null,
        plotWidth: ref(200),
        plotHeight: ref(100),
        xScale,
        yScale,
        plotCoords: (ev: MouseEvent) => ({ x: ev.clientX, y: ev.clientY }),
        onZoom
      })
      return () => h('div')
    }
  })
  render(harness)
  return { api, onZoom }
}

function drag(
  api: ReturnType<typeof useZoomGesture>,
  from: [number, number],
  to: [number, number]
): void {
  api.onPlotMouseDown(
    new MouseEvent('mousedown', { button: 0, clientX: from[0], clientY: from[1] })
  )
  window.dispatchEvent(new MouseEvent('mousemove', { clientX: to[0], clientY: to[1] }))
  window.dispatchEvent(new MouseEvent('mouseup'))
}

describe('useZoomGesture', () => {
  test('the plot cursor hints the armed axis', () => {
    expect(mountGesture('time').api.plotCursor.value).toBe('ew-resize')
    expect(mountGesture('value').api.plotCursor.value).toBe('ns-resize')
  })

  test('there is no selection band until a drag starts', () => {
    const { api } = mountGesture('time')

    expect(api.selectionBand.value).toBeNull()
  })

  test('a time-mode drag draws a full-height band across the x span', () => {
    const { api } = mountGesture('time')

    api.onPlotMouseDown(new MouseEvent('mousedown', { button: 0, clientX: 40, clientY: 30 }))
    window.dispatchEvent(new MouseEvent('mousemove', { clientX: 120, clientY: 80 }))

    expect(api.selectionBand.value).toEqual({ x: 40, y: 0, width: 80, height: 100 })

    window.dispatchEvent(new MouseEvent('mouseup'))
  })

  test('a horizontal drag past the threshold emits a time-range zoom', () => {
    const { api, onZoom } = mountGesture('time')

    drag(api, [40, 30], [120, 30])

    expect(onZoom).toHaveBeenCalledWith({ timeRange: { start: 1200, end: 1600, step: 60 } })
  })

  test('a vertical drag past the threshold emits a value-range zoom', () => {
    const { api, onZoom } = mountGesture('value')

    drag(api, [40, 25], [40, 75])

    expect(onZoom).toHaveBeenCalledWith({
      timeRange: { start: 1000, end: 2000, step: 60 },
      valueRange: { min: 25, max: 75 }
    })
  })

  test('a sub-threshold drag is treated as a click and emits nothing', () => {
    const { api, onZoom } = mountGesture('time')

    drag(api, [40, 30], [42, 30])

    expect(onZoom).not.toHaveBeenCalled()
  })
})
