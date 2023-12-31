import Form from "./Form";
import FormRowVertical from "./FormRowVertical";
import Input from "./Input";
import Button from "./Button";
import Heading from "./Heading";
import NormalText from "./NormalText";
import { useForm } from "react-hook-form";
import { useLoginUser } from "../features/users/useLoginUser";

const LoginForm = ({ closeModal, setFormType }) => {
  const { register, formState, handleSubmit } = useForm();
  const { errors } = formState;

  const { isLogging, loginUser } = useLoginUser();

  function onSubmit(data) {
    try {
      loginUser(data, {
        onSuccess: () => {
          closeModal();
        },
      });
    } catch (err) {
      console.log(err);
    }
  }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Heading as={"h4"}>Welcome back!</Heading>
      <FormRowVertical label="EMAIL" error={errors?.email?.message}>
        <Input
          type="email"
          id="email"
          {...register("email", {
            required: "This field  sfs sda is required",
            pattern: {
              value: /\S+@\S+\.\S+/,
              message: "Please provide a valid email address",
            },
          })}
        />
      </FormRowVertical>
      <FormRowVertical label="PASSWORD" error={errors?.password?.message}>
        <Input
          type="password"
          id="password"
          {...register("password", {
            required: "This field is required",
            minLength: {
              value: 8,
              message: "Password needs a minimum of 8 characters",
            },
          })}
        />
      </FormRowVertical>
      <FormRowVertical>
        <Button disabled={isLogging} size="large">
          Log in
        </Button>
      </FormRowVertical>
      <FormRowVertical>
        <p>
          {"Don't have an account?"}
          <NormalText
            onClick={() => setFormType("register")}
            as={"span"}
            style={{ marginLeft: "0.2rem", color: "#cf9fff" }}
          >
            Register
          </NormalText>
        </p>
      </FormRowVertical>
    </Form>
  );
};

export default LoginForm;
