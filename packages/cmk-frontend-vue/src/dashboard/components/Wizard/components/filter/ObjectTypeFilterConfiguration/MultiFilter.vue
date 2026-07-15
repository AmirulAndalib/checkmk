<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import {
  CmkAddFilterMessage,
  CmkFilterInputItem,
  CmkRemoveFilterButton,
  type ConfiguredValues,
  useFilterDefinitions
} from 'cmk-ui-library/components/filter'
import CmkParagraph from 'cmk-ui-library/components/typography/CmkParagraph.vue'
import CmkInlineButton from 'cmk-ui-library/components/user-input/CmkInlineButton.vue'
import usei18n from 'cmk-ui-library/lib/i18n'

import type { FilterConfigState } from '@/dashboard/components/Wizard/components/filter/utils.ts'
import type { ObjectType } from '@/dashboard/types/shared.ts'

interface Props {
  objectType: ObjectType
  objectConfiguredFilters: FilterConfigState
  inFocus: boolean
}

defineProps<Props>()

const emit = defineEmits<{
  (e: 'set-focus', target: ObjectType): void
  (e: 'update-filter-values', filterId: string, values: ConfiguredValues): void
  (e: 'remove-filter', filterId: string): void
}>()

const { _t } = usei18n()

const filterDefinitions = useFilterDefinitions()
</script>

<template>
  <div class="db-multi-filter__list-container">
    <div
      v-for="(configuredValues, name) in objectConfiguredFilters"
      :key="name as string"
      class="db-multi-filter__item-container"
    >
      <CmkFilterInputItem
        :filter-id="name as string"
        :configured-filter-values="configuredValues"
        @update-filter-values="
          (id: string, values: ConfiguredValues) => emit('update-filter-values', id, values)
        "
      />
      <CmkRemoveFilterButton
        class="db-multi-filter__remove-button"
        :filter-name="filterDefinitions[name]!.title || ''"
        @remove="emit('remove-filter', name as string)"
      />
    </div>
    <div
      v-if="!inFocus"
      :class="{ 'db-multi-filter__add-container': Object.keys(objectConfiguredFilters).length > 0 }"
    >
      <CmkParagraph style="padding-bottom: var(--dimension-4)">{{
        _t('Add optional filters to refine this widget')
      }}</CmkParagraph>
      <CmkInlineButton
        class="db-multi-filter__add-filter-button"
        icon="plus"
        @click="emit('set-focus', objectType)"
        >{{ _t('Add filter') }}</CmkInlineButton
      >
    </div>
    <CmkAddFilterMessage v-else />
  </div>
</template>
<style scoped>
.db-multi-filter__add-container {
  padding-top: var(--dimension-5);
}

.db-multi-filter__item-container {
  background-color: var(--ux-theme-3);
  padding: var(--dimension-7);
  position: relative;
  display: block;
}

.db-multi-filter__remove-button {
  position: absolute;
  top: var(--dimension-4);
  right: var(--dimension-4);
}

.db-multi-filter__list-container {
  gap: var(--dimension-4);
  display: flex;
  flex-direction: column;
}
</style>
