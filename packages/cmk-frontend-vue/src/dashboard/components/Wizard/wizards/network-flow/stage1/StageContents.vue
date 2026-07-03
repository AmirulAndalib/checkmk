<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import usei18n from '@/lib/i18n'

import CmkParagraph from '@/components/typography/CmkParagraph.vue'

import ContentSpacer from '@/dashboard/components/ContentSpacer.vue'
import SectionBlock from '@/dashboard/components/Wizard/components/SectionBlock.vue'
import StepsHeader from '@/dashboard/components/Wizard/components/StepsHeader.vue'
import type { WidgetItemList } from '@/dashboard/components/Wizard/components/WidgetSelection/types'
import type {
  WidgetContent,
  WidgetFilterContext,
  WidgetGeneralSettings,
  WidgetSpec
} from '@/dashboard/types/widget'

const { _t } = usei18n()

interface Stage1Props {
  editWidgetSpec: WidgetSpec | null
}
defineProps<Stage1Props>()

// The add-widget contract is declared up front so the individual widget tickets
// (CMK-36348..CMK-36351) only have to append their tile to `availableWidgets` and
// emit the selected content - the wizard wiring stays untouched.
defineEmits<{
  goBack: []
  addWidget: [
    content: WidgetContent,
    generalSettings: WidgetGeneralSettings,
    filterContext: WidgetFilterContext
  ]
}>()

// Populated by the individual network flow widget tickets.
const availableWidgets: WidgetItemList = []
</script>

<template>
  <StepsHeader
    :title="_t('Add network flow widget')"
    :subtitle="_t('Define widget')"
    @back="() => $emit('goBack')"
  />

  <ContentSpacer />

  <SectionBlock :title="_t('Choose what to display')">
    <CmkParagraph v-if="availableWidgets.length === 0">
      {{ _t('No network flow widgets are available yet.') }}
    </CmkParagraph>
  </SectionBlock>
</template>
