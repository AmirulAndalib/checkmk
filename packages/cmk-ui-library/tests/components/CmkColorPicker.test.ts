/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { fireEvent, render, screen } from '@testing-library/vue'
import CmkColorPicker from 'cmk-ui-library/components/CmkColorPicker.vue'
import { h } from 'vue'

const DARK_TEXT = 'rgb(30, 38, 46)'
const LIGHT_TEXT = 'rgb(255, 255, 255)'

function renderPicker(
  props: Record<string, unknown> = {},
  slots: Record<string, (props: never) => unknown> = {}
) {
  const { container } = render(CmkColorPicker, {
    props: { modelValue: '#ffe000', ...props },
    attrs: { 'aria-label': 'Color' },
    slots
  })
  return {
    root: container.querySelector('.cmk-color-picker') as HTMLElement,
    input: container.querySelector('input[type="color"]') as HTMLInputElement,
    content: container.querySelector('.cmk-color-picker__content') as HTMLElement | null,
    triangle: container.querySelector('.cmk-color-picker__triangle') as HTMLElement
  }
}

test('emits the picked color and forwards aria attributes to the native input', async () => {
  const { emitted } = render(CmkColorPicker, {
    props: { modelValue: '#ffe000' },
    attrs: { 'aria-label': 'Formula color' }
  })

  const input = screen.getByLabelText<HTMLInputElement>('Formula color')
  expect(input.type).toBe('color')

  await fireEvent.update(input, '#0667c1')
  expect(emitted('update:modelValue')).toEqual([['#0667c1']])
})

test('forwards fallthrough class and style to the visible root, not the input', () => {
  const { container } = render(CmkColorPicker, {
    props: { modelValue: '#ffe000' },
    attrs: { class: 'my-class', style: 'margin-right: 10px' }
  })
  const root = container.querySelector('.cmk-color-picker') as HTMLElement
  expect(root.classList).toContain('my-class')
  expect(root.style.marginRight).toBe('10px')
})

test.each([
  ['#ffe000', DARK_TEXT],
  ['#0667c1', LIGHT_TEXT]
])('overlay and triangle contrast with the picked color %s', (modelValue, expectedContrast) => {
  const { content, triangle } = renderPicker({ modelValue }, { default: () => 'F' })

  expect(content!.style.color).toBe(expectedContrast)
  expect(triangle.style.backgroundColor).toBe(expectedContrast)
})

test('overlays slot content on the swatch, hidden from assistive technology', () => {
  const { content } = renderPicker({}, { default: () => h('span', { class: 'badge' }, 'AB') })

  expect(content!.querySelector('.badge')).toHaveTextContent('AB')
  expect(content).toHaveAttribute('aria-hidden', 'true')
})

test('renders no overlay without slot content', () => {
  const { content } = renderPicker()
  expect(content).toBeNull()
})

test('passes the contrast color to the slot', () => {
  const { content } = renderPicker(
    { modelValue: '#0667c1' },
    { default: (props: { contrastColor: string }) => h('span', props.contrastColor) }
  )

  expect(content).toHaveTextContent(LIGHT_TEXT)
})

test('sizes to large by default and to small on request', () => {
  const { root } = renderPicker()
  expect(root.classList).not.toContain('cmk-color-picker--small')

  const { root: small } = renderPicker({ size: 'small' })
  expect(small.classList).toContain('cmk-color-picker--small')
})
