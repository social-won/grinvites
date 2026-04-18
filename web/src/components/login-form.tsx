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
import { Controller, useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { getUser } from "@/lib/api"
import { useUser } from "@/context/user-context"
import supabase from "@/lib/supabase"

import { LoginFormValues, loginSchema } from "@/lib/utils"

export function LoginForm() {
  const navigate = useNavigate()
  const { setUser } = useUser()

  const form = useForm<LoginFormValues>({
    defaultValues: {
      email: "",
      password: "",
    },
    resolver: zodResolver(loginSchema),
    reValidateMode: "onBlur",
  })

  const onSubmit = async (values: LoginFormValues) => {
    form.clearErrors()

    const { data, error } = await supabase.auth.signInWithPassword({
      email: values.email,
      password: values.password,
    })

    const supabaseUser = data.user

    if (error || !supabaseUser) {
      console.error(error)
      form.setError("password", {
        type: "server",
        message: "Incorrect password",
      })
      return
    }

    let apiUser = null
    try {
      apiUser = await getUser(data.user.id)
    } catch (fetchError) {
      console.error("Failed to load backend user data", fetchError)
    }

    const mergedUser = {
      ...apiUser,
      ...supabaseUser,
    }

    setUser(mergedUser)
    navigate("/home")
  }

  return (
    <div className="flex min-h-screen flex-col gap-6 p-4 items-center justify-center">
      <Card className="w-full max-w-xl">
        <CardHeader className="text-center">
          <CardTitle className="text-xl">Welcome Back</CardTitle>
          <CardDescription>
            Enter your email and password to sign in
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form noValidate onSubmit={form.handleSubmit(onSubmit)}>
            <FieldGroup>
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
                      placeholder="john@example.com"
                      aria-invalid={fieldState.invalid}
                    />
                    {fieldState.invalid && (
                      <FieldError errors={[fieldState.error]} />
                    )}
                  </Field>
                )}
              />

              <Controller
                name="password"
                control={form.control}
                render={({ field, fieldState }) => (
                  <Field>
                    <FieldLabel htmlFor="password">Password</FieldLabel>
                    <Input
                      id="password"
                      type="password"
                      placeholder="••••••••"
                      aria-invalid={fieldState.invalid}
                      {...field}
                    />
                    <FieldError errors={[fieldState.error]} />
                    <FieldDescription>
                      <Link to="" className="text-primary">Forgot your password?</Link>
                    </FieldDescription>
                  </Field>
                )}
              />

              <Field>
                <Button type="submit" className="w-full">Sign In</Button>
                <FieldDescription className="text-center">
                  Don't have an account? <Link to="/signup" className="text-primary">Sign up</Link>
                </FieldDescription>
              </Field>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>
      {/* <FieldDescription className="px-6 text-center">
        By signing in, you agree to our <a href="#" className="text-primary hover:underline">Terms of Service</a>{" "}
        and <a href="#" className="text-primary hover:underline">Privacy Policy</a>.
      </FieldDescription> */}
    </div >
  )
}
