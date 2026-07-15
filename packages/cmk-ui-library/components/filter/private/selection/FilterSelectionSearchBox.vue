<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import usei18n from '@/lib/i18n'

import CmkIcon from '@/components/CmkIcon'

const value = defineModel({ type: String, required: true })

const { _t } = usei18n()
</script>

<template>
  <div class="cmk-filter-selection-search-box__input-container">
    <CmkIcon class="cmk-filter-selection-search-box__icon" name="search" size="medium"></CmkIcon>
    <input
      v-model="value"
      :placeholder="_t('Search')"
      type="text"
      class="cmk-filter-selection-search-box__input"
    />
  </div>
</template>

<style scoped>
.cmk-filter-selection-search-box__input-container {
  display: flex;
  align-items: center;
  line-height: 15px;
  height: 27px;
  background-color: var(--default-form-element-bg-color);
  border-radius: var(--border-radius);
  border: 1px solid var(--default-form-element-border-color);

  &:focus-within {
    border: 1px solid var(--success);
  }
}

.cmk-filter-selection-search-box__input {
  background: transparent;
  border: 0;
  width: auto;
  line-height: 15px;
  height: 27px;
  padding: 0;
  margin-left: var(--dimension-4);
  flex-grow: 5;

  &::placeholder {
    color: var(--default-form-element-placeholder-color);
  }
}

.cmk-filter-selection-search-box__icon {
  margin-left: var(--spacing);
}
</style>
