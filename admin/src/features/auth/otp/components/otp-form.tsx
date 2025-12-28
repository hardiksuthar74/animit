import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "@tanstack/react-router";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  InputOTP,
  InputOTPGroup,
  InputOTPSlot,
  InputOTPSeparator,
} from "@/components/ui/input-otp";
import { useMutation } from "@tanstack/react-query";
import {
  AuthenticateRequest,
  authenticateV1LoginCodeAuthenticatePost,
} from "@/client";
import { useAuthStore } from "@/stores/auth-store";
import { toast } from "sonner";

const formSchema = z.object({
  otp: z
    .string()
    .min(6, "Please enter the 6-digit code.")
    .max(6, "Please enter the 6-digit code."),
});

type OtpFormProps = React.HTMLAttributes<HTMLFormElement>;

export function OtpForm({ className, ...props }: OtpFormProps) {
  const navigate = useNavigate();
  const { auth } = useAuthStore();
  const { mutate: verifyCode, isPending } = useMutation({
    mutationFn: (data: AuthenticateRequest) =>
      authenticateV1LoginCodeAuthenticatePost<true>({
        body: data,
      }),
  });

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { otp: "" },
  });

  // eslint-disable-next-line react-hooks/incompatible-library
  const otp = form.watch("otp");

  function onSubmit(data: z.infer<typeof formSchema>) {
    const email = sessionStorage.getItem("userEmail") as string;
    verifyCode(
      {
        code: data?.otp,
        email,
      },
      {
        onSuccess: ({ data }) => {
          const mockUser = {
            accountNo: "ACC001",
            email,
            role: ["user"],
            exp: Date.now() + 24 * 60 * 60 * 1000, // 24 hours from now
          };

          // Set user and access token
          auth.setUser(mockUser);
          auth.setAccessToken(data?.access_token as string);
          toast.success(`Welcome ${email}`);
          navigate({ to: "/users" });
        },
      }
    );
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className={cn("grid gap-2", className)}
        {...props}
      >
        <FormField
          control={form.control}
          name="otp"
          render={({ field }) => (
            <FormItem>
              <FormLabel className="sr-only">One-Time Password</FormLabel>
              <FormControl>
                <InputOTP
                  maxLength={6}
                  {...field}
                  containerClassName='justify-between sm:[&>[data-slot="input-otp-group"]>div]:w-12'
                >
                  <InputOTPGroup>
                    <InputOTPSlot index={0} />
                    <InputOTPSlot index={1} />
                  </InputOTPGroup>
                  <InputOTPSeparator />
                  <InputOTPGroup>
                    <InputOTPSlot index={2} />
                    <InputOTPSlot index={3} />
                  </InputOTPGroup>
                  <InputOTPSeparator />
                  <InputOTPGroup>
                    <InputOTPSlot index={4} />
                    <InputOTPSlot index={5} />
                  </InputOTPGroup>
                </InputOTP>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button className="mt-2" disabled={otp.length < 6 || isPending}>
          Verify
        </Button>
      </form>
    </Form>
  );
}
