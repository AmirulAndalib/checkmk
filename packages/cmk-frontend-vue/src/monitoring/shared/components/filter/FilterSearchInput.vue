<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkMultitoneIcon from 'cmk-ui-library/components/CmkIcon/CmkMultitoneIcon.vue'
import usei18n from 'cmk-ui-library/lib/i18n'
import type { TranslatedString } from 'cmk-ui-library/lib/i18nString'
import { computed } from 'vue'

const props = defineProps<{
  placeholder?: TranslatedString
  ariaLabel?: TranslatedString
}>()

const model = defineModel<string>({ default: '' })

const { _t } = usei18n()

const placeholderText = computed(() => props.placeholder ?? _t('Search'))
const ariaLabelText = computed(() => props.ariaLabel ?? _t('Search'))

function onEscape(event: KeyboardEvent): void {
  if (model.value) {
    model.value = ''
    event.stopPropagation()
  }
}
</script>

<template>
  <div class="monitoring-filter-search-input">
    <CmkMultitoneIcon
      name="search"
      :primary-color="{ custom: 'var(--color-mist-grey-60)' }"
      size="small"
      aria-hidden="true"
    />
    <input
      v-model="model"
      type="text"
      class="monitoring-filter-search-input__field"
      :placeholder="placeholderText"
      :aria-label="ariaLabelText"
      @keydown.escape="onEscape"
    />
  </div>
</template>

<style scoped>
.monitoring-filter-search-input {
  display: flex;
  align-items: center;
  gap: var(--dimension-3);
  box-sizing: border-box;
  width: 100%;
  margin: 0 0 var(--dimension-3);
  padding: var(--dimension-2) var(--dimension-4);
  background: var(--default-form-element-bg-color);
  border: 1px solid var(--default-form-element-border-color);
  border-radius: 2px;

  &:focus-within {
    outline: 1px solid var(--success);
    outline-offset: 1px;
  }
}

.monitoring-filter-search-input__field {
  flex: 1;
  min-width: 0;
  margin: 0;
  padding: 0;
  border: 0;
  background: transparent;
  font: inherit;
  color: var(--font-color);

  &:focus-visible {
    outline: none;
  }
}
</style>
