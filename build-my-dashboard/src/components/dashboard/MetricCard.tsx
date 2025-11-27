import { cn } from "@/lib/utils";

interface MetricCardProps {
  title: string;
  subtitle: string;
  value: string;
  unit?: string;
  chartData?: number[];
  className?: string;
}

export const MetricCard = ({ title, subtitle, value, unit, chartData, className }: MetricCardProps) => {
  const maxValue = chartData ? Math.max(...chartData) : 0;
  
  return (
    <div className={cn("glass-card rounded-3xl p-6", className)}>
      <div className="space-y-1 mb-4">
        <h3 className="text-sm font-semibold text-foreground">{title}</h3>
        <p className="text-xs text-muted-foreground">{subtitle}</p>
      </div>
      
      <div className="flex items-end justify-between gap-4">
        {chartData && (
          <div className="flex items-end gap-0.5 h-12 flex-1">
            {chartData.map((value, idx) => (
              <div
                key={idx}
                className="flex-1 bg-muted rounded-sm transition-all"
                style={{ 
                  height: `${(value / maxValue) * 100}%`,
                  opacity: 0.3 + (value / maxValue) * 0.7
                }}
              />
            ))}
          </div>
        )}
        
        <div className="text-right">
          <div className="text-2xl font-bold text-foreground">{value}</div>
          {unit && <div className="text-xs text-muted-foreground">{unit}</div>}
        </div>
      </div>
    </div>
  );
};
