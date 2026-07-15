/**
 * Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import type { ConfiguredValues } from 'cmk-ui-library/components/filter'

export enum FilterOrigin {
  DASHBOARD = 'DASHBOARD',
  QUICK_FILTER = 'QUICK_FILTER',
  LINKED_VIEW = 'LINKED_VIEW'
}

export interface ContextFilter {
  configuredValues: ConfiguredValues // TODO: later replace with FilterHTTPVars
  source: FilterOrigin
}

export type ContextFilters = Record<string, ContextFilter>

export enum RuntimeFilterMode {
  OVERRIDE = 'override',
  MERGE = 'merge'
}
