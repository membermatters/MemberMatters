import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';
import relativeTime from 'dayjs/plugin/relativeTime';
import duration from 'dayjs/plugin/duration';

dayjs.extend(duration);
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

export function formatDate(date: Date | number, time = true) {
  let parsedDate = date;
  // if it's earlier than 2000 it's clearly not been scaled to js time which is stored in milliseconds
  if (typeof date === 'number' && date < 9439200000) {
    parsedDate = date * 1000;
  }
  if (time) return dayjs(parsedDate).local().format('D MMM YYYY, h:mm a');
  return dayjs(parsedDate).local().format('D MMM YYYY');
}

export function formatDateSimple(date: Date, time = true) {
  if (time) return dayjs(date).local().format('DD/MM/YYYY, h:mm a');
  return dayjs(date).local().format('D/MMM/YYYY');
}

export function formatWhen(date: Date) {
  return dayjs(date).local().fromNow();
}

export function humanizeDurationOfSeconds(secondsToHumanize: number) {
  return dayjs.duration(secondsToHumanize, 'seconds').humanize();
}

export function humanizeDurationOfSecondsPrecise(secondsToHumanize: number) {
  const duration = dayjs.duration(secondsToHumanize, 'seconds');
  const days = duration.days();
  const hours = duration.hours();
  const minutes = duration.minutes();
  const seconds = duration.seconds();

  let formatted = '';
  if (days > 0) {
    formatted += `${days}d `;
  }
  if (hours > 0) {
    formatted += `${hours}h `;
  }
  if (minutes > 0) {
    formatted += `${minutes}m `;
  }
  if (seconds > 0) {
    formatted += `${seconds}s`;
  }

  return formatted;
}

export function formatBooleanYesNo(value: boolean) {
  // TODO: update to use vue-i18n translations
  return value ? 'Yes' : 'No';
}

export function capitaliseFirst(value: string) {
  return (
    String(value) && String(value)[0].toUpperCase() + String(value).slice(1)
  );
}

export function sortByFloat(a: string, b: string) {
  if (parseFloat(a) < parseFloat(b)) return -1;
  if (parseFloat(a) > parseFloat(b)) return 1;
  return 0;
}

export default {
  methods: {
    formatCsvList,
    formatDate,
    formatDateSimple,
    formatWhen,
    formatBooleanYesNo,
    capitaliseFirst,
    humanizeDurationOfSeconds,
    humanizeDurationOfSecondsPrecise,
    sortByFloat,
  },
};
