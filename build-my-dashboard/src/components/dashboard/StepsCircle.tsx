interface StepsCircleProps {
  current: number;
  goal: number;
}

export const StepsCircle = ({ current, goal }: StepsCircleProps) => {
  const percentage = (current / goal) * 100;
  const circumference = 2 * Math.PI * 120;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  return (
    <div className="glass-card rounded-3xl p-8 flex items-center justify-center">
      <div className="relative w-64 h-64">
        <svg className="transform -rotate-90 w-full h-full">
          {/* Background circle */}
          <circle
            cx="128"
            cy="128"
            r="120"
            stroke="currentColor"
            strokeWidth="12"
            fill="none"
            className="text-muted"
            opacity="0.2"
          />
          {/* Progress circle */}
          <circle
            cx="128"
            cy="128"
            r="120"
            stroke="currentColor"
            strokeWidth="12"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="text-primary transition-all duration-1000"
          />
        </svg>
        
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className="text-5xl font-bold text-foreground">
            {current.toLocaleString()}
          </div>
          <div className="text-sm text-muted-foreground mt-1">Steps</div>
          <div className="text-xs text-muted-foreground mt-6">
            {goal.toLocaleString()} Steps
          </div>
        </div>
      </div>
    </div>
  );
};
