import { api } from "./api/axios";


function App() {


  const testBackend = async()=>{
    const response = await api.get("/");
    console.log(response.data);
  };


  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4">

      <h1 className="text-4xl font-bold">
        CartFlow
      </h1>


      <button
        onClick={testBackend}
        className="rounded bg-black px-4 py-2 text-white"
      >
        Test Backend
      </button>

    </div>
  );
}

export default App;