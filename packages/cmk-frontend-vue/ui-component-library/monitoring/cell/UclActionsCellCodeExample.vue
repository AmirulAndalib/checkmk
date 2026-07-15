<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import type { TranslatedString } from 'cmk-ui-library/lib/i18nString'

import ActionsCell, { type CellAction } from '@/monitoring/shared/components/cell/ActionsCell.vue'

const actions: CellAction[] = [
  { id: 'acknowledge', label: 'Acknowledge' as TranslatedString, icon: 'acknowledge-test' },
  { id: 'downtime', label: 'Schedule downtime' as TranslatedString, icon: 'downtime' }
]

// Lazily fetched when the dropdown opens: links (url) render as anchors, url-less ones emit select.
async function loadMenu(): Promise<CellAction[]> {
  return [
    {
      id: 'download',
      label: 'Download agent output' as TranslatedString,
      icon: 'download',
      url: 'fetch_agent_output.py?host=demo&type=agent&_start=1'
    },
    { id: 'reschedule', label: 'Reschedule active checks' as TranslatedString, icon: 'reload' }
  ]
}
</script>

<template>
  <table>
    <tbody>
      <tr>
        <ActionsCell :actions="actions" :max-visible="2" :load="loadMenu" @select="() => {}" />
      </tr>
    </tbody>
  </table>
</template>
