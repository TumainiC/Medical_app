import { Moon } from "lucide-react";

interface SleepCardProps {
  hours: number;
  minutes: number;
  startTime: string;
  endTime: string;
}

export const SleepCard = ({ hours, minutes, startTime, endTime }: SleepCardProps) => {
  return (
    <div className="glass-card rounded-3xl p-6">
      <div className="space-y-4">
        <div>
          <h3 className="text-sm font-semibold text-foreground mb-1">Sleep time</h3>
          <p className="text-2xl font-bold text-foreground">
            {hours}:{minutes.toString().padStart(2, '0')}h
          </p>
        </div>
        
        <div className="flex items-center justify-between bg-foreground text-background rounded-full px-4 py-2 text-sm font-medium">
          <Moon className="w-4 h-4" />
          <span>{startTime} - {endTime}</span>
        </div>
        
        {/* Sleep quality bar */}
        <div className="relative h-2 bg-muted rounded-full overflow-hidden">
          <div 
            className="absolute left-0 top-0 h-full bg-primary rounded-full"
            style={{ width: '85%' }}
          />
        </div>
      </div>
    </div>
  );
};
