<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkColorPicker from 'cmk-ui-library/components/CmkColorPicker.vue'
import { ref } from 'vue'

const selectedColor = ref('#ff0000')
</script>

<template>
  <CmkColorPicker v-model="selectedColor" aria-label="Color" />
  <CmkColorPicker v-model="selectedColor" size="small" aria-label="Color for AB">AB</CmkColorPicker>
</template>
