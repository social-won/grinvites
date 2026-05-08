import React, { FC, useEffect, useState } from 'react'
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
  getInterests,
  getUserInterests,
  getUserSchedule,
  updateUserEmail,
  updateUserInterests,
  updateUserSchedule,
  updateUserTheme,
} from '@/lib/api'
import { Interest, GROUPS, GroupName } from '@/lib/types'
import { ChevronDown, ChevronRight, Sun, Moon, Monitor } from 'lucide-react'
import { Checkbox } from '../ui/checkbox'
import { useTheme, Theme } from '@/context/theme-context'
import { cn } from '@/lib/utils'
import supabase from '@/lib/supabase'

function InterestRow({ interest, selected, onToggle, indent = false }: { interest: Interest; selected: boolean; onToggle: (id: number) => void; indent?: boolean }) {
  return (
    <div
      onClick={() => onToggle(interest.id)}
      className={`w-full flex items-center gap-3 py-2.5 pr-6 text-sm transition-colors cursor-pointer hover:bg-accent ${indent ? 'pl-10' : 'pl-6'}`}
    >
      <Checkbox checked={selected} onCheckedChange={() => onToggle(interest.id)} onClick={(e) => e.stopPropagation()} />
      <span>{interest.formatted_name}</span>
    </div>
  )
}

