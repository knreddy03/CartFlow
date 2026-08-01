export default function LoginForm() {
  return (
    <form className="space-y-5">
      <div>
        <label className="mb-2 block text-sm font-medium">Email</label>

        <input
          type="email"
          placeholder="Enter your email"
          className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:outline-none"
        />
      </div>

      <div>
        <label className="mb-2 block text-sm font-medium">Password</label>

        <input
          type="password"
          placeholder="Enter your password"
          className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:outline-none"
        />
      </div>

      <button
        type="submit"
        className="w-full rounded-lg bg-blue-600 py-2 font-semibold text-white transition hover:bg-blue-700"
      >
        Login
      </button>
    </form>
  );
}
