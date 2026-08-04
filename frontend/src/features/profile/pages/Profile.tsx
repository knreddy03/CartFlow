import { useQuery } from "@tanstack/react-query";

import { getProfile } from "../profile.api";

import LogoutButton from "../../auth/components/LogoutButton";

function Profile() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["profile"],

    queryFn: getProfile,
  });

  if (isLoading) {
    return <h1>Loading profile...</h1>;
  }

  if (error) {
    return <h1>Failed to load profile</h1>;
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">My Profile</h1>

      <div
        className="
        rounded-lg
        border
        p-6
        space-y-3
      "
      >
        <p>
          <strong>Name:</strong> {data?.first_name} {data?.last_name}
        </p>

        <p>
          <strong>Email:</strong> {data?.email}
        </p>

        <p>
          <strong>Mobile:</strong> {data?.mobile}
        </p>

        <p>
          <strong>Date of Birth:</strong> {data?.date_of_birth}
        </p>
      </div>

      <div className="mt-6">
        <LogoutButton />
      </div>
    </div>
  );
}

export default Profile;
