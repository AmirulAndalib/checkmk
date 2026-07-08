/**
 * Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import type { WidgetProps } from '../../types'

export enum NetworkFlowWidgetType {
  TOP_TABLE = 'network_flow_top_table',
  DONUT = 'network_flow_donut'
}

export interface GetValidWidgetProps {
  getValidWidgetProps: () => WidgetProps | null
}
