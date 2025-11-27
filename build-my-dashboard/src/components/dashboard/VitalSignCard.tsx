import { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface VitalSignCardProps {
  icon: ReactNode;
  title: string;
  subtitle: string;
  value: string;
  chart?: ReactNode;
  className?: string;
}

export const VitalSignCard = ({ icon, title, subtitle, value, chart, className }: VitalSignCardProps) => {
  return (
    <div className={cn("glass-card rounded-3xl p-6", className)}>
      <div className="flex items-start gap-3 mb-4">
        <div className="w-10 h-10 rounded-full bg-accent/10 flex items-center justify-center text-accent flex-shrink-0">
          {icon}
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-semibold text-foreground">{title}</h3>
          <p className="text-xs text-muted-foreground">{subtitle}</p>
        </div>
      </div>
      
      {chart && (
        <div className="mb-4">
          {chart}
        </div>
      )}
      
      <div className="text-3xl font-bold text-foreground">{value}</div>
    </div>
  );
};
