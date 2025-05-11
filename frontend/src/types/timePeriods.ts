// Time period definition - not using an enum because of the null value
export const TIME_PERIODS = ["Morning", "Afternoon", "Evening"] as const;
export type TimePeriod = (typeof TIME_PERIODS)[number];
export type TimeOfDay = TimePeriod | null;

// UI options from TimeOfDay
export const TIME_OF_DAY_OPTIONS: { value: TimeOfDay; label: string }[] = [
  { value: null, label: "All Times" },
  ...TIME_PERIODS.map(period => ({
    value: period,
    label: period,
  })),
];
