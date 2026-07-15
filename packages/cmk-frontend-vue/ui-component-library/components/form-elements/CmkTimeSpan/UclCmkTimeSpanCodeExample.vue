<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkTimeSpan from 'cmk-ui-library/components/user-input/CmkTimeSpan/CmkTimeSpan.vue'
import { ref } from 'vue'

const data = ref<number | null>(0)
</script>

<template>
  <CmkTimeSpan
    v-model="data"
    :label="null"
    title="Duration"
    :input-hint="null"
    :displayed-magnitudes="['day', 'hour', 'minute', 'second']"
  />
</template>
