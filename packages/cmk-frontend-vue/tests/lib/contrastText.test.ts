/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { contrastTextColor } from '@/lib/contrastText'

const DARK_TEXT = 'rgb(30, 38, 46)'
const LIGHT_TEXT = 'rgb(255, 255, 255)'

test.each([
  ['#ffffff', DARK_TEXT],
  ['#ffe000', DARK_TEXT],
  ['#fff', DARK_TEXT],
  ['#000000', LIGHT_TEXT],
  ['#0667c1', LIGHT_TEXT],
  ['#147d70', LIGHT_TEXT],
  ['#00d000', DARK_TEXT],
  ['#ff00ff', DARK_TEXT],
  ['#ff0000', LIGHT_TEXT],
  ['#808080', LIGHT_TEXT]
])('picks readable text on %s', (background, expected) => {
  expect(contrastTextColor(background)).toBe(expected)
})

test('falls back to dark text for unparseable colors', () => {
  expect(contrastTextColor('var(--color-mid-grey-50)')).toBe(DARK_TEXT)
  expect(contrastTextColor('')).toBe(DARK_TEXT)
})
