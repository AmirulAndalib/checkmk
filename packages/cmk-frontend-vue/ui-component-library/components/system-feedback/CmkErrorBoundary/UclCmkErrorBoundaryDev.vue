<!--
Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->

<script setup lang="ts">
import { useCmkErrorBoundary } from 'cmk-ui-library/components/CmkErrorBoundary'
import { CmkError } from 'cmk-ui-library/lib/error.ts'
import { defineComponent } from 'vue'

const props = defineProps<{ screenshotMode: boolean }>()

class UclError<T extends Error> extends CmkError<T> {
  override name = 'UclError'
  override getContext(): string {
    return 'UclErrorContext'
  }
}

function throwCmkError() {
  try {
    try {
      throw new Error('something happened in code we can not control')
    } catch (error: unknown) {
      throw new UclError('internal error handler, but keeps bubbeling', error as Error)
    }
  } catch (error: unknown) {
    throw new CmkError('this is a cmk error', error as Error)
  }
}

function throwError(message: string) {
  throw new Error(message)
}

// eslint-disable-next-line @typescript-eslint/naming-convention
const ScreenshotModeEnabler = defineComponent(() => {
  return () => {
    if (props.screenshotMode) {
      throwError('cheese')
    }
  }
}, {})

// eslint-disable-next-line @typescript-eslint/naming-convention
const { CmkErrorBoundary } = useCmkErrorBoundary()
</script>

<template>
  <div>
    &lt;ErrorBoundary&gt;
    <CmkErrorBoundary>
      <button @click="throwError('this is a test error')">throw new Error()</button>
      <button @click="throwCmkError()">throw new CmkError()</button>
      <ScreenshotModeEnabler />
    </CmkErrorBoundary>
    &lt;/ErrorBoundary&gt;
  </div>
  <!-- I would have expected that this also triggers the onErrorCaptured method in useErrorBoundary, but its also fine this way -->
  <button @click="throwError('another error')">throw new Error() outside error boundary</button>
</template>
