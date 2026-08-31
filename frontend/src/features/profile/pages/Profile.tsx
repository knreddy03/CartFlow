import { useQuery } from "@tanstack/react-query";
import { X } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { getProfile } from "../api/profile.api";
import LogoutButton from "../../auth/components/LogoutButton";
import Loader from "../../../components/common/Loader";

function Profile() {
  const navigate = useNavigate();

  const { data, isLoading, error } = useQuery({
    queryKey: ["profile"],
    queryFn: getProfile,
  });

  function handleClose() {
    navigate("/");
  }

  return (
    <div className="fixed inset-0 z-50" role="presentation">
      {/* Backdrop */}
      <button
        type="button"
        aria-label="Close profile"
        onClick={handleClose}
        className="absolute inset-0 h-full w-full cursor-default bg-gray-900/30 backdrop-blur-[2px] transition-opacity duration-300 hover:bg-gray-900/40 focus-visible:outline-none"
      />

      {/* Profile drawer */}
      <aside
        aria-label="Profile sidebar"
        role="complementary"
        className="
          absolute right-0 top-0
          flex h-full w-full max-w-md
          flex-col
          overflow-y-auto
          bg-white
          shadow-2xl
          animate-[slideIn_250ms_ease-out]
        "
      >
        {/* Header */}
        <div className="flex items-center justify-between border-b border-gray-200 px-6 py-6 sticky top-0 bg-white/95 backdrop-blur-sm">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gray-600">
              Account
            </p>

            <h1 className="mt-2 text-2xl font-light text-gray-900">
              My Profile
            </h1>
          </div>

          <button
            type="button"
            aria-label="Close profile"
            onClick={handleClose}
            className="rounded-full p-2 text-gray-600 transition-all duration-200 hover:bg-gray-100 hover:text-gray-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-900 focus-visible:ring-offset-2"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 px-6 py-8 space-y-6">
          {isLoading && (
            <div
              className="flex flex-col items-center justify-center min-h-40 gap-4"
              role="status"
              aria-live="polite"
            >
              <Loader size="md" />
              <p className="text-sm text-gray-500 animate-pulse">
                Loading your profile...
              </p>
            </div>
          )}

          {error && (
            <div
              className="rounded-lg border border-red-200 bg-red-50 p-5 space-y-2"
              role="alert"
            >
              <p className="text-sm font-semibold text-red-800">
                Failed to load profile
              </p>
              <p className="text-sm text-red-700">
                Please try again or refresh the page.
              </p>
            </div>
          )}

          {data && (
            <div className="space-y-4 animate-fadeIn">
              {/* Name Section */}
              <div className="rounded-xl border border-gray-200 bg-white p-6 hover:shadow-md transition-shadow duration-300">
                <p className="text-xs font-semibold uppercase tracking-[0.15em] text-gray-600 mb-4">
                  Personal Information
                </p>

                <div className="space-y-5">
                  <div className="border-b border-gray-100 pb-4 last:border-b-0 last:pb-0">
                    <p className="text-xs font-medium uppercase tracking-[0.1em] text-gray-500">
                      Full Name
                    </p>
                    <p className="mt-2 text-lg font-semibold text-gray-900">
                      {data.first_name} {data.last_name}
                    </p>
                  </div>

                  <div className="border-b border-gray-100 pb-4 last:border-b-0 last:pb-0">
                    <p className="text-xs font-medium uppercase tracking-[0.1em] text-gray-500">
                      Email Address
                    </p>
                    <p className="mt-2 text-sm font-medium text-gray-900 break-all">
                      {data.email}
                    </p>
                  </div>

                  <div className="border-b border-gray-100 pb-4 last:border-b-0 last:pb-0">
                    <p className="text-xs font-medium uppercase tracking-[0.1em] text-gray-500">
                      Mobile
                    </p>
                    <p className="mt-2 text-sm font-medium text-gray-900">
                      {data.mobile || "Not provided"}
                    </p>
                  </div>

                  <div>
                    <p className="text-xs font-medium uppercase tracking-[0.1em] text-gray-500">
                      Date of Birth
                    </p>
                    <p className="mt-2 text-sm font-medium text-gray-900">
                      {data.date_of_birth
                        ? new Date(data.date_of_birth).toLocaleDateString()
                        : "Not provided"}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 bg-white px-6 py-6 sticky bottom-0">
          <LogoutButton />
        </div>
      </aside>
    </div>
  );
}

export default Profile;
