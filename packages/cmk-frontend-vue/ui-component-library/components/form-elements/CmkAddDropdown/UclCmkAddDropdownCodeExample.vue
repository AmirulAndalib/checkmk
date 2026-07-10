<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import { ref } from 'vue'

import CmkAddDropdown from '@/components/CmkDropdown/CmkAddDropdown.vue'
import type { Suggestions } from '@/components/CmkSuggestions'

const added = ref<string[]>([])
const options: Suggestions = {
  type: 'fixed',
  suggestions: [
    { name: 'cpu', title: 'CPU utilization' },
    { name: 'memory', title: 'Memory usage' }
  ]
}
</script>

<template>
  <CmkAddDropdown :options="options" label="Add metric" @select="(value) => added.push(value)" />
</template>
