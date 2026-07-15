<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkTag, { type Colors } from 'cmk-ui-library/components/CmkTag.vue'
import usei18n from 'cmk-ui-library/lib/i18n'
import type { TranslatedString } from 'cmk-ui-library/lib/i18nString'
import { computed } from 'vue'

import type { ServiceState } from '@/monitoring/shared/api/types'

const props = defineProps<{ state: ServiceState; pending?: boolean | undefined }>()

const { _t } = usei18n()

const stateLabel = computed<TranslatedString>(() => {
  if (props.pending) {
    return _t('PEND')
  }
  switch (props.state) {
    case 'OK':
      return _t('OK')
    case 'WARN':
      return _t('WARN')
    case 'CRIT':
      return _t('CRIT')
    case 'UNKNOWN':
    default:
      return _t('UNKN')
  }
})

const stateColor = computed<Colors>(() => {
  if (props.pending) {
    return 'default'
  }
  switch (props.state) {
    case 'OK':
      return 'success'
    case 'WARN':
      return 'warning'
    case 'CRIT':
      return 'danger'
    default:
      return 'unknown'
  }
})
</script>

<template>
  <CmkTag
    class="monitoring-service-state-display"
    :color="stateColor"
    variant="weighted"
    :content="stateLabel"
    size="small"
  />
</template>

<style scoped>
.monitoring-service-state-display {
  --service-state-display-height: 21px;
  --service-state-display-min-width: 60px;

  margin: 0;
  display: flex;
  box-sizing: border-box;
  height: var(--service-state-display-height);
  min-width: var(--service-state-display-min-width);
  align-items: center;
  justify-content: center;
}
</style>
