/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import type { TranslationLoader } from 'cmk-ui-library/lib/i18n'

// The compiled catalogs hold this application's strings plus the ones
// extracted from cmk-ui-library; every entry point hands this loader to initCmkUi().
export const translationLoader: TranslationLoader = async (language) =>
  (await import(`@/assets/locale/${language}.json`)).default
