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
          className="text-sm font-medium tracking-wide text-neutral-950"
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
          "text-sm text-neutral-950",
          "outline-none",
          "placeholder:text-neutral-400",
          "transition-colors duration-200",
          "focus-visible:ring-2 focus-visible:ring-neutral-950",
          "focus-visible:ring-offset-1",
          "disabled:cursor-not-allowed disabled:bg-neutral-100 disabled:text-neutral-500",
          error
            ? "border-red-500 focus:border-red-500 focus-visible:ring-red-500"
            : "border-neutral-200 focus:border-neutral-950",
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
