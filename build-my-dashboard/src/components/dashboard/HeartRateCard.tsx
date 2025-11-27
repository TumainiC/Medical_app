import heartImage from "@/assets/heart-3d.png";

interface HeartRateCardProps {
  bpm: number;
}

export const HeartRateCard = ({ bpm }: HeartRateCardProps) => {
  return (
    <div className="glass-card rounded-3xl p-8 relative overflow-hidden">
      <div className="relative z-10 flex items-center justify-between">
        <div className="flex-1">
          <img 
            src={heartImage} 
            alt="Heart" 
            className="w-64 h-64 object-contain mx-auto animate-pulse"
            style={{ animationDuration: '2s' }}
          />
        </div>
        
        <div className="flex-1 flex flex-col items-center">
          <div className="glass-card rounded-2xl p-4 bg-glass/40">
            <div className="flex items-center gap-4">
              <svg className="w-16 h-12" viewBox="0 0 100 40">
                <polyline
                  points="0,20 20,20 25,5 30,35 35,20 100,20"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  className="text-accent"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>
      
      <div className="mt-6 text-center">
        <h3 className="text-sm font-medium text-muted-foreground">Heart Rate</h3>
        <p className="text-xl font-semibold text-foreground mt-1">{bpm} bpm</p>
      </div>
    </div>
  );
};
