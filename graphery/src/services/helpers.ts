export function toLocalDateString(locale: string, dateString: string) {
  return new Intl.DateTimeFormat(locale).format(new Date(dateString));
}
