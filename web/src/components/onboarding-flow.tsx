"use client";

import { useState } from "react";
import {
  ChevronLeft,
  ChevronRight,
  Check,
  Mail,
  SquareArrowOutUpRight
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { cn } from "@/lib/utils";
import { useNavigate } from "react-router-dom";
import { FaMicrosoft, FaGoogle, FaApple } from "react-icons/fa";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "./ui/dialog";
import { useUser } from "@/context/user-context";
import { classesData, hoursData } from "@/lib/api";
import { InviteScheduleForm, DAYS_OF_WEEK, formatScheduleTime } from "./invite-schedule-form";

const steps = [
  // {
  //   id: 0,
  //   title: "Calendar Integration",
  //   description: "Connect your calendar"
  // },
  {
    id: 0,
    title: "Class Schedule",
    description: "Select your classes"
  },
  {
    id: 1,
    title: "Hours of Operation",
    description: "Select hours to watch"
  },
  {
    id: 2,
    title: "Invite Schedule",
    description: "Configure when to send invites"
  },
  {
    id: 3,
    title: "Email Setup",
    description: "Add Grinvites as a known sender"
  },
  {
    id: 4,
    title: "First Invite",
    description: "Check your calendar"
  }
];


export default function OnboardingFlow() {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({
    // calendarProvider: "", // google, apple, microsoft
    selectedClasses: [] as string[],
    selectedHours: [] as string[],
    classSearch: "",
    hoursSearch: "",
    inviteDays: [] as string[],
    inviteTimes: {} as Record<string, string>
  });

  const [emailOpened, setEmailOpened] = useState(false);

  const { user } = useUser();

  const isNextDisabled = () => {
    if (currentStep === 2) return formData.inviteDays.length === 0;
    if (currentStep === 3) return !emailOpened;
    return false;
  };

  const handleNext = () => {
    if (currentStep < 4) {
      setCurrentStep(currentStep + 1);
    } else {
      navigate("/home");
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const updateFormData = (field: string, value: string | boolean | string[]) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const toggleSelection = (id: string, field: "selectedClasses" | "selectedHours") => {
    setFormData((prev) => {
      const current = prev[field] as string[];
      const updated = current.includes(id)
        ? current.filter((item) => item !== id)
        : [...current, id];
      return { ...prev, [field]: updated };
    });
  };

  const navigate = useNavigate();

  const renderStepContent = () => {
    const filteredHours = hoursData.filter((hour) =>
      hour.name.toLowerCase().includes(formData.hoursSearch.toLowerCase())
    );

    switch (currentStep) {
      case 0:
        const filteredClasses = classesData.filter((cls) =>
          cls.name.toLowerCase().includes(formData.classSearch.toLowerCase())
        );

        return (
          <div className="space-y-6 w-full">
            <CardHeader className="px-0 pt-0">
              <CardTitle>Welcome! Add your class schedule here:</CardTitle>
              <CardDescription>
                Search and select the classes you want to track
              </CardDescription>
            </CardHeader>

            <div className="space-y-4">
              <Input
                placeholder="Search classes..."
                value={formData.classSearch}
                onChange={(e) => updateFormData("classSearch", e.target.value)}
                className="w-full"
              />

              <div className="border rounded-lg max-h-64 overflow-y-auto">
                {filteredClasses.map((cls) => (
                  <div
                    key={cls.id}
                    className="flex items-center gap-3 p-3 border-b last:border-b-0 hover:bg-gray-50 cursor-pointer"
                    onClick={() => toggleSelection(cls.id, "selectedClasses")}>
                    <Checkbox
                    // checked={formData.selectedClasses.includes(cls.id)}
                    // onCheckedChange={() => toggleSelection(cls.id, "selectedClasses")}
                    />
                    <label className="cursor-pointer flex-1">{cls.name}</label>
                  </div>
                ))}
                {filteredClasses.length === 0 && (
                  <div className="p-4 text-center text-gray-500">
                    No classes found
                  </div>
                )}
              </div>

              <div className="text-sm text-gray-600">
                Selected: {formData.selectedClasses.length} class{formData.selectedClasses.length > 1 ? "es" : ""}
              </div>
            </div>
          </div>
        );

      case 1:


        return (
          <div className="space-y-6 w-full">
            <CardHeader className="px-0 pt-0">
              <CardTitle>What hours do you want to monitor?</CardTitle>
              <CardDescription>
                Search and select the hours you want to track
              </CardDescription>
            </CardHeader>

            <div className="space-y-4">
              <Input
                placeholder="Search hours..."
                value={formData.hoursSearch}
                onChange={(e) => updateFormData("hoursSearch", e.target.value)}
                className="w-full"
              />

              <div className="border rounded-lg max-h-64 overflow-y-auto">
                {filteredHours.map((hour) => (
                  <div
                    key={hour.id}
                    className="flex items-center gap-3 p-3 border-b last:border-b-0 hover:bg-gray-50 cursor-pointer"
                    onClick={() => toggleSelection(hour.id, "selectedHours")}>
                    <Checkbox
                      checked={formData.selectedHours.includes(hour.id)}
                      onCheckedChange={() => toggleSelection(hour.id, "selectedHours")}
                    />
                    <label className="cursor-pointer flex-1">{hour.name}</label>
                  </div>
                ))}
                {filteredHours.length === 0 && (
                  <div className="p-4 text-center text-gray-500">
                    No hours found
                  </div>
                )}
              </div>

              <div className="text-sm text-gray-600">
                Selected: {formData.selectedHours.length} hour(s)
              </div>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6 w-full">
            <CardHeader className="px-0 pt-0">
              <CardTitle>When should we send your invites?</CardTitle>
              <CardDescription>
                Pick the days and times each week to receive your event invitations
              </CardDescription>
            </CardHeader>

            <InviteScheduleForm
                days={formData.inviteDays}
                times={formData.inviteTimes}
                onDaysChange={(days) => setFormData((prev) => ({ ...prev, inviteDays: days }))}
                onTimesChange={(times) => setFormData((prev) => ({ ...prev, inviteTimes: times }))}
              />

              {formData.inviteDays.length > 0 && (
                <p className="text-sm text-muted-foreground mt-2">
                  {DAYS_OF_WEEK.filter(({ short }) => formData.inviteDays.includes(short)).map(({ day, short }, i, arr) => (
                    <span key={short}>
                      <strong>{day}</strong> at <strong>{formatScheduleTime(formData.inviteTimes[short] ?? "08:00")}</strong>
                      {i < arr.length - 1 ? ", " : ""}
                    </span>
                  ))}
                </p>
              )}
          </div>
        );

      case 3:
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
              {/* <p className="text-center text-sm text-muted-foreground max-w-xs">
                Send the email below to <Link to="#">squirrel@grinvites.app</Link> so invites don't end up in spam.
              </p> */}
              <Button
                size="lg"
                // className="w-full"
                // variant={"secondary"}
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


      case 4:
        return (
          <div className="space-y-6 w-full">
            <CardHeader className="px-0 pt-0">
              <CardTitle>Your first invite is on its way!</CardTitle>
              <CardDescription>
                We've sent you an invite. Open your calendar or email to accept it.
              </CardDescription>
            </CardHeader>

            <div className="flex flex-col items-center gap-2">
              {/* <div className="rounded-full bg-primary/10 p-6">
                <Check className="h-10 w-10 text-primary" />
              </div>
              <p className="text-center text-sm text-muted-foreground max-w-sm">
                Check your inbox and calendar for a Grinvites invite.
              </p> */}
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
          {/* Step Indicator */}
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
                        ? "bg-sidebar-primary text-primary-foreground hover:brightness-110"
                        : currentStep === step.id
                          ? "bg-primary font-bold text-primary-foreground hover:brightness-110"
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

          {/* Navigation */}
          {currentStep < 4 && (
            <div className="mt-8 flex items-center justify-between border-t pt-6">
              <Button variant="outline" onClick={handlePrevious} disabled={!currentStep}>
                <ChevronLeft className="h-4 w-4" />
                <span>Back</span>
              </Button>

              <Button onClick={handleNext} disabled={isNextDisabled()}>
                <span>{currentStep === 3 ? "Next" : "Next"}</span>
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}