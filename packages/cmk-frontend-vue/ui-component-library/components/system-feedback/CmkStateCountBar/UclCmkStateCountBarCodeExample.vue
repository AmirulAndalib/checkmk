<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import usei18n from '@/lib/i18n'

import CmkStateCountBar from '@/components/CmkStateCountBar.vue'

const { _t } = usei18n()
</script>

<template>
  <CmkStateCountBar
    :segments="[
      { label: _t('OK'), count: 24, color: 'success' },
      { label: _t('WARN'), count: 3, color: 'warning' },
      { label: _t('CRIT'), count: 1, color: 'danger' },
      { label: _t('UNKNOWN'), count: 0, color: 'unknown' },
      { label: _t('PENDING'), count: 2, color: 'default' }
    ]"
  />
</template>
