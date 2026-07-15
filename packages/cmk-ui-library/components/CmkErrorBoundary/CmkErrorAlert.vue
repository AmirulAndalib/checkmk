<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkAlertBox from 'cmk-ui-library/components/CmkAlertBox.vue'
import CmkCollapsible, { CmkCollapsibleTitle } from 'cmk-ui-library/components/CmkCollapsible'
import CmkHtml from 'cmk-ui-library/components/CmkHtml.vue'
import CmkIndent from 'cmk-ui-library/components/CmkIndent.vue'
import { formatError } from 'cmk-ui-library/lib/error.ts'
import usei18n from 'cmk-ui-library/lib/i18n'
import { computed, ref } from 'vue'

const { _t } = usei18n()

const showDetails = ref<boolean>(false)

const props = defineProps<{ error: Error }>()

const detailMessage = computed<string>(() => {
  return formatError(props.error)
})
</script>

<template>
  <CmkAlertBox variant="error">
    <p>{{ _t('An unexpected error occurred') }}:</p>
    <CmkIndent>
      <CmkHtml :html="props.error.message" class="cmk-error-alert__short" />
    </CmkIndent>
    <p>
      {{
        _t(
          'Refresh the page to try again. If the problem persists, reach out to the Checkmk support.'
        )
      }}
    </p>
    <CmkCollapsibleTitle
      :title="_t('Details')"
      :open="showDetails"
      @toggle-open="() => (showDetails = !showDetails)"
    />
    <CmkCollapsible :open="showDetails">
      <CmkIndent>
        <pre>{{ detailMessage }}</pre>
      </CmkIndent>
    </CmkCollapsible>
  </CmkAlertBox>
</template>

<style scoped>
pre,
.cmk-error-alert__short {
  overflow-wrap: break-word;
  word-break: break-all;
}

pre {
  white-space: pre-wrap;
  padding: 0;
  margin: 0;
  line-height: 1.4;
}
</style>
