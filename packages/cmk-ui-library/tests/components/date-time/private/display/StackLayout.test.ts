/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { render } from '@testing-library/vue'
import StackLayout from 'cmk-ui-library/components/date-time/private/display/StackLayout.vue'
import { describe, expect, test } from 'vitest'

describe('StackLayout', () => {
  test('default direction is column', () => {
    const { container } = render(StackLayout)
    expect(container.firstElementChild).toHaveClass('cmk-stack-layout--column')
  })

  test('row direction', () => {
    const { container } = render(StackLayout, { props: { direction: 'row' } })
    expect(container.firstElementChild).toHaveClass('cmk-stack-layout--row')
  })
})
