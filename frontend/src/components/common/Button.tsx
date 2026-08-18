import type { ButtonHTMLAttributes, ReactNode } from "react";

type ButtonVariant = "primary" | "secondary" | "outline" | "ghost";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: ButtonVariant;
  fullWidth?: boolean;
}

const variants: Record<ButtonVariant, string> = {
  primary: "bg-neutral-950 text-white hover:bg-neutral-800",

  secondary:
    "border border-neutral-200 bg-white text-neutral-950 hover:border-neutral-300 hover:bg-neutral-50",

  outline:
    "border border-neutral-950 bg-transparent text-neutral-950 hover:bg-neutral-950 hover:text-white",

  ghost: "bg-transparent text-neutral-950 hover:bg-neutral-100",
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
        "text-sm font-medium tracking-[0.08em]",
        "transition-colors duration-200 ease-out",
        "focus-visible:outline-none",
        "focus-visible:ring-2 focus-visible:ring-neutral-950",
        "focus-visible:ring-offset-2",
        "active:scale-[0.99]",
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
