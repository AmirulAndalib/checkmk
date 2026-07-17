/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { type ComputedRef, computed, ref } from 'vue'

import type { FormulaItem, ItemId } from '../types'
import type { GraphItemsStore } from './useGraphItems'

export interface PendingDelete {
  ids: readonly ItemId[]
  /** The formulas that (transitively) reference `ids` and are deleted along with them. */
  dependents: readonly FormulaItem[]
}

export interface DeleteWithDependents {
  /** The delete awaiting confirmation because formulas depend on the rows; null otherwise. */
  pending: ComputedRef<PendingDelete | null>
  /** Deletes directly when no formula references `ids`; otherwise stores them as `pending`. */
  request: (ids: readonly ItemId[]) => void
  /** Deletes the pending rows together with their dependents. */
  confirm: () => void
  cancel: () => void
}

/**
 * The delete flow shared by the metrics table and the calculation slideout.
 * @param onRemoved Called with the removed ids after every removal.
 */
export function useDeleteWithDependents(
  store: GraphItemsStore,
  onRemoved: (ids: readonly ItemId[]) => void = () => {}
): DeleteWithDependents {
  const pending = ref<PendingDelete | null>(null)

  function remove(ids: readonly ItemId[]): void {
    store.removeMany(ids)
    onRemoved(ids)
  }

  function request(ids: readonly ItemId[]): void {
    const idSet = new Set(ids)
    const dependentById = new Map(
      ids.flatMap((id) =>
        store.dependentsOf(id).map((dependent) => [dependent.id, dependent] as const)
      )
    )
    const dependents = [...dependentById.values()].filter((dependent) => !idSet.has(dependent.id))
    if (dependents.length === 0) {
      remove(ids)
    } else {
      pending.value = { ids: [...ids], dependents }
    }
  }

  function confirm(): void {
    if (pending.value !== null) {
      remove([...pending.value.ids, ...pending.value.dependents.map((dependent) => dependent.id)])
      pending.value = null
    }
  }

  function cancel(): void {
    pending.value = null
  }

  return { pending: computed(() => pending.value), request, confirm, cancel }
}
