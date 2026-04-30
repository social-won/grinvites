import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Field,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Link, useNavigate } from "react-router-dom"
import { Controller, useForm, UseFormReturn } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import supabase from "@/lib/supabase"

import { signupSchema } from "@/lib/utils"
import { createUser } from "@/lib/api"
import { SignupFormValues } from "@/lib/types"

export function SignupPage() {
  const navigate = useNavigate()

  const [page, setPage] = useState(0);

  const form = useForm<SignupFormValues>({
    defaultValues: {
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
    resolver: zodResolver(signupSchema),
    reValidateMode: "onBlur",
  })

  const onSubmit = async (values: SignupFormValues) => {
    form.clearErrors()

    const { data, error } = await supabase.auth.signUp({
      email: values.email,
      password: values.password,
      options: {
        data: {
          display_name: values.name,
        },
      },
    })

    if (error) {
      console.error(error)
      form.setError("password", {
        type: "server",
        message: error.message || "Unable to sign up",
      })
      return
    }

    if (data.user) {
      createUser({
        id: data.user.id,
        email: data.user.email!!,
        display_name: data.user.user_metadata.display_name,
        invite_times: {}
      })

      navigate("/onboarding")
    }
  }

  return (
    <div className="flex min-h-screen flex-col gap-6 p-4 items-center justify-center">
      <Card className={page === 1 ? "w-full max-w-xl": "w-full max-w-sm"}>
        <CardHeader className="text-center">
          <CardTitle className="text-xl">{page == 1 ? "Create your account" : "Connect your email to Grinvites"}</CardTitle>
          <CardDescription>
            {page == 1 ? "Enter your details below to create your account" : "Enter the email you want to connect"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {page == 1 ? <SignupForm form={form} onSubmit={onSubmit} /> : <EmailForm form={form} setPage={setPage} />}
        </CardContent>
      </Card>
      {/* <FieldDescription className="px-6 text-center">
        By clicking continue, you agree to our <a href="#">Terms of Service</a>{" "}
        and <a href="#">Privacy Policy</a>.
      </FieldDescription> */}
    </div>
  )
}


export function SignupForm({ form, onSubmit }: { form: UseFormReturn<SignupFormValues>, onSubmit: (values: SignupFormValues) => Promise<void> }) {

  // return (
  //   <>
  //   hi
  //   </>
  // )
  return (
    <form noValidate onSubmit={form.handleSubmit(onSubmit)}>
      <FieldGroup className="gap-4 max-w-xl w-full">
        <Field className="grid grid-cols-2 gap-4">
          <Controller
            name="name"
            control={form.control}
            render={({ field, fieldState }) => (
              <Field>
                <FieldLabel htmlFor="name">Name</FieldLabel>
                <Input
                  {...field}
                  id="name"
                  type="text"
                  placeholder="Squirrel"
                  aria-invalid={fieldState.invalid}
                />
                {fieldState.invalid && (
                  <FieldError errors={[fieldState.error]} />
                )}
              </Field>
            )}
          />

          <Controller
            name="email"
            control={form.control}
            render={({ field, fieldState }) => (
              <Field>
                <FieldLabel htmlFor="email">Email</FieldLabel>
                <Input
                  {...field}
                  id="email"
                  type="email"
                  placeholder="squirrel@example.com"
                  aria-invalid={fieldState.invalid}
                />
                {fieldState.invalid && (
                  <FieldError errors={[fieldState.error]} />
                )}
              </Field>
            )}
          />
        </Field>


        <Controller
          name="password"
          control={form.control}
          render={({ field, fieldState }) => (
            <Field>
              <FieldLabel htmlFor="password">Password</FieldLabel>
              <Input
                {...field}
                id="password"
                type="password"
                placeholder="••••••••"
                aria-invalid={fieldState.invalid}
              />
              {fieldState.invalid && (
                <FieldError errors={[fieldState.error]} />
              )}
            </Field>
          )}
        />

        <Controller
          name="confirmPassword"
          control={form.control}
          render={({ field, fieldState }) => (
            <Field>
              <FieldLabel htmlFor="confirm-password">
                Confirm Password
              </FieldLabel>
              <Input
                {...field}
                id="confirm-password"
                type="password"
                placeholder="••••••••"
                aria-invalid={fieldState.invalid}
              />
              {fieldState.invalid && (
                <FieldError errors={[fieldState.error]} />
              )}
            </Field>
          )}
        />

        <Field>
          <Button type="submit">Create Account</Button>
          <FieldDescription className="text-center">
            Already have an account? <Link to="/login" className="text-primary hover:underline">Sign in</Link>
          </FieldDescription>
        </Field>
      </FieldGroup>
    </form>
  )
}

function EmailForm({ form, setPage }: { form: UseFormReturn<SignupFormValues>, setPage: React.Dispatch<React.SetStateAction<number>> }) {


  return (
    <form noValidate onSubmit={() => console.log(form)}>
      <FieldGroup className="flex justify-center items-center gap-4" >
        <Controller
          name="email"
          control={form.control}
          render={({ field, fieldState }) => (
            <Field className="max-w-3xs w-full">
              {/* <FieldLabel htmlFor="email">Email</FieldLabel> */}
              <Input
                {...field}
                id="email"
                type="email"
                placeholder="squirrel@example.com"
                aria-invalid={fieldState.invalid}
              />
              {fieldState.invalid && (
                <FieldError errors={[fieldState.error]} />
              )}
            </Field>
          )}
        />

          <Button 
            className="w-full max-w-3xs"
            onClick={async (_e) => {
            _e.preventDefault();
            const isValid = await form.trigger("email");
            if (isValid) {
              setPage(1);
            }
          }}>Next</Button>
          <FieldDescription className="text-center">
            Already have an account? <Link to="/login" className="text-primary hover:underline">Sign in</Link>
          </FieldDescription>
      </FieldGroup>
    </form>
  )
}