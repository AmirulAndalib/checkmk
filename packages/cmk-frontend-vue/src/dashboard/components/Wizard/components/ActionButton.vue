<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import type { ButtonVariants } from 'cmk-ui-library/components/CmkButton'
import CmkButton from 'cmk-ui-library/components/CmkButton'
import type { SimpleIcons } from 'cmk-ui-library/components/CmkIcon'
import CmkIcon from 'cmk-ui-library/components/CmkIcon'
import type { TranslatedString } from 'cmk-ui-library/lib/i18nString'

interface ActionButtonIcon {
  name: SimpleIcons
  side?: 'left' | 'right'
  rotate?: number
}

interface ActionButtonProps {
  label: TranslatedString
  variant?: ButtonVariants['variant']
  icon?: ActionButtonIcon
  action: () => void
}

defineProps<ActionButtonProps>()
</script>

<template>
  <CmkButton :variant="variant" @click="action">
    <span v-if="icon?.side === 'left'">
      <CmkIcon v-if="icon" :name="icon.name" :rotate="icon.rotate || 0" variant="inline" />
      {{ '\xa0' }}
    </span>
    {{ label }}
    <span v-if="icon?.side === 'right'">
      {{ '\xa0' }}
      <CmkIcon v-if="icon" :name="icon.name" :rotate="icon.rotate || 0" variant="inline" />
    </span>
  </CmkButton>
</template>
