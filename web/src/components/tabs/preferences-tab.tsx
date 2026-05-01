import { FC, useEffect, useState } from 'react'
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
import {
  type Interest,
  getInterests,
  getUserInterests,
  getUserSchedule,
  updateUserInterests,
  updateUserSchedule,
} from '@/lib/api'

const PreferencesTab: FC = () => {
  const { user } = useUser()

  const [emailOpen, setEmailOpen] = useState(false)
  const [calendarEmail, setCalendarEmail] = useState(user?.email ?? '')
  const [calendarEmailDraft, setCalendarEmailDraft] = useState(calendarEmail)

  const [scheduleOpen, setScheduleOpen] = useState(false)
  const [inviteTimes, setInviteTimes] = useState<Record<string, string>>({})
  const [draftTimes, setDraftTimes] = useState<Record<string, string>>({})

  const [passwordOpen, setPasswordOpen] = useState(false)
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const [allInterests, setAllInterests] = useState<Interest[]>([])
  const [userInterestIds, setUserInterestIds] = useState<number[]>([])
  const [interestSearch, setInterestSearch] = useState('')

  useEffect(() => {
    if (!user) return
    getUserSchedule(user.id).then(({ data }) => {
      if (data) setInviteTimes(data.invite_times)
    })
    getUserInterests(user.id).then(({ data }) => {
      if (data) setUserInterestIds(data.map((i) => i.id))
    })
    getInterests().then(({ data }) => { if (data) setAllInterests(data) })
  }, [user])

  const toggleInterest = async (id: number) => {
    const next = userInterestIds.includes(id)
      ? userInterestIds.filter((i) => i !== id)
      : [...userInterestIds, id]
    setUserInterestIds(next)
    if (user) await updateUserInterests(user.id, next)
  }

  const scheduleSummary = scheduleToSummary(inviteTimes)

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
                  if (!scheduleOpen) setDraftTimes({ ...inviteTimes })
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
              times={draftTimes}
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
                onClick={async () => {
                  setInviteTimes({ ...draftTimes })
                  setScheduleOpen(false)
                  if (user) await updateUserSchedule(user.id, draftTimes)
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
        {(['class', 'department', 'athletics', 'club'] as const).map((type) => {
          const items = allInterests.filter((i) => i.type === type && userInterestIds.includes(i.id))
          if (items.length === 0) return null
          const label = { class: 'Classes', department: 'Departments', athletics: 'Athletics', club: 'Clubs' }[type]
          return (
            <div key={type} className="space-y-2">
              <h4 className="text-sm font-medium">{label}</h4>
              <div className="flex flex-wrap gap-2">
                {items.map((item) => (
                  <Badge key={item.id}>
                    <X className="h-3.5 w-3.5 cursor-pointer" onClick={() => toggleInterest(item.id)} />
                    {item.name}
                  </Badge>
                ))}
              </div>
            </div>
          )
        })}
        {userInterestIds.length === 0 && (
          <p className="text-sm text-muted-foreground">No interests added yet.</p>
        )}

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
              {allInterests
                .filter(({ name }) => name.toLowerCase().includes(interestSearch.toLowerCase()))
                .map((interest) => {
                  const added = userInterestIds.includes(interest.id)
                  return (
                    <button
                      key={interest.id}
                      type="button"
                      onClick={() => toggleInterest(interest.id)}
                      className="w-full flex items-center justify-between px-3 py-2.5 rounded-md text-sm hover:bg-accent transition-colors text-left"
                    >
                      <div>
                        <span>{interest.name}</span>
                        <span className="ml-2 text-xs text-muted-foreground capitalize">{interest.type}</span>
                      </div>
                      {added && <span className="text-xs text-muted-foreground shrink-0">Added</span>}
                    </button>
                  )
                })}
              {allInterests.length === 0 && (
                <p className="px-3 py-4 text-sm text-muted-foreground text-center">No interests available</p>
              )}
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
