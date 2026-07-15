<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkCode from 'cmk-ui-library/components/CmkCode.vue'
import CmkHeading from 'cmk-ui-library/components/typography/CmkHeading.vue'
import { computed } from 'vue'

const props = defineProps<{
  code: string
}>()

const displayCode = computed(() => props.code.replace(/^<!--[\s\S]*?-->\n?/, '').trimStart())
</script>

<template>
  <div class="ucl-detail-page-code-example__section">
    <CmkHeading type="h2">Code example</CmkHeading>
    <CmkCode :code-text="displayCode" width="fill" />
  </div>
</template>

<style scoped>
.ucl-detail-page-code-example__section {
  display: flex;
  flex-direction: column;
  gap: var(--dimension-6);
}
</style>
