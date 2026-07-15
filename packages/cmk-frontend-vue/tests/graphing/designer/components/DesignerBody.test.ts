/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { fireEvent, render, screen, waitFor } from '@testing-library/vue'
import client from 'cmk-ui-library/lib/rest-api-client/client'
import { afterEach, beforeEach, expect, test, vi } from 'vitest'

import type { CustomGraphObject } from '@/graphing/designer/api'
import DesignerBody from '@/graphing/designer/components/DesignerBody.vue'

vi.mock('@/graphing/components/TimeSeriesGraph', () => ({
  default: {
    inheritAttrs: false,
    props: ['metrics', 'highlightedMetricName'],
    template: `<div data-testid="time-series-graph">
      <span data-testid="drawn">{{ metrics.map((m) => m.metadata.title).join(',') }}</span>
      <span data-testid="highlighted">{{ highlightedMetricName ?? '' }}</span>
    </div>`
  }
}))

vi.mock('@/graphing/api/graphPin', () => ({
  loadGraphPin: () => Promise.resolve(null),
  saveGraphPin: () => Promise.resolve()
}))

const PALETTE = ['#28a2f3', '#ff8400']

function rrdSource(id: string): unknown {
  return {
    type: 'rrd_metric',
    id,
    title: id,
    line_type: 'line',
    mirrored: false,
    visible: true,
    color: '#28a2f3',
    host_name: 'my-host',
    service_name: 'CPU utilization',
    metric_name: 'util',
    consolidation: 'avg'
  }
}

function graphObject(): CustomGraphObject {
  return {
    domainType: 'custom_graph',
    id: 'my_graph',
    title: 'My graph',
    links: [],
    extensions: {
      owner: 'me',
      is_editable: true,
      metadata: {
        description: '',
        topic: 'my_workplace',
        sort_index: 99,
        hidden: false,
        is_show_more: false,
        public: { type: 'private' }
      },
      content: {
        graph_options: {
          unit: { type: 'first_entry_with_unit' },
          explicit_vertical_range: { type: 'auto' },
          omit_zero_metrics: false
        },
        data_sources: [rrdSource('A'), rrdSource('B')]
      }
    }
  } as unknown as CustomGraphObject
}

function metric(sourceId: string, name: string, title: string): unknown {
  return {
    source_id: sourceId,
    metadata: {
      name,
      title,
      unit: {
        notation: 'decimal',
        symbol: '',
        precision: { type: 'auto', digits: 2 },
        convertible: false
      },
      color: '#28a2f3'
    },
    render: { stack: null, inverse: false, hidden: false },
    data_points: [1, 2]
  }
}

/** The fetch_data POST returns two series, one per (visible) data source. */
function fetchDataResponse(): unknown {
  return {
    data: {
      time_range: { start: 0, end: 3600, step: 60 },
      metrics: [metric('A', 'metric-a', 'CPU'), metric('B', 'metric-b', 'Memory')],
      horizontal_lines: []
    },
    error: undefined,
    response: new Response(null, { status: 200 })
  }
}

beforeEach(() => {
  vi.spyOn(client, 'POST').mockResolvedValue(fetchDataResponse())
})

afterEach(() => {
  vi.restoreAllMocks()
})

function renderBody(mode: 'view' | 'edit') {
  return render(DesignerBody, {
    props: {
      graph: graphObject(),
      graphName: 'my_graph',
      etag: '"etag-1"',
      ownerParam: undefined,
      mode,
      palette: PALETTE,
      thresholds: { warning: '#ffd000', critical: '#ff3232' },
      metricBackendAvailable: false,
      titleMacros: []
    }
  })
}

test('hiding a metric in the detached view-mode legend removes it from the preview', async () => {
  renderBody('view')

  const chart = await screen.findByTestId('time-series-graph')
  await waitFor(() => expect(chart).toHaveTextContent('CPU'))
  expect(chart).toHaveTextContent('Memory')

  await fireEvent.click(screen.getByRole('button', { name: 'CPU' }))
  await waitFor(() => expect(chart).not.toHaveTextContent('CPU'))
  expect(chart).toHaveTextContent('Memory')
})

test('hovering a metric in the detached legend highlights it in the preview', async () => {
  renderBody('view')

  await waitFor(() => expect(screen.getByTestId('drawn')).toHaveTextContent('CPU'))
  expect(screen.getByTestId('highlighted').textContent).toBe('')

  const cpuRow = screen.getByText('CPU').closest('tr')!
  await fireEvent.mouseEnter(cpuRow)
  expect(screen.getByTestId('highlighted')).toHaveTextContent('metric-a')

  await fireEvent.mouseLeave(cpuRow)
  expect(screen.getByTestId('highlighted').textContent).toBe('')
})

test('view mode renders the legend beneath the preview, not the config tabs', async () => {
  const { container } = renderBody('view')

  await waitFor(() => expect(screen.getByTestId('time-series-graph')).toHaveTextContent('CPU'))
  expect(container.querySelector('.graphing-graph-legend')).not.toBeNull()
  expect(screen.queryByRole('tab')).toBeNull()
})

test('edit mode renders the config tabs beneath the preview, not the legend', async () => {
  const { container } = renderBody('edit')

  expect(await screen.findByRole('tab', { name: 'Graph appearance' })).toBeInTheDocument()
  expect(screen.getByRole('tab', { name: 'Metrics selection' })).toBeInTheDocument()
  expect(container.querySelector('.graphing-graph-legend')).toBeNull()
})
