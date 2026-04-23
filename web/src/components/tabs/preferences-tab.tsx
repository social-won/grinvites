import { FC, useState } from 'react'
import { Pencil, Plus, X } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Field, FieldLabel } from '@/components/ui/field'
import { useUser } from '@/context/user-context'
import { Badge } from '../ui/badge'
import { Button } from '../ui/button'
import { InviteScheduleForm, scheduleToSummary } from '../invite-schedule-form'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../ui/dialog'

const ALL_INTERESTS = [
  { category: 'classes', label: 'CSC-151 — Fundamentals of CS' },
  { category: 'classes', label: 'CSC-207 — Object-Oriented Design' },
  { category: 'classes', label: 'CSC-301 — Algorithm Analysis' },
  { category: 'classes', label: 'MAT-218 — Discrete Structures' },
  { category: 'classes', label: 'MAT-316 — Foundations of Analysis' },
  { category: 'classes', label: 'PHY-132 — General Physics II' },
  { category: 'classes', label: 'ANT-104 — Introduction to Anthropology' },
  { category: 'classes', label: 'ENG-120 — Writing for College' },
  { category: 'departments', label: 'Computer Science' },
  { category: 'departments', label: 'Mathematics' },
  { category: 'departments', label: 'Physics' },
  { category: 'departments', label: 'Art' },
  { category: 'departments', label: 'Sociology' },
  { category: 'departments', label: 'English' },
  { category: 'departments', label: 'History' },
  { category: 'departments', label: 'Biology' },
  { category: 'departments', label: 'Chemistry' },
  { category: 'departments', label: 'Psychology' },
  { category: 'athletics', label: 'Football' },
  { category: 'athletics', label: 'Basketball' },
  { category: 'athletics', label: 'Soccer' },
  { category: 'athletics', label: 'Track & Field' },
  { category: 'athletics', label: 'Swimming' },
  { category: 'athletics', label: 'Tennis' },
  { category: 'athletics', label: 'Volleyball' },
  { category: 'athletics', label: 'Cross Country' },
  { category: 'clubs', label: 'Brazilian Jiu-Jitsu' },
  { category: 'clubs', label: 'Campus Wide' },
  { category: 'clubs', label: 'Chess Club' },
  { category: 'clubs', label: 'Debate Team' },
  { category: 'clubs', label: 'Film Society' },
  { category: 'clubs', label: 'Hiking Club' },
  { category: 'clubs', label: 'Photography Club' },
  { category: 'clubs', label: 'Student Government' },
  { category: 'clubs', label: 'Robotics Club' },
  { category: 'clubs', label: 'Community Garden' },
] as const

