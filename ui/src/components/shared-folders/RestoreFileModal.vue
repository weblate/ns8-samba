<!--
  Copyright (C) 2024 Nethesis S.r.l.
  SPDX-License-Identifier: GPL-3.0-or-later
-->
<template>
  <NsWizard
    size="default"
    :visible="isShown"
    :cancelLabel="$t('common.cancel')"
    :previousLabel="$t('common.previous')"
    :nextLabel="isLastStep ? $t('shares.restore') : $t('common.next')"
    :isPreviousDisabled="isFirstStep || loading.restoreBackupContent"
    :isNextDisabled="isNextButtonDisabled"
    :isNextLoading="loading.restoreBackupContent"
    @modal-shown="onModalShown"
    @modal-hidden="$emit('hide')"
    @cancel="$emit('hide')"
    @previousStep="previousStep"
    @nextStep="nextStep"
  >
    <template slot="title">{{ $t("shares.restore_file_or_folder") }}</template>
    <template slot="content">
      <cv-form @submit.prevent="nextStep">
        <template v-if="step == 'repository'">
          <div class="mg-bottom-md">
            {{ $t("shares.select_backup_destination") }}
          </div>
          <!-- listBackupRepositories error -->
          <NsInlineNotification
            v-if="error.listBackupRepositories"
            kind="error"
            :title="$t('action.list-backup-repositories')"
            :description="error.listBackupRepositories"
            :showCloseButton="false"
          />
          <cv-grid class="mg-top-lg mg-bottom-md no-padding">
            <cv-row>
              <cv-column>
                <BackupRepositorySelector
                  v-model="selectedRepositoryId"
                  :repositories="backupRepositories"
                  :instanceName="instanceName"
                  :loading="loading.listBackupRepositories"
                  :light="true"
                />
              </cv-column>
            </cv-row>
          </cv-grid>
        </template>
        <template v-if="step == 'snapshot'">
          <div>
            {{ $t("shares.select_backup_snapshot") }}
          </div>
          <!-- readBackupSnapshots error -->
          <NsInlineNotification
            v-if="error.readBackupSnapshots"
            kind="error"
            :title="$t('action.read-backup-snapshots')"
            :description="error.readBackupSnapshots"
            :showCloseButton="false"
          />
          <cv-grid class="mg-top-lg mg-bottom-md no-padding">
            <cv-row>
              <cv-column>
                <BackupSnapshotSelector
                  v-model="selectedSnapshotId"
                  :snapshots="backupSnapshots"
                  :loading="loading.readBackupSnapshots"
                  :light="true"
                />
              </cv-column>
            </cv-row>
          </cv-grid>
        </template>
        <template v-if="step == 'file'">
          <div>
            {{ $t("shares.select_file_or_folder_to_restore") }}
          </div>
          <NsComboSearchBox
            v-model="fileQuery"
            :results="fileSearchResults"
            :resultsLimitReached="resultsLimitReached"
            :loadingResults="loading.seekSnapshotContents"
            auto-highlight
            :placeholder="$t('shares.search_file_or_folder')"
            :invalid-message="error.group"
            light
            :clearFilterLabel="$t('ns_combo_search_box.clear_search')"
            :noResultsLabel="$t('ns_combo_search_box.no_results')"
            :resultsLimitReachedLabel="
              $t('ns_combo_search_box.results_limit_reached')
            "
            ref="fileSearch"
            class="mg-top-xlg"
            @change="selectedFile = $event"
            @search="seekSnapshotContents"
          />
          <!-- seekSnapshotContents error -->
          <NsInlineNotification
            v-if="error.seekSnapshotContents"
            kind="error"
            :title="$t('action.seek-snapshot-contents')"
            :description="error.seekSnapshotContents"
            :showCloseButton="false"
          />
          <NsInlineNotification
            kind="info"
            :description="
              $t('shares.restore_file_info', {
                restoredFolder: 'Restored folder',
                node: installationNodeLabel,
              })
            "
            :showCloseButton="false"
            class="mb-9"
          />
          <!-- restoreBackupContent error -->
          <NsInlineNotification
            v-if="error.restoreBackupContent"
            kind="error"
            :title="$t('action.restore-backup-content')"
            :description="error.restoreBackupContent"
            :showCloseButton="false"
          />
        </template>
      </cv-form>
    </template>
  </NsWizard>
