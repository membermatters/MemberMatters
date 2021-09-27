<template>
  <div>
    <div class="text-left proxy-votes">
      <h5 class="q-ma-md">
        {{ $t("meetings.proxyVotes") }}
      </h5>
      <template v-if="proxies.length">
        <q-markup-table>
          <thead>
            <tr>
              <th class="text-left">
                {{ $t("meetings.memberName") }}
              </th>
              <th class="text-right">
                {{ $t("meetings.proxy") }}
              </th>
              <th class="text-right">
                {{ $t("meetings.dateAssigned") }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="proxy in proxies" :key="proxy.name">
              <td class="text-left">
                {{ proxy.name }}
              </td>
              <td class="text-right">
                {{ proxy.proxyName }}
              </td>
              <td class="text-right">
                {{ formatDate(proxy.date) }}
              </td>
            </tr>
          </tbody>
        </q-markup-table>
      </template>
      <div v-else class="q-pl-md">
        {{ $t("meetings.noProxies") }}
      </div>
    </div>

    <div class="text-left attendees">
      <h5 class="q-pa-md q-ma-none">
        {{ $t("meetings.attendees") }}
      </h5>
      <p class="q-px-md">
        <template v-if="attendees.length">
          <span v-for="member in attendees" :key="member"> {{ member }}, </span>
        </template>
        <template v-else>
          {{ $t("meetings.noAttendees") }}
        </template>
      </p>
    </div>
  </div>
</template>

<script>
import formatMixin from "src/mixins/formatMixin";

export default {
  name: "MeetingsDetails",
  mixins: [formatMixin],
  props: {
    attendees: {
      type: Array,
      default: () => [],
    },
    proxies: {
      type: Array,
      default: () => [],
    },
  },
};
</script>
