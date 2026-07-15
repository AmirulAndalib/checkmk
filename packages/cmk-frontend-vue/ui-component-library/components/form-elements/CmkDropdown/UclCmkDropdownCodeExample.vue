<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkDropdown from 'cmk-ui-library/components/CmkDropdown'
import type { Suggestions } from 'cmk-ui-library/components/CmkSuggestions'
import { ref } from 'vue'

const selected = ref<string | null>(null)
const options: Suggestions = {
  type: 'fixed',
  suggestions: [
    { name: '1', title: 'one' },
    { name: '2', title: 'two' }
  ]
}
</script>

<template>
  <CmkDropdown
    v-model="selected"
    :options="options"
    input-hint="Input Hint"
    no-results-hint="No Results Hint"
    label="demo dropdown"
    required
  />
</template>
