<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script lang="ts">
import { type PanelConfig } from '@ucl/_ucl/components/detail-page'

import codeExample from './UclNumberCellCodeExample.vue?raw'

export const panelConfig = {
  value: {
    type: 'number' as const,
    title: 'value',
    initialState: 42,
    help: 'The numeric value rendered inside the cell.'
  },
  decimals: {
    type: 'number' as const,
    title: 'decimals',
    initialState: 0,
    help: 'Number of decimal places passed to value.toFixed(). Defaults to 0.'
  },
  linkEnabled: {
    type: 'boolean' as const,
    title: 'linkedTo',
    initialState: false,
    help: 'Wrap the cell content in an <a> tag.'
  },
  linkHref: {
    type: 'string' as const,
    title: '↳ href',
    initialState: 'https://checkmk.com'
  },
  linkTarget: {
    type: 'list' as const,
    title: '↳ target',
    options: [
      { title: '_self', name: '_self' },
      { title: '_blank', name: '_blank' }
    ],
    initialState: '_self'
  },
  linkVariant: {
    type: 'list' as const,
    title: '↳ variant',
    options: [
      { title: 'inline', name: 'inline' },
      { title: 'icon', name: 'icon' }
    ],
    initialState: 'inline'
  },
  tagEnabled: {
    type: 'boolean' as const,
    title: 'tagProperties',
    initialState: false,
    help: 'Render the value inside a CmkTag instead of as plain text.'
  },
  tagSize: {
    type: 'list' as const,
    title: '↳ size',
    options: [
      { title: 'small', name: 'small' },
      { title: 'medium', name: 'medium' },
      { title: 'large', name: 'large' }
    ],
    initialState: 'medium'
  },
  tagColor: {
    type: 'list' as const,
    title: '↳ color',
    options: [
      { title: 'default', name: 'default' },
      { title: 'success', name: 'success' },
      { title: 'warning', name: 'warning' },
      { title: 'unknown', name: 'unknown' },
      { title: 'danger', name: 'danger' }
    ],
    initialState: 'default'
  },
  tagVariant: {
    type: 'list' as const,
    title: '↳ variant',
    options: [
      { title: 'fill', name: 'fill' },
      { title: 'outline', name: 'outline' },
      { title: 'weighted', name: 'weighted' }
    ],
    initialState: 'outline'
  },
  tagMinWidth: {
    type: 'number' as const,
    title: '↳ minWidth',
    initialState: 0,
    help: 'Minimum width in px applied to the tag. 0 leaves it unset.'
  },
  tagJustify: {
    type: 'list' as const,
    title: '↳ justify',
    options: [
      { title: 'left', name: 'left' },
      { title: 'center', name: 'center' },
      { title: 'right', name: 'right' }
    ],
    initialState: 'right'
  },
  minWidth: {
    type: 'number' as const,
    title: 'minWidth',
    initialState: 60,
    help: 'Minimum column width in px (tanstack column minSize).'
  },
  maxWidth: {
    type: 'number' as const,
    title: 'maxWidth',
    initialState: 120,
    help: 'Maximum column width in px (tanstack column maxSize).'
  },
  justify: {
    type: 'list' as const,
    title: 'justify',
    options: [
      { title: 'left', name: 'left' },
      { title: 'center', name: 'center' },
      { title: 'right', name: 'right' }
    ],
    initialState: 'left',
    help: 'Horizontal alignment of the cell content.'
  }
} satisfies PanelConfig
</script>

<script setup lang="ts">
import type { ColumnDef, ColumnFiltersState, SortingState } from '@tanstack/vue-table'
import {
  UclDetailPageCodeExample,
  UclDetailPageComponent,
  UclDetailPageHeader,
  UclDetailPageLayout,
  UclPropertiesPanel
} from '@ucl/_ucl/components/detail-page'
import type { InferPanelState } from '@ucl/_ucl/types/prop-panel'
import { computed, ref } from 'vue'

import MonitoringTable from '@/monitoring/shared/components/MonitoringTable.vue'
import type { ColumnJustify } from '@/monitoring/shared/components/MonitoringTableContext'
import type { CellLink } from '@/monitoring/shared/components/cell/BaseCell.vue'
import NumberCell, { type NumberTagProps } from '@/monitoring/shared/components/cell/NumberCell.vue'

defineProps<{ screenshotMode: boolean }>()

const propState = ref(
  Object.fromEntries(
    Object.entries(panelConfig).map(([key, def]) => [key, def.initialState])
  ) as InferPanelState<typeof panelConfig>
)

