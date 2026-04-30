import { cn } from '@/lib/utils'

export const DAYS_OF_WEEK = [
  { day: 'Monday', short: 'Mon', letter: 'M' },
  { day: 'Tuesday', short: 'Tue', letter: 'T' },
  { day: 'Wednesday', short: 'Wed', letter: 'W' },
  { day: 'Thursday', short: 'Thu', letter: 'Th' },
  { day: 'Friday', short: 'Fri', letter: 'F' },
  { day: 'Saturday', short: 'Sat', letter: 'S' },
  { day: 'Sunday', short: 'Sun', letter: 'Su' },
]

export const TIMES_OF_DAY = [
  { label: 'Morning', value: '08:00', sub: '8am' },
  { label: 'Midday', value: '12:00', sub: '12pm' },
  { label: 'Afternoon', value: '16:00', sub: '4pm' },
  { label: 'Evening', value: '20:00', sub: '8pm' },
]

export function formatScheduleTime(value: string): string {
  const [h, m] = value.split(':').map(Number)
  const hour12 = h % 12 === 0 ? 12 : h % 12
  const isPM = h >= 12
  return `${hour12}:${String(m).padStart(2, '0')} ${isPM ? 'PM' : 'AM'}`
}

export function scheduleToSummary(days: string[], times: Record<string, string>): string {
  return DAYS_OF_WEEK.filter(({ short }) => days.includes(short))
    .map(({ day, short }) => `${day} at ${formatScheduleTime(times[short] ?? '08:00')}`)
    .join(', ')
}

interface InviteScheduleFormProps {
  days: string[]
  times: Record<string, string>
  onDaysChange: (days: string[]) => void
  onTimesChange: (times: Record<string, string>) => void
}

export function InviteScheduleForm({ days, times, onDaysChange, onTimesChange }: InviteScheduleFormProps) {
  const toggleDay = (short: string) => {
    if (days.includes(short)) {
      const updatedTimes = { ...times }
      delete updatedTimes[short]
      onDaysChange(days.filter((d) => d !== short))
      onTimesChange(updatedTimes)
    } else {
      onDaysChange([...days, short])
      onTimesChange({ ...times, [short]: '08:00' })
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-1.5">
        <label className="text-sm font-medium">Days of the week</label>
        <div className="grid grid-cols-7 gap-1.5">
          {DAYS_OF_WEEK.map(({ short, letter }) => {
            const selected = days.includes(short)
            return (
              <button
                key={short}
                type="button"
                onClick={() => toggleDay(short)}
                className={cn(
                  'h-10 w-full rounded-md border text-sm font-medium transition-colors',
                  selected
                    ? 'bg-primary text-primary-foreground border-primary'
                    : 'bg-background text-foreground border-input hover:bg-accent'
                )}
              >
                <span className="hidden sm:inline">{short}</span>
                <span className="sm:hidden">{letter}</span>
              </button>
            )
          })}
        </div>
      </div>

      {days.length > 0 && (
        <div className="flex flex-col gap-3">
          <label className="text-sm font-medium">Time of day</label>
          {DAYS_OF_WEEK.filter(({ short }) => days.includes(short)).map(({ short, day }) => (
            <div key={short} className="flex flex-col gap-1.5">
              <span className="text-xs text-muted-foreground">{day}</span>
              <div className="grid grid-cols-4 gap-1.5">
                {TIMES_OF_DAY.map(({ label, value, sub }) => {
                  const selected = (times[short] ?? '08:00') === value
                  return (
                    <button
                      key={value}
                      type="button"
                      onClick={() => onTimesChange({ ...times, [short]: value })}
                      className={cn(
                        'flex flex-col items-center justify-center h-14 rounded-md border text-sm font-medium transition-colors',
                        selected
                          ? 'bg-primary text-primary-foreground border-primary'
                          : 'bg-background text-foreground border-input hover:bg-accent'
                      )}
                    >
                      <span>{label}</span>
                      <span className="text-xs opacity-70">{sub}</span>
                    </button>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
