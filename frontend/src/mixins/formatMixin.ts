import * as dayjs from "dayjs";
import * as utc from "dayjs/plugin/utc";
import * as timezone from "dayjs/plugin/timezone";
import * as relativeTime from "dayjs/plugin/relativeTime";

dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.extend(relativeTime);
dayjs.tz.guess();

export function formatCsvList(list: Array<string>) {
  return list.map((x, i) => {
    if (list.length === i + 1) return x;
    return `${x}, `;
  });
}

export function formatDate(date: Date, time = true) {
  if (time) return dayjs(date).local().format("D MMM YYYY, h:mm a");
  return dayjs(date).local().format("D MMM YYYY");
}

export function formatDateSimple(date: Date, time = true) {
  if (time) return dayjs(date).local().format("DD/MM/YY, h:mm a");
  return dayjs(date).local().format("Do MMM YYYY");
}

export function formatWhen(date: Date) {
  return dayjs(date).local().fromNow();
}

export function capitaliseFirst(value: string) {
  return (
    String(value) && String(value)[0].toUpperCase() + String(value).slice(1)
  );
}

export default {
  methods: {
    formatCsvList,
    formatDate,
    formatDateSimple,
    formatWhen,
    capitaliseFirst,
  },
};
