/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */

/**
 * Shared eslint configuration for Checkmk Vue packages.
 *
 * Every Vue workspace package builds its `eslint.config.mjs` from this
 * factory, so the rules stay identical across packages:
 *
 *     import { checkmkVueConfig } from '../cmk-ui-library/eslint.shared.mjs'
 *     export default [checkmkVueConfig({ packageDir: 'packages/<name>', importMetaDirname: import.meta.dirname }), ...]
 */
export function checkmkVueConfig({
  packageDir,
  importMetaDirname,
  // The test config covers tests/ plus the sources; the source config picks
  // up files the test config deliberately excludes (e.g. lib/i18nString.ts,
  // whose weak test-only variant shadows it).
  project = ['tsconfig.test.json', 'tsconfig.json']
}) {
  return {
    files: [`${packageDir}/**/*.{ts,tsx,vue,js,mjs}`],
    languageOptions: {
      parserOptions: {
        project,
        tsconfigRootDir: importMetaDirname,
        parser: '@typescript-eslint/parser',
        ecmaVersion: 'latest'
      }
    },
    rules: {
      '@typescript-eslint/consistent-type-imports': 'error',
      '@typescript-eslint/no-misused-promises': 'error',
      '@typescript-eslint/no-floating-promises': 'error',
      '@typescript-eslint/naming-convention': [
        'error',
        {
          selector: 'import',
          format: ['camelCase', 'PascalCase']
        },
        {
          selector: 'variableLike',
          format: ['camelCase', 'UPPER_CASE'],
          leadingUnderscore: 'allow'
        },
        {
          selector: 'typeLike',
          format: ['PascalCase']
        },
        { selector: 'property', format: [] }
      ],
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': [
        'error',
        {
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_'
        }
      ],
      eqeqeq: 'error',
      'vue/eqeqeq': 'error',
      'no-var': 'error',
      curly: 'error',
      'prefer-template': 'error',
      'vue/prefer-template': 'error',
      'vue/prop-name-casing': 'off',
      'vue/require-default-prop': 'off',
      'vue/no-import-compiler-macros': 'error',
      'vue/no-undef-components': 'error',
      'vue/no-bare-strings-in-template': [
        'error',
        {
          allowlist: [
            'x',
            '(',
            ')',
            ',',
            '.',
            '&',
            '+',
            '-',
            '=',
            '*',
            '/',
            '#',
            '%',
            '!',
            '?',
            ':',
            '[',
            ']',
            '{',
            '}',
            '<',
            '>',
            '\u00b7',
            '\u2022',
            '\u2010',
            '\u2013',
            '\u2014',
            '\u2212',
            '|'
          ],
          attributes: {
            '/.+/': [
              'title',
              'aria-label',
              'aria-placeholder',
              'aria-roledescription',
              'aria-valuetext'
            ],
            input: ['placeholder'],
            img: ['alt']
          },
          directives: ['v-text']
        }
      ]
    }
  }
}

/** Shared rules for a package's tests/ tree. */
export function checkmkVueTestConfig(packageDir) {
  return {
    files: [`${packageDir}/tests/**/*`],
    rules: {
      'vue/one-component-per-file': 'off',
      'no-restricted-imports': [
        'error',
        {
          paths: [
            {
              name: '@vue/test-utils',
              message:
                'Use @testing-library/vue instead of @vue/test-utils. ' +
                'See https://wiki.lan.checkmk.net/spaces/DEV/pages/149528812/All+things+Vue'
            }
          ]
        }
      ]
    }
  }
}
