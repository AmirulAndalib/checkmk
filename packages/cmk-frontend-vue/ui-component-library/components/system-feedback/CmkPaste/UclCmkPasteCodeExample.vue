<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkButton from 'cmk-ui-library/components/CmkButton'
import CmkPaste from 'cmk-ui-library/components/CmkPaste.vue'
import { ref } from 'vue'

const inputValue = ref('')
</script>

<template>
  <CmkPaste>
    <template #trigger>
      <CmkButton variant="secondary">Paste</CmkButton>
    </template>
    <template #input>
      <input v-model="inputValue" />
    </template>
  </CmkPaste>
</template>