const PreferencesTab: FC = () => {
  const { user } = useUser()
  const { theme, setTheme } = useTheme()

  const [emailOpen, setEmailOpen] = useState(false)
  const [calendarEmail, setCalendarEmail] = useState(user?.email ?? '')
  const [calendarEmailDraft, setCalendarEmailDraft] = useState(calendarEmail)

  const [scheduleOpen, setScheduleOpen] = useState(false)
  const [inviteTimes, setInviteTimes] = useState<Record<string, string>>({})
  const [draftTimes, setDraftTimes] = useState<Record<string, string>>({})

  const [emailError, setEmailError] = useState('')
  const [emailSuccess, setEmailSuccess] = useState('')

  const [passwordOpen, setPasswordOpen] = useState(false)
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [passwordError, setPasswordError] = useState('')
  const [passwordSuccess, setPasswordSuccess] = useState('')

  const [allInterests, setAllInterests] = useState<Interest[]>([])
  const [userInterestIds, setUserInterestIds] = useState<number[]>([])
  const [interestDialogOpen, setInterestDialogOpen] = useState(false)
  const [draftInterestIds, setDraftInterestIds] = useState<number[]>([])
  const [interestSearch, setInterestSearch] = useState('')
  const [collapsedDialogGroups, setCollapsedDialogGroups] = useState<Set<GroupName>>(new Set(GROUPS))

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

  const removeInterest = async (id: number) => {
    const next = userInterestIds.filter((i) => i !== id)
    setUserInterestIds(next)
    if (user) await updateUserInterests(user.id, next)
  }

  const toggleDraftInterest = (id: number) => {
    setDraftInterestIds((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    )
  }

  const openInterestDialog = () => {
    setDraftInterestIds([...userInterestIds])
    setInterestSearch('')
    setCollapsedDialogGroups(new Set(GROUPS))
    setInterestDialogOpen(true)
  }

  const saveInterests = async () => {
    setUserInterestIds([...draftInterestIds])
    setInterestDialogOpen(false)
    if (user) await updateUserInterests(user.id, draftInterestIds)
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
        {userInterestIds.length === 0 ? (
          <p className="text-sm text-muted-foreground">No interests added yet.</p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {allInterests
              .filter((i) => userInterestIds.includes(i.id))
              .map((item) => (
                <Badge key={item.id} className="gap-1">
                  <button type="button" onClick={() => removeInterest(item.id)}>
                    <X className="h-3 w-3" />
                  </button>
                  {item.formatted_name}
                </Badge>
              ))}
          </div>
        )}

        <Dialog open={interestDialogOpen} onOpenChange={(open) => { if (!open) setInterestDialogOpen(false) }}>
          <DialogTrigger asChild>
            <Button variant="outline" className="w-full" onClick={openInterestDialog}>
              <Plus className="h-4 w-4" />
              Add interests
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-md flex flex-col gap-0 p-0">
            <DialogHeader className="px-6 pt-6 pb-4">
              <DialogTitle>Edit interests</DialogTitle>
            </DialogHeader>
            <div className="px-6 pb-3">
              <Input
                placeholder="Search departments, clubs, sports..."
                value={interestSearch}
                onChange={(e) => setInterestSearch(e.target.value)}
                autoFocus
              />
            </div>
            <div className="overflow-y-auto flex-1 max-h-96 border-y">
              {interestSearch ? (
                allInterests
                  .filter(({ formatted_name, name }) =>
                    formatted_name.toLowerCase().includes(interestSearch.toLowerCase()) ||
                    name.toLowerCase().includes(interestSearch.toLowerCase())
                  )
                  .sort((a, b) => a.formatted_name.localeCompare(b.formatted_name))
                  .map((interest) => (
                    <InterestRow key={interest.id} interest={interest} selected={draftInterestIds.includes(interest.id)} onToggle={toggleDraftInterest} />
                  ))
              ) : (
                GROUPS.map((group) => {
                  const items = allInterests
                    .filter((i) => i.groups?.includes(group))
                    .sort((a, b) => a.formatted_name.localeCompare(b.formatted_name))
                  if (items.length === 0) return null
                  const collapsed = collapsedDialogGroups.has(group)
                  const selectedCount = items.filter((i) => draftInterestIds.includes(i.id)).length
                  return (
                    <div key={group}>
                      <button
                        type="button"
                        className="w-full flex items-center gap-2 px-6 py-2 bg-muted text-sm font-medium text-left sticky top-0"
                        onClick={() => setCollapsedDialogGroups((prev) => {
                          const next = new Set(prev)
                          next.has(group) ? next.delete(group) : next.add(group)
                          return next
                        })}
                      >
                        {collapsed ? <ChevronRight className="h-3.5 w-3.5 shrink-0" /> : <ChevronDown className="h-3.5 w-3.5 shrink-0" />}
                        {group}
                        {selectedCount > 0 && (
                          <span className="text-xs text-muted-foreground font-normal">({selectedCount})</span>
                        )}
                      </button>
                      {!collapsed && items.map((interest) => (
                        <InterestRow key={interest.id} interest={interest} selected={draftInterestIds.includes(interest.id)} onToggle={toggleDraftInterest} indent />
                      ))}
                    </div>
                  )
                })
              )}
              {allInterests.length === 0 && (
                <p className="px-6 py-4 text-sm text-muted-foreground text-center">No interests available</p>
              )}
            </div>
            <div className="flex items-center justify-between gap-2 px-6 py-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => {
                  const nonEmptyGroups = GROUPS.filter(g => allInterests.some(i => i.groups?.includes(g)))
                  const allCollapsed = nonEmptyGroups.every(g => collapsedDialogGroups.has(g))
                  setCollapsedDialogGroups(allCollapsed ? new Set() : new Set(nonEmptyGroups))
                }}
              >
                {GROUPS.filter(g => allInterests.some(i => i.groups?.includes(g))).every(g => collapsedDialogGroups.has(g))
                  ? 'Expand all'
                  : 'Collapse all'}
              </Button>
              <div className="flex gap-2">
                <Button variant="outline" onClick={() => setInterestDialogOpen(false)}>Cancel</Button>
                <Button onClick={saveInterests}>Save</Button>
              </div>
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
                onChange={(e) => { setCalendarEmailDraft(e.target.value); setEmailError(''); setEmailSuccess('') }}
              />
            </Field>
            {emailError && <p className="text-sm text-destructive">{emailError}</p>}
            {emailSuccess && <p className="text-sm text-green-600">{emailSuccess}</p>}
            <p className="text-sm text-muted-foreground">
              This will change which email you get sent invitations to and may need to be reverified.
            </p>
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={() => { setEmailOpen(false); setEmailError(''); setEmailSuccess('') }}
              >
                Cancel
              </Button>
              <Button
                onClick={async () => {
                  setEmailError('')
                  setEmailSuccess('')
                  const { error } = await supabase.auth.updateUser({ email: calendarEmailDraft }, {emailRedirectTo: `${window.location.origin}/home`})
                  if (error) { setEmailError(error.message); return }
                  setCalendarEmail(calendarEmailDraft)
                  if (user) await updateUserEmail(user.id, calendarEmailDraft)
                  setEmailSuccess('Check your new inbox for a confirmation link.')
                  // setEmailOpen(false)
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
                onChange={(e) => { setCurrentPassword(e.target.value); setPasswordError(''); setPasswordSuccess('') }}
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
                  onChange={(e) => { setNewPassword(e.target.value); setPasswordError(''); setPasswordSuccess('') }}
                />
              </Field>
              <Field>
                <FieldLabel htmlFor="confirm-new-password">Confirm new password</FieldLabel>
                <Input
                  id="confirm-new-password"
                  type="password"
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => { setConfirmPassword(e.target.value); setPasswordError(''); setPasswordSuccess('') }}
                />
              </Field>
            </div>
            {confirmPassword && newPassword !== confirmPassword && (
              <p className="text-sm text-destructive">Passwords do not match.</p>
            )}
            {passwordError && <p className="text-sm text-destructive">{passwordError}</p>}
            {passwordSuccess && <p className="text-sm text-green-600">{passwordSuccess}</p>}
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={() => {
                  setCurrentPassword('')
                  setNewPassword('')
                  setConfirmPassword('')
                  setPasswordError('')
                  setPasswordSuccess('')
                  setPasswordOpen(false)
                }}
              >
                Cancel
              </Button>
              <Button
                disabled={!currentPassword || !newPassword || newPassword !== confirmPassword}
                onClick={async () => {
                  setPasswordError('')
                  setPasswordSuccess('')
                  const { error: signInError } = await supabase.auth.signInWithPassword({
                    email: calendarEmail,
                    password: currentPassword,
                  })
                  if (signInError) { setPasswordError('Current password is incorrect.'); return }
                  const { error } = await supabase.auth.updateUser({ password: newPassword })
                  if (error) { setPasswordError(error.message); return }
                  setCurrentPassword('')
                  setNewPassword('')
                  setConfirmPassword('')
                  setPasswordSuccess('Password updated successfully.')
                  setPasswordOpen(false)
                }}
              >
                Update password
              </Button>
            </div>
          </div>
        )}
      </section>

      <div className="border-t" />

      {/* Theme */}
      <section className="space-y-3">
        <h3 className="text-base font-semibold">Theme</h3>
        <div className="flex gap-2">
          {([
            { value: 'light', label: 'Light', icon: Sun },
            { value: 'system', label: 'System', icon: Monitor },
            { value: 'dark', label: 'Dark', icon: Moon },
          ] as { value: Theme; label: string; icon: React.FC<{ className?: string }> }[]).map(({ value: t, label, icon: Icon }) => (
            <button
              key={t}
              type="button"
              onClick={async () => {
                setTheme(t)
                if (user) await updateUserTheme(user.id, t)
              }}
              className={cn(
                'flex-1 flex items-center justify-center gap-1.5 rounded-md border py-2 text-sm font-medium transition-colors',
                theme === t
                  ? 'bg-primary text-primary-foreground border-primary'
                  : 'bg-background text-foreground border-input hover:bg-accent'
              )}
            >
              <Icon className="h-4 w-4" />
              {label}
            </button>
          ))}
        </div>
      </section>

    </div>
  )
}

export default PreferencesTab
