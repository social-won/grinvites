"use client";

import { useEffect, useState } from "react";
import {
  ChevronLeft,
  ChevronRight,
  Check,
  Mail,
  SquareArrowOutUpRight,
  ChevronDown,
  ChevronRight as ChevronRightIcon,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { cn } from "@/lib/utils";
import { useNavigate } from "react-router-dom";
import { useUser } from "@/context/user-context";
import { getInterests, getUserInterests, getUserSchedule, updateUserInterests, updateUserSchedule } from "@/lib/api";
import { InviteScheduleForm, DAYS_OF_WEEK, formatScheduleTime } from "./invite-schedule-form";
import { Interest, GROUPS, GroupName } from "@/lib/types";

function interestsForGroup(groupName: GroupName, interests: Interest[]): Interest[] {
  return interests
    .filter((i) => i.groups?.includes(groupName))
    .sort((a, b) => a.formatted_name.localeCompare(b.formatted_name));
}

// ---------------------------------------------------------------------------
// Steps
// ---------------------------------------------------------------------------

const steps = [
  // { id: 0, title: "Class Schedule", description: "Select your classes" },
  { id: 0, title: "Interests", description: "Select organizations to follow" },
  { id: 1, title: "Invite Schedule", description: "Configure when to send invites" },
  { id: 2, title: "Email Setup", description: "Add Grinvites as a known sender" },
  { id: 3, title: "First Invite", description: "Check your calendar" },
];

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function OnboardingFlow() {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({
    selectedOrgs: [] as number[],
    orgSearch: "",
    inviteSchedule: {} as Record<string, string>,
  });
  const [collapsedGroups, setCollapsedGroups] = useState<Set<string>>(new Set(GROUPS));
  const [emailOpened, setEmailOpened] = useState(false);
  const [interestsArray, setInterestsArray] = useState<Interest[]>([]);


  const { user } = useUser();
  const navigate = useNavigate();

  useEffect(() => {
    getInterests().then(({ data }) => {

      if (data?.length) {
        setInterestsArray(data)
      }
    })
  }, [])

  useEffect(() => {
    if (!user) return;
    getUserInterests(user.id).then(({ data }) => {
      if (data) setFormData(prev => ({ ...prev, selectedOrgs: data.map(i => i.id) }));
    });
    getUserSchedule(user.id).then(({ data }) => {
      if (data) setFormData(prev => ({ ...prev, inviteSchedule: data.invite_times }));
    });
  }, [user]);




  const isNextDisabled = () => {
    if (currentStep === 1) return Object.keys(formData.inviteSchedule).length === 0;
    if (currentStep === 2) return !emailOpened;
    return false;
  };

  const handleNext = async () => {
    if (currentStep === 0 && user) {
      await updateUserInterests(user.id, formData.selectedOrgs);
    }
    else if (currentStep === 1 && user) {
      await updateUserSchedule(user.id, formData.inviteSchedule);
    }
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    } else {
      navigate("/home");
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) setCurrentStep(currentStep - 1);
  };

  const toggleOrg = (id: number) => {
    setFormData((prev) => {
      const next = prev.selectedOrgs.includes(id)
        ? prev.selectedOrgs.filter((o) => o !== id)
        : [...prev.selectedOrgs, id];
      return { ...prev, selectedOrgs: next };
    });
  };

  const toggleGroup = (groupName: GroupName) => {
    const ids = interestsForGroup(groupName, interestsArray).map((i) => i.id);
    const allSelected = ids.every((id) => formData.selectedOrgs.includes(id));
    setFormData((prev) => {
      const next = allSelected
        ? prev.selectedOrgs.filter((id) => !ids.includes(id))
        : [...new Set([...prev.selectedOrgs, ...ids])];
      return { ...prev, selectedOrgs: next };
    });
  };

  const toggleCollapse = (groupName: string) => {
    setCollapsedGroups((prev) => {
      const next = new Set(prev);
      next.has(groupName) ? next.delete(groupName) : next.add(groupName);
      return next;
    });
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 0: {
        const search = formData.orgSearch.toLowerCase();
        const isSearching = search.length > 0;

        const flatFiltered = isSearching
          ? interestsArray
            .filter((i) => i.formatted_name.toLowerCase().includes(search) || i.name.includes(search))
            .sort((a, b) => a.formatted_name.localeCompare(b.formatted_name))
          : null;

        return (
          <div className="space-y-4 w-full">
            <CardHeader className="px-0 pt-0">
              <CardTitle>What are you interested in?</CardTitle>
              <CardDescription>
                Select the organizations and departments you want to receive invites from
              </CardDescription>
            </CardHeader>

            <div className="flex gap-2">
              <Input
                placeholder="Search organizations..."
                value={formData.orgSearch}
                onChange={(e) => setFormData((p) => ({ ...p, orgSearch: e.target.value }))}
                autoFocus
              />
              <Button
                variant="outline"
                // size="sm"
                className="shrink-0"
                onClick={() => {
                  const allGroupNames = GROUPS.filter(g => interestsForGroup(g, interestsArray).length > 0);
                  const allCollapsed = allGroupNames.every(g => collapsedGroups.has(g));
                  setCollapsedGroups(allCollapsed ? new Set() : new Set(allGroupNames));
                }}
              >
                {GROUPS.filter(g => interestsForGroup(g, interestsArray).length > 0).every(g => collapsedGroups.has(g))
                  ? "Expand all"
                  : "Collapse all"}
              </Button>
            </div>

            <div className="border rounded-lg max-h-60 overflow-y-auto">
              {flatFiltered ? (
                flatFiltered.length > 0 ? (
                  flatFiltered.map((interest) => (
                    <div
                      key={interest.id}
                      className="flex items-center gap-3 px-3 py-2.5 border-b last:border-b-0 hover:bg-accent cursor-pointer"
                      onClick={() => toggleOrg(interest.id)}
                    >
                      <Checkbox
                        checked={formData.selectedOrgs.includes(interest.id)}
                        onCheckedChange={() => toggleOrg(interest.id)}
                        onClick={(e) => e.stopPropagation()}
                      />
                      <div className="flex-1 min-w-0">
                        <span className="text-sm">{interest.formatted_name}</span>
                        {/* <span className="ml-2 text-xs text-muted-foreground">
                          {interest.groups?.join(", ")}
                        </span> */}
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="p-4 text-center text-sm text-muted-foreground">No results</div>
                )
              ) : (
                GROUPS.map((groupName) => {
                  const orgs = interestsForGroup(groupName, interestsArray);
                  if (orgs.length === 0) return null;
                  const selectedCount = orgs.filter((i) => formData.selectedOrgs.includes(i.id)).length;
                  const allSelected = selectedCount === orgs.length;
                  const someSelected = selectedCount > 0 && !allSelected;
                  const collapsed = collapsedGroups.has(groupName);

                  return (
                    <div key={groupName}>
                      <div className="flex items-center gap-2 px-3 py-2 bg-muted border-b sticky top-0">
                        <Checkbox
                          checked={someSelected ? "indeterminate" : allSelected}
                          onCheckedChange={() => toggleGroup(groupName)}
                          onClick={(e) => e.stopPropagation()}
                        />
                        <button
                          type="button"
                          className="flex items-center gap-1.5 flex-1 text-left"
                          onClick={() => toggleCollapse(groupName)}
                        >
                          <span className="text-sm font-medium">{groupName}</span>
                          {selectedCount > 0 && (
                            <span className="text-xs text-muted-foreground">({selectedCount})</span>
                          )}
                          <span className="ml-auto text-muted-foreground">
                            {collapsed
                              ? <ChevronRightIcon className="h-4 w-4" />
                              : <ChevronDown className="h-4 w-4" />
                            }
                          </span>
                        </button>
                      </div>
                      {!collapsed && orgs.map((interest) => (
                        <div
                          key={interest.id}
                          className="flex items-center gap-3 pl-8 pr-3 py-2.5 border-b last:border-b-0 hover:bg-accent cursor-pointer"
                          onClick={() => toggleOrg(interest.id)}
                        >
                          <Checkbox
                            checked={formData.selectedOrgs.includes(interest.id)}
                            onCheckedChange={() => toggleOrg(interest.id)}
                            onClick={(e) => e.stopPropagation()}
                          />
                          <span className="text-sm">{interest.formatted_name}</span>
                        </div>
                      ))}
                    </div>
                  );
                })
              )}
            </div>

            <div className="flex items-center gap-3">
              <p className="text-sm text-muted-foreground">
                {formData.selectedOrgs.length} total interests selected
              </p>
              <Button
                variant="ghost"
                size="xs"
                className={cn("text-primary", formData.selectedOrgs.length === 0 && "invisible")}
                onClick={() => setFormData((prev) => ({ ...prev, selectedOrgs: [] }))}
              >
                Clear selected
              </Button>
            </div>
          </div>
        );
      }

      case 1:
        return (
          <div className="space-y-6 w-full">
            <CardHeader className="px-0 pt-0">
              <CardTitle>When should we send your invites?</CardTitle>
              <CardDescription>
                Pick the days and times each week to receive your event invitations
              </CardDescription>
            </CardHeader>

            <InviteScheduleForm
              times={formData.inviteSchedule}
              onTimesChange={(times) => setFormData((prev) => ({ ...prev, inviteSchedule: times }))}
            />

            {Object.keys(formData.inviteSchedule).length > 0 && (
              <p className="text-sm text-muted-foreground mt-2">
                {DAYS_OF_WEEK.filter(({ short }) => short in formData.inviteSchedule).map(({ day, short }, i, arr) => (
                  <span key={short}>
                    <strong>{day}</strong> at <strong>{formatScheduleTime(formData.inviteSchedule[short] ?? "08:00")}</strong>
                    {i < arr.length - 1 ? ", " : ""}
                  </span>
                ))}
              </p>
            )}
          </div>
        );

      case 2:
        return (
          <div className="space-y-6 w-full">
            <CardHeader className="px-0 pt-0">
              <CardTitle>Make Grinvites a trusted sender</CardTitle>
              <CardDescription>
                Send the email below to us so invites don't end up in spam.
              </CardDescription>
            </CardHeader>

            <div className="flex flex-col items-center gap-4">
              <div className="rounded-full bg-primary/10 p-6">
                <Mail className="h-10 w-10 text-primary" />
              </div>
              <Button
                size="lg"
                onClick={() => {
                  const subject = encodeURIComponent("Ready to start getting invites");
                  const body = encodeURIComponent(
                    "Hi Grinvites,\n\nI'm ready to start getting invites!\n\nThanks"
                  );
                  window.location.href = `mailto:squirrel@grinvites.app?subject=${subject}&body=${body}`;
                  setEmailOpened(true);
                }}
              >
                <SquareArrowOutUpRight className="h-4 w-4" />
                Open email draft
              </Button>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6 w-full">
            <CardHeader className="px-0 pt-0">
              <CardTitle>Your first invite is on its way!</CardTitle>
              <CardDescription>
                We've sent you an invite. Open your calendar or email to accept it.
              </CardDescription>
            </CardHeader>

            <div className="flex flex-col items-center gap-2">
              <div className="flex gap-3 w-full border-t pt-6">
                <Button
                  variant="secondary"
                  className="flex-1"
                  onClick={() => {
                    const subject = encodeURIComponent("Ready to start getting invites");
                    const body = encodeURIComponent(
                      "Hi Grinvites,\n\nI'm ready to start getting invites!\n\nThanks"
                    );
                    window.location.href = `mailto:squirrel@grinvites.app?subject=${subject}&body=${body}`;
                  }}
                >
                  <Mail className="mr-2 h-4 w-4" />
                  Resend invite
                </Button>
                <Button className="flex-1" onClick={() => navigate("/home")}>
                  Finish setup
                </Button>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="flex min-h-screen flex-col p-4 items-center justify-center">
      <Card className="w-full max-w-xl gap-6">
        <CardHeader className="md:px-12">
          <div className="flex items-start">
            {steps.map((step, i) => (
              <>
                <div
                  key={step.id}
                  className={cn("flex flex-col items-center gap-2 shrink-0 rounded-lg px-1 py-1 transition-colors", step.id <= currentStep && "cursor-pointer hover:bg-accent")}
                  onClick={() => step.id <= currentStep && setCurrentStep(step.id)}
                >
                  <div
                    className={cn(
                      "flex h-10 w-10 items-center justify-center rounded-full text-sm font-semibold transition-colors duration-300",
                      currentStep > step.id
                        ? "bg-sidebar-primary text-primary-foreground"
                        : currentStep === step.id
                          ? "bg-primary font-bold text-primary-foreground"
                          : "bg-gray-200 text-gray-600"
                    )}>
                    {currentStep > step.id ? <Check className="h-5 w-5" /> : step.id + 1}
                  </div>
                  <span className={cn(
                    "text-center text-xs font-medium w-16",
                    currentStep > step.id
                      ? "text-muted-foreground"
                      : currentStep === step.id
                        ? "font-bold text-sidebar-primary"
                        : "text-muted-foreground"
                  )}>
                    {step.title}
                  </span>
                </div>
                {i < steps.length - 1 && (
                  <div
                    key={`line-${step.id}`}
                    className={cn(
                      "h-0.5 flex-1 mt-5 transition-colors duration-300 bg-gray-200",
                      currentStep > step.id && "bg-sidebar-primary"
                    )}
                  />
                )}
              </>
            ))}
          </div>
        </CardHeader>

        <CardContent className="px-6 md:px-8">
          {renderStepContent()}

          {currentStep < 3 && (
            <div className="mt-4 flex items-center justify-between border-t pt-6">
              <Button variant="outline" onClick={handlePrevious} disabled={!currentStep}>
                <ChevronLeft className="h-4 w-4" />
                <span>Back</span>
              </Button>
              <Button onClick={handleNext} disabled={isNextDisabled()}>
                <span>Next</span>
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
