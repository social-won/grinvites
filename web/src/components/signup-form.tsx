import { useEffect, useRef, useState } from "react"
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
import { useUser } from "@/context/user-context"

export function SignupPage() {
  const navigate = useNavigate()
  const { user, setUser } = useUser()
  const justSignedUp = useRef(false)

  useEffect(() => {
    if (user && !justSignedUp.current) {
      navigate("/home");
    }
  }, [user])

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

    // SUPABASE AUTH sign up   NOT CC
    supabase.auth.signUp({
      email: values.email,
      password: values.password,
      options: {
        data: {
          display_name: values.name,
        },
        emailRedirectTo: `${window.location.origin}/onboarding`
      },
    }).then(({ data }) => {

      if (data.user) {
        const newUser = {
          id: data.user.id,
          email: data.user.email!!,
          display_name: data.user.user_metadata.display_name,
          invite_times: {},
          theme: "light"
        }
        // if user is created, make BACKEND API call
        createUser(newUser).then((({ status }) => {
          console.log("user created", status);

          if (status == 201) {
            justSignedUp.current = true
            setUser(newUser)
            navigate("/onboarding")
          } else {
            console.error("status: ", status)
            form.setError("password", {
              type: "server",
              message: "Unable to create user error code: " + status.toString()
            })
            //TODO: Delete user from supabase?
          }
        }))
      }
    }).catch(error => {
      console.error(error)
      form.setError("password", {
        type: "server",
        message: error.message || "Unable to register user",
      })
    })
  }

  return (
    <div className="flex min-h-screen flex-col gap-6 p-4 items-center justify-center">
      <Card className="w-full max-w-xl">
        <CardHeader className="text-center">
          <CardTitle className="text-xl">{page == 1 ? "Create your account" : "Connect your calendar email to Grinvites"}</CardTitle>
          <CardDescription>
            {page == 1 ? "Enter your details below to create your account" : "Enter the email you use for your calendar"}
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
    <form noValidate onSubmit={() => console.log(form)} className="w-full">
      <FieldGroup className="flex justify-center items-center gap-4" >
        <Controller
          name="email"
          control={form.control}
          render={({ field, fieldState }) => (
            <Field className="w-full">
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
          className="w-full"
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