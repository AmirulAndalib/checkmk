<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkParagraph from 'cmk-ui-library/components/typography/CmkParagraph.vue'
import usei18n from 'cmk-ui-library/lib/i18n'
import type { TranslatedString } from 'cmk-ui-library/lib/i18nString'

const { _t } = usei18n()

interface AddFilterMessageProps {
  label?: TranslatedString
}

defineProps<AddFilterMessageProps>()
</script>
<template>
  <div class="cmk-add-filter-message__container">
    <div class="cmk-add-filter-message__inner">
      <CmkParagraph>{{ label ?? _t('Add filter from left panel') }}</CmkParagraph>
    </div>
  </div>
</template>

<style scoped>
.cmk-add-filter-message__container {
  padding: var(--dimension-4);
  color: var(--font-color-breadcrumb-inactive);
  background-color: var(--ux-theme-3);
}

.cmk-add-filter-message__inner {
  border: var(--dimension-1) dashed var(--dashed-border-color);
  background-color: var(--ux-theme-2);
  padding: var(--dimension-4);
}
</style>
