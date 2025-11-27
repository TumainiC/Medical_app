import { cn } from "@/lib/utils";
import { TrendingUp } from "lucide-react";

interface OrganCardProps {
  title: string;
  status: "Normal" | "Warning" | "Critical";
  image: string;
  className?: string;
}

export const OrganCard = ({ title, status, image, className }: OrganCardProps) => {
  const statusColor = {
    Normal: "text-success",
    Warning: "text-chart-3",
    Critical: "text-accent"
  };

  return (
    <div className={cn("glass-card-hover rounded-3xl p-6 relative group", className)}>
      <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
        <TrendingUp className="w-5 h-5 text-muted-foreground" />
      </div>
      
      <div className="flex flex-col items-center justify-center space-y-4">
        <div className="w-32 h-32 flex items-center justify-center">
          <img 
            src={image} 
            alt={title} 
            className="w-full h-full object-contain"
          />
        </div>
        
        <div className="text-center space-y-1">
          <h3 className="text-lg font-semibold text-foreground">{title}</h3>
          <div className="flex items-center justify-center gap-2">
            <div className={cn("w-2 h-2 rounded-full", statusColor[status])} />
            <p className={cn("text-sm font-medium", statusColor[status])}>{status}</p>
          </div>
        </div>
      </div>
    </div>
  );
};
