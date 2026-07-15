<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkButton from 'cmk-ui-library/components/CmkButton'
import CmkPopup from 'cmk-ui-library/components/CmkPopup.vue'
import CmkHeading from 'cmk-ui-library/components/typography/CmkHeading.vue'
import CmkParagraph from 'cmk-ui-library/components/typography/CmkParagraph.vue'
import usei18n from 'cmk-ui-library/lib/i18n'
import { DialogTitle } from 'reka-ui'
import { computed } from 'vue'

import { useItemDescription } from '../composables/useItemDescription'
import type { GraphItem, ItemId } from '../types'

const { _t } = usei18n()

const { ids, dependents } = defineProps<{
  open: boolean
  /** The rows the user asked to delete. */
  ids: readonly ItemId[]
  /** Formulas that (transitively) reference them; they are deleted along with them on confirm. */
  dependents: readonly GraphItem[]
}>()

const emit = defineEmits<{
  /** Delete the rows and all their dependents. */
  confirm: []
  close: []
}>()

const { describeItem } = useItemDescription()

const joinedIds = computed(() => ids.join(', '))
</script>

<template>
  <CmkPopup :open="open" @close="emit('close')">
    <div class="graphing-delete-with-dependents-popup">
      <DialogTitle>
        <CmkHeading type="h2">
          {{ _t('Delete %{ids}?', { ids: joinedIds }) }}
        </CmkHeading>
      </DialogTitle>
      <CmkParagraph>
        {{
          _t('The following calculations reference the selected rows and will be deleted as well:')
        }}
      </CmkParagraph>
      <ul class="graphing-delete-with-dependents-popup__dependents">
        <li v-for="dependent in dependents" :key="dependent.id">
          {{ dependent.id }} — {{ describeItem(dependent) }}
        </li>
      </ul>
      <div class="graphing-delete-with-dependents-popup__buttons">
        <CmkButton variant="danger" @click="emit('confirm')">
          {{ _t('Delete all') }}
        </CmkButton>
        <CmkButton variant="secondary" @click="emit('close')">
          {{ _t('Cancel') }}
        </CmkButton>
      </div>
    </div>
  </CmkPopup>
</template>

<style scoped>
.graphing-delete-with-dependents-popup {
  display: flex;
  flex-direction: column;
  gap: var(--dimension-6);
}

.graphing-delete-with-dependents-popup__dependents {
  margin: 0;
  padding-left: var(--dimension-8);
}

.graphing-delete-with-dependents-popup__buttons {
  display: flex;
  gap: var(--dimension-4);
}
</style>
