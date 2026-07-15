<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import type { ButtonVariants } from 'cmk-ui-library/components/CmkButton'
import CmkButton from 'cmk-ui-library/components/CmkButton'
import type { SimpleIcons } from 'cmk-ui-library/components/CmkIcon'
import CmkIcon, { type IconSizeNames } from 'cmk-ui-library/components/CmkIcon'
import { getWizardContext } from 'cmk-ui-library/components/CmkWizard/utils.ts'
import usei18n from 'cmk-ui-library/lib/i18n'
import type { TranslatedString } from 'cmk-ui-library/lib/i18nString'
import { computed } from 'vue'

export interface CmkWizardButtonProps {
  type: 'next' | 'previous' | 'finish' | 'other'
  iconName?: SimpleIcons | undefined
  iconRotate?: number
  overrideLabel?: TranslatedString
  validationCb?: () => Promise<boolean>
  disabled?: boolean | undefined
}

const { _t } = usei18n()
const context = getWizardContext()
const props = defineProps<CmkWizardButtonProps>()

async function onClick() {
  if (props.disabled) {
    return
  }
  switch (props.type) {
    case 'next':
      if (props.validationCb) {
        const isValid = await props.validationCb()
        if (!isValid) {
          return
        }
      }
      context.navigation.next()
      break
    case 'previous':
      context.navigation.prev()
      break
  }
}

function getLabel() {
  if (props.overrideLabel) {
    return props.overrideLabel
  }
  switch (props.type) {
    case 'next':
      return _t('Next step')
    case 'previous':
      return _t('Previous step')
    case 'finish':
      return _t('Finish')
    default:
      return ''
  }
}

function getButtonConfig(
  variant: 'next' | 'previous' | 'finish' | unknown,
  iconName: SimpleIcons | undefined,
  iconRotate: number = 0
): {
  variant?: ButtonVariants['variant']
  icon: { name: SimpleIcons; rotate: number }
  iconSize?: IconSizeNames
} {
  let icon: { name: SimpleIcons; rotate: number } = {
    name: 'continue',
    rotate: 0
  }

  if (iconName) {
    icon = { name: iconName, rotate: iconRotate }
  }

  switch (variant) {
    case 'other':
      return {
        variant: 'secondary',
        icon
      }
    case 'previous':
      return {
        icon: { name: 'continue', rotate: -90 }
      }
    case 'next':
      return {
        variant: 'secondary',
        icon: { name: 'continue', rotate: 90 }
      }
    case 'finish':
      return {
        variant: 'primary',
        icon: { name: 'check', rotate: 0 },
        iconSize: 'small'
      }
    default:
      throw new Error(`Unknown button variant: ${variant}`)
  }
}

const buttonConfig = getButtonConfig(props.type, props.iconName, props.iconRotate)

const isVisible = computed(
  () => context.mode() !== 'overview' || (props.type !== 'next' && props.type !== 'previous')
)
</script>

<template>
  <CmkButton
    v-if="isVisible"
    class="cmk-wizard-button"
    :variant="buttonConfig.variant"
    :disabled="props.disabled"
    @click="onClick"
  >
    <CmkIcon
      :name="buttonConfig.icon.name"
      :size="buttonConfig.iconSize"
      :rotate="buttonConfig.icon.rotate"
      variant="inline"
    />
    {{ getLabel() }}
  </CmkButton>
</template>

<style scoped>
.cmk-wizard-button {
  width: fit-content;
}
</style>
