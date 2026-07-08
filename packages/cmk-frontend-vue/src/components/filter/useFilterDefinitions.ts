/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { type InjectionKey, type Ref, inject, provide, ref } from 'vue'

import client, { unwrap } from '@/lib/rest-api-client/client'

import type { FilterDefinitions, FilterGroups } from './types.ts'

const filterDefinitionsKey = Symbol() as InjectionKey<Ref<FilterDefinitions | null>>
const filterGroupsKey = Symbol() as InjectionKey<Ref<FilterGroups | null>>

async function fetchFilterDefinitions(): Promise<FilterDefinitions> {
  const collection = unwrap(await client.GET('/domain-types/visual_filter/collections/all'))
  const definitions: FilterDefinitions = {}
  collection.value.forEach((filter) => {
    definitions[filter.id!] = filter
  })
  return definitions
}

async function fetchFilterGroups(): Promise<FilterGroups> {
  const collection = unwrap(await client.GET('/domain-types/visual_filter_group/collections/all'))
  const groups: FilterGroups = {}
  collection.value.forEach((group) => {
    groups[group.id!] = group
  })
  return groups
}

/**
 * Provides the filter definitions and groups consumed by the filter components
 * (CmkFilterInputItem, CmkFilterDisplayItem, CmkFilterSelection, ...).
 *
 * Call this in an app root and load the definitions from the REST API via the
 * returned `loadFilterDefinitions`. Pass `initial` values instead when the
 * definitions are known upfront (e.g. pre-baked contexts that need no filters).
 */
export function useProvideFilterDefinitions(initial?: {
  definitions: FilterDefinitions
  groups: FilterGroups
}): {
  filterDefinitions: Ref<FilterDefinitions | null>
  filterGroups: Ref<FilterGroups | null>
  loadFilterDefinitions: () => Promise<void>
} {
  const filterDefinitions = ref<FilterDefinitions | null>(initial?.definitions ?? null)
  const filterGroups = ref<FilterGroups | null>(initial?.groups ?? null)
  provide(filterDefinitionsKey, filterDefinitions)
  provide(filterGroupsKey, filterGroups)

  const loadFilterDefinitions = async () => {
    const [definitions, groups] = await Promise.all([fetchFilterDefinitions(), fetchFilterGroups()])
    filterDefinitions.value = definitions
    filterGroups.value = groups
  }

  return { filterDefinitions, filterGroups, loadFilterDefinitions }
}

export function useFilterDefinitions(): FilterDefinitions {
  const filterDefinitions = inject(filterDefinitionsKey)
  if (!filterDefinitions) {
    throw new Error('No provider for filter definitions')
  }
  if (!filterDefinitions.value) {
    throw new Error('Filter definitions are not available yet')
  }
  return filterDefinitions.value
}

export function useFilterGroups(): FilterGroups {
  const filterGroups = inject(filterGroupsKey)
  if (!filterGroups) {
    throw new Error('No provider for filter groups')
  }
  if (!filterGroups.value) {
    throw new Error('Filter groups are not available yet')
  }
  return filterGroups.value
}
