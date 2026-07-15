<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkCollapsible, { CmkCollapsibleTitle } from 'cmk-ui-library/components/CmkCollapsible'
import CmkIndent from 'cmk-ui-library/components/CmkIndent.vue'
import { ref } from 'vue'

defineProps<{ screenshotMode: boolean }>()

const open = ref(false)
</script>

<template>
  <div class="ucl-cmk-collapsible-dev__title-container">
    <CmkCollapsibleTitle
      :title="'Collapsible Title'"
      :side-title="'Side Title'"
      :open="open"
      :help-text="'Some help text'"
      class="ucl-cmk-collapsible-dev__collapsible"
      @toggle-open="open = !open"
    />
    <CmkCollapsible :open="open">
      <CmkIndent> Some text inside the collapsible </CmkIndent>
    </CmkCollapsible>
  </div>
</template>

<style scoped>
.ucl-cmk-collapsible-dev__title-container {
  min-width: 400px;
}

.ucl-cmk-collapsible-dev__collapsible {
  width: 100%;
}
</style>
