/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */

export interface DonutSlice {
  /** Stable key for the slice (used as the render key). */
  key: string
  /** Localized label shown in the legend. */
  label: string
  /** Numeric weight of the slice; percentages are derived from the sum of all values. */
  value: number
  /** CSS color of the slice arc and its legend swatch. */
  color: string
}

export interface CmkDonutChartProps {
  /**
   * Slices in display order. The caller provides them pre-ranked and already
   * includes any aggregated "Other" slice; percentages are computed from the
   * sum of all slice values.
   */
  slices: DonutSlice[]
}