</template>

<script>
import {
  UtilService,
  TaskService,
  IconService,
  NsComboSearchBox,
} from "@nethserver/ns8-ui-lib";
import to from "await-to-js";
import { mapState } from "vuex";
import BackupRepositorySelector from "./BackupRepositorySelector.vue";
import BackupSnapshotSelector from "./BackupSnapshotSelector.vue";

export default {
  name: "RestoreFileModal",
  components: {
    BackupRepositorySelector,
    BackupSnapshotSelector,
    NsComboSearchBox,
  },
  mixins: [UtilService, TaskService, IconService],
  props: {
    isShown: {
      type: Boolean,
      default: true,
    },
    shareName: String,
  },
  data() {
    return {
      step: "",
      steps: ["repository", "snapshot", "file"],
      backupRepositories: [],
      backupSnapshots: [],
      selectedRepositoryId: "",
      selectedSnapshotId: "",
      selectedFile: "",
      fileQuery: "",
      fileSearchResults: [],
      resultsLimitReached: false,
      status: null,
      loading: {
        listBackupRepositories: true,
        restoreBackupContent: false,
        readBackupSnapshots: false,
        getStatus: false,
        seekSnapshotContents: false,
      },
      error: {
        listBackupRepositories: "",
        restoreBackupContent: "",
        readBackupSnapshots: "",
        getStatus: "",
        seekSnapshotContents: "",
      },
    };
  },
  computed: {
    ...mapState(["instanceName", "core"]),
    stepIndex() {
      return this.steps.indexOf(this.step);
    },
    isFirstStep() {
      return this.stepIndex == 0;
    },
    isLastStep() {
      return this.stepIndex == this.steps.length - 1;
    },
    isNextButtonDisabled() {
      return (
        this.loading.restoreBackupContent ||
        (this.step == "repository" && !this.selectedRepositoryId) ||
        (this.step == "snapshot" && !this.selectedSnapshotId) ||
        (this.step == "file" && !this.selectedFile)
      );
    },
    selectedRepository() {
      return this.backupRepositories.find(
        (repo) => repo.repository_id === this.selectedRepositoryId
      );
    },
    installationNodeLabel() {
      if (this.status) {
        if (this.status.node_ui_name) {
          return this.status.node_ui_name;
        } else {
          return `${this.$t("status.node")} ${this.status.node}`;
        }
      } else {
        return "-";
      }
    },
  },
  watch: {
    step: function () {
      if (this.step == "repository") {
        this.selectedRepositoryId = "";
      } else if (this.step == "snapshot") {
        this.selectedSnapshotId = "";
        this.readBackupSnapshots();
      } else if (this.step == "file") {
        this.selectedFile = "";
        this.getStatus();
      }
    },
  },
  methods: {
    nextStep() {
      if (this.isNextButtonDisabled) {
        return;
      }

      if (this.isLastStep) {
        this.restoreBackupContent();
      } else {
        this.step = this.steps[this.stepIndex + 1];
      }
    },
    previousStep() {
      if (!this.isFirstStep) {
        this.step = this.steps[this.stepIndex - 1];
      }
    },
    onModalShown() {
      // show first step
      this.step = this.steps[0];
      this.selectedRepositoryId = "";
      this.listBackupRepositories();
    },
    async listBackupRepositories() {
      this.loading.listBackupRepositories = true;
      this.error.listBackupRepositories = "";
      const taskAction = "list-backup-repositories";
      const eventId = this.getUuid();

      // register to task error
      this.core.$root.$once(
        `${taskAction}-aborted-${eventId}`,
        this.listBackupRepositoriesAborted
      );

      // register to task completion
      this.core.$root.$once(
        `${taskAction}-completed-${eventId}`,
        this.listBackupRepositoriesCompleted
      );

      const res = await to(
        this.createModuleTaskForApp(this.instanceName, {
          action: taskAction,
          extra: {
            title: this.$t("action." + taskAction),
            isNotificationHidden: true,
            eventId,
          },
        })
      );
      const err = res[0];

      if (err) {
        console.error(`error creating task ${taskAction}`, err);
        this.error.listBackupRepositories = this.getErrorMessage(err);
        this.loading.listBackupRepositories = false;
        return;
      }
    },
    listBackupRepositoriesAborted(taskResult, taskContext) {
      console.error(`${taskContext.action} aborted`, taskResult);
      this.error.listBackupRepositories = this.$t("error.generic_error");
      this.loading.listBackupRepositories = false;
    },
    listBackupRepositoriesCompleted(taskContext, taskResult) {
      let backupRepositories = taskResult.output;

      // sort repositories by name
      backupRepositories.sort(this.sortByProperty("repository_name"));
      this.backupRepositories = backupRepositories;

      // select the first repository if there is only one
      if (this.backupRepositories.length == 1) {
        this.selectedRepositoryId = this.backupRepositories[0].repository_id;
      }
      this.loading.listBackupRepositories = false;
    },
    async readBackupSnapshots() {
      this.error.readBackupSnapshots = "";
      this.loading.readBackupSnapshots = true;
      const taskAction = "read-backup-snapshots";

      // register to task error
      this.core.$root.$off(taskAction + "-aborted");
      this.core.$root.$once(
        taskAction + "-aborted",
        this.readBackupSnapshotsAborted
      );

      // register to task completion
      this.core.$root.$off(taskAction + "-completed");
      this.core.$root.$once(
        taskAction + "-completed",
        this.readBackupSnapshotsCompleted
      );

      const res = await to(
        this.createClusterTaskForApp({
          action: taskAction,
          data: {
            repository: this.selectedRepositoryId,
            path: this.selectedRepository.path,
          },
          extra: {
            title: this.$t("action." + taskAction),
            isNotificationHidden: true,
          },
        })
      );
      const err = res[0];

      if (err) {
        console.error(`error creating task ${taskAction}`, err);
        this.error.readBackupSnapshots = this.getErrorMessage(err);
        this.loading.readBackupSnapshots = false;
        return;
      }
    },
    readBackupSnapshotsAborted(taskResult, taskContext) {
      console.error(`${taskContext.action} aborted`, taskResult);
      this.error.readBackupSnapshots = this.$t("error.generic_error");
      this.loading.readBackupSnapshots = false;
    },
    readBackupSnapshotsCompleted(taskContext, taskResult) {
      let snapshots = taskResult.output;

      // sort snapshots by timestamp descending (most recent first)
      snapshots.sort(this.sortByProperty("timestamp")).reverse();
      this.backupSnapshots = snapshots;

      // select the first snapshot if there is only one
      if (this.backupSnapshots.length == 1) {
        this.selectedSnapshotId = this.backupSnapshots[0].id;
      }
      this.loading.readBackupSnapshots = false;
    },
    async restoreBackupContent() {
      this.loading.restoreBackupContent = true;
      this.error.restoreBackupContent = "";
      const taskAction = "restore-backup-content";
      const eventId = this.getUuid();

      // register to task error
      this.$root.$off(taskAction + "-aborted");
      this.$root.$once(
        `${taskAction}-aborted-${eventId}`,
        this.restoreBackupContentAborted
      );

      // register to task completion
      this.$root.$off(taskAction + "-completed");
      this.$root.$once(
        `${taskAction}-completed-${eventId}`,
        this.restoreBackupContentCompleted
      );

      const res = await to(
        this.createModuleTaskForApp(this.instanceName, {
          action: taskAction,
          data: {
            snapshot: this.selectedSnapshotId,
            destination: this.selectedRepositoryId,
            repopath: this.selectedRepository.path,
            share: this.shareName,
            content: this.selectedFile,
          },
          extra: {
            title: this.$t("action." + taskAction),
            description: this.$t("shares.restoring_to_share_name", {
              name: this.shareName,
            }),
          },
        })
      );
      const err = res[0];

      if (err) {
        console.error(`error creating task ${taskAction}`, err);
        this.error.restoreBackupContent = this.getErrorMessage(err);
        this.loading.restoreBackupContent = false;
        return;
      }

      // close modal immediately, no validation needed
      this.$emit("hide");
      this.loading.restoreBackupContent = false;
      this.fileQuery = "";
    },
    restoreBackupContentAborted(taskResult, taskContext) {
      console.error(`${taskContext.action} aborted`, taskResult);
      this.error.restoreBackupContent = this.$t("error.generic_error");
      this.loading.restoreBackupContent = false;
    },
    restoreBackupContentCompleted() {
      this.loading.restoreBackupContent = false;
    },
    async getStatus() {
      this.loading.getStatus = true;
      this.error.getStatus = "";
      const taskAction = "get-status";
      const eventId = this.getUuid();

      // register to task error
      this.core.$root.$once(
        `${taskAction}-aborted-${eventId}`,
        this.getStatusAborted
      );

      // register to task completion
      this.core.$root.$once(
        `${taskAction}-completed-${eventId}`,
        this.getStatusCompleted
      );

      const res = await to(
        this.createModuleTaskForApp(this.instanceName, {
          action: taskAction,
          extra: {
            title: this.$t("action." + taskAction),
            isNotificationHidden: true,
            eventId,
          },
        })
      );
      const err = res[0];

      if (err) {
        console.error(`error creating task ${taskAction}`, err);
        this.error.getStatus = this.getErrorMessage(err);
        this.loading.getStatus = false;
        return;
      }
    },
    getStatusAborted(taskResult, taskContext) {
      console.error(`${taskContext.action} aborted`, taskResult);
      this.error.getStatus = this.$t("error.generic_error");
      this.loading.getStatus = false;
    },
    getStatusCompleted(taskContext, taskResult) {
      this.status = taskResult.output;
      this.loading.getStatus = false;
    },
    async seekSnapshotContents(textQuery) {
      this.loading.seekSnapshotContents = true;
      this.error.seekSnapshotContents = "";
      const taskAction = "seek-snapshot-contents";
      const eventId = this.getUuid();

      // register to task error
      this.core.$root.$once(
        `${taskAction}-aborted-${eventId}`,
        this.seekSnapshotContentsAborted
      );

      // register to task completion
      this.core.$root.$once(
        `${taskAction}-completed-${eventId}`,
        this.seekSnapshotContentsCompleted
      );

      const res = await to(
        this.createModuleTaskForApp(this.instanceName, {
          action: taskAction,
          data: {
            snapshot: this.selectedSnapshotId,
            destination: this.selectedRepositoryId,
            repopath: this.selectedRepository.path,
            share: this.shareName,
            limit: 50,
            query: textQuery,
          },
          extra: {
            title: this.$t("action." + taskAction),
            isNotificationHidden: true,
            eventId,
          },
        })
      );
      const err = res[0];

      if (err) {
        console.error(`error creating task ${taskAction}`, err);
        this.error.seekSnapshotContents = this.getErrorMessage(err);
        this.loading.seekSnapshotContents = false;
        return;
      }
    },
    seekSnapshotContentsAborted(taskResult, taskContext) {
      console.error(`${taskContext.action} aborted`, taskResult);
      this.error.seekSnapshotContents = this.$t("error.generic_error");
      this.loading.seekSnapshotContents = false;
    },
    seekSnapshotContentsCompleted(taskContext, taskResult) {
      this.fileSearchResults = taskResult.output.contents.map((item) => ({
        name: item,
        label: item,
        value: item,
      }));

      this.resultsLimitReached = taskResult.output.limit_reached;
      this.loading.seekSnapshotContents = false;
    },
  },
};
</script>

<style scoped lang="scss">
.mb-9 {
  margin-bottom: 9rem;
}
</style>
