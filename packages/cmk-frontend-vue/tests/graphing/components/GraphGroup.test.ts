/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { CalendarDateTime, type ZonedDateTime, toZoned } from '@internationalized/date'
import { fireEvent, render, screen, waitFor } from '@testing-library/vue'
import type { CmkTimeSeriesGraph } from 'cmk-shared-typing/typescript/cmk_time_series_graph'
import type { components } from 'cmk-shared-typing/typescript/openapi_internal'

import client from '@/lib/rest-api-client/client'

import type { DateTimeRange } from '@/components/date-time'

import { useGlobalTimeRange } from '@/graphing/GlobalTimePicker/useGlobalTimeRange'
import GraphGroup from '@/graphing/components/GraphGroup.vue'

// Stub keeps the test independent of the panel's rendering; the button simulates
// a local time range interaction (e.g. a brush zoom) reported back to the group.
vi.mock('@/graphing/components/GraphPanel.vue', () => ({
  default: {
    props: ['metrics', 'dataTimeRange', 'requestedTimeRange', 'title'],
    emits: ['update:requestedTimeRange', 'update:consolidationFn'],
    template: `<div data-testid="graph-panel">
      <span>{{ title }}</span>
      <button @click="$emit('update:requestedTimeRange', { start: 100, end: 200 })">zoom</button>
    </div>`
  }
}))

const TZ = 'Europe/Berlin'
const zoned = (day: number): ZonedDateTime =>
  toZoned(new CalendarDateTime(2026, 3, day, 0, 0), TZ, 'compatible')
const range = (fromDay: number, toDay: number): DateTimeRange => ({
  from: zoned(fromDay),
  to: zoned(toDay)
})
const epochSeconds = (value: ZonedDateTime): number => Math.floor(value.toDate().getTime() / 1000)

const UNIT: components['schemas']['ApiUnitFormat'] = {
  notation: 'decimal',
  symbol: '',
  precision: { type: 'auto', digits: 2 },
  convertible: true
}

function makeGraphDefinition(title: string): CmkTimeSeriesGraph {
  return {
    size: { width: 70, height: 16, mode: 'fixed' },
    options: {
      header: { title, show_graph_time: true },
      name: title.toLowerCase(),
      x_axis: null,
      y_axis: null,
      show_pin: true,
      font_size_pt: 8
    },
    interaction: { burger: 'enabled', zoom: 'enabled', panning: 'enabled', hover: 'enabled' },
    internal: '{"graphs": []}'
  }
}

const FETCHED = {
  metrics: [
    {
      metadata: { name: 'cpu', title: 'CPU', unit: UNIT, color: '#ff0000' },
      render: { stack: 'area', inverse: false, hidden: false },
      data_points: [1, 2, 3]
    }
  ],
  time_range: { start: 1_000, end: 2_000, step: 60 },
  horizontal_lines: []
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
let postSpy: any

beforeEach(() => {
  useGlobalTimeRange().setActiveTimeRange(null)
  postSpy = vi.spyOn(client, 'POST')
  postSpy.mockResolvedValue({
    data: FETCHED,
    error: undefined,
    response: new Response('{}', { status: 200 })
  } as never)
})

afterEach(() => {
  vi.restoreAllMocks()
})

function renderGroup(graphs: CmkTimeSeriesGraph[] = [makeGraphDefinition('CPU utilization')]) {
  return render(GraphGroup, {
    props: {
      initial_time_range_start: 1_000,
      initial_time_range_end: 2_000,
      graphs
    }
  })
}

test('shows the loading state while the fetch is pending', () => {
  postSpy.mockReturnValue(new Promise(() => {}))
  renderGroup()
  expect(screen.getByText('Loading graphs…')).toBeInTheDocument()
})

test('renders one panel per graph definition once data arrives', async () => {
  renderGroup([makeGraphDefinition('CPU utilization'), makeGraphDefinition('Memory')])

  expect(await screen.findAllByTestId('graph-panel')).toHaveLength(2)
  expect(screen.getByText('CPU utilization')).toBeInTheDocument()
  expect(screen.getByText('Memory')).toBeInTheDocument()
})

test('shows the error message when fetching fails', async () => {
  postSpy.mockRejectedValue(new Error('crash'))
  renderGroup()
  expect(await screen.findByText('crash')).toBeInTheDocument()
})

test('fetches with the initial time range from props', async () => {
  renderGroup()

  await waitFor(() => expect(postSpy).toHaveBeenCalledTimes(1))
  const body = postSpy.mock.calls[0][1].body
  expect(body.internal).toBe('{"graphs": []}')
  expect(body.consolidation_function).toBe('avg')
  expect(body.requested_time_range).toEqual({ start: 1_000, end: 2_000, step: 60 })
})

test('refetches when the global picker publishes a range', async () => {
  renderGroup()
  await waitFor(() => expect(postSpy).toHaveBeenCalledTimes(1))

  const published = range(9, 10)
  useGlobalTimeRange().setActiveTimeRange(published)

  await waitFor(() => expect(postSpy).toHaveBeenCalledTimes(2))
  const body = postSpy.mock.calls[1][1].body
  expect(body.requested_time_range.start).toBe(epochSeconds(published.from))
  expect(body.requested_time_range.end).toBe(epochSeconds(published.to))
})

test('refetches when a panel reports a local time range update', async () => {
  renderGroup()
  await waitFor(() => expect(postSpy).toHaveBeenCalledTimes(1))

  await fireEvent.click(await screen.findByText('zoom'))

  await waitFor(() => expect(postSpy).toHaveBeenCalledTimes(2))
  const body = postSpy.mock.calls[1][1].body
  expect(body.requested_time_range).toEqual({ start: 100, end: 200, step: 60 })
})
