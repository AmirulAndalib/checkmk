/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { render } from '@testing-library/vue'
import {
  timeZoneRegionLabel,
  timeZoneShortLabel
} from 'cmk-ui-library/components/date-time/dateTimeUtils'
import TimeZoneTag from 'cmk-ui-library/components/date-time/private/display/TimeZoneTag.vue'
import { untranslated } from 'cmk-ui-library/lib/i18n'
import { describe, expect, test } from 'vitest'

import { TZ_BERLIN } from '../../dateTimeTestFixtures'

// A fixed summer instant so the DST-dependent offset is stable; expected strings are derived from
// the same utilities, so the test asserts the composition, not a hard-coded ICU abbreviation.
const AT = new Date('2026-07-01T12:00:00Z')
const SHORT = timeZoneShortLabel(TZ_BERLIN, AT)
const REGION = timeZoneRegionLabel(TZ_BERLIN)

const visibleTag = (container: Element) => container.querySelector('.cmk-tag')

describe('TimeZoneTag', () => {
  test('the visible badge shows the short label and is hidden from assistive tech', () => {
    const { container } = render(TimeZoneTag, {
      props: { timeZone: TZ_BERLIN, at: AT }
    })
    const tag = visibleTag(container)!
    expect(tag.textContent?.trim()).toBe(SHORT)
    expect(tag).toHaveAttribute('aria-hidden', 'true')
  })

  test('the accessible text is region + short, with no prefix by default', () => {
    const { getByText } = render(TimeZoneTag, {
      props: { timeZone: TZ_BERLIN, at: AT }
    })
    expect(getByText(`${REGION}, ${SHORT}`)).toBeInTheDocument()
  })

  test('accessibleLabel prefixes the accessible text', () => {
    const { getByText } = render(TimeZoneTag, {
      props: {
        timeZone: TZ_BERLIN,
        at: AT,
        accessibleLabel: untranslated('Timezone')
      }
    })
    expect(getByText(`Timezone: ${REGION}, ${SHORT}`)).toBeInTheDocument()
  })
})
