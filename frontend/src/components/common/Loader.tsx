interface LoaderProps {
  size?: "sm" | "md" | "lg";
}

const sizes = {
  sm: "h-4 w-4",
  md: "h-6 w-6",
  lg: "h-10 w-10",
};

export default function Loader({ size = "md" }: LoaderProps) {
  return (
    <div
      className={`
        ${sizes[size]}
        animate-spin
        rounded-full
        border-2
        border-neutral-200
        border-t-neutral-900
      `}
      role="status"
      aria-label="Loading"
    />
  );
}
