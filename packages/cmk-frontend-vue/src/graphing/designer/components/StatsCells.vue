<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import BaseCell from '@/monitoring/shared/components/cell/BaseCell.vue'

import type { MetricStats } from '../../components/legend/legendUtils'

defineProps<{ stats: MetricStats | undefined }>()
</script>

<template>
  <BaseCell column-id="min" vertical-align="middle" no-wrap>{{ stats?.min }}</BaseCell>
  <BaseCell column-id="avg" vertical-align="middle" no-wrap>{{ stats?.avg }}</BaseCell>
  <BaseCell column-id="max" vertical-align="middle" no-wrap>{{ stats?.max }}</BaseCell>
  <BaseCell column-id="last" vertical-align="middle" no-wrap>{{ stats?.last }}</BaseCell>
</template>
