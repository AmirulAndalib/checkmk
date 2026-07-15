<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkCatalogPanel from 'cmk-ui-library/components/CmkCatalogPanel.vue'
import usei18n from 'cmk-ui-library/lib/i18n'
import type { TranslatedString } from 'cmk-ui-library/lib/i18nString'

import FieldComponent from '@/dashboard/components/Wizard/components/TableForm/FieldComponent.vue'
import FieldDescription from '@/dashboard/components/Wizard/components/TableForm/FieldDescription.vue'
import TableForm from '@/dashboard/components/Wizard/components/TableForm/TableForm.vue'
import TableFormRow from '@/dashboard/components/Wizard/components/TableForm/TableFormRow.vue'

const { _t } = usei18n()

interface Props {
  label: TranslatedString
}

defineProps<Props>()
</script>

<template>
  <div>
    <CmkCatalogPanel :title="_t('Data settings')" variant="padded">
      <TableForm>
        <TableFormRow>
          <FieldDescription>{{ label }}</FieldDescription>
          <FieldComponent>
            <slot />
          </FieldComponent>
        </TableFormRow>
      </TableForm>
    </CmkCatalogPanel>
  </div>
</template>
