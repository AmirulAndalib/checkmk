/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */

type Rgb = [number, number, number]

// --color-conference-grey-100
const DARK_TEXT_RGB: Rgb = [30, 38, 46]
//--color-white-100
const LIGHT_TEXT_RGB: Rgb = [255, 255, 255]

function cssColor([r, g, b]: Rgb): string {
  return `rgb(${r}, ${g}, ${b})`
}

function parseHexColor(color: string): Rgb | null {
  const hex = color.replace('#', '')
  const expanded =
    hex.length === 3
      ? [...hex].map((nibble) => nibble + nibble).join('')
      : hex.length === 6
        ? hex
        : null
  if (expanded === null || !/^[0-9a-fA-F]{6}$/.test(expanded)) {
    return null
  }
  return [
    parseInt(expanded.slice(0, 2), 16),
    parseInt(expanded.slice(2, 4), 16),
    parseInt(expanded.slice(4, 6), 16)
  ]
}

function linearize(channel: number): number {
  const c = channel / 255
  return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4
}

// WCAG 2.x relative luminance (https://www.w3.org/TR/WCAG22/#dfn-relative-luminance).
function relativeLuminance([r, g, b]: Rgb): number {
  return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)
}

function contrastRatio(luminanceA: number, luminanceB: number): number {
  const [lighter, darker] =
    luminanceA >= luminanceB ? [luminanceA, luminanceB] : [luminanceB, luminanceA]
  return (lighter + 0.05) / (darker + 0.05)
}

const DARK_TEXT = cssColor(DARK_TEXT_RGB)
const LIGHT_TEXT = cssColor(LIGHT_TEXT_RGB)
const DARK_TEXT_LUMINANCE = relativeLuminance(DARK_TEXT_RGB)
const LIGHT_TEXT_LUMINANCE = relativeLuminance(LIGHT_TEXT_RGB)

/** Dark or light text color, whichever has the higher WCAG contrast ratio on the given hex background color. */
export function contrastTextColor(backgroundColor: string): string {
  const rgb = parseHexColor(backgroundColor)
  if (rgb === null) {
    return DARK_TEXT
  }
  const background = relativeLuminance(rgb)
  return contrastRatio(background, DARK_TEXT_LUMINANCE) >=
    contrastRatio(background, LIGHT_TEXT_LUMINANCE)
    ? DARK_TEXT
    : LIGHT_TEXT
}
