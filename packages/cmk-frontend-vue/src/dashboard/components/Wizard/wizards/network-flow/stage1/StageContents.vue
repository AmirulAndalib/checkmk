<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import { type ShallowRef, computed, ref, toValue, useTemplateRef } from 'vue'

import usei18n from '@/lib/i18n'

import CmkParagraph from '@/components/typography/CmkParagraph.vue'

import ContentSpacer from '@/dashboard/components/ContentSpacer.vue'
import ActionBar from '@/dashboard/components/Wizard/components/ActionBar.vue'
import ActionButton from '@/dashboard/components/Wizard/components/ActionButton.vue'
import SectionBlock from '@/dashboard/components/Wizard/components/SectionBlock.vue'
import StepsHeader from '@/dashboard/components/Wizard/components/StepsHeader.vue'
import WidgetTiles from '@/dashboard/components/Wizard/components/WidgetSelection/WidgetTiles.vue'
import type { WidgetItemList } from '@/dashboard/components/Wizard/components/WidgetSelection/types'
import type { DashboardKey } from '@/dashboard/types/dashboard'
import type {
  WidgetContent,
  WidgetFilterContext,
  WidgetGeneralSettings,
  WidgetSpec
} from '@/dashboard/types/widget'

import TopTable from '../TopTable/TopTable.vue'
import { type GetValidWidgetProps, NetworkFlowWidgetType } from '../types'

const { _t } = usei18n()

interface Stage1Props {
  dashboardKey: DashboardKey
  editWidgetSpec: WidgetSpec | null
}
defineProps<Stage1Props>()

const emit = defineEmits<{
  goBack: []
  addWidget: [
    content: WidgetContent,
    generalSettings: WidgetGeneralSettings,
    filterContext: WidgetFilterContext
  ]
}>()

const availableWidgets: WidgetItemList = [
  { id: NetworkFlowWidgetType.TOP_TABLE, label: _t('Top-N table'), icon: 'networking' }
]
const enabledWidgets = computed(() => {
  return availableWidgets.map((item) => item.id)
})

const selectedWidget = ref<NetworkFlowWidgetType>(NetworkFlowWidgetType.TOP_TABLE)

const topTableRef = useTemplateRef<InstanceType<typeof TopTable>>('topTableRef')
const widgetRefs: Record<
  NetworkFlowWidgetType,
  Readonly<ShallowRef<GetValidWidgetProps | null>>
> = {
  [NetworkFlowWidgetType.TOP_TABLE]: topTableRef
}

function gotoNextStage() {
  const selected = widgetRefs[selectedWidget.value].value
  if (!selected) {
    return
  }

  const widgetProps = selected.getValidWidgetProps()
  if (widgetProps) {
    emit(
      'addWidget',
      toValue(widgetProps.content),
      toValue(widgetProps.general_settings),
      toValue({
        filters: {},
        uses_infos: widgetProps.effective_filter_context.uses_infos
      } as WidgetFilterContext)
    )
  }
}
</script>

<template>
  <StepsHeader
    :title="_t('Add network flow widget')"
    :subtitle="_t('Define widget')"
    @back="() => emit('goBack')"
  />

  <ContentSpacer />

  <ActionBar align-items="left">
    <ActionButton
      :label="!!editWidgetSpec ? _t('Save widget') : _t('Add & place widget')"
      :action="gotoNextStage"
      variant="primary"
    />
  </ActionBar>

  <ContentSpacer :dimension="8" />

  <SectionBlock :title="_t('Choose what to display')">
    <CmkParagraph v-if="availableWidgets.length === 0">
      {{ _t('No network flow widgets are available yet.') }}
    </CmkParagraph>
    <WidgetTiles
      v-else
      v-model:selected-widget="selectedWidget as NetworkFlowWidgetType"
      :available-items="availableWidgets"
      :enabled-widgets="enabledWidgets"
    />
  </SectionBlock>

  <TopTable
    v-show="selectedWidget === NetworkFlowWidgetType.TOP_TABLE"
    ref="topTableRef"
    :dashboard-key="dashboardKey"
    :edit-widget-spec="editWidgetSpec"
  />
</template>
