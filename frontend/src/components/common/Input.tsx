import type { InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export default function Input({
  label,
  error,
  className = "",
  id,
  ...props
}: InputProps) {
  const errorId = id ? `${id}-error` : undefined;

  return (
    <div className="flex w-full flex-col gap-2">
      {label && (
        <label
          htmlFor={id}
          className="text-xs font-semibold uppercase tracking-[0.08em] text-gray-900"
        >
          {label}
        </label>
      )}

      <input
        id={id}
        aria-invalid={error ? true : undefined}
        aria-describedby={errorId}
        className={[
          "min-h-11 w-full",
          "border bg-white px-4 py-3",
          "text-sm text-gray-900",
          "outline-none",
          "placeholder:text-gray-400",
          "transition-all duration-200",
          "focus-visible:ring-2 focus-visible:ring-offset-1",
          "disabled:cursor-not-allowed disabled:bg-gray-50 disabled:text-gray-500",
          error
            ? "border-red-500 focus:border-red-500 focus-visible:ring-red-500"
            : "border-gray-300 hover:border-gray-400 focus:border-gray-900 focus-visible:ring-gray-900",
          className,
        ]
          .filter(Boolean)
          .join(" ")}
        {...props}
      />

      {error && (
        <p
          id={errorId}
          role="alert"
          className="text-xs leading-relaxed text-red-600"
        >
          {error}
        </p>
      )}
    </div>
  );
}
