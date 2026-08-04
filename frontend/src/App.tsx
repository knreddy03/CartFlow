import { useQuery } from "@tanstack/react-query";

import { getCurrentUser } from "./api/user.api";

import LogoutButton from "./features/auth/components/LogoutButton";

function App() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["me"],

    queryFn: getCurrentUser,
  });

  if (isLoading) {
    return <h1>Loading...</h1>;
  }

  if (error) {
    return <h1>Failed to load user</h1>;
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold">CartFlow</h1>

      <pre className="my-5">{JSON.stringify(data, null, 2)}</pre>

      <LogoutButton />
    </div>
  );
}

export default App;
