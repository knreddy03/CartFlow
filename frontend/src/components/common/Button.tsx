import type { ButtonHTMLAttributes, ReactNode } from "react";

type ButtonVariant = "primary" | "secondary" | "outline" | "ghost";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: ButtonVariant;
  fullWidth?: boolean;
}

const variants: Record<ButtonVariant, string> = {
  primary: "bg-gray-900 text-white hover:bg-gray-800 active:bg-gray-950",

  secondary:
    "border border-gray-300 bg-white text-gray-900 hover:border-gray-400 hover:bg-gray-50",

  outline:
    "border border-gray-900 bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white",

  ghost: "bg-transparent text-gray-900 hover:bg-gray-100",
};

export default function Button({
  children,
  variant = "primary",
  fullWidth = false,
  className = "",
  type = "button",
  disabled = false,
  ...props
}: ButtonProps) {
  return (
    <button
      type={type}
      disabled={disabled}
      aria-disabled={disabled || undefined}
      className={[
        "inline-flex items-center justify-center gap-2",
        "min-h-11 px-6 py-3",
        "text-sm font-semibold tracking-[0.08em] uppercase",
        "transition-all duration-200 ease-out",
        "focus-visible:outline-none",
        "focus-visible:ring-2 focus-visible:ring-gray-900",
        "focus-visible:ring-offset-2",
        "active:scale-[0.98]",
        "disabled:pointer-events-none disabled:opacity-50",
        variants[variant],
        fullWidth ? "w-full" : "",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
      {...props}
    >
      {children}
    </button>
  );
}
