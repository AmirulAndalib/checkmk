<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkDualList from 'cmk-ui-library/components/CmkDualList/CmkDualList.vue'
import { type DualListElement } from 'cmk-ui-library/components/CmkDualList/index.ts'
import { ref } from 'vue'

const availableRoles = ref<DualListElement[]>([
  { name: 'admin', title: 'Admin' },
  { name: 'editor', title: 'Editor' },
  { name: 'viewer', title: 'Viewer' }
])

const selectedRoles = ref<DualListElement[]>([availableRoles.value[2]!])
</script>

<template>
  <CmkDualList
    v-model="selectedRoles"
    :elements="availableRoles"
    title="Assign User Roles"
    width="medium"
  />
</template>