const PreferencesTab: FC = () => {
  const { user } = useUser()

  const [emailOpen, setEmailOpen] = useState(false)
  const [calendarEmail, setCalendarEmail] = useState(user?.email ?? '')
  const [calendarEmailDraft, setCalendarEmailDraft] = useState(calendarEmail)

  const [scheduleOpen, setScheduleOpen] = useState(false)
  const [inviteDays, setInviteDays] = useState<string[]>(['Mon', 'Wed', 'Fri'])
  const [inviteTimes, setInviteTimes] = useState<Record<string, string>>({
    Mon: '08:00',
    Wed: '12:00',
    Fri: '08:00',
  })
  const [draftDays, setDraftDays] = useState(inviteDays)
  const [draftTimes, setDraftTimes] = useState(inviteTimes)

  const [passwordOpen, setPasswordOpen] = useState(false)
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const [watching, setWatching] = useState({
    classes: ['MAT-444', 'ANT-260', 'CSC-324'],
    departments: ['Art', 'Sociology', 'Computer Science'],
    athletics: ['Football', 'Track'],
    clubs: ['Brazilian Jujitsu', 'Campus Wide'],
  })

  const [interestSearch, setInterestSearch] = useState('')

  const addItem = (category: keyof typeof watching, item: string) => {
    setWatching((prev) => ({
      ...prev,
      [category]: prev[category].includes(item) ? prev[category] : [...prev[category], item],
    }))
  }

  const removeItem = (category: keyof typeof watching, item: string) => {
    setWatching((prev) => ({
      ...prev,
      [category]: prev[category].filter((i) => i !== item),
    }))
  }

  const scheduleSummary = scheduleToSummary(inviteDays, inviteTimes)

  return (
    <div className="p-6 space-y-6 w-full pb-24">

      {/* Invite Schedule */}
      <section className="space-y-3">
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-base font-semibold">Invite Schedule</h3>
              <button
                className="text-muted-foreground hover:text-foreground transition-colors"
                onClick={() => {
                  if (!scheduleOpen) {
                    setDraftDays([...inviteDays])
                    setDraftTimes({ ...inviteTimes })
                  }
                  setScheduleOpen((o) => !o)
                }}
              >
                <Pencil className="h-4 w-4" />
              </button>
            </div>
            <p className="text-sm text-muted-foreground mt-1">
              {scheduleSummary || 'No days selected'}
            </p>
          </div>
        </div>

        {scheduleOpen && (
          <div className="space-y-4 pt-1">
            <InviteScheduleForm
              days={draftDays}
              times={draftTimes}
              onDaysChange={setDraftDays}
              onTimesChange={setDraftTimes}
            />
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={() => setScheduleOpen(false)}
              >
                Cancel
              </Button>
              <Button
                onClick={() => {
                  setInviteDays([...draftDays])
                  setInviteTimes({ ...draftTimes })
                  setScheduleOpen(false)
                }}
              >
                Save
              </Button>
            </div>
          </div>
        )}
      </section>

      <div className="border-t" />

      {/* Current Interests */}
      <section className="space-y-4">
        <h3 className="text-base font-semibold">Current Interests</h3>
        {(['classes', 'departments', 'athletics', 'clubs'] as const).map((category) => (
          <div key={category} className="space-y-2">
            <h4 className="text-sm font-medium capitalize">{category}</h4>
            <div className="flex flex-wrap gap-2">
              {watching[category].map((item) => (
                <Badge key={item}>
                  <X
                    className="h-3.5 w-3.5 cursor-pointer"
                    onClick={() => removeItem(category, item)}
                  />
                  {item}
                </Badge>
              ))}
            </div>
          </div>
        ))}

        <Dialog onOpenChange={(open) => { if (!open) setInterestSearch('') }}>
          <DialogTrigger asChild>
            <Button variant="outline" className="w-full">
              <Plus className="h-4 w-4" />
              Add interests
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>Add interests</DialogTitle>
            </DialogHeader>
            <Input
              placeholder="Search classes, clubs, sports..."
              value={interestSearch}
              onChange={(e) => setInterestSearch(e.target.value)}
              autoFocus
            />
            <div className="overflow-y-auto max-h-96 -mx-6 px-6 space-y-1">
              {ALL_INTERESTS.filter(({ label }) =>
                label.toLowerCase().includes(interestSearch.toLowerCase())
              ).map(({ category, label }) => {
                const added = (watching[category as keyof typeof watching] as string[]).includes(label)
                return (
                  <button
                    key={`${category}-${label}`}
                    type="button"
                    onClick={() => addItem(category as keyof typeof watching, label)}
                    disabled={added}
                    className="w-full flex items-center justify-between px-3 py-2.5 rounded-md text-sm hover:bg-accent transition-colors disabled:opacity-40 disabled:cursor-default text-left"
                  >
                    <div>
                      <span>{label}</span>
                      <span className="ml-2 text-xs text-muted-foreground capitalize">{category}</span>
                    </div>
                    {added && <span className="text-xs text-muted-foreground">Added</span>}
                  </button>
                )
              })}
            </div>
          </DialogContent>
        </Dialog>
      </section>

      <div className="border-t" />

      {/* Change Email */}
      <section className="space-y-3">
        <div className="flex items-center gap-2">
          <h3 className="text-base font-semibold">Change Email</h3>
          <button
            className="text-muted-foreground hover:text-foreground transition-colors"
            onClick={() => {
              if (!emailOpen) setCalendarEmailDraft(calendarEmail)
              setEmailOpen((o) => !o)
            }}
          >
            <Pencil className="h-4 w-4" />
          </button>
        </div>
        <Input value={calendarEmail} readOnly className="text-muted-foreground" />
        {emailOpen && (
          <div className="space-y-3 pt-1">
            <Field>
              <FieldLabel htmlFor="cal-email">New email</FieldLabel>
              <Input
                id="cal-email"
                type="email"
                value={calendarEmailDraft}
                onChange={(e) => setCalendarEmailDraft(e.target.value)}
              />
            </Field>
            <p className="text-sm text-muted-foreground">
              This will change which email you get sent invitations to and may need to be reverified.
            </p>
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={() => setEmailOpen(false)}
              >
                Cancel
              </Button>
              <Button
                onClick={() => {
                  setCalendarEmail(calendarEmailDraft)
                  setEmailOpen(false)
                }}
              >
                Update email
              </Button>
            </div>
          </div>
        )}
      </section>

      <div className="border-t" />

      {/* Change Password */}
      <section className="space-y-3">
        <div className="flex items-center gap-2">
          <h3 className="text-base font-semibold">Change Password</h3>
          <button
            className="text-muted-foreground hover:text-foreground transition-colors"
            onClick={() => {
              if (passwordOpen) {
                setCurrentPassword('')
                setNewPassword('')
                setConfirmPassword('')
              }
              setPasswordOpen((o) => !o)
            }}
          >
            <Pencil className="h-4 w-4" />
          </button>
        </div>
        {passwordOpen && (
          <div className="space-y-3">
            <Field>
              <FieldLabel htmlFor="current-password">Current password</FieldLabel>
              <Input
                id="current-password"
                type="password"
                placeholder="••••••••"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
              />
            </Field>
            <div className="grid grid-cols-2 gap-3">
              <Field>
                <FieldLabel htmlFor="new-password">New password</FieldLabel>
                <Input
                  id="new-password"
                  type="password"
                  placeholder="••••••••"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                />
              </Field>
              <Field>
                <FieldLabel htmlFor="confirm-new-password">Confirm new password</FieldLabel>
                <Input
                  id="confirm-new-password"
                  type="password"
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </Field>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={() => {
                  setCurrentPassword('')
                  setNewPassword('')
                  setConfirmPassword('')
                  setPasswordOpen(false)
                }}
              >
                Cancel
              </Button>
              <Button
                disabled={!currentPassword || !newPassword || newPassword !== confirmPassword}
                onClick={() => {
                  setCurrentPassword('')
                  setNewPassword('')
                  setConfirmPassword('')
                  setPasswordOpen(false)
                }}
              >
                Update password
              </Button>
            </div>
          </div>
        )}
      </section>

    </div>
  )
}

export default PreferencesTab
