/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { fireEvent, render, screen } from '@testing-library/vue'

import DeleteWithDependentsPopup from '@/graphing/designer/components/DeleteWithDependentsPopup.vue'

import { formulaItem } from '../fixtures'

// The dialog mounts its content on the open transition, so open starts false.
async function renderPopup(ids: string[] = ['D']) {
  const props = {
    open: false,
    ids,
    dependents: [formulaItem('F', { ast: { op: 'ref', id: 'D' } })]
  }
  const utils = render(DeleteWithDependentsPopup, { props })
  await utils.rerender({ ...props, open: true })
  return utils
}

test('lists the dependents that will be deleted as well', async () => {
  await renderPopup()
  expect(screen.getByText('Delete D?')).toBeInTheDocument()
  expect(screen.getByText(/F — = D/)).toBeInTheDocument()
})

test('names every row of a bulk deletion', async () => {
  await renderPopup(['A', 'B'])
  expect(screen.getByText('Delete A, B?')).toBeInTheDocument()
})

test('confirming emits confirm, cancelling emits close', async () => {
  const { emitted } = await renderPopup()
  await fireEvent.click(screen.getByRole('button', { name: 'Delete all' }))
  expect(emitted('confirm')).toHaveLength(1)

  await fireEvent.click(screen.getByRole('button', { name: 'Cancel' }))
  expect(emitted('close')).toHaveLength(1)
})
