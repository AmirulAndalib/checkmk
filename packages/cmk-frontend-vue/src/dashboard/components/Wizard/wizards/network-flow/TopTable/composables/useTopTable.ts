/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import usei18n from 'cmk-ui-library/lib/i18n'
import { type Ref, computed, ref, watch } from 'vue'

import {
  type UseWidgetVisualizationOptions,
  useWidgetVisualizationProps
} from '@/dashboard/components/Wizard/components/WidgetVisualization/useWidgetVisualization'
import type { UseWidgetHandler, WidgetProps } from '@/dashboard/components/Wizard/types'
import { useInjectDashboardConstants } from '@/dashboard/composables/useProvideDashboardConstants'
import { usePreviewWidgetTitle } from '@/dashboard/composables/useWidgetTitles'
import type { NetworkFlowTopTableContent, WidgetSpec } from '@/dashboard/types/widget'
import { buildWidgetEffectiveFilterContext } from '@/dashboard/utils'

const CONTENT_TYPE = 'network_flow_top_table'

export const MAX_ROWS = 50

type Dimension = NetworkFlowTopTableContent['dimension']
type Accent = NetworkFlowTopTableContent['accent']

// Mockup defaults: local hosts blue, remote hosts magenta, everything else green.
const suggestedAccent: Record<Dimension, Accent> = {
  local_hosts: 'blue',
  remote_hosts: 'magenta',
  applications: 'green',
  autonomous_systems: 'green'
}

export interface UseTopTable extends UseWidgetHandler, UseWidgetVisualizationOptions {
  dimension: Ref<Dimension>
  accent: Ref<Accent>
  limitTo: Ref<number>
  limitToValidationErrors: Ref<string[]>
}

export function useTopTable(currentSpec: WidgetSpec | null): UseTopTable {
  const { _t } = usei18n()
  const constants = useInjectDashboardConstants()

  // Default widget title per dimension; mirrors the dimension dropdown labels.
  const dimensionTitles: Record<Dimension, string> = {
    local_hosts: _t('Top local hosts'),
    remote_hosts: _t('Top remote hosts'),
    applications: _t('Top applications ingress / egress'),
    autonomous_systems: _t('Autonomous systems')
  }

  const currentContent =
    currentSpec?.content?.type === CONTENT_TYPE
      ? (currentSpec?.content as NetworkFlowTopTableContent)
      : undefined
  const initialDimension: Dimension = currentContent?.dimension ?? 'local_hosts'

  const {
    title,
    showTitle,
    showTitleBackground,
    showWidgetBackground,
    titleUrlEnabled,
    titleUrl,
    titleUrlValidationErrors,
    validate: validateVisualization,
    widgetGeneralSettings,
    titleMacros
  } = useWidgetVisualizationProps(
    dimensionTitles[initialDimension],
    currentSpec?.general_settings,
    CONTENT_TYPE
  )

  const dimension = ref<Dimension>(initialDimension)
  const accent = ref<Accent>(currentContent?.accent ?? suggestedAccent[dimension.value])
  const limitTo = ref<number>(currentContent?.limit_to ?? 10)
  const limitToValidationErrors = ref<string[]>([])

  // Changing the dimension resets the accent to the suggested one and, unless
  // the user has customized the title, updates it to the new dimension's
  // default. The user can still override both afterwards.
  watch(dimension, (newDimension, oldDimension) => {
    accent.value = suggestedAccent[newDimension]
    if (title.value === dimensionTitles[oldDimension]) {
      title.value = dimensionTitles[newDimension]
    }
  })

  function validate(): boolean {
    limitToValidationErrors.value = []
    if (limitTo.value < 1 || limitTo.value > MAX_ROWS) {
      limitToValidationErrors.value.push(`1 - ${MAX_ROWS}`)
    }
    return validateVisualization() && limitToValidationErrors.value.length === 0
  }

  const content = computed<NetworkFlowTopTableContent>(() => {
    return {
      type: CONTENT_TYPE,
      dimension: dimension.value,
      accent: accent.value,
      limit_to: limitTo.value
    }
  })

  const effectiveTitle = usePreviewWidgetTitle(
    computed(() => {
      return {
        generalSettings: widgetGeneralSettings.value,
        content: content.value,
        effectiveFilters: {}
      }
    })
  )

  const widgetProps = computed<WidgetProps>(() => {
    return {
      general_settings: widgetGeneralSettings.value,
      content: content.value,
      effectiveTitle: effectiveTitle.value,
      effective_filter_context: buildWidgetEffectiveFilterContext(
        content.value,
        {},
        [], // mock data does not use any filter infos yet
        constants
      )
    }
  })

  return {
    title,
    showTitle,
    showTitleBackground,
    showWidgetBackground,
    titleUrlEnabled,
    titleUrl,
    titleUrlValidationErrors,
    titleMacros,
    validate,

    dimension,
    accent,
    limitTo,
    limitToValidationErrors,

    widgetProps,
    getSubmitProps: async () => widgetProps.value
  }
}
