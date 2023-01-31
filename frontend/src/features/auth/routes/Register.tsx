import { useNavigate } from "react-router-dom";

import { Layout } from "../components/Layout";
import { RegisterBox } from "../components/RegisterBox";

export const Register = () => {
  const navigate = useNavigate();

  return (
    <Layout>
      <RegisterBox onSuccess={() => navigate("/")} />
    </Layout>
  );
};
