import { useQuery } from "@tanstack/react-query";

import { api } from "./api/axios";

function App() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["health"],

    queryFn: async () => {
      const response = await api.get("/");

      return response.data;
    },
  });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error</div>;
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <h1 className="text-4xl font-bold">{JSON.stringify(data)}</h1>
    </div>
  );
}

export default App;