const linkedTo = computed<CellLink | undefined>(() =>
  propState.value.linkEnabled
    ? {
        href: propState.value.linkHref,
        target: propState.value.linkTarget,
        variant: propState.value.linkVariant as CellLink['variant']
      }
    : undefined
)

const tagProperties = computed<NumberTagProps | undefined>(() =>
  propState.value.tagEnabled
    ? {
        size: propState.value.tagSize as NumberTagProps['size'],
        color: propState.value.tagColor as NumberTagProps['color'],
        variant: propState.value.tagVariant as NumberTagProps['variant'],
        minWidth: propState.value.tagMinWidth || undefined,
        justify: (propState.value.tagJustify || 'right') as NumberTagProps['justify']
      }
    : undefined
)

const justify = computed<ColumnJustify>(() => propState.value.justify as ColumnJustify)

const LINK_SUB_KEYS = ['linkHref', 'linkTarget', 'linkVariant'] as const
const TAG_SUB_KEYS = ['tagSize', 'tagColor', 'tagVariant', 'tagMinWidth', 'tagJustify'] as const

const visibleConfig = computed(() =>
  Object.fromEntries(
    Object.entries(panelConfig).filter(([key]) => {
      if (!propState.value.linkEnabled && (LINK_SUB_KEYS as readonly string[]).includes(key)) {
        return false
      }
      if (!propState.value.tagEnabled && (TAG_SUB_KEYS as readonly string[]).includes(key)) {
        return false
      }
      return true
    })
  )
)

type DemoRow = { id: string }

const rows: DemoRow[] = [{ id: 'demo' }]
const sortState = ref<SortingState>([])
const filterState = ref<ColumnFiltersState>([])

const columns = computed<ColumnDef<DemoRow>[]>(() => [
  {
    id: 'cell',
    header: 'Value',
    minSize: propState.value.minWidth,
    maxSize: propState.value.maxWidth,
    meta: { justify: justify.value }
  }
])
</script>

<template>
  <UclDetailPageLayout>
    <UclDetailPageHeader>NumberCell</UclDetailPageHeader>

    <UclDetailPageComponent>
      <div class="ucl-number-cell__table-wrap">
        <MonitoringTable
          :rows="rows"
          :fetch-state="'idle'"
          :has-loaded="true"
          :columns="columns"
          :sort-state="sortState"
          :filter-state="filterState"
          @update:sort-state="sortState = $event"
          @update:filter-state="filterState = $event"
        >
          <template #row>
            <NumberCell
              column-id="cell"
              :value="propState.value"
              :decimals="propState.decimals"
              :tag-properties="tagProperties"
              :linked-to="linkedTo"
            />
          </template>
        </MonitoringTable>
      </div>

      <template #properties>
        <UclPropertiesPanel
          v-model="propState"
          :config="visibleConfig"
          class="ucl-number-cell__panel"
        />
      </template>
    </UclDetailPageComponent>

    <UclDetailPageCodeExample :code="codeExample" />
  </UclDetailPageLayout>
</template>

<style scoped>
.ucl-number-cell__table-wrap {
  width: 100%;
}

/* The demo has a single sized column. MonitoringTable stretches its table to
   width: 100%, which (with table-layout: fixed) would spread the slack onto that
   lone column and hide its size. Let the table size to its columns instead. */
/* stylelint-disable-next-line selector-pseudo-class-no-unknown, checkmk/vue-bem-naming-convention */
.ucl-number-cell__table-wrap :deep(.monitoring-table__table) {
  width: auto;
}

/* stylelint-disable selector-pseudo-class-no-unknown */
.ucl-number-cell__panel :deep(div:has(> div > label[for$='-linkHref'])),
.ucl-number-cell__panel :deep(div:has(> div > label[for$='-linkTarget'])),
.ucl-number-cell__panel :deep(div:has(> div > label[for$='-linkVariant'])),
.ucl-number-cell__panel :deep(div:has(> div > label[for$='-tagSize'])),
.ucl-number-cell__panel :deep(div:has(> div > label[for$='-tagColor'])),
.ucl-number-cell__panel :deep(div:has(> div > label[for$='-tagVariant'])),
.ucl-number-cell__panel :deep(div:has(> div > label[for$='-tagMinWidth'])),
.ucl-number-cell__panel :deep(div:has(> div > label[for$='-tagJustify'])) {
  padding-left: 16px;
}
/* stylelint-enable selector-pseudo-class-no-unknown */
</style>
