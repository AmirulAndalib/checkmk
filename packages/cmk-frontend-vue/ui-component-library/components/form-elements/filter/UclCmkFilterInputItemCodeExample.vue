<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import {
  CmkFilterInputItem,
  type ConfiguredValues,
  useProvideFilterDefinitions
} from 'cmk-ui-library/components/filter'
import { onBeforeMount, ref } from 'vue'

// Definitions become available to all filter components below this component.
// Usually called once in an app root.
const { loadFilterDefinitions } = useProvideFilterDefinitions()
onBeforeMount(loadFilterDefinitions)

const configuredValues = ref<ConfiguredValues>({ host_regex: 'db-server.*' })
</script>

<template>
  <CmkFilterInputItem
    filter-id="hostregex"
    :configured-filter-values="configuredValues"
    @update-filter-values="(_filterId, values) => (configuredValues = values)"
  />
</template>
