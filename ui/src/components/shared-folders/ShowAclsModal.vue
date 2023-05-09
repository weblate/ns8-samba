<!--
  Copyright (C) 2023 Nethesis S.r.l.
  SPDX-License-Identifier: GPL-3.0-or-later
-->
<template>
  <NsModal
    size="default"
    :visible="isShown"
    @modal-hidden="onModalHidden"
    @primary-click="onModalHidden"
  >
    <template slot="title">{{
      $t("shares.shared_folder_name_acls", { name: share ? share.name : "" })
    }}</template>
    <template slot="content">
      <div v-if="share" class="mg-top-md">
        <div
          v-for="(acl, index) in share.acls"
          :key="index"
          class="key-value-setting"
        >
          <span class="label">{{ acl.subject }}</span>
          <span class="value">
            {{ $t(`shares.acl_${acl.rights}`) }}
          </span>
        </div>
      </div>
    </template>
    <template slot="primary-button">{{ $t("common.close") }}</template>
  </NsModal>
</template>

<script>
import { UtilService, TaskService, IconService } from "@nethserver/ns8-ui-lib";

export default {
  name: "ShowAclsModal",
  mixins: [UtilService, TaskService, IconService],
  props: {
    isShown: Boolean,
    share: Object,
  },
  methods: {
    onModalHidden() {
      this.$emit("hide");
    },
    getAclColor(rights) {
      switch (rights) {
        case "ro":
          return "green";
        case "rw":
          return "red";
        case "full":
          return "high-contrast";
        default:
          return "blue";
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "../../styles/carbon-utils";
</style>
