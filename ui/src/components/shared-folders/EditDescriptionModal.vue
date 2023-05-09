<!--
  Copyright (C) 2023 Nethesis S.r.l.
  SPDX-License-Identifier: GPL-3.0-or-later
-->
<template>
  <NsModal
    size="default"
    :visible="isShown"
    :primary-button-disabled="loading.alterShare"
    @modal-hidden="onModalHidden"
    @primary-click="alterShare"
  >
    <template slot="title">{{
      $t("shares.edit_shared_folder_description")
    }}</template>
    <template slot="content">
      <cv-form @submit.prevent="alterShare">
        <cv-text-input
          :label="
            $t('shares.description') + ' (' + core.$t('common.optional') + ')'
          "
          v-model.trim="newDescription"
          :placeholder="$t('shares.no_description')"
          ref="newDescription"
        >
        </cv-text-input>
        <div v-if="error.alterShare">
          <NsInlineNotification
            kind="error"
            :title="$t('action.alter-share')"
            :description="error.alterShare"
            :showCloseButton="false"
          />
        </div>
      </cv-form>
    </template>
    <template slot="secondary-button">{{ core.$t("common.cancel") }}</template>
    <template slot="primary-button">{{ $t("common.save") }}</template>
  </NsModal>
</template>

<script>
import { UtilService, TaskService, IconService } from "@nethserver/ns8-ui-lib";
import to from "await-to-js";
import { mapState } from "vuex";

export default {
  name: "EditDescriptionModal",
  mixins: [UtilService, TaskService, IconService],
  props: {
    isShown: Boolean,
    share: Object,
  },
  data() {
    return {
      newDescription: "",
      loading: {
        alterShare: false,
      },
      error: {
        alterShare: "",
        newDescription: "",
      },
    };
  },
  computed: {
    ...mapState(["instanceName", "core", "appName"]),
  },
  watch: {
    isShown: function () {
      if (this.isShown) {
        this.clearErrors();
        this.newDescription = this.share.description;

        setTimeout(() => {
          this.focusElement("newDescription");
        }, 300);
      }
    },
  },
  methods: {
    async alterShare() {
      this.loading.alterShare = true;
      this.error.alterShare = "";
      const taskAction = "alter-share";
      const eventId = this.getUuid();

      // register to task error
      this.core.$root.$once(
        `${taskAction}-aborted-${eventId}`,
        this.alterShareAborted
      );

      // register to task completion
      this.core.$root.$once(
        `${taskAction}-completed-${eventId}`,
        this.alterShareCompleted
      );

      const res = await to(
        this.createModuleTaskForApp(this.instanceName, {
          action: taskAction,
          data: {
            name: this.share.name,
            description: this.newDescription,
          },
          extra: {
            title: this.$t("shares.edit_shared_folder_description"),
            description: this.$t("common.processing"),
            eventId,
          },
        })
      );

      const err = res[0];
      if (err) {
        console.error(`error creating task ${taskAction}`, err);
        this.error.alterShare = this.getErrorMessage(err);
        this.loading.alterShare = false;
        return;
      }
    },
    alterShareAborted(taskResult, taskContext) {
      console.error(`${taskContext.action} aborted`, taskResult);
      this.loading.alterShare = false;
      // hide modal so that user can see error notification
      this.$emit("hide");
    },
    alterShareCompleted() {
      this.loading.alterShare = false;
      this.$emit("hide");
      this.$emit("descriptionUpdated");
    },
    onModalHidden() {
      this.clearErrors();
      this.$emit("hide");
    },
  },
};
</script>

<style scoped lang="scss">
@import "../../styles/carbon-utils";
</style>
