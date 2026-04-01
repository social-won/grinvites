"use client";

import { useState } from "react";
import {
  ChevronLeft,
  ChevronRight,
  Check
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
import { classesData, hoursData } from "@/api";

const steps = [
  {
    id: 1,
    title: "Calendar Integration",
    description: "Connect your calendar"
  },
  {
    id: 2,
    title: "Class Schedule",
    description: "Select your classes"
  },
  {
    id: 3,
    title: "Hours of Operation",
    description: "Select hours to watch"
  }
];

export default function OnboardingFlow() {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    calendarProvider: "", // google, apple, microsoft
    selectedClasses: [] as string[],
    selectedHours: [] as string[],
    classSearch: "",
    hoursSearch: ""
  });

  const [connected, setConnected ] = useState(false);

  const { user } = useUser();

  // Mock data - in real app, this would come from API calls

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    } else {
      console.log(formData);
      
      navigate("/home");
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
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
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6 w-full">
            <CardHeader className="px-0 pt-0">
              <CardTitle>What calendar do you want to connect?</CardTitle>
              <CardDescription>
                Select your calendar provider to sync your schedule
              </CardDescription>
            </CardHeader>

            <div className="flex items-center gap-3 flex-col">
              <Button variant="secondary" type="button" className="w-full max-w-sm">
                <FaApple />
                Login with Apple
              </Button>
              <Dialog>
                <DialogTrigger asChild>
                  <Button variant="secondary" type="button" className="w-full max-w-sm" onClick={() => setConnected(true)}>
                    <FaGoogle />
                    Login with Google
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Connection Successful</DialogTitle>
                    <DialogDescription>
                      Connected to {user?.email}
                    </DialogDescription> 
                    <Button onClick={handleNext}>
                      Next
                      <ChevronRight className="h-4 w-4" />
                    </Button>
                  </DialogHeader>
                </DialogContent>
              </Dialog>

              <Button variant="secondary" type="button" className="w-full max-w-sm">
                <FaMicrosoft />
                Login with Microsoft
              </Button>
            </div>
          </div>
        );

      case 2:
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
                      checked={formData.selectedClasses.includes(cls.id)}
                      onCheckedChange={() => toggleSelection(cls.id, "selectedClasses")}
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

      case 3:
        const filteredHours = hoursData.filter((hour) =>
          hour.name.toLowerCase().includes(formData.hoursSearch.toLowerCase())
        );

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

      default:
        return null;
    }
  };

  return (
    <div className="flex items-center justify-center p-4">
      <Card className="w-screen max-w-3xl shadow-lg">
        <CardHeader className="pb-0">
          {/* Step Indicator */}
          <div className="mb-6 flex items-center justify-between">
            {steps.map((step) => (
              <div key={step.id} className="relative flex flex-1 flex-col items-center">
                <div
                  className={cn(
                    "flex h-10 w-10 items-center justify-center rounded-full text-sm font-semibold transition-colors duration-300",
                    currentStep > step.id
                      ? "bg-chart-3 text-white"
                      : currentStep === step.id
                        ? "bg-primary text-white"
                        : "bg-gray-200 text-gray-600"
                  )}>
                  {currentStep > step.id ? <Check className="h-5 w-5" /> : step.id}
                </div>
                <div
                  className={cn(
                    "mt-2 text-center text-sm font-medium",
                    currentStep >= step.id ? "text-gray-800" : "text-gray-500"
                  )}>
                  {step.title}
                </div>
                {step.id < steps.length && (
                  <div
                    className={cn(
                      "absolute top-5 left-[calc(50%+20px)] h-0.5 w-[calc(100%-40px)] -translate-y-1/2 bg-gray-200 transition-colors duration-300",
                      currentStep > step.id && "bg-sidebar-primary"
                    )}
                  />
                )}
              </div>
            ))}
          </div>
        </CardHeader>

        <CardContent className="p-6 md:p-8">
          {renderStepContent()}

          {/* Navigation */}
          <div className="mt-8 flex items-center justify-between border-t pt-6">
            <Button variant="outline" onClick={handlePrevious} disabled={currentStep === 1}>
              <ChevronLeft className="h-4 w-4" />
              <span>Back</span>
            </Button>

            <Button onClick={handleNext} disabled={!connected}>
              <span>{currentStep === 3 ? "Complete" : "Next"}</span>
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}