/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import type { FilterDefinitions } from 'cmk-ui-library/components/filter'

/**
 * A small selection of filter definitions as served by the visual_filter REST
 * endpoint, covering the most common filter component types.
 */
export const SAMPLE_FILTER_DEFINITIONS: FilterDefinitions = {
  hostregex: {
    domainType: 'visual_filter',
    links: [],
    id: 'hostregex',
    title: 'Hostname',
    extensions: {
      info: 'host',
      group: null,
      is_show_more: false,
      components: [{ component_type: 'text_input', id: 'host_regex', label: 'Hostname (regex)' }]
    }
  },
  site: {
    domainType: 'visual_filter',
    links: [],
    id: 'site',
    title: 'Site',
    extensions: {
      info: 'host',
      group: null,
      is_show_more: false,
      components: [
        {
          component_type: 'dropdown',
          id: 'site',
          choices: {
            '': '(all sites)',
            central: 'Central site',
            remote: 'Remote site'
          },
          default_value: ''
        }
      ]
    }
  },
  hoststate: {
    domainType: 'visual_filter',
    links: [],
    id: 'hoststate',
    title: 'Host states',
    extensions: {
      info: 'host',
      group: null,
      is_show_more: false,
      components: [
        { component_type: 'checkbox', id: 'hst0', label: 'UP', default_value: true },
        { component_type: 'checkbox', id: 'hst1', label: 'DOWN', default_value: true },
        { component_type: 'checkbox', id: 'hst2', label: 'UNREACH', default_value: true }
      ]
    }
  }
}
